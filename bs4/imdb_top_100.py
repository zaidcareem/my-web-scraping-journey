from bs4 import BeautifulSoup
import requests as reqs
import pandas as pd
from datetime import date

# list to store a 100 dictionaries with movie_name, rating as key value pairs
movies = [] # used later with pandas

# mimic that the GET request is from a browser
headers = {'User-Agent' : 'Mozilla/5.0 (iPhone14,3; U; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/19A346 Safari/602.1'}

# IMDB updates this list of top 100 movies on a daily basis
url = 'https://www.imdb.com/chart/moviemeter/?ref_=nv_mv_mpm&sort=popularity%2Casc'
page = reqs.get(url=url, headers=headers)

if page.status_code == 200:
    print('fetching page SUCCESS')
else:
    print('fetching page FAILED')
    print(page.status_code)

lassana_soup = BeautifulSoup(page.text, 'html.parser')

top_hundred_movies = lassana_soup.find_all('li', class_='ipc-metadata-list-summary-item sc-10233bc-0 iherUv cli-parent') # returns a result set of 100 'li' tags corresponding to the top 100 movies

for movie in top_hundred_movies:

    data = {}
    movie_name = movie.find('h3', class_='ipc-title__text').text
    data['Name'] = movie_name
    
    try:
        movie_rating = movie.find('span', class_='ipc-rating-star ipc-rating-star--base ipc-rating-star--imdb ratingGroup--imdb-rating').text[:3]
        data['Rating'] = movie_rating
    except AttributeError:
        data['Rating'] = 'NaN'
    
    movies.append(data)
    
dataframe = pd.DataFrame(movies)

todays_date = date.today()

file_name = 'top-hundred-movies-on-' + str(todays_date) + '.csv'

dataframe.to_csv(file_name) # create a .csv file and write the data into it, the file will be overwritten if your running the program more than once on the same day.

   
        