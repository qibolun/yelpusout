# yelpusout
install virtual box
install docker
install python 3.6

#useful docker command to start docker
http://testdriven.io/part-one-workflow/

Currently the project/yelp_fusion.py file has logic for querying the Yelp Fusion API. It's in a separate file as its in a proof of concept state.
You can run it like this:  
  python yelp_fusion.py --price="1" --location="San Francisco, CA"
Or just python yelp_fusion.py if you'd like to use the default values of price=2 and location="San Francisco, CA"

Where location is a city, state, address, zip code, etc.
  We may want to move to lat/long
Price is either a number (1 or 2 or 3 or 4) or a list of numbers "1,2" or "1,2,3,4" which will include multiple price tiers

