import streamlit as st
from scrape import scrape_website

st.title("AI Web Scraper") # Title of the Web App
url = st.text_input("Enter Website URL:") # Text Input for URL

if st.button("Scrape"): # Button to start scraping
    st.write("Scraping...") # Displaying a message
    result = scrape_website(url) # Calling the scrape_website function
    st.text_area("Scraped HTML:", result, height=300) # Displaying the scraped HTML

