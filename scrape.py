import random
import time
import base64
from PIL import Image
from io import BytesIO
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import Proxy
from selenium.webdriver.common.proxy import ProxyType
from bs4 import BeautifulSoup
from parse import solve_captcha_with_ai
from fake_useragent import UserAgent
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set up the proxy
proxy = Proxy({
    "proxyType": ProxyType.MANUAL,
    "httpProxy": os.getenv("BRIGHTDATA_PROXY_URL"),
    "sslProxy": os.getenv("BRIGHTDATA_PROXY_URL"),
})

# Get random headers for the request
def get_random_headers():
    try:
        ua = UserAgent()  # Initialize UserAgent object
        return {
            "User-Agent": ua.random,  # Set User-Agent header
            "Accept-Language": "en-US,en;q=0.9",  # Set Accept-Language header
            "Referer": "https://www.google.com/",  # Set Referer header
            "DNT": "1",  # Set Do Not Track header
        }
    except Exception as e:
        print(f"Error generating User-Agent: {e}")
        return {  # Fallback to a static User-Agent if fake_useragent fails
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
        }

# Simulate human-like interaction before clicking
def human_like_interaction(driver, element):
    actions = ActionChains(driver)
    actions.move_to_element(element)
    time.sleep(random.uniform(0.5, 2.0))  # Random delay
    actions.click().perform()

def scrape_website(website, max_retries=3, use_proxy=True):
    print("Launching Browser")

    # Get the Bright Data proxy URL from environment variables
    proxy_url = os.getenv("BRIGHTDATA_PROXY_URL") if use_proxy else None

    if use_proxy and not proxy_url:
        print("Error: Proxy URL not found in environment variables.")
        return None

    if use_proxy:
        print(f"Using proxy: {proxy_url}")

    # Configure ChromeOptions
    options = ChromeOptions()
    options.add_argument("--headless")  # Enable headless mode
    options.add_argument("--disable-gpu")  # Disable GPU acceleration
    options.add_argument("--no-sandbox")  # Bypass OS-level security restrictions
    options.add_argument("--disable-dev-shm-usage")  # Prevent resource issues
    options.add_argument(f"user-agent={get_random_headers()['User-Agent']}")  # Set User-Agent header
    options.add_argument("--profile-directory=Default")  # Set Chrome profile directory
    options.add_argument("--user-data-dir=/path/to/your/chrome/profile")  # Set Chrome user data directory
    options.add_argument("--disable-blink-features=AutomationControlled")  # Disable automation features

    # Add the proxy to ChromeOptions if enabled
    if use_proxy and proxy_url:
        options.add_argument(f"--proxy-server={proxy_url}")

    for attempt in range(max_retries):  # Only one loop
        driver = None  # Initialize driver as None
        try:
            driver = webdriver.Chrome(options=options)
            print(f'Attempt {attempt + 1}: Navigating to {website}...')
            driver.get(website)  
            time.sleep(2)  # Allow time for page to load

            captcha_image = detect_and_solve_captcha(driver)  # Check for CAPTCHA
            if captcha_image:
                captcha_text = solve_captcha_with_ai(captcha_image)  # Solve it
                if captcha_text:
                    captcha_input = driver.find_element(By.NAME, "captcha")  # Locate CAPTCHA input field
                    captcha_input.send_keys(captcha_text)  # Submit solution
                    driver.find_element(By.TAG_NAME, "form").submit()  # Submit form
                    time.sleep(2)

            print('Scraping page content...')
            html = driver.page_source
            return html  
        except Exception as e:
            print(f"Error during attempt {attempt + 1}: {e}")
        finally:
            if driver:  
                driver.quit()  

        time.sleep(5)  

    print("Failed to scrape website after multiple attempts.")
    return None  

# Detect and solve CAPTCHA
def detect_and_solve_captcha(driver):
    """Detects CAPTCHA and extracts the image."""
    try:
        print("Checking for CAPTCHA element...")
        # Check if the CAPTCHA element exists
        captcha_elements = driver.find_elements(By.CSS_SELECTOR, "div.captcha-image")  # Update selector as needed
        if not captcha_elements:
            print("No CAPTCHA element found on the page.")
            return None

        # Wait for the CAPTCHA element to be visible
        captcha_element = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "div.captcha-image"))  # Update selector as needed
        )
        print("CAPTCHA element found.")

        # Take a screenshot of the CAPTCHA element
        captcha_screenshot = captcha_element.screenshot_as_png

        # Save the screenshot for debugging
        with open("captcha.png", "wb") as f:
            f.write(captcha_screenshot)

        # Convert the screenshot to an image
        captcha_image = Image.open(BytesIO(captcha_screenshot))
        return captcha_image  # Return CAPTCHA image for AI processing
    except Exception as e:
        print(f"No CAPTCHA detected: {e}")
        return None  # No CAPTCHA found

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