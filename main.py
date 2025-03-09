import streamlit as st
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

    result = scrape_website(url) # Calling the scrape_website function
    body_content = extract_data(result) # Extracting the body content
    cleaned_content = clean_content(body_content) # Cleaning the content

    st.session_state.dom_content = cleaned_content # Storing the cleaned content in session state

    with st.expander("View DOM Content"):
        st.text_area("DOM Content", cleaned_content, height=400) # Displaying the cleaned content
    
if "dom_content" in st.session_state: # if the cleand content is available in session state
    parse_description = st.text_area("Describe what you want to parse:") # Text Area for user input

    if st.button("Parse"): # Button to start parsing
        st.write("Parsing...") # Displaying a message that parsing is in progress

        dom_chunks = split_dom_content(st.session_state.dom_content) # Splitting the content into chunks
        result = parse_with_ollama(dom_chunks, parse_description)
        st.write(result)