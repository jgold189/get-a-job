#Doesn't have properly built in waits for slow internet

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import random
import time
import sys

#Class that handles all the scraping for Indeed
class IndeedScraper:
    #age = "30"
    age = "7"
    sort = "date"
    jobType = "fulltime"
    expLevel = ["entry_level", "mid_level"]

    #Sets the job and location for the scrape
    def __init__(self, job, location):
        self.job = job
        self.location = location

    #Gets the exact URL to go to
    def getURL(self):
        baseURL = "https://www.indeed.com/jobs?"
        jobURL = "q=" + self.job.replace(" ", "+")
        locationURL = "l=" + self.location.replace(" ", "+")
        jobTypeURL = "jt=" + self.jobType
        #Currently on does entry level experience level
        expLevelURL = "explvl=" + self.expLevel[0]
        dateURL = "fromage=" + self.age
        sortURL = "sort=" + self.sort
        fullURL = baseURL+jobURL+"&"+locationURL+"&"+jobTypeURL+"&"+expLevelURL+"&"+dateURL+"&"+sortURL
        return fullURL

    #Does all the actual scraping here
    def scrape(self):
        URL = self.getURL()
        #Set the filename to what we scraped
        fileName = self.job + "_" + self.location + "_" + self.jobType + "_" + self.expLevel[0] + ".txt"
        fout = open(fileName.replace(" ", "-"), "a")

        #In case of exceptions this is all in a try catch finally
        try:
            #Open the driver, set it to wait 1 second, and open the url
            driver = webdriver.Firefox()
            driver.implicitly_wait(1)
            driver.get(URL)
            #If for some reason we haven't loaded Indeed, raise an error
            if "Indeed" not in driver.title:
                raise Exception("Navigated off Indeed somehow")
            #Let stuff load in
            time.sleep(1)

            moreToScrape = True
            #Keep scraping until we hit the last page and there isn't anything left
            while moreToScrape:

                #Every job is represented by a jobsearch-SerpJobCard
                jobs = driver.find_elements_by_class_name('jobsearch-SerpJobCard')
                for job in jobs:
                    #Have to keep scrolling the items into view before we click on them or it errors
                    driver.execute_script("arguments[0].scrollIntoView();", job)
                    job.click()
                    #Again if we somehow got off Indeed by clicking a link then raise an error
                    if "Indeed" not in driver.title:
                        raise Exception("Navigated off Indeed")
                    #The info we want is the innerHTML of the vjs-container. Replace the | with / to prevent run-ins with our ETL
                    fout.write(driver.find_element_by_id('vjs-container').get_attribute('innerHTML').replace("|", "/"))
                    #Add a small field on the end with the URL for use in the ETL
                    fout.write("<p class=\"URL\">" + driver.current_url + "</p>")
                    #Add a pipe to seperate entries
                    fout.write("|")
                    #Sleep for a random short amount of time to hopefully fool Indeed
                    time.sleep(random.random())
            
                #Look for an item with the css on it that denotes it is the next page arrow
                #If its there then click it, otherwise we are on the last page and thus done with scraping
                nextPage = driver.find_elements_by_css_selector("a[aria-label='Next']")
                if len(nextPage) == 1:
                    #Click on the next page, wait a sec to load in
                    nextPage[0].click()
                    time.sleep(1)
                    #If a popup x appears then a popup has appeared and we need to close it so just click it
                    popupX = driver.find_elements_by_class_name('popover-x-button-close')
                    if len(popupX) == 1:
                        popupX[0].click()
                        time.sleep(random.random())
                    #If there are too many popup X buttons panic and throw an error. What has the world come too...
                    elif len(popupX) > 1:
                        raise Exception("Too many X buttons")
                else:
                    moreToScrape = False

        #Print any exception we have
        except Exception as e:
            print(e)

        #Finally quit the driver and close the open file
        finally:
            driver.quit()
            fout.close()


if __name__ == "__main__":
    #Grab the configurations from file
    with open(sys.argv[1], "r") as configFile:
        config = configFile.read()
    config = config.split("\n")
    jobs = config[0].split(",")[1:]
    locations = config[1].split(",")[1:]

    #TODO: Uncomment this when ready
    #for job in jobs:
    #    for location in locations:
    #        scraper(job, location).scrape()
    #        time.sleep(5 + random.random())
    IndeedScraper(jobs[0], locations[0]).scrape()
