# -*- coding: utf-8 -*-

"""
(Built on top of a) Yelp Fusion API code sample.

This program requires the Python requests library, which you can install via:
`pip install -r requirements.txt`.

Sample usage:
`python yelp_fusion.py --price="1" --location="San Francisco, CA"`

Will search for restaurants with a price value of $
    Other values are 2,3,4 OR you can search "2,3,4" to include restaurants that are either $$,$$$,$$$$
"""
from __future__ import print_function

import argparse
import json
import pprint
import requests
import sys
import urllib


# This client code can run on Python 2.x or 3.x.  Your imports can be
# simpler if you only need one of those.
try:
    # For Python 3.0 and later
    from urllib.error import HTTPError
    from urllib.parse import quote
    from urllib.parse import urlencode
except ImportError:
    # Fall back to Python 2's urllib2 and urllib
    from urllib2 import HTTPError
    from urllib import quote
    from urllib import urlencode


# OAuth credential placeholders that must be filled in by users.
# You can find them on
# https://www.yelp.com/developers/v3/manage_app
CLIENT_ID = None
CLIENT_SECRET = None


# API constants, you shouldn't have to change these.
API_HOST = 'https://api.yelp.com'
SEARCH_PATH = '/v3/businesses/search'
BUSINESS_PATH = '/v3/businesses/'  # Business ID will come after slash.
TOKEN_PATH = '/oauth2/token'
GRANT_TYPE = 'client_credentials'


# Defaults for our simple example.
DEFAULT_PRICE = '2'
DEFAULT_LOCATION = 'San Francisco, CA'
DEFAULT_CATEGORIES = ''

def request(host, path, bearer_token, url_params=None):
    """Given a bearer token, send a GET request to the API.

    Args:
        host (str): The domain host of the API.
        path (str): The path of the API after the domain.
        bearer_token (str): OAuth bearer token, obtained using client_id and client_secret.
        url_params (dict): An optional set of query parameters in the request.

    Returns:
        dict: The JSON response from the request.

    Raises:
        HTTPError: An error occurs from the HTTP request.
    """
    url_params = url_params or {}
    url = '{0}{1}'.format(host, quote(path.encode('utf8')))
    headers = {
        'Authorization': 'Bearer %s' % bearer_token,
    }

    print(u'Querying {0} ...'.format(url))

    response = requests.request('GET', url, headers=headers, params=url_params)

    return response.json()


def search(bearer_token, price, location, categories):
    """Query the Search API by a search price and location.

    Args:
        price (str): The search price passed to the API.
        location (str): The search location passed to the API.

    Returns:
        dict: The JSON response from the request.
    """

    RESTAURANT_LIMIT = 3

    url_params = {
        'term': 'restaurants',
        'location': location.replace(' ', '+'),
        'limit': RESTAURANT_LIMIT,
        'open_now': 'true',
        'price': price,
        'categories': categories
    }
    return request(API_HOST, SEARCH_PATH, bearer_token, url_params=url_params)


def get_business(bearer_token, business_id):
    """Query the Business API by a business ID.

    Args:
        business_id (str): The ID of the business to query.

    Returns:
        dict: The JSON response from the request.
    """
    business_path = BUSINESS_PATH + business_id

    return request(API_HOST, business_path, bearer_token)


def query_api(price , location, categories):
    """Queries the API by the input values from the user.

    Args:
        price (str): The search price to query.
        location (str): The location of the business to query.
    """
    bearer_token = 'B5XYOw2fqoxnXH5dUEaf3Mp57gTsUkGHQBiDa8viH1uYQDlCxox7p9G0b45QVr2BiJkziIGWaPhjdQhd-xtfhf1AUZ9yx2Xejn3GTNPEojfgCAVOn7stSbYvKDJ6WXYx'

    response = search(bearer_token, price, location, categories)

    businesses = response.get('businesses')

    if not businesses:
        print(u'No businesses for {0} in {1} found.'.format(price, location))
        return

    #business_id = businesses[0]['id']
    for index, biz in enumerate(businesses):
        biz_id = businesses[index]['id']
        response = get_business(bearer_token, biz_id)
        pprint.pprint(response, indent=2)

    if len(businesses) == 0:
        print('No businesses found')

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('--price', dest='price', default=DEFAULT_PRICE, type=str, help='Search price (default: %(default)s)')
    parser.add_argument('--location', dest='location', default=DEFAULT_LOCATION, type=str, help='Search location (default: %(default)s)')
    parser.add_argument('--categories', dest='categories', default=DEFAULT_CATEGORIES, type=str, help='Search location (default: %(default)s)')

    input_values = parser.parse_args()

    try:
        query_api(input_values.price, input_values.location, input_values.categories)
    except HTTPError as error:
        sys.exit(
            'Encountered HTTP error {0} on {1}:\n {2}\nAbort program.'.format(
                error.code,
                error.url,
                error.read(),
            )
        )


if __name__ == '__main__':
    main()
