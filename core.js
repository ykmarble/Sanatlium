jQuery(function(){
	//set tab_handler
	tab_handler.make_tab("timeline" ,function(tweet){return true});
	tab_handler.make_tab("replytab" ,function(tweet){
		return tweet.text.indexOf(api_handler.user_info.screen_name) != -1
	});
	tab_handler.make_tab("myposttab" ,function(tweet){
		return tweet.user.screen_name == api_handler.user_info.screen_name
	});
	tab_handler.make_tab("marbletab" ,function(tweet){
		return tweet.text.indexOf("まーぶる") != -1
	});
	tab_handler.draw_handler = function(id ,tweet){
		jQuery("#"+id).prepend(api_handler.make_tweet_tag(tweet));
	};
	
	//global variable
	var in_reply_to = ["" ,""];//0:in_reply_to_id 1:status
	
	//load last 200 Home TimeLine and reply
	//api_handler.get_user_tl("yk_marble" ,200);
	//api_handler.get_mention(200);
	//api_handler.get_tl(200);
	
	//set timeline div size
	var postformheight = jQuery("#post_form").innerHeight();	
	var windowheight = jQuery(window).height();
	jQuery(".maintab").height(windowheight-postformheight-60);
	
	// set UserStreamings Event Lisetener
	setInterval(function(){
		tab_handler.update(api_handler.check_que());
		jQuery("#post_count").text(tab_handler.container.__len__());
	} ,500);
	/*
	//reflesh html
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
		if (in_reply_to[0] != ""){
			api_handler.update(jQuery("#post_status").val() ,in_reply_to[0]);
			in_reply_to = ["" ,""];
			jQuery("#in_reply_to_indicator").remove();
		}else{
			api_handler.update(jQuery("#post_status").val());
		}
		jQuery("#post_status").val("");
	});
	//reply
	jQuery(".reply").live("click",function(){
		var getAcount = jQuery(this).parents(".tweet").find(".acountname").text();
		jQuery("#post_status").text(getAcount+" ");
		jQuery("#post_status").focus();
		in_reply_to[0] = jQuery(this).parents(".tweet").attr("id");
		in_reply_to[1] = "in reply to..."+getAcount+":"+jQuery(this).parents(".tweet").find(".acounttext").text();
		if (jQuery("#in_reply_to_indicator").size() == 0){
			jQuery("#post_form").prepend("\
				<div id='in_reply_to_indicator'>"+in_reply_to[1]+"<button id='in_reply_to_delete'>解除</button></div>\
				");
		}else{
			jQuery("#in_reply_to_indicator").html(in_reply_to[1]+"<button id='in_reply_to_delete'>解除</button>");
		}
		var getAcount ="";
	});
	/*
	//Unofficial RT
	jQuery(".tweet").live("click",function(){
		var getAcount = jQuery(this).find(".acountname").text();
		var getText =jQuery(this).find(".acounttext").text();
		jQuery("#post_status").text(" RT "+getAcount+": "+getText);
		jQuery("#post_status").focus();
		var getAcount ="";
	});
	*/
	//QT
	jQuery(".QT").live("click",function(){
		var getAcount = jQuery(this).parents(".tweet").find(".acountname").text();
		var getText = jQuery(this).parents(".tweet").find(".acounttext").text();
		jQuery("#post_status").text(" QT "+getAcount+": "+getText);
		jQuery("#post_status").focus();
		in_reply_to[0] = jQuery(this).parents(".tweet").attr("id");
		in_reply_to[1] = "in reply to..."+getAcount+":"+getText;
		if (jQuery("#in_reply_to_indicator").size() == 0){
			jQuery("#post_form").prepend("\
				<div id='in_reply_to_indicator'>"+in_reply_to[1]+"<button id='in_reply_to_delete'>解除</button></div>\
				");
		}else{
			jQuery("#in_reply_to_indicator").html(in_reply_to[1]+"<button id='in_reply_to_delete'>解除</button>");
		}
		var getAcount ="";
	});
	//create favorite
	jQuery(".fav").live("click",function(){
		api_handler.create_favorite(jQuery(this).parents(".tweet").attr("id"));
		alert("favarited");
	});
	/*
	//create RT
	jQuery(".tweet").live("click",function(){
		api_handler.create_retweet(jQuery(this).attr("id"));
		alert("RTed");
	});
	*/
	//icon clicked
	jQuery(".icon").live("click" ,function(){
		var memo = jQuery(this).parent().find(".acountname").text();
		api_handler.urlopen("https://twitter.com/"+memo.slice(1));
	});
	//anchor clicked
	jQuery("a").live("click" ,function(){
		api_handler.urlopen(jQuery(this).attr("href"));
	});
	//delete in_reply_to
	jQuery("#in_reply_to_delete").live("click" ,function(){
		in_reply_to = ["" ,""];
		jQuery("#in_reply_to_indicator").remove();
	});
	
	
	/*
	//reply bom
	jQuery(".reply_bom").live("click",function(){
	var getAcount = jQuery(this).parents(".tweet").find(".acountname").text();
	for(var z = 1; z < 10;z++){
		getAcount = getAcount+".";
		api_handler.update(jQuery(getAcount).val());
		}
	getAcount = "";
	});
	*/
				
	//make tab script
	jQuery(".tab li a").click(function(){
		jQuery(".tab li a").removeClass("selected");
		jQuery(this).addClass("selected");
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
	jQuery(".tweet input").live("mousemove" ,function(e){
		var tipID = "#"+jQuery(this).attr("class")+"_tip";
		jQuery(tipID).css({"top":e.pageY-20+"px","left":e.pageX-20+"px"});
	});
	
	//display string length of post_form
	jQuery("#post_status").bind("change keyup",function(){
		var WriLeng = jQuery(this).val().length;
		var Leng = 140 - WriLeng;
		jQuery("#textcount").text(Leng);
		if(Leng < 0){
			jQuery("#textcount").css("color","red");
		}else{
			jQuery("#textcount").css("color","#000");
		}
	});
	
	//set Window Resize Event Handler
	jQuery(window).resize(function(){
		windowheight = jQuery(window).height();
		jQuery(".maintab").height(windowheight-postformheight-60);
	});
	
	//set Key Config
	jQuery("#post_form").gpKey("down" ,{
		"^enter":function(){
			jQuery("#post_button").click();
			
		},
	});
	
	//delay post
	jQuery("#after_post").live("click" ,function(){
		jQuery("#backgray").fadeIn(1000);
		jQuery("#outimage").fadeIn(900);
		jQuery("#outimage").fadeIn(500).html("<div id='after_top'>予約投稿</div><div id='after_bottom'><span style='font-size:200%;'>何を投稿する？</span><br /><textarea id='after_area'></textarea><br /><input type='text' id='gethour' value='0' />時間<input type='text' id='getminute' value='0' />分<input type='text' id='getsecond' value='0' />秒後に送信する<br /><input type='button' id='gopost' value='予約投稿' /></div>");
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
		jQuery("#outimage").fadeOut(1000);
		jQuery("#backgray").fadeOut(1000);	
	});
});