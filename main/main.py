import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from main.restaurant import get_restaurants
from main.weather import check_rain

def recommend_restaurants(prev_restaurant, address):
    # Get restaurants
    restaurants = get_restaurants(address)

    # Merge array of restaurant types to one string
    for restaurant in restaurants:
        temp = []

        if restaurant['type']:
            for types in restaurant['type']:
                for type in types:
                    temp.append(type)

            restaurant['type'] = ' '.join(temp)

    # Cut restaurant name in location
    for restaurant in restaurants:
        length = len(restaurant['name'])
        restaurant['location'] = restaurant['location'][length + 2:]

    # Append name to type
    for restaurant in restaurants:
        if 'type' in restaurant and restaurant['type']:
            temp = restaurant['name']
            temp += ' '
            temp += restaurant['type']
            restaurant['type'] = temp

    # Read Python Dictionary using Pandas
    restaurants_df = pd.DataFrame(restaurants)

    # Check if the previous restaurant name exists in the recommendation list
    if not (restaurants_df['name'] == prev_restaurant['name']).any():
        restaurants_df = restaurants_df.append(prev_restaurant, ignore_index=True)

    # Transform text to feature vectors
    tfv = TfidfVectorizer(min_df=2, strip_accents='unicode', analyzer='word', token_pattern=r'\w{1,}', ngram_range=(1, 2))

    # Fitting the TF-IDF on the 'type' text
    tfv_matrix = tfv.fit_transform(restaurants_df['type'])

    # Find the cosine similarity
    cosine_sim = linear_kernel(tfv_matrix, tfv_matrix)

    # Reverse mapping of indices and restaurant names
    indices = pd.Series(restaurants_df.index, index=restaurants_df['name']).drop_duplicates()

    # Get the index of the restaurant that matches the name
    idx = indices[prev_restaurant['name']]

    # Get the pairwise similarity scores of all restaurants with previous restaurant
    sim_scores = list(enumerate(cosine_sim[idx]))

    # Sort the restaurants based on the similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get the restaurant indices
    restaurant_indices = [i[0] for i in sim_scores]

    # Exclude restaurant that matches the previous restaurant
    for indice in restaurant_indices:
        if indice == idx:
            restaurant_indices.remove(indice)
            break

    # Create array for sorted restaurants
    sorted_restaurants = []

    # Sort restaurants by restaurant indices
    for indice in restaurant_indices:
        sorted_restaurants.append(restaurants[indice])

    # Check whether the weather condition is raining or not
    if check_rain(address):
        result = prioritize_rain_food_restaurants(sorted_restaurants)
    else:
        result = {
            'is_rain': False,
            'restaurants': sorted_restaurants
        }

    return result

def show_restaurants(address):
    # Get restaurants
    restaurants = get_restaurants(address)

    # Merge array of restaurant types to one string
    for restaurant in restaurants:
        temp = []

        if restaurant['type']:
            for types in restaurant['type']:
                for type in types:
                    temp.append(type)

            restaurant['type'] = ' '.join(temp)

    # Cut restaurant name in location
    for restaurant in restaurants:
        length = len(restaurant['name'])
        restaurant['location'] = restaurant['location'][length + 2:]

    # Append name to type
    for restaurant in restaurants:
        if 'type' in restaurant and restaurant['type']:
            temp = restaurant['name']
            temp += ' '
            temp += restaurant['type']
            restaurant['type'] = temp

    # Check whether the weather condition is raining or not
    if check_rain(address):
        result = prioritize_rain_food_restaurants(restaurants)
    else:
        result = {
            'is_rain': False,
            'restaurants': restaurants
        }

    return result

def prioritize_rain_food_restaurants(restaurants):
    # List all Indonesian foods that are suitable for rain
    foods = ['bakso', 'baso', 'soto', 'tongseng', 'rawon', 'tengkleng', 'seblak', 'soup', 'sup', 'kuah', 'noodle', 'mie', 'hotpot']

    # Create array for rain food restaurants and non rain food restaurants
    rain_food_restaurants = []
    non_rain_food_restaurants = []
    check = False

    # Find all restaurants that have food suitable for rain
    for restaurant in restaurants:
        if restaurant['type']:
            for food in foods:
                if food in restaurant['type'].lower():
                    rain_food_restaurants.append(restaurant)
                    check = True
                    break

        if not check:
            non_rain_food_restaurants.append(restaurant)
        else:
            check = False

    # Store result in Python Dictionary
    result = {
        'is_rain': True,
        'rain_food_restaurants': rain_food_restaurants,
        'non_rain_food_restaurants': non_rain_food_restaurants
    }

    return result