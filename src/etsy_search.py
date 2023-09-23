
import requests, os, time
from selenium import webdriver
import pandas as pd
from selenium.webdriver.common.by import By

keywords = {}
# format is {keyword: [count]}

# Title element is: # //*[@id="listing-title-1326781863"]

# TODO:
'''
scrape the listing-title keywords
break up each word by space -> only keep the text, no special characters or spaces
put into the keyword dictionary
update the page number and redo
sort the keywords by the count -> create a word map with the dictionary
'''
def get_titles(browser, page_limit):
    titles=[]
    for pageNum in range(0,page_limit):
        url = "https://www.etsy.com/ca/market/nails?ref=pagination&page="+str(pageNum+1)

        
        browser.get(url)
        title_elements=browser.find_elements(By.XPATH, "//*[starts-with(@id, 'listing-title')]")
        for title in title_elements:
            print("title is: ", title.text)
            titles.append(title)
    return titles

if __name__ == "__main__":
    browser = webdriver.Chrome()
    titles = get_titles(browser, 2)