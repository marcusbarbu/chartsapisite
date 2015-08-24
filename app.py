from flask import Flask 
from flask import make_response
from flask import render_template
from ChartScraper import Top40Scraper
import os
import json


app = Flask(__name__)

scrape = Top40Scraper()

@app.route('/')
def index():
	return render_template('index.html')
# @app.route('/boop')
# def boop():
# 	return "hadsf"

@app.route('/chartsapi/<chart>', methods=['GET'])
def get_chart(chart):
	try:
		return scrape.get_chart(chart)
	except ValueError as e:
		return json.dumps(["That chart does not exist"], indent = 2)

@app.route('/chartsapi/<chart>/<option>', methods=['GET'])
def get_options(chart, option):
	try:
		scrape.get_chart(chart)
	except ValueError as e:
		return json.dumps(["That chart does not exist"], indent = 2)
	if option == 'songs':
		return scrape.get_song_list()
	elif option == 'artists':
		return scrape.get_artist_list()

@app.route('/chartsapi/charts', methods=['GET'])
def deliver_charts():
	return scrape.get_chart_titles()

@app.errorhandler(404)
def not_found(error):
	return json.dumps(["That chart does not exist"], indent = 2)

@app.errorhandler(500)
def internal_error(error):
	return json.dumps(["An internal error occured"], indent = 2)
app.debug = False

if (__name__) == '__main__':
	port = int(os.environ.get("PORT", 5000))
	app.run(host = '0.0.0.0', port=port)