from flask import Flask, render_template, request
import requests
import json


app = Flask(__name__)

API_KEY = ""
API_KEY1 = ""


def calculate_distance(origin, destination):
    """Calculates the distance between two locations using the Google Maps Distance Matrix API."""
    url = f"https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins={origin}&destinations={destination}&key={API_KEY}"
    response = requests.get(url)
    data = json.loads(response.text)

    # Extract the distance value from the API response
    distance = data.get("rows", [{}])[0].get("elements", [{}])[0].get("distance", {}).get("value")
    return distance

def find_shortest_route(user1_location, user2_location, locations):
    """Finds the shortest route between user1_location, user2_location, and a list of locations."""

    distances = {}
    for location in locations:
        # Calculate the distances between user1_location, user2_location, and each location
        user1_distance = calculate_distance(user1_location,location)
        user2_distance = calculate_distance(user2_location,location)
        distances[location] = user1_distance + user2_distance

    # Sort the locations by their combined distance
    sorted_locations = sorted(distances, key=distances.get)
    picked_location = sorted_locations[0]

    photos = get_place_photos(picked_location)

    return picked_location, photos



def get_place_photos(location):
    """Retrieves photos of a location using the Google Places API."""
    url = f"https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input={location}&inputtype=textquery&fields=place_id&key={API_KEY1}"
    response = requests.get(url)
    data = json.loads(response.text)

    if "candidates" in data and data["candidates"]:
        place_id = data["candidates"][0]["place_id"]

        url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&fields=photos&key={API_KEY1}"
        response = requests.get(url)
        data = json.loads(response.text)

        photos = []
        if "photos" in data["result"]:
            for photo in data["result"]["photos"]:
                photo_reference = photo["photo_reference"]
                photo_url = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={photo_reference}&key={API_KEY1}"
                photos.append(photo_url)

        return photos[0:3]

    return []
  






@app.route("/", methods=['GET', 'POST'])
def index():
    regions = ["Gauteng", "North-West", "Western Cape"]
  
    locations = ["Manaka Coffee, Waterfall"]

    if request.method == 'POST':
        # Retrieve the submitted form data
        location1 = request.form.get('input1')
        location2 = request.form.get('input2')

    

        # Call your backend function with the form data and get the result
        picked_location, photos = find_shortest_route(location1, location2, locations)

  

        # Pass the result and photos to the template
        return render_template('home.html', picked_location=picked_location, photos=photos, regions=regions)



    # Render the template initially without any data
    return render_template('home.html', regions=regions)








  
if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
