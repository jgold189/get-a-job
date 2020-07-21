import sys
from bs4 import BeautifulSoup
from datetime import datetime
import pymongo
import bson
import hashlib

if __name__ == "__main__":
    #Open and read in the actual data scraped
    fin = open(sys.argv[1], "r")
    data = fin.read().split("|")
    fin.close()

    #Open and read in the tags the user has added
    fin = open(sys.argv[2], "r")
    goodTags = fin.read().split(",")
    fin.close()

    client = pymongo.MongoClient('localhost', 27017)
    db = client.jobDB
    jobs = db.jobs

    for item in data:
        #Make sure the item actually has data
        if len(item) > 1:
            soup = BeautifulSoup(item, 'html.parser')
            temp = {}
            #Grab the fields from the data
            temp["jobTitle"] = soup.find("div", id="vjs-jobtitle").string
            temp["companyName"] = soup.find("span", id="vjs-cn").string
            #For the location split it into state, city, and zip if a zip exists
            location = {}
            loc = soup.find("span", id="vjs-loc").getText().strip()[2:]
            location["city"], locState = loc.split(",")
            location["state"] = locState[1:3]
            temp["location"] = location
            temp["desc"] = soup.find("div", id="vjs-desc").getText()
            #If there is a dollar sign then there is a salary field so grab that
            index = item.find("$")
            if index != -1:
                temp["salary"] = item[index:item.find("<", index)]
            #If there is a button that has that class then there is an apply button with a link to get
            applyButton = soup.find("a", class_="view-apply-button blue-button")
            if applyButton != None:
                temp["applyLink"] = "indeed.com" + applyButton.get("href")
            #The URL of the page was added on by the scraper
            temp["url"] = soup.find("p", class_="URL").getText()
            itemTag = []
            tempDesc = temp["desc"].lower()
            #Loop through every tag and add it if it's found within the description
            for goodTag in goodTags:
                if tempDesc.find(goodTag) >= 0:
                    itemTag.append(goodTag)
            temp["tags"] = itemTag
            temp["date"] = datetime.today()
            #The title is the hopefully unique key for every posting made up of the title, company, and location
            idString = (",".join([temp["jobTitle"], temp["companyName"], loc])).replace(" ", "")
            #Hash the title string with md5 (smallest digest since we need to truncate)
            idHash = hashlib.md5(idString.encode())
            #Truncate the hash into only 24 hex bytes and convert it to a bson and make that the _id (for duplicate prevention)
            temp["_id"] = bson.ObjectId(idHash.hexdigest()[0:24])
            #Try to insert the entry, if it fails thats because it is a duplicate (hopefully)
            try:
                newJob = jobs.insert_one(temp)
                print(newJob.inserted_id)
            except pymongo.errors.DuplicateKeyError as e:
                print(e)