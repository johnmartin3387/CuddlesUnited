from twisted.internet import reactor

from scrapy.utils.project import get_project_settings
from threading import Thread

from scrapy.crawler import CrawlerProcess
from lostpet.spiders.helpinglostpets import Helpinglostpets
from lostpet.database import getClients

def scrape_module():
    print "start spider"
    param = [{
        "id": "1",
        "client_name": "John",
        "client_email": "johnmartin3387@gmail.com", 
        "pet_name": "Cute Dog",
        "traits":{
            "type": "dog",	# dog or cat
            "breed": "American Bulldog",
            "size": "large", 	# small, medium, large
            "color": "white",	# black, brown, gray, red, tan, white, yellow
            "sex": "boy",		# boy or girl
            "date": "08/15/2016",   # month/day/year
            "state": "",
            "zip_code": "60613",
        }
    },]

    params = []
    clients = getClients()

    for client in clients:	
        param = {
            "id": str(client[0]),
            "client_name": client[1],
            "client_email": client[2],
            "pet_name": client[3],
            "traits":{
                "type": client[4],	# dog or cat
                "breed": client[6],
                "size": client[5], 	# small, medium, large
                "color": client[7],	# black, brown, gray, red, tan, white, yellow
                "sex": client[8],		# boy or girl
                "date": client[9].split(" ")[0],   # year-month-day
                "state": client[10],
                "zip_code": client[11],
            }
        }

        params.append(param)

    crawler = CrawlerProcess(get_project_settings())
    crawler.crawl(Helpinglostpets, param=params)
    Thread(target=crawler.start)
    reactor.run()

scrape_module()
