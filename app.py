import streamlit as st
import requests

# Streamlit UI
st.title("Google Trends Scraper")

# User Inputs
keyword = st.text_input("Enter Keyword")
location = st.selectbox("Select Location", ["United States", "India", "United Kingdom"])
date_range = st.selectbox("Select Time Range", ["Past 90 days", "Past 5 years"])

# Mapping location names to API-compatible format
location_map = {
    "United States": "US",
    "India": "IN",
    "United Kingdom": "UK"
}

# Scrape Data Button
if st.button("Scrape Google Trends"):
    if keyword:
        api_url = "https://scrapping-53885457727.us-central1.run.app/scrape/"
        params = {
            "keyword": keyword,
            "location": location_map.get(location, "US"),  # Default to 'US' if not found
            "date_range": date_range
        }

        try:
            response = requests.get(api_url, params=params)

            if response.status_code == 200:
                data = response.json()
                st.success("Data scraped successfully!")
                st.json(data)
            else:
                st.error(f"Failed to scrape data. Status Code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            st.error(f"Request failed: {e}")
    else:
        st.warning("Please enter a keyword.")