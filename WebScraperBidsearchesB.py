#!/usr/bin/env python
# coding: utf-8

# In[1]:


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

# Function to scrape bids from bidsearch.com for ink and toner
def scrape_bids_bidsearch(search_term):
    # Setup selenium with ChromeDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get('https://www.bidsearch.com')

    # Allow time for the page to load
    time.sleep(5)
    
    # Find the search input field, enter the search term, and submit the search
    try:
        search_box = driver.find_element(By.ID, 'search-input')  # Adjust ID based on the actual site structure
        search_box.send_keys(search_term)
        search_box.send_keys(Keys.RETURN)
    except Exception as e:
        print(f"Error finding search box: {e}")
        driver.quit()
        return []

    time.sleep(5)  # Wait for search results to load

    # Extract bid details from the search results
    bids = []
    try:
        bid_listings = driver.find_elements(By.CLASS_NAME, 'bid-listing')  # Adjust class name if needed
        for bid in bid_listings:
            title = bid.find_element(By.TAG_NAME, 'h2').text.strip()
            description = bid.find_element(By.CLASS_NAME, 'description').text.strip()
            deadline = bid.find_element(By.CLASS_NAME, 'deadline').text.strip()
            link = bid.find_element(By.TAG_NAME, 'a').get_attribute('href')

            bids.append({
                'Title': title,
                'Description': description,
                'Deadline': deadline,
                'Link': link
            })
    except Exception as e:
        print(f"Error extracting bids: {e}")
    
    driver.quit()  # Close the browser when done
    return bids

# Function to save bids to a CSV file
def save_to_csv(bids, filename='bidsearch_bids.csv'):
    df = pd.DataFrame(bids)
    df.to_csv(filename, index=False)
    print(f"Data saved to {filename}")

# Search term for ink and toner related bids
search_term = "ink toner"

# Scrape bids from bidsearch.com using the search term
bids = scrape_bids_bidsearch(search_term)

# Save the collected bids to a CSV file
if bids:
    save_to_csv(bids)
else:
    print("No bids found.")


# In[ ]:




