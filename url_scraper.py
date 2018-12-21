from threading import Thread
import time
from selenium import webdriver
import json
from selenium.webdriver.chrome.options import Options


class Scrape(Thread):

    def __init__(self, page_min, page_max):
        """
        Scrapes the URLs from the Dofus forum. Downloads all URLs from pages {min} to {max}
        :param page_min: minimum number of page for the scraper to start at
        :param page_max: maximum number of page for the scraper to end at
        """
        Thread.__init__(self)
        self.min = page_min
        self.max = page_max
        print('Scraping with', page_min, page_max)

    def run(self):
        links = []
        driver = webdriver.Chrome('D:/chromedriver', options=chrome_options)
        website_url = "https://www.dofus.com/fr/forum/1103-discussions-generales"
        driver.get(website_url)

        for page_number in range(self.min, self.max):
            print('Fetching page', page_number)
            driver.get(website_url+"?page="+str(page_number))

            elements = driver.find_elements_by_class_name("ak-title-topic")
            names = list(map(lambda element: element.text, elements))
            href = list(map(lambda element: element.get_attribute('href'), elements))

            for j in range(len(href)):
                links.append({"name": names[j], "link": href[j]})

            if page_number % 20 == 0:
                with open('post_urls/data'+str(int(page_number/20))+'.json', 'w', encoding="utf-8") as outfile:
                    json.dump(links, outfile, ensure_ascii=False)
                links = []


threads = []

number_of_threads = 4
number_of_pages = 2536
offset = number_of_pages/number_of_threads
batches = [[int(offset*i), int(offset*(i+1))] for i in range(number_of_threads)]

chrome_options = Options()
chrome_options.add_argument("--headless")

for batch in batches:
    threads.append(Scrape(batch[0], batch[1]))

[thread.start() for thread in threads]
[thread.join() for thread in threads]
