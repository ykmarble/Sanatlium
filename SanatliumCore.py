import TwitLib2

class TwitterAPIHandler(object):
    def __init__(self):
        cons_key = "4co1ltUgx33uBTjhrgpUw"
        cons_secret = "429iCfnuBckdOpmCn2IisjKy2TEDCbtMf72pm4E8AE"
        acs_token = "201709742-SYl13dJ0Xwwc9saSS8QwEORdeR6tbHaH4cRrOyjN"
        acs_secret = "L8r3MUXoj2XTdxz38oQyRW0PRGKba0yyaoq40OBRTY"
        self.api = TwitLib2.TwitterAPICore(cons_key ,cons_secret ,acs_token ,acs_secret)
#        def callback_userstreaming(self ,event):
#            if isinstance(event ,Event):
#                if event.event == "favorite":
#                    print "<%s(@%s) faved %s(@%s)%s>"%(event.source.name ,event.source.screen_name
#                                                       ,event.target.name ,event.target.screen_name
#                                                       ,event.target_object.text)
#                elif event.event == "unfavorite":
#                    print "<%s(@%s) unfaved %s(@%s)%s>"%(event.source.name ,event.source.screen_name
#                                                         ,event.target.name ,event.target.screen_name
#                                                         ,event.target_object.text)
#                elif event.event == "follow":
#                    print "<%s(@%s) followed %s(@%s)>"%(event.source.name ,event.source.screen_name
#                                                        ,event.target.name ,event.target.screen_name)
#                else:
#                    print "<%s event received.>"
#
#            elif isinstance(event ,Tweet):
#                self.que.append(event)
#                print "%s(@%s):%s"%(event.user.name ,event.user.screen_name ,event.text)
#            else:
#                print "TypeError:%s is not supported"%type(event)
#        self.userstreaming = TwitLib2.UserStreamCore(self.api ,callback_userstreaming)
#        self.userstreaming.start()
        
                
    def update(self ,status):
        status = status.decode("utf-8")
        tweet = self.api.post_tweet(status)
        return self.make_tl_tag([tweet])
        
    def get_tl(self):
        print "called"
        tl = self.api.get_home_timeline()
        return self.make_tl_tag(tl)
    
    def create_favorite(self ,id):
        self.api.create_favorite(id)
        
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
                %s(@%s)<br />
                %s
            </div>
            <hr />
        </div>
        """%(tweet.id
            ,tweet.user.profile_image_url 
            ,tweet.user.name 
            ,tweet.user.screen_name 
            ,tweet.text)
        for tweet in tl])
        
    