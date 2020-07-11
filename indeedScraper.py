#Doesn't have properly built in waits for slow internet

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import random
import time
import sys

class scraper:
    #age = "30"
    age = "7"
    sort = "date"
    jobType = "fulltime"
    expLevel = ["entry_level", "mid_level"]

    def __init__(self, job, location):
        self.job = job
        self.location = location

    def getURL(self):
        baseURL = "https://www.indeed.com/jobs?"
        jobURL = "q=" + self.job.replace(" ", "+")
        locationURL = "l=" + self.location.replace(" ", "+")
        jobTypeURL = "jt=" + self.jobType
        expLevelURL = "explvl=" + self.expLevel[0]
        dateURL = "fromage=" + self.age
        sortURL = "sort=" + self.sort
        fullURL = baseURL+jobURL+"&"+locationURL+"&"+jobTypeURL+"&"+expLevelURL+"&"+dateURL+"&"+sortURL
        return fullURL

    def scrape(self):
        URL = self.getURL()
        fileName = self.job + "_" + self.location + "_" + self.jobType + "_" + self.expLevel[0] + ".txt"
        fout = open(fileName.replace(" ", "-"), "a")

        try:
            driver = webdriver.Firefox()
            driver.implicitly_wait(1)
            driver.get(URL)
            if "Indeed" not in driver.title:
                raise Exception("Navigated off Indeed somehow")
            time.sleep(2)

            moreToScrape = True
            while moreToScrape:

                jobs = driver.find_elements_by_class_name('jobsearch-SerpJobCard')
                for job in jobs:
                    driver.execute_script("arguments[0].scrollIntoView();", job)
                    job.click()
                    if "Indeed" not in driver.title:
                        raise Exception("Navigated off Indeed")
                    #TODO: See how this replace works
                    fout.write(driver.find_element_by_id('vjs-container').get_attribute('innerHTML').replace("|", "/"))
                    #TODO: Make sure URL is there
                    fout.write("<p class=\"URL\">" + driver.current_url + "</p>")
                    fout.write("|")
                    time.sleep(random.random())
            
                nextPage = driver.find_elements_by_css_selector("a[aria-label='Next']")
                if len(nextPage) == 1:
                    nextPage[0].click()
                    time.sleep(1)
                    popupX = driver.find_elements_by_class_name('popover-x-button-close')
                    if len(popupX) == 1:
                        popupX[0].click()
                        time.sleep(random.random())
                    else:
                        raise Exception("Too many X buttons")
                else:
                    moreToScrape = False

        except Exception as e:
            print(e)

        finally:
            driver.quit()
            fout.close()


if __name__ == "__main__":
    with open(sys.argv[1], "r") as configFile:
        config = configFile.read()
    config = config.split("\n")
    jobs = config[0].split(",")[1:]
    locations = config[1].split(",")[1:]

    #for job in jobs:
    #    for location in locations:
    #        scraper(job, location).scrape()
    #        time.sleep(5 + random.random())
    scraper(jobs[0], locations[0]).scrape()
