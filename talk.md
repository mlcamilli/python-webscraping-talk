I just wanted to preface this talk with scraping and ethics. Web scraping is an
amazing tool for automating data collection on websites that don't provide an
easy way to get access to their information. That being said, be ethical about
your scraping habits. If someone has an API, use it. Don't DDOS their site by
making 1000 requests a second, etc. Truth is if it feels sketchy you probably
shouldn't be doing it. 

---

So as previously stated this is a guide to scraping with python. Becoming good
at web scraping basically entails becoming very familiar with a set of tools.

The first tool in our toolkit is the Chrome Developer Tools. They are a set of
tools for web authoring and debugging. The most notable features for scraping
will be the ability to inspect elements on a screen and see the html
representations behind them and the ability to record and view network traffic.
This will expose API endpoints to us and all the data needed to be passed to
said endpoints.

---

Next up is the requests library in python. If you have worked with anything web
related in python you have probably used this library. It is an HTTP library
whose tagline reads "for human beings". Basically if you have ever had to use
urlib2 or 3 you know what a pain it is to interact with, requests makes it very
very easy to make http calls as shown by this code example.

---
Then we have beautiful soup which is a python library for parsing data out of
HTML and XML. This goes pretty hand in hand with requests, utilizing requests
to grab the html, and beautiful soup to parse that html to get the needed data
out.


---
For the more complicated or javascript ridden scrapes we turn to Selenium,
specificaly their WebDriver tool which provides an API to drive a browser
natively as a user would. Selenium is often used in a lot of testing, for
functional front end testing / cross browser testing. However it also has some
pretty amazing applications when it comes to web scraping. While actually using
Selenium Webdriver isn't all that difficult, getting all the dependencies set
correctly can be a horrible adventure.

This example shows a firefox browser navigating to yahoo, searching for
something, and then exiting. 

---
Lastly I utilize the gloriousness that is redis. Redis is an open source
advanced key-value cache and store that is great for storing session
information and cookies which is really helpful when dealing with some advanced
scrapes that need to get past authentication walls.

---

For our first scrape I want to keep things simple and take part of a side
project I'm working on called dcmusic. The idea is to constantly pull concert
information from all of dc's local venues and to provide all the upcoming
concerts and links to tickets in a convenient calendar view. Progress wise all
the scrapers have been set up, now I just need to dive into the front end.

---

So the first step in any scraping problem is to find out what you want and
where it is located. Simply enough for 930 club we want to just scrape all the
concerts in the concerts tab of its website. This website is pretty simple html
with no javascript or authentication wall for us to overcome, so requests and
beautiful soup will be all we need for this scrape.

Looking at the html it is apparent that all the concerts are listed in the same
sort of style, so to figure out exactly what we should scrape we will just
right click on one of the concerts and click inspect element, taking us into an
html view of that element.

---

Here we can start to notice some patterns, like the parent div has a class
"list-view-item" on it, which all concert divs have. 
Beautiful soup has numerous ways of navigating html and searching for elements.
To collect all of the divs that the concerts are in first we will get the html
of this page, create a beautiful soup object out of it, and then utilize
beautiful soup's find_all function. We will search for divs, specifically that
have a class attribute of list-view-item in them.

---

Now that we have all the concert divs, it is time to figure out how to get the
data we want out of them. 
For starters lets look at the artist field, how do we find our headliner.
Looking at it it is stored in the h1 field, and there is only one h1 field. So
we can simply call the concertdiv's h1 field and then extract the text
associated with it.
Next up we will want to grab the date and the time of this concert.
Conveniently the html of dates has the class dates and time has the class
times. We can grab the two texts, concatonate them, and then have the nifty
python dateutil library parse the date out of it.
then we simply grab the ticketfly link to the concert and detect whether it is
sold out or not based on whether the ticket link is there or not.
---

So that covers a good majority of scraping scenarios, load a page, soup the
page, grab data out. The next two examples I want to go over involve getting
through authentication, typically after you authenticate you can then just soup
the page and do what we just did to extract data, so I won't be focusing on the
data extraction parts of the next two examples.

