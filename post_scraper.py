from threading import Thread, active_count
from selenium import webdriver, common
from selenium.webdriver.chrome.options import  Options
import json
import time
from queue import LifoQueue


def scrape(url, file_name, driver):
    try:
        driver.get(url)
        try:
            post = driver.find_element_by_class_name('ak-item-mid').find_element_by_class_name('ak-text').text
        except common.exceptions.NoSuchElementException:
            print("Can't find element mid. Reloading the page and loading.")
            driver.get(url)
            time.sleep(5)
            try:
                post = driver.find_element_by_class_name('ak-item-mid').find_element_by_class_name('ak-text').text
            except common.exceptions.NoSuchElementException:
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
            except:
                print('Failed to get <p> element')

        same_page = False
        counter = 2
        if len(comments) > 0:
            first_element = comments[0]
            while not same_page:
                driver.get(url+"?page="+str(counter))
                comment_elements = driver.find_elements_by_class_name('ak-content-post')
                if not len(comment_elements) > 0:
                    print("Didn't find comments in", url)
                    time.sleep(5)
                    comment_elements = driver.find_elements_by_class_name('ak-content-post')
                    print('Fetched comments size after 5 seconds :', len(comment_elements))

                if len(comment_elements) > 0:
                    elem = comment_elements[0].find_element_by_class_name('ak-text')
                    try:
                        elem = elem.find_element_by_tag_name('*').text
                    except:
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
                        except:
                            print('Failed to get <p> element')
                    counter += 1
                else:
                    break

        with open("posts/" + file_name + '.json', 'w', encoding="utf-8") as outfile:
            json.dump({"post": post, "comments": comments}, outfile, ensure_ascii=False)
    except common.exceptions.TimeoutException:
        print('Timeout error !')


class Scrape(Thread):
    def __init__(self, index):
        Thread.__init__(self)
        self.index = i
        print('Initiating thread. Running threads :', active_count())

    def run(self):
        driver = webdriver.Chrome('D:/chromedriver', options=chrome_options)
        while urls.qsize():
            post = urls.get()
            print(urls.qsize(), post['name'].encode('utf-8'))
            scrape(post['link'], str(urls.qsize()), driver)
        driver.close()


chrome_options = Options()
chrome_options.add_argument("--headless")

files = ['post_urls/data'+str(i)+'.json' for i in range(127)]
urls = LifoQueue()

for file in files:
    with open(file, encoding='utf-8') as f:
        posts = json.load(f)
        for post in posts:
            urls.put(post)

number_of_threads = 8
threads = []

for i in range(number_of_threads):
    threads.append(Scrape(i))

[thread.start() for thread in threads]
[thread.join() for thread in threads]