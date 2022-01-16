import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from main.restaurant import get_restaurants

def recommend_restaurants(prev_restaurant):
    # Get restaurants
    restaurants = get_restaurants()

    # Merge array of restaurant types to one string
    for restaurant in restaurants:
        temp = []

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
        if 'type' in restaurant:
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

    # Create array for recommendation results
    results = []

    # Sort restaurants by restaurant indices
    for indice in restaurant_indices:
        results.append(restaurants[indice])

    return results

def show_restaurants():
    # Get restaurants
    restaurants = get_restaurants()

    # Cut restaurant name in location
    for restaurant in restaurants:
        length = len(restaurant['name'])
        restaurant['location'] = restaurant['location'][length + 2:]

    return restaurants