So for this next example we are going to log in to meetup.com and store the
cookies so that we can later visit the site without reauthenticating. 
---
The first step here is again to navigate to the login page of meetup
---
For logins what I then do is bring up the chrome developer tools, open the
network tab, hit record, and then log into the website. This shows the request,
the method used, the endpoint hit, the headers used, and the form data passed
to the login.

The most notable challenge for us to overcome here is that there is a Cross
Site Request Forgery token sent to the endpoint.
These are generated on the page, we can't just use one every single time, we
will have to extract that from the page first and then authenticate using it.
---
Now that we know what we need to supply the endpoint with, we need to fetch the
information off of the page. We start this process by once again inspecting the
form element to see the markup behind it.  We can see a hidden input with the
name token that contains the csrf token that we are trying to extract.


So in this case, we are going to use what is called a request session. This is
similar to using the request object however it stores state and cookies, more
closely tied with the behavior of a browser.  So our first step is to
instantiate the session, grab the login page, soup it, and then extract that
token.

Now that we have the token, we want to prepare the data for our form post.
Then we just post to the login url with that data and I threw in an assert here
to just double check that we are in fact logged in. An invalid login would keep
us on the same login page while a successful one will redirect us to the base
site.

Lastly I pull up redis so that I can dump all of the cookies we just received
into a redis store with the key meetup.
---
Now when we want to revisit this site as an authenticated user we just have to
reinstantiate our session object, fetch the cookies out of redis, load the
cookies into the session object, and if we hit that page we should not be able
to find the login button as we are already logged in.
---
For our last example we are going to auth into airbnb which is a pretty
contemporary site. The first challenge we see right off the bat is that this
probably a single page app that is just loaded with javascript. Hell there is
a movie playing in the background of the website. Let's see if the login is at
least easy.
---

Ah a modal, well modals make everything more difficult. As do frames, new
windows, and the various other problems that can arise when trying to
authenticate on some sites. For instance soundcloud opens a new window and
almost always asks for a captcha.
---
Our solution for this? We are going to go headless and use selenium's webdriver
+ a headless browser to emulate a users' interaction on a page.

Like I previously mentioned often the hardest part of using selenium and
headless browsers is getting the dependcies to work and have everything
installed correctly. Honestly this part can take hours. So instead I made
a dockerfile that includes all the dependencies and pip installs a custom
scraping library I made implementing these different browsers.

---
Basically it creates a wrapper class that instantiates the webdriver with
a common user agent and exposes the webdriver along with a few helper commands.
You can also pass in a proxy here if need be.
---
This is the FirefoxScraper which utilizes a pyvirtualdisplay package which
basically uses the linux package  xbfb, X virtual framebuffer , which is
basically a virtual display server. Basically before we can have our virtual
browser running we have to have a virtual dispaly to attach it to. This is
actaully a really awesome feature as we will be able to take screenshots in the
middle of scraping later to see our progress.
---
So for this scrape I'm actually going to do the parts live and incrementally,
**fingers crossed**.
--- 
The first step is to go to the page and click the login button. 
I'll take a screenshot before and after clicking the login button. I'll explain
the implicit wait in a little bit.
---
So here is the full code for the login. Actually pretty simple. But to explain
the implicit wait, basically when I click that login button on the screen, it
might take the javascript a second or less to respond. However when I try to
send my email to a field immediately after clicking that button it might not
exist yet. Implicit wait basically states that when finding elements if they
don't exist upon the first look, poll the dom up to 10 seconds after to see if
they do. If they don't in that time it will error out. Which is exactly what
happened the first several times I tried to get this to work. 
After that we simply hit submit on the login button which will just call submit
on the form itself.

As you can hopefully see in the screenshot after this worked!
Just like in the previous session example we will then dump the cookies into
redis so we can use them later
---
Revisitng the site in a headless browser is just slightly different as
firefox's webdriver has some specific rules to it about setting cookies that
chrome does not have. You can only set cookies that pertain to the domain that
you are currently on. So to load cookies in this example we have to get the
page first, delete all current cookies, load the cookies desired, and then
reload the page.
---
That's all I have, questions?
