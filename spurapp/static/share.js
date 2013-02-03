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
    
    setUpFBLink();
};

function setUpFBLink()
{
	fblink = document.getElementById("facebook");
	
	$(fblink).click(function(){
	    FB.getLoginStatus(function(response) {
		    if (response.status === 'connected') {
			    // connected
			    console.log("Logged in already. Ready to go!!!");
			    short_token = response.authResponse.accessToken;
			    share();
			} else {
			    // not_logged_in or not authorized
			    login();
			}
		});
		return false;
	});
};

function login() {
    FB.login(function(response) {
        if (response.authResponse) {
            // connected
            short_token = response.authResponse.accessToken;
        }
    }, {scope: 'email,publish_actions'});
}

function share(id)
{
	FB.ui(
	  {
	   method: 'feed',
	   name: 'I just donated $$$$ to Charity!',
	   caption: 'I just donated to charity and you should too!',
	   description: (
		  "I'm sharing the gift of giving. By clicking on this link and stuff you can donate to the charity I donated to and it's awesoemsauce!"
	   ),
	   link: 'http://sleepy-ridge-5514.herokuapp.com/'
	  },
	  function(response) {
		if (response && response.post_id) {
		  window.location.href = 'http://sleepy-ridge-5514.herokuapp.com/';
		} else {
		  alert('Post was not published.');
		}
	  }
	);
	console.log(donate_url+"?donatorbadge_parent="+id);
	//FB.ui(obj, function(){document.write("Thank you for your donation!! Redirecting now..."); window.location.href = 'http://proto.okcollaborative.org/';});
	FB.ui(obj, function(){window.location.href = 'http://sleepy-ridge-5514.herokuapp.com/';});
};