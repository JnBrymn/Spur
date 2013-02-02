// Load Facebook API
(function(d){
     var js, id = 'facebook-jssdk', ref = d.getElementsByTagName('script')[0];
     if (d.getElementById(id)) {return;}
     js = d.createElement('script'); js.id = id; js.async = true;
     js.src = "//connect.facebook.net/en_US/all.js";
     ref.parentNode.insertBefore(js, ref);
   }(document));


window.fbAsyncInit = function() {
	console.log("Facebook API is loaded");
    FB.init({
      appId      : '379998022075309', // App ID from the App Dashboard
      //channelUrl : '//WWW.YOUR_DOMAIN.COM/channel.html', // Channel File for x-domain communication
      status     : true, // check the login status upon init?
      cookie     : true, // set sessions cookies to allow your server to access the session?
      xfbml      : true  // parse XFBML tags on this page?
    });
};

function createBadge()
{
	fblink = document.getElementById("facebook");
	if(div == null) return;
	
	fblink.onclick = function(){
	    FB.getLoginStatus(function(response) {
		    if (response.status === 'connected') {
			    // connected
			    console.log("Logged in already. Ready to go!!!");
			    short_token = response.authResponse.accessToken;
			    recordDonation();
			} else {
			    // not_logged_in or not authorized
			    login();
			}
		});
		return false;
	};
};

function login() {
    FB.login(function(response) {
        if (response.authResponse) {
            // connected
            short_token = response.authResponse.accessToken;
        }
    }, {scope: 'email,publish_actions'});
}

function createLink(id)
{
	parent_id = getCookie("donatorbadge_parent");
	var obj = {
		method: 'feed',
		link: donate_url+"?donatorbadge_parent="+id,
		picture: 'http://proto.okcollaborative.org/badge.png',
		name: fb_title,
		caption: fb_caption,
		description: fb_description
	};

	console.log(donate_url+"?donatorbadge_parent="+id);
	//FB.ui(obj, function(){document.write("Thank you for your donation!! Redirecting now..."); window.location.href = 'http://proto.okcollaborative.org/';});
	FB.ui(obj, function(){window.location.href = 'http://proto.okcollaborative.org/';});
};