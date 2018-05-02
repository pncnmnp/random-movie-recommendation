import csv
import random
import re
import time
import requests
import tkinter
import os
import webbrowser
from PIL import Image, ImageTk
import bs4


def main():
	'''

	This function first extracts a random movie data from the csv files,
	Then it extracts information of that particular movie from IMDB

	'''
	fields = []
	rows = []

	# The number of rows in the movies.csv is 9126
	# To select a random row index
	random_row_index = random.randint(1, 9126)

	# Path of csv to select a random movie
	filename = "data/movies.csv"

	# To store the movie values in the list 'rows'
	# If you optimize the code we should store only the index:
	# 'random_row_index' found
	with open(filename, 'r') as csvfile:

		csvreader = csv.reader(csvfile)

		fields = csvreader.__next__()

		for row in csvreader:
			rows.append(row)

	# The columns are divided into:
	# 0 -> movie_id (used to find the IMDB link key)
	# 1 -> movie name (contains movie TITLE and YEAR OF RELEASE)
# 2 -> genre
	movie_id = rows[random_row_index][0]
	movie = rows[random_row_index][1]
	movie_genre = rows[random_row_index][2]

	movie_values = str(movie)

	movie_name = ''

	# to SEPARATE the movie title and year
	for i in range(len(movie_values)):

		# The movie YEAR is stored in brackets. EG: (1994)
		if(movie_values[i] == '('):

			# Get all the numbers in the entire string
			movie_year_regex = re.compile(r'\d+')

			# As the last integer value is always the YEAR number
			movie_year = movie_year_regex.findall(movie)[-1]
			break

		movie_name += movie_values[i]

	# Path of csv to find the IMDB link
	# The links.csv file is divided into:
	# 0 -> movie id
	# 1 -> IMDB link key
	filename_links = "data/links.csv"

	links_id = []
	links_imdb_key = []

	with open(filename_links, 'r') as csvfile:

		csvreader = csv.reader(csvfile)

		# To store all the links id value and their IMDB key with SAME INDEX VALUE
		for row in csvreader:
			links_id.append(row[0])
			links_imdb_key.append(row[1])

	if(movie_id in links_id):
		index = links_id.index(movie_id)

	# Using the index value we just found to create an IMDB url
	# Using global was a necessary evil
	# The function 'callback()' needs the url to open IMDB page on
	# a web browser, but it accepts only ONE parameter - 'event'
	# WOULD LOVE TO HEAR A MORE EFFICIENT SOLUTION ;-)
	global url
	url = "https://www.imdb.com/title/tt" + str(links_imdb_key[index]) + "/"

	# Extracting our movie webpage's contents from IMDB
	while(True):
		try:
			open_url = requests.get(url)
			break
		except requests.exceptions.RequestException:
			print("Network Issue (PAGE)")
			time.sleep(30)
			print("Trying Again....")

	soup = bs4.BeautifulSoup(open_url.content, 'html.parser')

	imdbRating = soup.find_all('span', itemprop='ratingValue')

	summary = soup.find_all('div', class_='summary_text')

	screenTime = soup.find_all('time', itemprop='duration')

	director = soup.find_all('span', itemprop='name')

	actors = soup.find_all('td', itemprop='actor')

	print("Movie: %s" % movie_name)

	print("Release Year: %s" % movie_year)

	print("Genre: %s" % movie_genre)

	print('IMDB link: %s' % url)

	print('IMDB rating: %s' % imdbRating[0].text)

	print('Runtime: %s' % (screenTime[0].text.strip()))

	print('Director: %s' % (director[0].text.strip()))

	print('Cast: %s, %s, %s' % (actors[0].text.strip(), actors[1].text.strip(), actors[2].text.strip()))

	print('Summary: %s' % (summary[0].text.strip()))

	# To extract the movie poster
	image = soup.find_all('img', itemprop="image")

	# To get the .jpg source from the image element
	image_link = image[0].get('src', '')

	file_name_poster = 'photo/image.jpg'

	# To download the movie poster
	poster = requests.get(image_link)

	# To create a local copy
	with open(file_name_poster, 'wb') as img_handle:
		img_handle.write(poster.content)

	gui(movie_name, movie_year, movie_genre, url, imdbRating[0].text, screenTime[0].text.strip(), director[0].text.strip(), actors[0].text.strip(), actors[1].text.strip(), actors[2].text.strip(), summary[0].text.strip(), file_name_poster)


def button_switch(movie_name_label, movie_year_label, movie_genre_label, url_label, imdbRating_label, screenTime_label, director_label, actors_label, summary_label, poster_label):
	'''

	After the 'Show a Random Movie !' button is pressed, we pack the various information on canvas

	'''
	poster_label.pack(side="top", fill="both", expand="yes")

	movie_name_label.pack()

	movie_year_label.pack()

	movie_genre_label.pack()

	url_label.pack()

	imdbRating_label.pack()

	screenTime_label.pack()

	director_label.pack()

	actors_label.pack()

	summary_label.pack()


def callback(event):
	'''

	To open the IMDB hyperlink

	'''
	print("url being opened is %s" % url)
	webbrowser.open(url)


def gui(movie_name, movie_year, movie_genre, url, imdbRating, screenTime, director, actor_1, actor_2, actor_3, summary, file_name_poster):
	'''

	Using Tkinter to create a GUI version of the application

	'''
	window = tkinter.Tk()

	window.title('Movie Recommendation Engine')

	# Creating various labels which would be displayed after 'Show a Random Movie !' button is pressed
	movie_name_label = tkinter.Label(window, text=("Movie: %s" % movie_name))

	movie_year_label = tkinter.Label(window, text=("Release Year: %s" % movie_year))

	movie_genre_label = tkinter.Label(window, text=("Genre: %s" % movie_genre))

	url_label = tkinter.Label(window, text=("IMDB link: %s" % url), fg="blue", cursor="hand2")

	imdbRating_label = tkinter.Label(window, text=("IMDB rating: %s/10" % imdbRating))

	screenTime_label = tkinter.Label(window, text=("Runtime: %s" % screenTime))

	director_label = tkinter.Label(window, text=("Director: %s" % director))

	actors_label = tkinter.Label(window, text=("Cast: %s, %s, %s" % (actor_1, actor_2, actor_3)))

	summary_label = tkinter.Label(window, text=("Summary: %s" % summary))

	# The image is in '.jpg' format
	# We are using ImageTk to convert it to '.gif' as tkinter.Label accepts only '.gif' format
	print("Poster is: %s" % file_name_poster)
	poster_fetch = ImageTk.PhotoImage(Image.open(file_name_poster))

	# Creating a label for movie poster
	poster_label = tkinter.Label(window, image=poster_fetch)

	# A reference of image is necessary
	poster_label.image = poster_fetch

	# It is after user presses this button, the function 'button_switch' gets executed and
	# The Movie information is printed on the canvas
	recommendation_button = tkinter.Button(window, text='Show a Random Movie !', width=25, command=lambda: button_switch(movie_name_label, movie_year_label, movie_genre_label, url_label, imdbRating_label, screenTime_label, director_label, actors_label, summary_label, poster_label))

	# Creating a HyperLink of IMDB link
	url_label.bind("<Button-1>", callback)

	# To terminate the application
	exit_button = tkinter.Button(window, text='Exit', width=25, command=window.destroy)

	recommendation_button.pack()

	exit_button.pack()

	window.mainloop()


if __name__ == '__main__':
	main()
