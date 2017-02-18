# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from lostpet.settings import *
from lostpet.send_email_smtp import *
from lostpet.database import *
import sqlite3

class LostpetPipeline(object):
    def open_spider(self, spider):
        # self.file = open('pets.csv', 'wb')
        self.conn = sqlite3.connect('../web/db.sqlite3')

        self.clients = dict()

    def close_spider(self, spider):
        # save result into csv file
        '''for pet in self.pets:
            self.file.write("%s\n" % pet)
        self.file.close()'''
        self.conn.close()

        print self.clients
        for client_id in self.clients:
            client = self.clients[client_id]

            # send result via gmail smtp server
            subject = "Possible Match Found for %s" % client["pet_name"]
            body = self.get_email_body(client["client_name"], client["pet_name"], client["pets"])

            print body
            send_email(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, DEFAULT_FROM_EMAIL, client["client_email"], subject, body)
        print "************* End crawler ***************"

    def process_item(self, item, spider):
        id = str(item["client_id"])
        
        if checkPaidUser(self.conn, item["client_email"]) == False:
           return item

        # if this url is in database.
        if checkPet(self.conn, item):
           return item

        if id not in self.clients:
            self.clients[id] = {"pets": []}
            self.clients[id]["client_name"] = item["client_name"]
            self.clients[id]["client_email"] = item["client_email"]
            self.clients[id]["pet_name"] = item["pet_name"]

        self.clients[id]["pets"].append(item["url"])

        return item

    def get_email_body(self, client, pet_name, pets):
        body = "<p>Hi <b>%s</b>,</p><p>Our system has found a potential match for <b>%s</b>.</p>" % (client, pet_name)
        urls = "<p>%s</p>" % "<br/><br/>".join(["<a href='%s'>%s</a>" % (url, url) for url in pets])
        body += urls + "<p>Our automated system has flagged the above listing(s) for \
                           having similar traits such as breed, gender, size, and hair color.</p><p>Thanks,<br/>Cuddles United Team</p>"

        return body
        
