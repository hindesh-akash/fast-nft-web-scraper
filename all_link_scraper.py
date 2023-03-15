from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import pandas as pd
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import cpu_count, Pool

# Setting up the web-browser

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(service=Service(
    ChromeDriverManager().install()), options=options)
action = ActionChains(driver)


# Getting the webpage till bottom

homepage_url = 'https://raritysniper.com/nft-collections/'

def get_webpage(url):
    driver.get(url=url)
    time.sleep(3)
    height = driver.execute_script('return document.body.scrollHeight;')
    while True:
        driver.execute_script('window.scrollTo(0,document.body.scrollHeight);')
        time.sleep(2)
        new_height = driver.execute_script(
            'return document.body.scrollHeight;')
        if height == new_height:
            break
        height = new_height

# Getting all the links:
def get_all_links(homepage_url):
    get_webpage(homepage_url)
    collections = driver.find_elements(by=By.TAG_NAME, value='a')
    links = []
    for collect in collections:
        links.append(collect.get_attribute('href'))

    #We can check manually that first 20 links are not from nft-collection
    return links[17:]


all_links = get_all_links(homepage_url)


start = time.time()
all_links = get_all_links(homepage_url)
collection_names = [i.split('/')[-1] for i in all_links]
all_urls = pd.DataFrame(list(zip(collection_names,all_links)),columns=['collection_name','collection_link'])
all_urls.to_csv('all_nft_collections.csv',index=False)

stop = time.time()
print("Total time: ", stop-start)

