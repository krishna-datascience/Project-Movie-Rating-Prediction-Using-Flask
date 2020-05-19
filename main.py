from flask import Flask, render_template, redirect,request
import random
app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'some random string'

@app.route('/', methods=['GET','POST'])
def index():
	if request.method == 'POST':
		from movie_rating import calculate_rating_user
		movie_name = request.form.get('movie')
		movie,rating,link = calculate_rating_user(movie_name)
		if not movie:
			check = False
		else:
			check = True
		return render_template('user_movie.html',movie = movie,
			rating = rating,check = check,link = link)
	return render_template("index.html")

def compute():
	global data
	from movie_rating import compute_rating

	data = compute_rating()
	return data

@app.route('/ratingss')
def ratingss():

	movie = "Rishabh"
	rating = 10
	check = True
	return render_template('user_movie.html',movie = movie,
		rating = rating,check = check)


@app.route('/ratings')
def ratings():

	data = compute()
	movie_titles = data['title']
	movie_ratings = data['rating'].round(2) 
	movies = list(zip(movie_titles,movie_ratings))
	sample_movies = random.sample(movies,12)
	print(sample_movies)
	return render_template("ratings.html", movies = sample_movies,
		all_movies = movie_titles)

if __name__ == "__main__":
	
	app.run()