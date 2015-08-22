from flask import Flask 
from ChartScraper import Top40Scraper
import os


app = Flask(__name__)

scrape = Top40Scraper()

# @app.route('/')
# def index():
# 	return "hello world"

# @app.route('/boop')
# def boop():
# 	return "hadsf"

@app.route('/chartsapi/<chart>', methods=['GET'])
def get_chart(chart):
	return scrape.get_chart(chart)

@app.route('/chartsapi/<chart>/<option>', methods=['GET'])
def get_options(chart, option):
	scrape.get_chart(chart)
	if option == 'songs':
		return scrape.get_song_list()
	elif option == 'artists':
		return scrape.get_artist_list()

@app.route('/chartsapi/charts', methods=['GET'])
def deliver_charts():
	return scrape.get_chart_titles()


app.debug = False

if (__name__) == '__main__':
	port = int(os.environ.get("PORT", 5000))
	app.run(host = '0.0.0.0', port=port)