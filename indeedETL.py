import sys
from bs4 import BeautifulSoup
import json

if __name__ == "__main__":
    fin = open(sys.argv[1], "r")
    data = fin.read().split("|")
    fin.close()

    results = []

    for item in data:
        if len(item) > 1:
            soup = BeautifulSoup(item, 'html.parser')
            temp = {}
            temp["jobTitle"] = soup.find("div", id="vjs-jobtitle").string
            temp["companyName"] = soup.find("span", id="vjs-cn").string
            temp["location"] = soup.find("span", id="vjs-loc").getText().strip()[2:]
            temp["desc"] = soup.find("div", id="vjs-desc").getText()
            index = item.find("$")
            if index != -1:
                temp["salary"] = item[index:item.find("<", index)]
            applyButton = soup.find("a", class_="view-apply-button blue-button")
            if applyButton != None:
                temp["applyLink"] = "indeed.com" + applyButton.get("href")
            #TODO: THIS
            #temp["url"] = soup.find("p", class_="URL").getText()
            title = ",".join([temp["jobTitle"], temp["companyName"], temp["location"]])
            results.append({title: temp})

    print(json.dumps(results, sort_keys=True, indent=4))