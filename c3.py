import requests_with_caching
import json


def get_movies_from_tastedive(movie_name):
    td_url = 'https://tastedive.com/api/similar'
    td_params = {'q': movie_name, 'type': 'movies', 'limit': '5'}

    res = requests_with_caching.get(td_url, params=td_params)

    text = res.text
    py_dict = json.loads(text)
    # print(py_dict)

    return py_dict


def extract_movie_titles(some_dict):
    movies_lst = some_dict['Similar']['Results']

    titles = []

    for d in movies_lst:
        title = d['Name']
        # print(title)
        titles.append(title)
    return titles


def get_related_titles(movie_lst):
    # print(movie_lst)
    related_lst = []
    for title in movie_lst:
        get_m = get_movies_from_tastedive(title)
        ext_titles = extract_movie_titles(get_m)

        for movie in ext_titles:
            if movie not in related_lst:
                related_lst.append(movie)
    return related_lst


def get_movie_data(movie_title):
    o_url = 'http://www.omdbapi.com/'
    o_params = {'t': movie_title, 'r': 'json'}

    r = requests_with_caching.get(o_url, o_params)

    py_dict = json.loads(r.text)

    return py_dict


def get_movie_rating(o_dict):
    if len(o_dict['Ratings']) > 1:
        if o_dict['Ratings'][1]['Source'] == 'Rotten Tomatoes':
            rotten_rating = o_dict['Ratings'][1]['Value'][:2]
            rotten_rating = int(rotten_rating)
        else:
            rotten_rating = 0

        return rotten_rating


def get_sorted_recommendations(movie_lst):
    print("Movie List --", movie_lst)
    new_list = get_related_titles(movie_lst)
    print("---------------")
    print("new_list-- ", new_list)
    new_d = {}
    for i in new_list:
        rating = get_movie_rating(get_movie_data(i))
        new_d[i] = rating

    print(sorted(new_d, reverse=True))
    return [i[0] for i in sorted(new_d.items(), key=lambda item: (item[1], item[0]), reverse=True)]


# some invocations that we use in the automated tests; uncomment these if you are getting errors and want better error messages
# get_sorted_recommendations(["Bridesmaids", "Sherlock Holmes"])
