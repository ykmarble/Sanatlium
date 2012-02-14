import urllib
import urllib2
import simplejson as json
import threading
import oauth2

class TwitterAPICore(object):
    base_url = "https://api.twitter.com/1/"

    def __init__(self ,consumer_key ,consumer_secret ,token_key=None ,token_secret=None):
        self.oauth_consumer = oauth2.Consumer(consumer_key ,consumer_secret)
        if token_key and token_secret:
            self.oauth_token = oauth2.Token(token_key ,token_secret)
        else:
            self.oauth_token = None

    def set_oauth_token(self ,token_key ,token_secret):
        self.oauth_token = oauth2.Token(token_key ,token_secret)

    def get_requesttoken(self):
        url = "https://api.twitter.com/oauth/request_token"
        response = {}
        [response.__setitem__(key ,value) for key ,value in [couple.split("=") for couple in self._http_get(url).read().split("&")]]
        return response["oauth_token"] ,response["oauth_token_secret"]

    def get_accesstoken(self ,pin):
        url = "https://api.twitter.com/oauth/access_token"
        response = {}
        [response.__setitem__(key ,value) for key ,value in [couple.split("=") for couple in self._http_post(url ,{"oauth_verifier":pin}).read().split("&")]]
        return response["oauth_token"] ,response["oauth_token_secret"]

    def check_twitter_server(self):
        path = "help/test.json"
        res = self._http_get("%s%s"%(self.base_url ,path))
        js = json.loads(res.read().decode("utf-8"))
        print js ,res.info()

    def check_following(self ,target):
        path = "friendships/show.json"
        arg = {"target_id":target.id}
        #GET

    def create_favorite(self ,id):
        path = "favorites/create/%s.json"%id
        self._http_post("%s%s"%(self.base_url ,path))
        return

    def create_follow(self ,user):
        path = "friendships/create/%s.json"%user.id
        self._http_post("%s%s"%(self.base_url ,path))
        return
    
    def create_retweet(self ,tweet):
        path = "statuses/retweet/%s.json"%s
        self._http_post("%s%s"%(self.base_url ,path))
        return

    def destroy_favorite(self ,tweet):
        path = "favorites/destroy/%s.json"%tweet.id
        self._http_post("%s%s"%(self.base_url ,path))
        return

    def destroy_follow(self ,user):
        path = "friendships/destroy/%s.json"%user.id
        self._http_post("%s%s"%(self.base_url ,path))
        return

    def destroy_tweet(self ,tweet):
        path = "statuses/destroy/%s.json"%tweet.id
        self._http_post("%s%s"%(self.base_url ,path))
        return

    def get_home_timeline(self ,count=None ,since_id=None ,max_id=None):
        path = "statuses/home_timeline.json"
        args = {}
        if count:
            if count > 200:
               count = 200
            args["count"] = count
        if since_id:
           args["since_id"] = since_id
        if max_id:
           args["max_id"] = max_id
        connect = self._http_get("%s%s"%(self.base_url ,path) ,args)
        try:
            responce = connect.read().decode("utf-8")
        finally:
            connect.close()
        status_list = json.loads(responce)
        tl = [Tweet(status) for status in status_list]
        return tl

    def get_user(self ,user_id):
        path = "users/show/%s.json"%user_id
        connect = self._http_get("%s%s"%(self.base_url ,path))
        try:
            responce = connect.read().decode("utf-8")
        finally:
            connect.close()
        user = User(status_dict[json.loads(responce)])


    def get_user_timeline(self ,screen_name ,count=None ,since_id=None ,max_id=None ,include_rts=None):
        path = "statuses/user_timeline.json"
        args = {"screen_name":screen_name}
        if count:
            if count > 200:
               count = 200
            args["count"] = count
        if since_id:
           args["since_id"] = since_id
        if max_id:
           args["max_id"] = max_id
        if include_rts:
           args["include_rts"] = include_rts
        connect = self._http_get("%s%s"%(self.base_url ,path) ,args)
        try:
            responce = connect.read().decode("utf-8")
        finally:
            connect.close()
        status_list = json.loads(responce)
        tl = [Tweet(status) for status in status_list]
        return tl

    def get_mention(self ,count=None ,since_id=None ,max_id=None):
        path = "statuses/mentions.json"
        args = {}
        if count:
            if count > 200:
               count = 200
            args["count"] = count
        if since_id:
           args["since_id"] = since_id
        if max_id:
           args["max_id"] = max_id
        connect = self._http_get("%s%s"%(self.base_url ,path) ,args)
        try:
            responce = connect.read().decode("utf-8")
        finally:
            connect.close()
        status_list = json.loads(responce)
        tl = [Tweet(status) for status in status_list]
        return tl

    def post_tweet(self ,status ,in_reply_to = None):
        path = "statuses/update.json"
        if len(status) > 141:
            status = status[:140]
        args = {"status":status.encode("utf-8")}
        connect = self._http_post("%s%s"%(self.base_url ,path) ,args)
        try:
            responce = connect.read().decode("utf-8")
        finally:
            connect.close()
        status = json.loads(responce)
        return Tweet(status)

    def _http_post(self ,url ,args = {}):
        body = urllib.urlencode(args)
        req = oauth2.Request.from_consumer_and_token(self.oauth_consumer ,self.oauth_token
                                                    ,http_method="POST" ,http_url=url
                                                    ,parameters=args ,body=body)
        req.sign_request(oauth2.SignatureMethod_HMAC_SHA1() ,self.oauth_consumer ,self.oauth_token)
        print url ,body ,req.to_header()
        return urllib2.urlopen(urllib2.Request(url ,data=body ,headers = req.to_header()))

    def _http_get(self ,url ,args = {}):
        body = urllib.urlencode(args)
        req = oauth2.Request.from_consumer_and_token(self.oauth_consumer ,self.oauth_token
                                                    ,http_method="GET" ,http_url=url
                                                    ,parameters=args ,body=body)
        req.sign_request(oauth2.SignatureMethod_HMAC_SHA1() ,self.oauth_consumer ,self.oauth_token)
        return urllib2.urlopen(urllib2.Request("%s?%s"%(req.normalized_url ,body) ,headers = req.to_header()))

    
