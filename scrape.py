import random
from selenium import webdriver
from selenium.webdriver import Remote, ChromeOptions
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup


# Bright Data Proxy with session-based rotation
def get_proxy():
    session_id = random.randint(100000, 999999)  # Random session ID for each request
    return f"https://brd-customer-hl_cc258aa6-zone-ai_scraper-session-{session_id}:e9xsr5wigla2@brd.superproxy.io:9515"

def scrape_website(website):
    print("Launching Browser")

    proxy_url = get_proxy()  # Get a new proxy for each request
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Enable headless mode
    options.add_argument("--disable-gpu")  # Disable GPU acceleration (for compatibility)
    options.add_argument("--no-sandbox")  # Bypass OS-level security restrictions
    options.add_argument("--disable-dev-shm-usage")  # Prevent resource issues in Docker/Linux
    options.add_argument(f"--proxy-server={proxy_url}")  # Use rotating proxy

    driver = webdriver.Remote(command_executor=proxy_url, options=options)

    try:
        print('Waiting for captcha to solve')
        solve_res = driver.execute_script("""
            return new Promise((resolve) => {
                setTimeout(() => resolve({status: 'solved'}), 10000);
            });
        """)
        print('Captcha solve status:', solve_res['status'])

        driver.get(website)  # Navigate to the website
        print('Navigated to Website! Scraping page content now...')
        html = driver.page_source
        return html
    finally:
        driver.quit()  # Close the browser after scraping

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
    cleaned_content = "\m".join(
        line.strip() for line in cleaned_content.splitlines() if line.strip()
    )
    
    return cleaned_content

def split_dom_content(dom_content, max_length=6000): # Split the content into chunks
    return [
        dom_content[i:i + max_length] for i in range(0, len(dom_content), max_length) # Split the content into chunks of 6000 characters once limit is reached it starts a new chunk at 6000 + i
    ]


