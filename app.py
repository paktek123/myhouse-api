import requests
from flask import Flask, request, jsonify

app = Flask(__name__)
app.debug = True

NESTORIA_BASE_URL = "http://api.nestoria.co.uk/api"
LISTING_URL = "?action=search_listings&encoding=json&place_name={}&listing_type={}"

@app.route('/search', methods=['GET'])
def quick_search():
  location_by_place = request.args.get('location_by_place')
  location_by_coordinates = request.args.get('location_by_coordinates')
  listing_type = request.args.get('listing_type', 'buy')

  nestoria_call = requests.get(NESTORIA_BASE_URL + LISTING_URL.format(location_by_place, listing_type))
  nestoria_response = nestoria_call.json()

  listings = []
  for listing in nestoria_response['response']['listings']:
    build_listing = dict(bedrooms=listing.get('bedroom_number'), 
                         bathrooms=listing.get('bathroom_number'),
                         title=listing.get('title'),
                         description=listing.get('summary'),
                         price=listing.get('price_high'),
                         lister_name=listing.get('lister_name'),
                         longitude=listing.get('longitude'),
                         latitude=listing.get('latitude'),
                         image=listing.get('thumb_url'),
                         lister_url=listing.get('lister_url'),
                         last_updated=listing.get('updated_in_days_formatted'))
    listings.append(build_listing)

  return jsonify(data=listings, nestoria_api_time_elapsed=nestoria_call.elapsed.total_seconds())

if __name__ == "__main__":
      app.run(host="0.0.0.0", port=8070)