class UserStreamCore(threading.Thread):
    def __init__(self ,oauth_handler ,callback = None):
        threading.Thread.__init__(self)
        self.setDaemon(True)
        url = "https://userstream.twitter.com/2/user.json"
        body = {"delimited":"length"}
        self.que = []
        self.stream = oauth_handler._http_post(url ,body)
        if callback:
            self.callback = callback
        else:
            self.que = []
            self.callback = lambda e:self.que.append(e)

    def run(self):
        while 1:
            len = ""
            while True:
                c = self.stream.read(1)
                if c=="\n": break
                len += c
            len = len.strip()
            if not len.isdigit(): continue
            buf = self.stream.read(int(len)).decode("utf-8")
            event_dict = json.loads(buf)
            if event_dict.has_key("event"):
                event = Event(event_dict)
            elif event_dict.has_key("text"):
                event = Tweet(event_dict)
            else:continue
            self.callback(self ,event)


class Tweet(object):
    def __init__(self ,status_dict):
        self.id = status_dict["id"]
        self.user_id = status_dict["user"]["id"]
        self.text = status_dict["text"]
        self.created_at = status_dict["created_at"]
        self.favorited = status_dict["favorited"]
        self.retweeted = status_dict["retweeted"]
        self.source = status_dict["source"]
        self.in_reply_to_user_id = status_dict["in_reply_to_user_id"]
        self.in_reply_to_status_id = status_dict["in_reply_to_status_id"]
        if status_dict["user"].__len__() >= 2:
            self.user = User(status_dict["user"])


class User(object):
    def __init__(self ,status_dict):
        self.name = status_dict["name"]
        self.profile_image_url = status_dict["profile_image_url"]
        self.id = status_dict["id"]
        self.followers_count = status_dict["followers_count"]
        self.friends_count = status_dict["friends_count"]
        self.statuses_count = status_dict["statuses_count"]
        self.following = status_dict["following"]
        self.screen_name = status_dict["screen_name"]
        self.description = status_dict["description"]


class Event(object):
    def __init__(self ,status_dict):
        try:
            self.event= status_dict["event"]
            self.target = User(status_dict["target"])
            self.source = User(status_dict["source"])
            if self.event != "follow":
                self.target_object = Tweet(status_dict["target_object"])
            self.created_at = status_dict["created_at"]
        except KeyError:
            print status_dict.keys()
