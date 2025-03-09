import random
import time
import json
from selenium import webdriver
from selenium.webdriver import Remote, ChromeOptions
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup


# Bright Data Proxy with session-based rotation
def get_proxy():
    with open("config.json", "r") as file:
        config = json.load(file)
    return config.get("proxy", None) # use default none if no proxy is set

def scrape_website(website, max_retries=3): # Scrape the website using a rotating proxy
    print("Launching Browser")

    proxy_url = get_proxy()  # Get a new proxy for each request
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Enable headless mode
    options.add_argument("--disable-gpu")  # Disable GPU acceleration (for compatibility)
    options.add_argument("--no-sandbox")  # Bypass OS-level security restrictions
    options.add_argument("--disable-dev-shm-usage")  # Prevent resource issues in Docker/Linux
    options.add_argument(f"--proxy-server={proxy_url}")  # Use rotating proxy

    for attempt in range(max_retries):
        driver = webdriver.Remote(command_executor=proxy_url, options=options)

        try:
            print(f'Attempt {attempt + 1}: Navigating to {website}...')
            driver.get(website)  
            time.sleep(2)  # Allow time for page to load

            if "captcha" in driver.page_source.lower():  
                print("Captcha detected! Retrying with new proxy...")
                driver.quit()
                continue  

            print('Scraping page content...')
            html = driver.page_source
            return html
        except Exception as e:
            print(f"Error: {e}")
        finally:
            driver.quit()  
        time.sleep(5)  # Wait before retrying
    
    print("Failed to scrape website after multiple attempts.")
    return None

def extract_data(html_content): # Extract the body content from the HTML
    soup = BeautifulSoup(html_content, 'html.parser') # Parse the HTML content
    body_content = soup.body # Get the body content
    if body_content: # If body content exists
        return str(body_content) # Return the body content as a string
    return "" # Return an empty string if body content is not found

def clean_content(body_content): # Clean the body content by removing scripts and styles
    soup = BeautifulSoup(body_content, 'html.parser') # Parse the body content
    for script_or_style in soup(["script", "style"]): # Find all script and style tags
        script_or_style.extract() # Remove the script and style tags
    
    cleaned_content = soup.get_text(separator="\n") # Get the text content of the body
    cleaned_content = "\n".join(
        line.strip() for line in cleaned_content.splitlines() if line.strip()
    )
    
    return cleaned_content

def split_dom_content(dom_content, max_length=6000): # Split the content into chunks
    return [
        dom_content[i:i + max_length] for i in range(0, len(dom_content), max_length) # Split the content into chunks of 6000 characters once limit is reached it starts a new chunk at 6000 + i
    ]


