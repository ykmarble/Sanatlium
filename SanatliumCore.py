import TwitLib2
import thread
import urllib2
import webbrowser
import re

class TwitterAPIHandler(object):
    def __init__(self ,cons_key ,cons_secret ,acs_token ,acs_secret):
        self.api = TwitLib2.TwitterAPICore(cons_key ,cons_secret ,acs_token ,acs_secret)
        def callback_userstreaming(self ,event):
            if isinstance(event ,TwitLib2.Tweet):
                self.que.put([event])
        self.userstreaming = TwitLib2.UserStreamCore(cons_key ,cons_secret ,acs_token ,acs_secret ,callback_userstreaming)
        self.userstreaming.start()
        self.user_info = self.api.get_verify()
        self.url_anchor_re = re.compile(r"(https?://[A-Za-z0-9\'~+\-=_.,/%\?!;:@#\*&\(\)]+)")
        self.name_anchor_re = re.compile(r"(^|\W)@(\w+)")
        
                
    def update(self ,status ,in_reply_to_id = None):
        status = status.decode("utf-8")
        try:
            thread.start_new_thread(self.api.post_tweet, (status ,in_reply_to_id))
        except urllib2.HTTPError ,error:
            print error.code
            print type(error.code)

        
    def get_tl(self ,count = None):
        thread.start_new_thread(lambda self ,count:self.userstreaming.que.put(self.api.get_home_timeline(count)) ,(self ,count))

    def get_mention(self ,count = None):
        thread.start_new_thread(lambda self ,count:self.userstreaming.que.put(self.api.get_mention(count)) ,(self ,count))

    def get_user_tl(self ,screen_name ,count = None):
        thread.start_new_thread(lambda self ,screen_name ,count:self.userstreaming.que.put(self.api.get_user_timeline(screen_name ,count)) ,(self ,screen_name ,count))

    
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
            
    def destroy_favorite(self ,tweet_id):
        try:
            thread.start_new_thread(self.api.destroy_favorite ,(tweet_id,))
        except:
            print "error in destroy_favorite"
        
    def check_que(self):
        tl = []
        while not self.userstreaming.que.empty():
            tl.extend(self.userstreaming.que.get())
        return tl
    
    def urlopen(self ,url):
        webbrowser.open(url)
        
    def wrap_anchor(self ,tweet):
        url_wraped = self.url_anchor_re.sub(r"<a href='\1' onclick='return false'>\1</a>" ,tweet.text)
        for long_url ,short_url in  tweet.entities.urls:
            url_wraped = url_wraped.replace(short_url ,long_url)
        name_wraped = self.name_anchor_re.sub(r"<a href='https://twitter.com/\2' onclick='return false'>\1@\2</a>" ,url_wraped)
        return name_wraped
    
    def make_tweet_tag(self ,tweet):
        return """
        <div class="tweet %s %s %s" id="%s">
            <img src="%s" class="icon" />
            <div class="tweet_value">
                %s(<a href="https://twitter.com/%s" onclick='return false'>@<span class="accountname">%s</span></a>)
                <div class="doicon">
                    <input type="image" src="icon/reply.png" class="reply">
                    <input type="image" src="icon/QuoteTweet.png" class="QT">
                    <input type="image" src="icon/favorite.png" class="fav">
                </div><br />
                <span class="accounttext">%s</span>
            </div>
            <hr size="1" noshade/>
        </div>
        """%("mypost" if self.user_info.screen_name == tweet.user.screen_name else ""
            ,"mention" if self.user_info.screen_name in tweet.text else ""
            ,"retweeted" if tweet.retweeted_status else ""
            ,tweet.id if not tweet.retweeted_status else tweet.retweeted_status.id
            ,tweet.user.profile_image_url if not tweet.retweeted_status else tweet.retweeted_status.user.profile_image_url
            ,tweet.user.name if not tweet.retweeted_status else tweet.retweeted_status.user.name
            ,tweet.user.screen_name if not tweet.retweeted_status else tweet.retweeted_status.user.name
            ,tweet.user.screen_name if not tweet.retweeted_status else tweet.retweeted_status.user.screen_name
            ,self.wrap_anchor(tweet) if not tweet.retweeted_status else self.wrap_anchor(tweet.retweeted_status.text))

    def make_tl_tag(self ,tl):
        return "".join(map(self.make_tweet_tag ,tl))
        
class TabHandler:
    def __init__(self ,draw_handler):
        self.tab_dict = {}
        self.unread_dict = {}
        self.draw_handler = draw_handler
        self.container = []
        
    def make_tab(self ,id ,func):
        self.tab_dict[id] = func
        self.unread_dict[id] = 0
        
    def update(self ,tl):
        self.container.extend(tl)
        for tweet in tl:
            for id in self.tab_dict.keys():
                if self.tab_dict[id](tweet):
                    self.draw_handler(id ,tweet)
                    self.unread_dict[id] += 1
