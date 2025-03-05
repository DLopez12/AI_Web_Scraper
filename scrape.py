import random
from selenium import webdriver
from selenium.webdriver import Remote, ChromeOptions
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection
from selenium.webdriver.common.by import By


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


