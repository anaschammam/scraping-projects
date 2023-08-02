import time
import scrapy
import json
from checkme import check_key_exists

class MySpider(scrapy.Spider):
    name = "my_spider"
    start_urls = ['https://api.sofascore.com/api/v1/sport/football/events/live']
    custom_settings = {
        'DUPEFILTER_CLASS': 'scrapy.dupefilters.BaseDupeFilter'
    }

    def parse_newpage(self, response):
        jsondata = json.loads(response.text)
        jsondata2 = jsondata["events"]
        j = 0
        a = dict()
        for i in jsondata2:
            a[j] = {
                'League': str(i['tournament']['category']['name']) + "-" + str(i['tournament']['name']),
                'status': str(i['status']['description']),
                'Team1': str(i['homeTeam']['name']),
                'Score1': i['homeScore']['current'],
                'Score2': i['awayScore']['current'],
                'Team2': str(i['awayTeam']['name']),
                'Diff': abs(i['homeScore']['current'] - i['awayScore']['current'])
            }
            j = j + 1
        a = dict(sorted(a.items(), key=lambda x: int(x[1]['Diff']), reverse=True))
        with open("output.json", "w") as f:
            json.dump(a, f, indent=4)
        next_request = scrapy.Request(response.url, callback=self.parse)
        # delay the next request for a few seconds to avoid overloading the server
        time.sleep(5)
        # yield the new request to the engine to be processed in the next iteration of the loop
        yield next_request

    def parse(self, response):
        jsondata = json.loads(response.text)
        jsondata2 = jsondata["events"]
        if not check_key_exists(jsondata2,'current'):
            print("current does'nt existe")
            yield scrapy.Request(url="https://api.sofascore.com/api/v1/sport/football/events/live", callback=self.parse_newpage)
        else :
            j = 0
            a = dict()
            for i in jsondata2:
                a[j] = {
                    'League': str(i['tournament']['category']['name']) + "-" + str(i['tournament']['name']),
                    'status': str(i['status']['description']),
                    'Team1': str(i['homeTeam']['name']),
                    'Score1': i['homeScore']['current'],
                    'Score2': i['awayScore']['current'],
                    'Team2': str(i['awayTeam']['name']),
                    'Diff': abs(i['homeScore']['current'] - i['awayScore']['current'])
                }
                j = j + 1
            a = dict(sorted(a.items(), key=lambda x: int(x[1]['Diff']), reverse=True))
            with open("output.json", "w",encoding='utf-8') as f:
                json.dump(a, f,ensure_ascii=False, indent=4)
            print("good")

            next_request = scrapy.Request(response.url, callback=self.parse)

            # delay the next request for a few seconds to avoid overloading the server
            time.sleep(5)

            # yield the new request to the engine to be processed in the next iteration of the loop
            yield next_request
