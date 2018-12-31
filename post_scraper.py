from threading import Thread, active_count
from selenium import webdriver, common
from selenium.webdriver.chrome.options import  Options
from webdriver_manager.chrome import ChromeDriverManager
import json
import time
from queue import LifoQueue
from cli import display_progress
import sys

cli_info = False


def scrape(url, file_name, driver):

    start = time.time()

    try:
        driver.get(url)
        try:
            post = driver.find_element_by_class_name('ak-item-mid').find_element_by_class_name('ak-text').text
        except common.exceptions.NoSuchElementException:
            if cli_info:
                print("Can't find element mid. Reloading the page and loading.")
            driver.get(url)
            time.sleep(5)
            try:
                post = driver.find_element_by_class_name('ak-item-mid').find_element_by_class_name('ak-text').text
            except common.exceptions.NoSuchElementException:
                if cli_info:
                    print("Reeeeeally can't find element mid. Reloading the page and loading.")
                driver.get(url)
                time.sleep(120)
                try:
                    post = driver.find_element_by_class_name('ak-item-mid').find_element_by_class_name('ak-text').text
                except common.exceptions.NoSuchElementException:
                    return

        comment_elements = driver.find_elements_by_class_name('ak-content-post')
        comments = []
        for i in range(len(comment_elements)):
            elem = comment_elements[i].find_element_by_class_name('ak-text')
            try:
                elem = elem.find_element_by_tag_name('*').text
                if len(elem) > 0:
                    comments.append(elem)
            except common.exceptions.NoSuchElementException:
                if cli_info:
                    print('Failed to get <p> element')

        same_page = False
        counter = 2
        if len(comments) > 0:
            first_element = comments[0]
            while not same_page:
                driver.get(url+"?page="+str(counter))
                comment_elements = driver.find_elements_by_class_name('ak-content-post')
                if not len(comment_elements) > 0:
                    if cli_info:
                        print("Didn't find comments in", url)
                    time.sleep(5)
                    comment_elements = driver.find_elements_by_class_name('ak-content-post')
                    if cli_info:
                        print('Fetched comments size after 5 seconds :', len(comment_elements))

                if len(comment_elements) > 0:
                    elem = comment_elements[0].find_element_by_class_name('ak-text')
                    try:
                        elem = elem.find_element_by_tag_name('*').text
                    except common.exceptions.NoSuchElementException:
                        if cli_info:
                            print('Failed to get <p> element')
                        break
                    if elem == first_element:
                        break
                    first_element = elem
                    if len(elem) > 0:
                        comments.append(elem)
                    for i in range(1, len(comment_elements)):
                        elem = comment_elements[i].find_element_by_class_name('ak-text')
                        try:
                            elem = elem.find_element_by_tag_name('*').text
                            if len(elem) > 0:
                                comments.append(elem)
                        except common.exceptions.NoSuchElementException:
                            if cli_info:
                                print('Failed to get <p> element')
                    counter += 1
                else:
                    break

        with open("posts/" + file_name + '.json', 'w', encoding="utf-8") as outfile:
            json.dump({"post": post, "comments": comments}, outfile, ensure_ascii=False)
            end = time.time() - start
            times.append(end/number_of_threads)
            while len(times) > 50:
                times.pop(0)
    except common.exceptions.TimeoutException:
        print('Timeout error !')

times = []


class Scrape(Thread):
    def __init__(self, i):
        Thread.__init__(self)
        self.index = i
        print('Initiating thread', i)

    def run(self):
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
        while urls.qsize():
            post = urls.get()
            scrape(post['link'], str(urls.qsize()), driver)
            display_progress(initial_size - urls.qsize(), initial_size, times)
        driver.close()


chrome_options = Options()
chrome_options.add_argument("--headless")

files = ['post_urls/data'+str(i)+'.json' for i in range(127)]
urls = LifoQueue()
start_index = 63
end_index = 1000000

for file in files:
    with open(file, encoding='utf-8') as f:
        posts = json.load(f)

        for post in posts:
            urls.put(post)

number_of_threads = 16
initial_size = urls.qsize()
threads = []



for i in range(number_of_threads):
    threads.append(Scrape(i))

[thread.start() for thread in threads]
[thread.join() for thread in threads]