print("Importing the required Modules..")
import numpy as np
import pandas as pd
from pandas.compat import StringIO
from difflib import get_close_matches
import requests
from bs4 import BeautifulSoup

print("Modules Imported!!")

def compute_rating():

	#Loading the movies
	print("Loading the movies..")
	movie=pd.read_csv(r"seed_data/movies.dat",delimiter='::',
		header=None,names=['Movie_id','title','type'])
	print("Done!")

	# Loading the Ratings
	print("Loading the Ratings")
	rating=pd.read_csv(r"seed_data/ratings.dat",delimiter='::',
		header=None,names=['user_id','Movie_id','rating','timestamp'])
	print("Done!")

	# Loading the Users
	print("Loading the Users")
	user=pd.read_csv(r"seed_data/users.dat",delimiter='::',
		header=None,names=['user_id','twitter_id'])
	print("Done!")

	df = pd.merge(movie,rating,on='Movie_id')
	df2=df.groupby('Movie_id')['rating'].mean()
	df3=df.iloc[:,0:2]
	df4=pd.DataFrame(df.groupby('Movie_id')['rating'].mean())


	final=pd.merge(df3,df4,on='Movie_id')
	# # sorting by first name 
	# final.sort_values("title", inplace = True) 
  
	# # dropping ALL duplicte values 
	# final.drop_duplicates(subset ="title",keep = False, inplace = True) 

	return final

def calculate_rating_user(movie):

	data = compute_rating()

	movie = movie.strip().title()

	effective_movie = get_close_matches(movie,data['title'],cutoff=0.45)
	
	
	if effective_movie:
		movie_data = effective_movie[0]
		m_imdb = movie_data + " imdb"
		goog_search = "https://www.google.co.uk/search?sclient=psy-ab&"+\
			"client=ubuntu&hs=k5b&channel=fs&biw=1366&bih=648&noj=1&q=" +\
			m_imdb
		r = requests.get(goog_search)
		soup = BeautifulSoup(r.content)
		g = soup.find_all('div',{'class':'kCrYT'})
		if g:
			g = g[0]
			link = g.find_all('a')[0]['href'].split('=')[1].split('&')[0]
		else:
			link = ''
		index = data.index[data.title == movie_data][0]
		rating = data.iloc[index]['rating'].round(2)
	else:
		movie_data = ''
		rating = ''
		link = ''

	return movie_data,rating,link




