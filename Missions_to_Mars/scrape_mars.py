# Dependencies
from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import requests
import pymongo
from flask import Flask, render_template
from flask_pymongo import PyMongo
from webdriver_manager.chrome import ChromeDriverManager

def init_browser():
    # @NOTE: Path to my chromedriver
    executable_path = {"executable_path": ChromeDriverManager().install()}
    return Browser("chrome", **executable_path, headless=False)

# Create Mission to Mars global dictionary that can be imported into Mongo
mars_info = {}

# NASA Mars News
def scrape_mars_news():
        browser = init_browser()

        news_url = 'https://mars.nasa.gov/news/'
        browser.visit(news_url)

        html = browser.html
        news_soup = bs(html, 'html.parser')
        
        news_title = news_soup.find_all('div', class_='content_title')[0].text
        news_p = news_soup.find_all('div', class_='article_teaser_body')[0].text

        mars_info['news_title'] = news_title
        mars_info['news_paragraph'] = news_p

        return mars_info

        browser.quit()

# JPL Mars Space Images - Featured Image
def scrape_mars_image():
        browser = init_browser()

        featured_image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
        browser.visit(featured_image_url)# Visit Mars Space Images through splinter module

        html_image = browser.html
        image_soup = bs(html_image, 'html.parser')

        image_url  = image_soup.find('article')['style'].replace('background-image: url(','').replace(');', '')[1:-1]
        main_url = 'https://www.jpl.nasa.gov'
        image_url = main_url + image_url
        print(image_url) 

        mars_info['image_url'] = image_url 
        
        browser.quit()

        return mars_info
      
# Mars Facts
def scrape_mars_facts():
        browser = init_browser()

        mars_facts_url = 'http://space-facts.com/mars/'
        browser.visit(mars_facts_url)

        tables = pd.read_html(mars_facts_url)
        mars_facts_df = tables[0]
    
        mars_facts_df.columns = ['Description', 'Value']

        mars_facts_html = mars_facts_df.to_html()

        mars_info['tables'] = mars_facts_html

        return mars_info

# Mars Hemisphere
def scrape_mars_hemispheres():
        browser = init_browser()

        hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        browser.visit(hemispheres_url)

        html_hemispheres = browser.html
        soup = bs(html_hemispheres, 'html.parser')

        items = soup.find_all('div', class_='item')

        hemisphere_image_urls = []

        hemispheres_main_url = 'https://astrogeology.usgs.gov' 

        for i in items: 
            title = i.find('h3').text

            partial_img_url = i.find('a', class_='itemLink product-item')['href']
            
            browser.visit(hemispheres_main_url + partial_img_url)
            
            partial_img_html = browser.html
            
            soup = bs( partial_img_html, 'html.parser')

            img_url = hemispheres_main_url + soup.find('img', class_='wide-image')['src']
            
            hemisphere_image_urls.append({"title" : title, "img_url" : img_url})

        mars_info['hemisphere_image_urls'] = hemisphere_image_urls

        browser.quit()

        return mars_info