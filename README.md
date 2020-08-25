# Job Finder Program |UNFINISHED|

This program is designed to scrape job postings that would interest you from major job boards and aggregate them in an easy to order and sort centralized place. As I'm sure you could read in the title though this program was never fully finished. Hopefully one day I have the time to come back to this and work on it. Right now all that works (at the time of writing this) is the Indeed scraper and Indeed ETL operation to scrape data from Indeed and transform it into a NoSQL format, specifically MongoDB, but could be quickly changed to work with another NoSQL database.

## Setup
Needs Selenium, BeautifulSoup4, and PyMongo to run.  
Customize config.cfg to whatever job titles and locations you want the program to search for. First line should be for jobs, second line for locations. Leave in the jobs and locations tags. There must be at least one job and at least one location for the program to work.  
Customize tags.cfg to whatever tags you think might be important to sort by in jobs. This can be useful for looking for jobs that have exactly what you want.  

## Running
To run the Indeed scraper just run `python indeedScraper.py /path/to/config.cfg`  
**Note:** Selenium is currently not set to run headlessly so a robot browser will pop up that must remain open while the scraper runs.  
  
To run the Indeed ETL operation just run `python indeedETL.py /path/to/saved/data.txt /path/to/tags.cfg`  
**Note:** The ETL operation currently tries to put things into MongoDB using PyMongo so make sure it is properly configured to access your MongoDB cluster.  

### Features/Quirks
A note on a feature that has not been fully tested (only initial tests were done) that may cause a problem later down the line or work perfectly is the ID of documents inserted into MongoDB. Currently the ID is based off a MD5 hash of the job title, company, and location truncated to fit into the MongoDB ID field. The purpose of this was to prevent duplicates efficiently. Between Indeed's search mechanism and jobs being posted on multiple sites there would be an extremely high amount of duplicates with no clear single field that could tell duplicates. Theoretically there would be no problem with the method of hashing on job title, company, and location besides possible punctuation or capitalization which could be easily fixed. The only problem comes with the fact that even with MD5, which has a small digest size, the full hashed value cannot fit into MongoDB's ID field. As such we need to truncate it. I don't know enough about the risks of hash collisons when truncating hashes to say whether this is fully safe for duplicate prevention or not. Ideally there would be thorough testing that would go into this feature but considering how the program isn't even close to a minimum viable product I never got around to in-depth testing, only some surface level tests which showed that it was working. Duplicates were being prevented while all unique postings were saved, it's quite possible that it could just have a small chance of blocking a non-duplicate.

## Planned Features
If I ever actually get around to this program again here are some planned features to really flesh it out:  

- Front-End program or website for displaying data and providing a search/sort UI
- Automation for scraper/ETL. Ideally through cron jobs and bash scripts if kept local or airflow if distributed
- Scraper and ETL for LinkedIn, Handshake, and some other job aggregators
- Fancy NLP features:
  - Find tags and keywords automatically
  - Have the user rate which jobs sound good or bad to eventually create a personalised supervised system to sort jobs
- If this ever actually gets distributed: Kafka pipelines to keep data flow smooth and continuous
- The ULTIMATE STRETCH FEATURE: Automatic job application process where it both finds jobs you might like and applies to jobs over a certain threshold automatically (This is pretty advanced and honestly out of the scope of this project. But it would be super cool)
