from __future__ import unicode_literals
from soupy import Soupy, Q
import requests
import string
import json
class Top40Scraper:
    
    def __init__(self):
        self.chart_name = ""
        self.chart_list = []
        self.url = ""
        self.base_url = 'http://top40-charts.com/chart.php?cid='
        self.chart_titles_dict = {u'': 69, u'brazil': 8, u'hungary': 50, u'italy': 18, u'Canada': 9, u'World Soundtracks / OST': 44, u'France': 11, u'Airplay World Official': 36, u'Digital Sales': 5, u'Ireland': 15, u'Argentina': 3, u'Norway': 19, u'Australia': 4, u'World RnB': 33, u'World Jazz': 1, u'Europe Official': 31, u'China': 42, u'Chile': 37, u'Belgium': 7, u'Spain': 21, u'Ukraine': 47, u'Netherlands': 13, u'HeatSeekers Radio': 48, u'Denmark': 32, u'Finland': 10, u'Sweden': 22, u'UK Singles': 25, u'Switzerland': 23, u'New Zealand': 17, u'World Dance': 40, u'Russia': 45, u'Bulgaria': 49, u'World Modern Rock': 41, u'Hispanic America': 46, u'Portugal': 20, u'World Adult': 29, u'German': 12, u'USA Singles': 27, u'World Country': 30, u'India': 43, u'Top40-Charts.com Web': 39, u'USA Albums @ ': 28, u'World Latin': 34, u'Austria': 6, u'UK': 26, u'Greece': 2, u'Japan': 16, u'Taiwan': 14, u'World Singles Official': 35, u'Muchmusic': 24}
        self.chart_titles_dict = dict((k.lower(), v) for k,v in self.chart_titles_dict.iteritems())
        self.song_title_constant = 2
        self.song_artist_constant = 3
    
    def get_chart(self, chart_name):
        self.chart_list = []
        self.chart_name = chart_name.lower()
        global KeyError
        try:
            number = self.chart_titles_dict[self.chart_name]
        except KeyError:
            return json.dumps(["That chart does not exist"], indent = 2)
        self.url = self.base_url + str(number)
        raw = requests.get(self.url)
        soup = Soupy(raw.text)
        tr_container = soup.find_all('tr',{'class':'latc_song'})
        global NameError
        pos = 0
        song_title_constant = 2
        song_artist_constant = 3
        for table_row in tr_container:
            children = table_row.children
            null_container_holder = type(children[0].find('table').find_all('a'))
            for child in children:
                links = child.find('table').find_all('a')
                if type(links) is not null_container_holder:
                    try:
                        try:
                            pos = pos + 1
                            song_title = links[song_title_constant].contents.first().val().string
                            song_artist = links[song_artist_constant].contents.first().val().string
                            self.chart_list.append((('position',pos),('title',song_title), ('artist',song_artist)))
                        except NullValueError, NameError:
                            print ('\n')
                    except NameError:
                        song_title = links[song_title_constant-1].contents.first().val().string
                        song_artist = links[song_artist_constant-1].contents.first().val().string
                        self.chart_list.append((('position',pos),('title',song_title), ('artist',song_artist)))
        return json.dumps(self.chart_list, indent = 3)
        
    def get_song_list(self):
        if self.chart_list:
            song_list = []
            for entry in range(len(self.chart_list)):
                song_list.append(((self.chart_list[entry][0]),(self.chart_list[entry][1])))
            return json.dumps(song_list, indent = 2)
        else:
            return json.dumps(["You must get a chart first"], indent = 2)
    
    def get_artist_list(self):
        if self.chart_list:
            artist_list = []
            for entry in range(len(self.chart_list)):
                artist_list.append(((self.chart_list[entry][0]),(self.chart_list[entry][2])))
            return json.dumps(artist_list, indent = 2)
        else:
            return json.dumps(["You must get a chart first"], indent = 2)
    
    def get_chart_titles(self):
        return json.dumps(self.chart_titles_dict.keys(), indent = 2)