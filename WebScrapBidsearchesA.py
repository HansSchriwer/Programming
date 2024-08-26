#!/usr/bin/env python
# coding: utf-8

# In[1]:


pip install requests beautifulsoup4 pandas selenium webdriver-manager


# In[3]:


import requests
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

# Function to scrape a website for bids using requests and BeautifulSoup (for static pages)
def scrape_bids_static(url):
    try:
        # Send an HTTP request to the website
        response = requests.get(url)
        response.raise_for_status()  # Check if request was successful
        
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract relevant information, such as bid titles, descriptions, deadlines, and links
        bids = []
        for bid in soup.find_all('div', class_='bid-listing'):  # Adjust based on the actual site structure
            title = bid.find('h2').text.strip()
            description = bid.find('p', class_='description').text.strip()
            deadline = bid.find('span', class_='deadline').text.strip()
            link = bid.find('a', href=True)['href']
            
            bids.append({
                'Title': title,
                'Description': description,
                'Deadline': deadline,
                'Link': link
            })
        
        return bids
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from {url}: {e}")
        return []

# Function to scrape a website for bids using Selenium (for dynamic pages)
def scrape_bids_dynamic(url):
    # Setup selenium
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(url)
    time.sleep(5)  # Allow some time for the page to load (adjust as needed)
    
    bids = []
    elements = driver.find_elements(By.CLASS_NAME, 'bid-listing')  # Adjust class name based on actual site structure
    
    for elem in elements:
        title = elem.find_element(By.TAG_NAME, 'h2').text.strip()
        description = elem.find_element(By.CLASS_NAME, 'description').text.strip()
        deadline = elem.find_element(By.CLASS_NAME, 'deadline').text.strip()
        link = elem.find_element(By.TAG_NAME, 'a').get_attribute('href')
        
        bids.append({
            'Title': title,
            'Description': description,
            'Deadline': deadline,
            'Link': link
        })
    
    driver.quit()  # Close the browser when done
    return bids

# Function to save bids to a CSV file
def save_to_csv(bids, filename='bids.csv'):
    df = pd.DataFrame(bids)
    df.to_csv(filename, index=False)
    print(f"Data saved to {filename}")

# URLs of websites to scrape (example websites)
static_urls = [
    'https://www.bidsearch.com',  # Replace with actual bid portal URLs
]

dynamic_urls = [
    'https://www.bidsearch.com',  # Replace with actual bid portal URLs
]

# Collect all bids from static websites
all_bids = []
for url in static_urls:
    bids = scrape_bids_static(url)
    all_bids.extend(bids)

# Collect all bids from dynamic websites
for url in dynamic_urls:
    bids = scrape_bids_dynamic(url)
    all_bids.extend(bids)

# Save the collected bids to a CSV file
if all_bids:
    save_to_csv(all_bids)
else:
    print("No bids found.")


# In[ ]:




