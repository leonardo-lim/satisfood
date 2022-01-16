import requests
import json
from main.location import get_location

# Get user location
loc = get_location()
lat = loc['lat']
lon = loc['lon']

map_url = f'https://www.google.com/search?tbm=map&authuser=0&hl=id&gl=id&pb=!4m9!1m3!1d2004.922555559405!2d{lon}!3d{lat}!2m0!3m2!1i518!2i772!4f13.1!7i20!10b1!12m8!1m1!18b1!2m3!5m1!6e2!20e3!10b1!16b1!19m4!2m3!1i360!2i120!4i8!20m57!2m2!1i203!2i100!3m2!2i4!5b1!6m6!1m2!1i86!2i86!1m2!1i408!2i240!7m42!1m3!1e1!2b0!3e3!1m3!1e2!2b1!3e2!1m3!1e2!2b0!3e3!1m3!1e8!2b0!3e3!1m3!1e10!2b0!3e3!1m3!1e10!2b1!3e2!1m3!1e9!2b1!3e2!1m3!1e10!2b0!3e3!1m3!1e10!2b1!3e2!1m3!1e10!2b0!3e4!2b1!4b1!9b0!22m6!1sJxzgYbKAJ6bMrgSDtYugAw:21!2zMWk6Myx0OjExODg3LGU6MixwOkp4emdZYktBSjZiTXJnU0R0WXVnQXc6MjE!7e81!12e3!17sJxzgYbKAJ6bMrgSDtYugAw:32!18e15!24m59!1m21!13m8!2b1!3b1!4b1!6i1!8b1!9b1!14b1!20b1!18m11!3b1!4b1!5b1!6b1!9b1!12b0!13b1!14b1!15b0!17b1!20b1!2b1!5m5!2b1!3b1!5b1!6b1!7b1!10m1!8e3!14m1!3b1!17b1!20m2!1e3!1e6!24b1!25b1!26b1!29b1!30m1!2b1!36b1!43b1!52b1!54m1!1b1!55b1!56m2!1b1!3b1!65m5!3m4!1m3!1m2!1i224!2i298!89b1!26m4!2m3!1i80!2i92!4i8!30m0!34m17!2b1!3b1!4b1!6b1!8m5!1b1!3b1!4b1!5b1!6b1!9b1!12b1!14b1!20b1!23b1!25b1!26b1!37m1!1e81!42b1!47m0!49m5!3b1!6m1!1b1!7m1!1e3!50m4!2e2!3m2!1b1!3b1!67m2!7b1!10b1!69i587&q=restaurant'

def grab_map():
    # Request and get map data
    res = requests.get(map_url)
    raw_content = res.content

    # Convert bytes data to string
    raw_content = raw_content.decode('utf8')

    # Cut first 5 unnecessary letter
    cleaned_content = raw_content[5:]

    # Parse JSON to Python Dictionary
    cleaned_content = json.loads(cleaned_content)

    return cleaned_content

def get_restaurants():
    # Create array for restaurants info
    restaurants = []

    # Get data from map
    data = grab_map()

    # Iterate through all restaurant index
    for i in range(1, len(data[0][1])):
        if data[0][1][i]:
            single = data[0][1][i]

            if single[14]:
                restaurant = single[14]
                temp = {}

                try:
                    temp['name'] = restaurant[11]
                except:
                    pass

                try:
                    temp['type'] = restaurant[76]
                except:
                    pass

                try:
                    temp['location'] = restaurant[18]
                except:
                    pass

                try:
                    temp['phone'] = restaurant[178][0][0]
                except:
                    pass

                try:
                    temp['rating'] = restaurant[4][7]
                except:
                    pass

                try:
                    temp['review'] = restaurant[4][8]
                except:
                    pass

                try:
                    temp['image'] = restaurant[37][0][0][6][0]
                except:
                    pass

                restaurants.append(temp)

    return restaurants