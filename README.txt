AI Web Scraper

Overview

This project is an AI-powered web scraper built using Python, Selenium, and proxy rotation. The purpose of this project is to demonstrate web scraping techniques, including bypassing captchas, handling proxies, and automating browser interactions.

Features

Selenium-based web scraping – Automates website interaction.

Proxy Rotation Support – Uses Bright Data (as an example) but can be replaced with free or paid proxies.

Headless Mode – Runs the browser without a visible UI for efficiency.

Captcha Handling (Demo) – Implements a placeholder for handling captchas.

Setup Instructions

1. Clone the Repository

git clone https://github.com/yourusername/ai-web-scraper.git
cd ai-web-scraper

2. Install Dependencies

Make sure you have Python installed, then install the required libraries:
pip install selenium streamlit requests

3. Set Up Selenium WebDriver

Download the correct Chrome WebDriver for your browser version and place it in the project folder.
Download ChromeDriver

4. Configure Proxy (Optional)

By default, the scraper uses Bright Data as a proxy example. If you want to use your own proxies:
Edit scrape.py and replace SBR_WEBDRIVER with your proxy.
Or, use free proxies by modifying get_random_proxy() in the code.

Usage
Run the Streamlit App
streamlit run main.py
This will open a web interface where you can enter a URL and scrape its content.

Running the Scraper Manually

If you want to run the scraper without the web UI:
python scrape.py

Notes

This project is for learning purposes only and should not be used for scraping websites without permission.
Bright Data proxies are used as a placeholder – you can replace them with free or paid proxies.
Some websites block headless browsers – you may need to tweak the code for better success.

Future Improvements

- Improve error handling and retry logic.
- Add support for more advanced anti-bot bypassing techniques.
- Implement a proxy pool for better rotation.

License

This project is open-source under the MIT License.
Author: Devanno Lopez
NameGitHub: DLopez12