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
        
                
    def update(self ,status ,in_reply_to_id = None):
        status = status.decode("utf-8")
        try:
            thread.start_new_thread(self.api.post_tweet, (status ,in_reply_to_id))
        except urllib2.HTTPError ,error:
            print error.code
            print type(error.code)

        
    def get_tl(self ,count = None):
        tl = self.api.get_home_timeline(count)
        return self.make_tl_tag(tl)
    
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
            return self.make_tl_tag(tl)
            
    def make_tl_tag(self ,tl):
        return "".join([
        """
        <div class="tweet" id="%s">
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
            <hr />
        </div>
        """%(tweet.id
            ,tweet.user.profile_image_url 
            ,tweet.user.name 
            ,tweet.user.screen_name 
            ,tweet.text)
        for tweet in tl])
        
    