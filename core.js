//global variable
var in_reply_to_id = "";

jQuery(function(){
	//get Consumer and Token
	var cons_key = parser.get("consumer", "key");
	var cons_secret = parser.get("consumer", "secret");
	var acs_token = parser.get("token", "key");
	var acs_secret = parser.get("token", "secret");
	
	if (cons_key == "" || cons_secret == "" || acs_token == "" || acs_secret == ""){
		jQuery("#backgray").fadeIn(500);
		jQuery("#setup").fadeIn(500);
		while (True);
	}
	
	//make handler
	var api_handler = SanatliumCore.TwitterAPIHandler(cons_key ,cons_secret ,acs_token ,acs_secret);
	var tab_handler = SanatliumCore.TabHandler(function(id ,tweet){
		jQuery("#"+id).prepend(api_handler.make_tweet_tag(tweet))
	});
	
	//set tab_handler
	tab_handler.make_tab("timeline" ,function(tweet){
		return true
	});
	tab_handler.make_tab("replytab" ,function(tweet){
		return tweet.text.indexOf(api_handler.user_info.screen_name) != -1
	});
	tab_handler.make_tab("myposttab" ,function(tweet){
		return tweet.user.screen_name == api_handler.user_info.screen_name
	});
	tab_handler.make_tab("marbletab" ,function(tweet){
		return tweet.text.indexOf("まーぶる") != -1
	});
	
	//load last Home TimeLine and reply
	api_handler.get_user_tl("yk_marble" ,20);
	api_handler.get_mention(20);
	api_handler.get_tl(20);
	
	// set UserStreamings Event Lisetener
	setInterval(function(){
		if (!api_handler.userstreaming.que.empty()){
			var view_id = jQuery(".tab .current_tab").attr("href");
			var scr_pos = jQuery(view_id).scrollTop();
			var old_height = jQuery(view_id).get(0).scrollHeight;
			tab_handler.update(api_handler.check_que());
			var new_height = jQuery(view_id).get(0).scrollHeight;
			if (scr_pos!=0 && !jQuery("#auto_scroll").hasClass("enable")){
				jQuery(view_id).scrollTop(scr_pos + new_height - old_height);
			};
			jQuery("#post_count").text(tab_handler.container.__len__());
		};
	} ,500);

	
	//set timeline div size
	var postformheight = jQuery("#post_form").innerHeight();	
	var windowheight = jQuery(window).height();
	jQuery(".maintab").height(windowheight-postformheight-60);
	
	/*
	//limit the number of statuses in html
	setInterval(function(){
		var postCount= jQuery(".tweet").length;
		if(postCount >500){
			for(var c = postCount; 500<=c;c--){
				jQuery(".tweet").eq(c).remove();
			}
		}
	},500);
	*/
		
		
	//set UI Event Handler
	//POST button
	jQuery("#post_button").click(function(){
		var status = jQuery("#post_status").val();
		if (status != ""){
			if (in_reply_to_id != ""){
				api_handler.update(status ,in_reply_to_id);
				in_reply_to_id = "";
				jQuery("#in_reply_to_indicator").remove();
			}else{
				api_handler.update(status);
			}
			jQuery("#post_status").val("");
			jQuery("#post_status").keyup();
			jQuery("#post_status").blur();
		}
	});
	//reply
	jQuery(".reply").live("click",function(){
		var screenname = jQuery(this).parents(".tweet").find(".accountname").text();
		jQuery("#post_status").text("@"+screenname+" ");
		jQuery("#post_status").focus();
		in_reply_to_id = jQuery(this).parents(".tweet").attr("id");
		var in_reply_to_status = "in reply to...@"+screenname+":"+jQuery(this).parents(".tweet").find(".accounttext").text();
		if (jQuery("#in_reply_to_indicator").size() == 0){
			jQuery("#post_form").prepend( 
				"<div id='in_reply_to_indicator'>"+in_reply_to_status+"<button id='in_reply_to_delete'>解除</button></div>"
			);
		}else{
			jQuery("#in_reply_to_indicator").html(in_reply_to_status+"<button id='in_reply_to_delete'>解除</button>");
		}
		return false
	});
	/*
	//Unofficial RT
	jQuery(".UnofficialRT").live("click",function(){
		var screenname = jQuery(this).find(".accountname").text();
		var text =jQuery(this).find(".accounttext").text();
		jQuery("#post_status").text(" RT @"+screenname+": "+text);
		jQuery("#post_status").focus();
	});
	*/
	//QT
	jQuery(".QT").live("click",function(){
		var screenname = jQuery(this).parents(".tweet").find(".accountname").text();
		var text = jQuery(this).parents(".tweet").find(".accounttext").text();
		jQuery("#post_status").text(" QT @"+screenname+": "+text);
		jQuery("#post_status").focus();
		in_reply_to_id = jQuery(this).parents(".tweet").attr("id");
		var in_reply_to_status = "in reply to...@"+screenname+":"+text;
		if (jQuery("#in_reply_to_indicator").size() == 0){
			jQuery("#post_form").prepend(
				"<div id='in_reply_to_indicator'>"+in_reply_to_status+"<button id='in_reply_to_delete'>解除</button></div>"
			);
		}else{
			jQuery("#in_reply_to_indicator").html(in_reply_to_status+"<button id='in_reply_to_delete'>解除</button>");
		}
		return false
	});
	//create favorite
	jQuery(".fav").live("click",function(){
		var id = jQuery(this).parents(".tweet").attr("id");
		if (jQuery(this).parents(".doicon").children("span").hasClass("faved")){
			api_handler.destroy_favorite(id);
			jQuery(this).parents(".doicon").children(".faved").remove();
		}else{
			api_handler.create_favorite(id);
			jQuery(this).parents(".doicon").prepend("<span class='faved'>★</span>");
		};
		return false
	});
	//create RT
	jQuery(".RT").live("click",function(){
		api_handler.create_retweet(jQuery(this).attr("id"));
		return false
	});
	//tweet cliked
	jQuery(".tweet").live("click" ,function(){
		if (jQuery(this).hasClass("selected_status")){
			jQuery(".tweet").removeClass("selected_status");
		}else{
			jQuery(".tweet").removeClass("selected_status");
			jQuery(this).addClass("selected_status");
		};
	});
	//icon clicked
	jQuery(".icon").live("click" ,function(){
		var screenname = jQuery(this).parent().find(".accountname").text();
		api_handler.urlopen("https://twitter.com/"+screenname);
		return false
	});
	//anchor clicked
	jQuery(":not(.tab li) a").live("click" ,function(){
		api_handler.urlopen(jQuery(this).attr("href"));
		return false
	});
	//delete in_reply_to
	jQuery("#in_reply_to_delete").live("click" ,function(){
		in_reply_to = "";
		jQuery("#in_reply_to_indicator").remove();
	});
	//auto scroll toggle button
	jQuery("#auto_scroll").live("click" ,function(){
		jQuery(this).toggleClass("enable");
	});

				
	//change tab
	jQuery(".tab li a").click(function(){
		jQuery(".tab li a").removeClass("current_tab");
		jQuery(this).addClass("current_tab");
		jQuery(".maintab").hide();
		jQuery(jQuery(this).attr("href")).fadeIn(0);
		return false;
	});		
	
	//check if mouse cursor on timeline
	jQuery(".maintab").mouseover(function(){
		jQuery(this).focus();
		jQuery(".tooltip").css("display","none");				
	});
	
	//tool tip
	jQuery(".tweet input").live("mouseover",function(e){
		var tipID = "#"+jQuery(this).attr("class")+"_tip";
		jQuery(tipID).css({"top":e.pageY-20+"px","left":e.pageX-20+"px"});
		jQuery(tipID).fadeIn(300);
	});
	jQuery(".tweet input").live("mouseout",function(){
		jQuery(".tooltip").css("display","none");
	});

	//display string length of post_form
	jQuery("#post_status").bind("change keyup",function(){
		var length = jQuery(this).val().length;
		jQuery("#textcount").text(length);
		if(length > 140){
			jQuery("#textcount").css("color","red");
		}else{
			jQuery("#textcount").css("color","#000");
		}
	});
	
	//set Window Resized Event Handler
	jQuery(window).resize(function(){
		windowheight = jQuery(window).height();
		jQuery(".maintab").height(windowheight-postformheight-57);
	});
	
	//set Key Config
	jQuery("body").keydown(function(e){
		var keyCode = e.which;
		
		//convertKeyCode to Ascii
		if ((48 <= keyCode && keyCode <= 48 + 10) 
		 || (65 <= keyCode && keyCode <= 65 + 25)){
			var keyChar = String.fromCharCode(keyCode);
		}else if (keyCode == 13){
			var keyChar = "ENTER";
		}else if (keyCode == 27){
			var keyChar = "ESCAPE";
		}else{
			var keyChar = "ANOTHER";
		}
		if (e.ctrlKey && keyChar == "ENTER"){
		 	if (jQuery("#post_status:focus").length != 0){
		 		jQuery("#post_button").click();
		 	}else if (jQuery("#after_area:focus").length != 0){
		 		jQuery("#gopost").click();
		 	};
		}else if (keyChar == "ENTER"){
			if (jQuery("#post_status:focus").length == 0 && jQuery("#after_area").size() == 0){
				jQuery("#post_status").focus();
				return false
			};
		};
		if (keyChar == "ESCAPE"){
			if (jQuery("#post_status:focus").length != 0){
				jQuery("#post_status").blur();
				return false
			}else{
				jQuery(".tweet").removeClass("selected_status");
			};
		};
		if (jQuery("#post_status:focus").length == 0 && jQuery("#after_area:focus").length == 0){
			var cur_tab = jQuery(".tab .current_tab").attr("href");
			if (keyChar == "J"){
				if (jQuery(cur_tab).children().hasClass("selected_status")){
					var status_id = jQuery(".selected_status").next().attr("id");
					if (status_id != null){
						jQuery(cur_tab).children().removeClass("selected_status");
						jQuery("#"+status_id).addClass("selected_status");
					};
				}else{
					jQuery(cur_tab).children().slice(0 ,1).addClass("selected_status");
				};
				//scroll control
				if (jQuery(".selected_status").offset().top < jQuery(cur_tab).offset().top){
					jQuery(cur_tab).scrollTop(jQuery(".selected_status").offset().top - jQuery(cur_tab).children().offset().top)
				}else if (jQuery(".selected_status").offset().top + jQuery(".selected_status").height() > jQuery(window).height()){
					jQuery(cur_tab).scrollTop(jQuery(".selected_status").offset().top - jQuery(cur_tab).children().offset().top + jQuery(".selected_status").height()-jQuery(cur_tab).height()+22);
				};
			};
			if (keyChar == "K"){
				var status_id = jQuery(".selected_status").prev().attr("id");
				jQuery(cur_tab).children().removeClass("selected_status");
				if (status_id != null){
					jQuery("#"+status_id).addClass("selected_status");
					//scroll control
					if (jQuery(".selected_status").offset().top < jQuery(cur_tab).offset().top){
						jQuery(cur_tab).scrollTop(jQuery(".selected_status").offset().top - jQuery(cur_tab).children().offset().top)
					}else if (jQuery(".selected_status").offset().top + jQuery(".selected_status").height() > jQuery(window).height()){
						jQuery(cur_tab).scrollTop(jQuery(".selected_status").offset().top - jQuery(cur_tab).children().offset().top + jQuery(".selected_status").height()-jQuery(cur_tab).height()+22);
					};
				};
			};
			if (e.ctrlKey && keyChar == "R"){
				
			}else if (keyChar == "R"){
				jQuery(".selected_status").children(".tweet_value").children(".doicon").children(".reply").click();
				return false
			};
			if (keyChar == "F"){
				jQuery(".selected_status").children(".tweet_value").children(".doicon").children(".fav").click();
				return false
			};
			if (e.ctrlKey &&keyChar == "Q"){
				jQuery(".selected_status").children(".tweet_value").children(".doicon").children(".QT").click();
				return false
			};
		};
	});
	//delay post
	jQuery("#after_post").live("click" ,function(){
		jQuery("#backgray").fadeIn(1000);
		jQuery("#outimage").fadeIn(900);
		jQuery("#outimage").fadeIn(500).html(" \
			<div id='after_top'>予約投稿</div> \
			<div id='after_bottom'> \
				<span style='font-size:200%;'>何を投稿する？</span><br /> \
				<textarea id='after_area'>"+jQuery("#post_status").val()+"</textarea><br /> \
				<input type='text' id='gethour' value='0' />時間<input type='text' id='getminute' value='0' />分<input type='text' id='getsecond' value='0' />秒後に送信する<br /> \
				<input type='button' id='gopost' value='予約投稿' /> \
			</div> \
		");
		jQuery("#after_area").focus();
	});
	jQuery("#after_top").live("click" ,function(){
		jQuery("#outimage").fadeOut(1000);
		jQuery("#backgray").fadeOut(1000);	
	});
	jQuery("#backgray").live("click" ,function(){
		jQuery("#outimage").fadeOut(1000);
		jQuery("#backgray").fadeOut(1000);	
	});
	jQuery("#gopost").live("click" ,function(){
		var getH = jQuery("#gethour").val()*60*60*1000;
		var getM = jQuery("#getminute").val()*60*1000;
		var getS = jQuery("#getsecond").val()*1000;
		var getT = getH+getM+getS;
		var text = jQuery("#after_area").val();
		jQuery("#after_area").val("");
		setTimeout(function(s){
			api_handler.update(text);
		}　,getT ,text);
		jQuery("#post_status").val("");
		jQuery("#post_status").keyup();
		jQuery("#post_status").blur();
		jQuery("#outimage").fadeOut(1000);
		jQuery("#backgray").fadeOut(1000);
	});
});