import streamlit as st
import asyncio
from scrape import (
    scrape_website, 
    extract_data, 
    clean_content, 
    split_dom_content,
)
from parse import parse_with_ollama

st.title("AI Web Scraper") # Title of the Web App
url = st.text_input("Enter Website URL:") # Text Input for URL

if st.button("Scrape"): # Button to start scraping
    st.write("Scraping...") # Displaying a message

    # Call scrape_website with use_proxy=False to disable the proxy
    result = scrape_website(url, use_proxy=False)
    
    if result is None:  # Check if scraping failed
        st.error("Scraping failed after multiple attempts. Please try another URL.")
    else:
        body_content = extract_data(result)  # Extracting the body content
        cleaned_content = clean_content(body_content)  # Cleaning the content

        st.session_state.dom_content = cleaned_content  # Store cleaned content

        with st.expander("View DOM Content"):
            st.text_area("DOM Content", cleaned_content, height=400)  # Display the cleaned content
    
if "dom_content" in st.session_state: # if the cleaned content is available in session state
    parse_description = st.text_area("Describe what you want to parse:") # Text Area for user input

    if st.button("Parse"): # Button to start parsing
        st.write("Parsing...") # Displaying a message that parsing is in progress

        dom_chunks = split_dom_content(st.session_state.dom_content) # Splitting the content into chunks
        
        # Use asyncio to run the async function in a Streamlit-compatible way
        async def run_parsing():
            return await parse_with_ollama(dom_chunks, parse_description)
        
        # Run the coroutine in a way that works with Streamlit
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            result = loop.run_until_complete(run_parsing())
        finally:
            loop.close()
        
        st.write(result)  # Display the parsed result