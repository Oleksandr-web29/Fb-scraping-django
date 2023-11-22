# selenium-related
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from bs4 import BeautifulSoup as bs

# other necessary ones
import urllib.request
import pandas as pd
import json
import time
import re
import warnings
import os

warnings.filterwarnings('ignore')

class FacebookScraper:
    def __init__(self):
        #self.option = option
        self.option = Options()
        self.option.add_argument('--headless')
        self.option.add_argument('--no-sandbox')
        self.option.add_argument("--disable-dev-shm-usage")
        self.option.add_argument("--disable-infobars")
        self.option.add_argument("start-maximized")
        self.option.add_argument("--disable-extensions")
        #self.browser = browser
        # CHROMEDRIVER_PATH = '/root/Scrapers/FacebookGUI/chromedriver'

        # Get the directory of the current file (views.py)
        current_directory = os.path.dirname(os.path.abspath(__file__))

        # Path to chromedriver.exe within the same directory as views.py
        CHROMEDRIVER_PATH = os.path.join(current_directory, 'chromedriver.exe')

      #   CHROMEDRIVER_PATH = 'chromedriver.exe'
        s = Service(executable_path=CHROMEDRIVER_PATH)
        self.browser = webdriver.Chrome(service=s, options=self.option)
        #self.browser = webdriver.Chrome(executable_path=":~/Scrapers/FacebookGUI/webdriver/chromedriver-linux64/chromedriver", options=self.option)
        self.scroll_page = self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        
        
        # X-paths
        # x-path to main article containing each comment
        self.article_class = 'by bz ca'
        self.article_id = 'u_0_'
        
        # footer class xpath under article holding comments, React, Share
        self.footer = 'cx'
        
        # span class xpath to obtain comments storylink
        self.story_href= 'l cy'
        
        # once storylink is clicked the div class xpath to each commnet
        self.comments_class = 'ek'
        
        # nameid of the one commenting a class xpath under h3 
        self.name_id = 'el bs'
        # div class xpath to the comment
        self.raw_comment = 'em'
        
    # login function
    def login(self, email,password):
        # facebook basic -- choosen for it's simplicity
        self.browser.get("https://mbasic.facebook.com/")
        self.browser.maximize_window()
        wait = WebDriverWait(self.browser, 30)
        # login 
        email_field = wait.until(EC.visibility_of_element_located((By.NAME, 'email')))
        email_field.send_keys(email)
        pass_field = wait.until(EC.visibility_of_element_located((By.NAME, 'pass')))
        pass_field.send_keys(password)
        pass_field.send_keys(Keys.RETURN) 
    
    # function to obtain pages links
    def get_page(self,query):
        self.browser.get(f'https://mbasic.facebook.com/search/pages/?q={query}')
        src = self.browser.page_source
        # list to store hrefs links  
        hrefs = []
        # parser by beautiful soup
        soup=bs(src,'html.parser') 
        for s in soup.find_all('a'):
            href = s.get('href')
            hrefs.append(href)
        prof_links = []
        for hfs in hrefs:
            for h in hfs.split(" "):
                if "offic" in h:
                    prof_links.append(h)
        return prof_links
        
    
    # function to obtain the /storyid/ 
    def get_storylink(self):
        # footer xpath
        self.scroll_page
        footer = self.browser.find_elements_by_xpath(f"//footer[@class='{self.footer}']")
        # list to store links
        links_sum = []
        for foot in footer:
            # comment link xpath
            com_links = foot.find_elements_by_xpath(f"//div[@class='{self.story_href}']")
            for com_link in com_links:
                # storyid href xpath
                # get all that contains story
                elem = com_link.find_element_by_xpath("//a[contains(@href,'/story.php?')]")
                story_link = elem.get_attribute('href')
                links_sum.append(story_link)
        # yield story links
        return links_sum
    
    ## gets comment links
    def navigate(self, prof_link):
        #print("Navigating...")
        # prioritize for the first one
        prof_ck = self.browser.find_element_by_xpath(f"//a[@href='{prof_link[0]}']").click()
        
        # sleep 
        time.sleep(5)
    
        # click on Timeline
        element = self.browser.find_element_by_xpath("//a[contains(text(), 'Timeline')]").click()
    
        # sleep
        time.sleep(5)
    
        # scroll
        self.scroll_page
    
        # sleep
        time.sleep(1)
    
        # see more stories click 
        element2 = self.browser.find_element_by_xpath("//span[contains(text(), 'See more stories')]").click()
    
        # sleep
        time.sleep(5)
        # scroll
        self.scroll_page
        #self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # get comments
        
    def all_comments(self):
        self.scroll_page
        time.sleep(5)
        src = self.browser.page_source
        # list to store hrefs links  
        hrefs = []
        # parser by beautiful soup
        soup=bs(src,'html.parser') 
        for s in soup.find_all('a'):
            href = s.get('href')
            hrefs.append(href)
        stry_links = []
        for hfs in hrefs:
            for h in hfs.split(" "):
                if "/story.php?" in h:
                    stry_links.append(h)
        return set(stry_links)
        
    # get comments, name, url
    def get_comments_links(self,stry_link):
        # dictionary to name of one who commented, url to the post, comment
        comments = {}
        c_h = stry_link.encode(encoding = 'UTF-8')
        c_h = repr(c_h)[2:-1]
        time.sleep(5)
        
        # click the story
        self.browser.get(f"{str(c_h)}")
        
        # sleep
        time.sleep(5)
        
        # scroll
     
        self.scroll_page
        time.sleep(5)
        #comms = self.browser.find_elements_by_xpath(f"//div[@class='{self.comments_class}']")
#         # get all from comments class
#         comms = self.browser.find_elements(By.CLASS_NAME,f"{self.comments_class}")
#         for com in comms:
        self.scroll_page
        IDs = self.browser.find_elements_by_xpath("//*[contains(@id, '0') or contains(@id, '1') or contains(@id, '2') or contains(@id, '3') or contains(@id, '4') or contains(@id, '5') or contains(@id, '6') or contains(@id, '7') or contains(@id, '8') or contains(@id, '9')]")
        pattern = r'^[0-9]{15,16}$'
        for ID in IDs:
            ID_at = ID.get_attribute("id")
            # Use re.findall to find all matching strings
            com_ids = [Id for Id in ID_at if re.search(pattern, ID_at)]
            coms_id = ''.join(com_ids)
            time.sleep(5)
            #h3 = Id.find_element(By.TAG_NAME,'div')
            if coms_id != "":
                comment = self.browser.find_element_by_xpath(f"//*[@id='{coms_id}']/div/div[1]").text
                name_id = self.browser.find_element_by_xpath(f"//*[@id='{coms_id}']/div/h3/a").text
                #print("**name", name_id)
                #print("***comment", comment)
                #print("*** Name ",name_id)
                #comments['Name'] = name_id
                #comments['Url'] = stry_link
                #comments['Comment'] = comment
                return stry_link, name_id, comment