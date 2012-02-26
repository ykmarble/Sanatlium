import TwitLib2
import thread
import urllib2

class TwitterAPIHandler(object):
    def __init__(self):
        import ConfigParser
        parser = ConfigParser.SafeConfigParser()
        parser.read("C:\sanatliumconfig.ini")
        cons_key = parser.get("consumer", "key")
        cons_secret = parser.get("consumer", "secret")
        acs_token = parser.get("token", "key")
        acs_secret = parser.get("token", "secret")
        self.api = TwitLib2.TwitterAPICore(cons_key ,cons_secret ,acs_token ,acs_secret)
        def callback_userstreaming(self ,event):
            if isinstance(event ,TwitLib2.Tweet):
                self.que.append(event)
        self.userstreaming = TwitLib2.UserStreamCore(cons_key ,cons_secret ,acs_token ,acs_secret ,callback_userstreaming)
        self.userstreaming.start()
        self.user_info = self.api.get_verify()
        
                
    def update(self ,status ,in_reply_to_id = None):
        status = status.decode("utf-8")
        try:
            thread.start_new_thread(self.api.post_tweet, (status ,in_reply_to_id))
        except urllib2.HTTPError ,error:
            print error.code
            print type(error.code)

        
    def get_tl(self ,count = None):
        thread.start_new_thread(lambda self ,count:self.userstreaming.que.extend(self.api.get_home_timeline(count)) ,(self ,count))

    def get_mention(self ,count = None):
        thread.start_new_thread(lambda self ,count:self.userstreaming.que.extend(self.api.get_mention(count)) ,(self ,count))

    
    def create_favorite(self ,tweet_id):
        try:
            thread.start_new_thread(self.api.create_favorite ,(tweet_id,))
        except:
            print "error in create_favorite"

    def create_retweet(self ,tweet_id):
        try:
            thread.start_new_thread(self.api.create_retweet ,(tweet_id,))
        except:
            print "error in create_retweet"
        
    def check_que(self):
        if self.userstreaming.que:
            tl = self.userstreaming.que[:]
            self.userstreaming.que = []
            return tl
        else:
            return []

    def make_tweet_tag(self ,tweet):
        return """
        <div class="tweet %s %s %s" id="%s">
            <img src="%s" />
            <div class="tweet_value">
                %s(<span class="acountname">@%s</span>)
                <div class="doicon">
                    <input type="image" src="icon/reply.png" class="reply">
                    <input type="image" src="icon/QuoteTweet.png" class="QT">
                    <input type="image" src="icon/favorite.png" class="fav">
                </div><br />
                <span class="acounttext">%s</span>
            </div>
            <hr size="1" noshade/>
        </div>
        """%("mypost" if self.user_info.screen_name == tweet.user.screen_name else ""
            ,"mention" if self.user_info.screen_name in tweet.text else ""
            ,"retweeted" if tweet.retweeted_status else ""
            ,tweet.id if not tweet.retweeted_status else tweet.retweeted_status.id
            ,tweet.user.profile_image_url if not tweet.retweeted_status else tweet.retweeted_status.user.profile_image_url
            ,tweet.user.name if not tweet.retweeted_status else tweet.retweeted_status.user.name
            ,tweet.user.screen_name if not tweet.retweeted_status else tweet.retweeted_status.user.screen_name
            ,tweet.text if not tweet.retweeted_status else tweet.retweeted_status.text)

    def make_tl_tag(self ,tl):
        return "".join([
        """
        <div class="tweet %s %s %s" id="%s">
            <img src="%s" />
            <div class="tweet_value">
                %s(<span class="acountname">@%s</span>)
                <div class="doicon">
                    <input type="image" src="icon/reply.png" class="reply">
                    <input type="image" src="icon/QuoteTweet.png" class="QT">
                    <input type="image" src="icon/favorite.png" class="fav">
                </div><br />
                <span class="acounttext">%s</span>
            </div>
            <hr size="1" noshade/>
        </div>
        """%("mypost" if self.user_info.screen_name == tweet.user.screen_name else ""
            ,"mention" if self.user_info.screen_name in tweet.text else ""
            ,"retweeted" if tweet.retweeted_status else ""
            ,tweet.id if not tweet.retweeted_status else tweet.retweeted_status.id
            ,tweet.user.profile_image_url if not tweet.retweeted_status else tweet.retweeted_status.user.profile_image_url
            ,tweet.user.name if not tweet.retweeted_status else tweet.retweeted_status.user.name
            ,tweet.user.screen_name if not tweet.retweeted_status else tweet.retweeted_status.user.screen_name
            ,tweet.text if not tweet.retweeted_status else tweet.retweeted_status.text)
        for tweet in tl])
        
class TabHandler:
    def __init__(self ,draw_handler):
        self.tab_dict = {}
        self.draw_handler = draw_handler
        
    def make_tab(self ,id ,func):
        self.tab_dict[id] = func
        
    def update(self ,tl):
        for tweet in tl:
            for id in self.tab_dict.keys():
                if self.tab_dict[id](tweet):
                    self.draw_handler(id ,tweet)
