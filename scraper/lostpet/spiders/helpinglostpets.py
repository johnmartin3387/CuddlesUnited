import scrapy
from scrapy import signals
from lostpet.constant import *
from lostpet.items import LostpetItem

import urllib
import urlparse
import copy

from twisted.internet import reactor
import math
import datetime

class Helpinglostpets(scrapy.Spider):
    name = "lostpets"

    help_url = "http://www.helpinglostpets.com/v2/OrgPet.aspx?oid=188"
    harbor_url = "http://petharbor.com"

    def __init__(self, param):
        self.param = param

        # configuration for www.helpinglostpets.com
        self.data = []
        self.hardor_data = []

        for pm in self.param:
            data = dict()
            data["param"] = copy.deepcopy(HELP_PARAM)

            data["client_id"] = pm["id"]
            data["client_name"] = pm["client_name"]
            data["client_email"] = pm["client_email"]
            data["pet_name"] = pm["pet_name"]
            data["date"] = pm["traits"]["date"]
            data["gender"] = HELP_GENDER[pm["traits"]["sex"]]

            data["param"]["ddlSpecies"] = HELP_SPECIES[pm["traits"]["type"]][0]
            data["param"]["CascadingDropDown_Species_ClientState"] = HELP_SPECIES[pm["traits"]["type"]][1]

            if pm["traits"]["breed"] in HELP_BREED[pm["traits"]["type"]]:
                data["param"]["ddlBreed1"] = HELP_BREED[pm["traits"]["type"]][pm["traits"]["breed"]]
                data["param"]["CascadingDropDown_Breed1_ClientState"] = "%s:::%s:::" % \
                    (HELP_BREED[pm["traits"]["type"]][pm["traits"]["breed"]], pm["traits"]["breed"])
            # data["ddlSizes"] = HELP_SIZE[pm["traits"]["size"]][0]
            # data["CascadingDropDown_Sizes_ClientState"] = HELP_SIZE[pm["traits"]["size"]][1]
	
            # data["txtColor"] = pm["traits"]["color"]

            data["param"]["ddlGender"] = HELP_GENDER[pm["traits"]["sex"]]

            if pm["traits"]["state"] != "":
                data["param"]["ddlProvince"] = pm["traits"]["state"]

            date_str = pm["traits"]["date"].split("-")
            data["param"]["txtStatusDate"] = "%s %s, %s" % (HELP_MONTH[date_str[1]], date_str[2], date_str[0])
            
            self.data.append(data)
            # configuration for petharbor.com
            search = ["type_%s" % pm["traits"]["type"].upper()]
            if pm["traits"]["size"] != "":
                search.append("size_%s" % pm["traits"]["size"][0].lower())

            if pm["traits"]["sex"] == "boy":
                search.append("gender_m")
            else:
                search.append("gender_f")

            if pm["traits"]["color"] in ["white", "brown", "black"]:
                search.append("color_%s" % pm["traits"]["color"][0])
        
            if pm["traits"]["breed"] in PATHARBOR_BREED:
                search.append("breed_%s" % PATHARBOR_BREED[pm["traits"]["breed"]])

            hardor_data = copy.deepcopy(PATHARBOR_PARAM)
            hardor_data["client_id"] = pm["id"]
            hardor_data["client_name"] = pm["client_name"]
            hardor_data["client_email"] = pm["client_email"]
            hardor_data["pet_name"] = pm["pet_name"]
            hardor_data["date"] = pm["traits"]["date"]

            hardor_data["where"] = ",".join(search)
            hardor_data["zip"] = pm["traits"]["zip_code"]

            search_data = {"gender": pm["traits"]["sex"], "color": pm["traits"]["color"], "breed": pm["traits"]["breed"]}

            self.hardor_data.append([hardor_data, search_data])

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(Helpinglostpets, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
        return spider

    def spider_closed(self, spider):
        reactor.stop()
        spider.logger.info('Spider closed: %s', spider.name)

    # make a request for scraping list page.
    def start_requests(self):

        for data in self.data:

            request = scrapy.FormRequest(url=self.help_url,
                    formdata=data["param"],
                    callback=self.help_parse, dont_filter=True)
            request.meta["page"] = 1
            request.meta["total_page"] = 0
            request.meta["client"] = {"client_id": data["client_id"], "client_name": data["client_name"], \
                    "client_email": data["client_email"], "pet_name": data["pet_name"], "date": data["date"], \
                    "gender": data["gender"]}

            request.meta["data"] = data
            yield request

        for item in self.hardor_data:
            hardor_data = item[0]
            request = scrapy.Request(url=self.harbor_url + "/results.asp?" + urllib.urlencode(hardor_data), callback=self.hardbor_parse, dont_filter=True)
            request.meta["page"] = 0
            request.meta["total_page"] = 0

            request.meta["client"] = {"client_id": hardor_data["client_id"], "client_name": hardor_data["client_name"], \
                    "client_email": hardor_data["client_email"], "pet_name": hardor_data["pet_name"], "date": hardor_data["date"]}

            request.meta["data"] = hardor_data
            request.meta["search"] = item[1]
            yield request

    # scrape data from www.helpinglostpets.com
    def help_parse(self, response):
        page = response.meta["page"]
        total_page = response.meta["total_page"]

        items = response.xpath("//table[contains(@style, '#EEEEEE')]")

        for item in items:
            status = self.validate(item.xpath(".//span[contains(@id, 'gvOrgPets_lblStatusDesc')]//font/text()"))

            if status != "Found":
                continue

            url = self.validate(item.xpath(".//a[contains(@id, 'gvOrgPets_lnkDetailPage')]/@href"))
            address = self.validate(item.xpath(".//span[contains(@id, 'gvOrgPets_lblAddress')]/text()"))
            date = self.validate(item.xpath(".//span[contains(@id, 'gvOrgPets_lblModifiedDate')]/text()"))
            date = date.split(":")[1].strip()

            description = ' '.join(item.xpath(".//tr[2]//td[2]//b/text()").extract())

            # check address
            # if self.param["traits"]["location"] != "" and self.param["traits"]["location"] not in address:
            #    continue

            pet = LostpetItem()
            pet["url"] = url
            pet["client_id"] = response.meta["client"]["client_id"]
            pet["client_name"] = response.meta["client"]["client_name"]
            pet["client_email"] = response.meta["client"]["client_email"]
            pet["pet_name"] = response.meta["client"]["pet_name"]

            date_db = datetime.datetime.strptime(response.meta["client"]["date"], "%Y-%m-%d")
            date_item = datetime.datetime.strptime(date, "%b %d, %Y")

            if date_db <= date_item and response.meta["client"]["gender"] in description:
                yield pet

        # scrape total number of pets.
        if page == 1:
            try:
                total = int(self.validate(response.xpath("//span[@id='lblPetCounts']//b/text()")))
                total_page = int(math.ceil(total/15.0))
            except:
                return

        # if this is last page, exit scraping data
        if page >= total_page:
            return;

        # make an request for the next page.
        page += 1
        data = response.meta["data"]
        data["__EVENTARGUMENT"] = "Page$%d" % page
        
        request = scrapy.FormRequest(url=self.help_url,
                    formdata=data,
                    callback=self.parse, dont_filter=True)

        request.meta["page"] = page
        request.meta["total_page"] = total_page
        request.meta["client"] = response.meta["client"]
        request.meta["data"] = data
        yield request
        
    # scrape data from petharbor.com
    def hardbor_parse(self, response):
        page = response.meta["page"]
        total_page = response.meta["total_page"]
        data = response.meta["data"]
        search = response.meta["search"]

        # scrape list of shelters
        if page == 0:
            shelters = response.xpath("//input[@type='CHECKBOX']/@name")

            # it there is no shelter at this area, exit spider.
            if len(shelters) == 0:
                return;

            shelters = ",".join(["'%s'" % shelter.extract().replace("chk", "").strip() for shelter in shelters]) 

            data["shelterlist"] = shelters

            # make a request with the given shelters
            request = scrapy.Request(url=self.harbor_url + "/results.asp?" + urllib.urlencode(data), callback=self.hardbor_parse, dont_filter=True)
            request.meta["page"] = 1
            request.meta["total_page"] = 0
            request.meta["client"] = response.meta["client"]
            request.meta["data"] = data
            request.meta["search"] = search

            yield request
            return

        elif page == 1:
            try:
                total = self.validate(response.xpath("//form[@id='frmResults']//center[1]/text()"))
                total = int(total.split(" ")[2])
                total_page = int(math.ceil(total/10.0))
            except:
                return

        # if this is last page, exit scraping data
        items = response.xpath("//form[@id='frmResults']//table[@class='ResultsTable']//tr")
 
        index = 0
        for item in items:
            if index == 0:
                index = 1
            else:
                url = self.harbor_url + self.validate(item.xpath(".//td[1]//a/@href"))
                date = self.validate(item.xpath(".//td[7]/text()"))

                sex = self.validate(item.xpath(".//td[3]/text()"))
                color = self.validate(item.xpath(".//td[4]/text()"))
                breed = self.validate(item.xpath(".//td[5]/text()"))

                print sex, color, breed
                print search

                if (sex == "Male" and search["gender"] == "girl") or \
                        (sex == "Female" and search["gender"] == "boy"):
                    continue
                if (search["color"].lower() == "brown" and ("Br" in color or "Brn" in color)):
                    pass
                elif color.lower() != search["color"].lower():
                    continue

                if (breed.replace(" ", "").lower() != search["breed"].replace(" ", "").lower()):
                    continue

                query = urlparse.parse_qs(urlparse.urlsplit(url).query)
                
                try:
                    url = "%s/pet.asp?uaid=%s.%s" % (self.harbor_url, query["LOCATION"][0], query["ID"][0])
                    pet = LostpetItem()
                    pet["url"] = url
                    pet["client_id"] = response.meta["client"]["client_id"]
                    pet["client_name"] = response.meta["client"]["client_name"]
                    pet["client_email"] = response.meta["client"]["client_email"]
                    pet["pet_name"] = response.meta["client"]["pet_name"]

                    date_db = datetime.datetime.strptime(response.meta["client"]["date"], "%Y-%m-%d")
                    date_item = datetime.datetime.strptime(date, "%Y.%m.%d")

                    print date_db, date_item
                    if date_db <= date_item:
                        yield pet
                except:
                    pass

        if page >= total_page:
            return

        # make an request for the next page.
        page += 1

        data["page"] = str(page)
        request = scrapy.Request(url=self.harbor_url + "/results.asp?" + urllib.urlencode(data), callback=self.hardbor_parse, dont_filter=True)
        request.meta["page"] = page
        request.meta["total_page"] = total_page
        request.meta["client"] = response.meta["client"]
        request.meta["data"] = data
        request.meta["search"] = search 
        yield request
        

    # validate the value of html node
    #    return string value, if data is validated
    #    return "", otherwise
    def validate(self, node):
        if len(node) > 0:
            temp = node[0].extract().strip()
            return temp
        else:	
            return ""

    def matches(self, data):
        pass

