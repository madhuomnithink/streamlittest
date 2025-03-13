import streamlit as st
from pytrends.request import TrendReq
import pandas as pd
from google.cloud import storage
from datetime import datetime
import os

# Google Cloud Configuration
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "causal-fort-404816-fae141dd31c5.json"


def upload_to_gcs(bucket_name, file_path, destination_blob_name):
    """
    Uploads a file to Google Cloud Storage.
    """
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(file_path)
    st.success(f"File uploaded to GCS: {bucket_name}/{destination_blob_name}")


# Streamlit UI
st.title("Google Trends Data Fetcher")

# Input fields
keywords_input = st.text_area("Enter keywords separated by a comma:")
bucket_name = st.text_input("Enter Google Cloud Storage bucket name:")

if st.button("Fetch Trends and Save to GCS"):
    if keywords_input and bucket_name:
        # Parse keywords input
        Totallist = [keyword.strip() for keyword in keywords_input.split(",")]

        # Initialize Pytrends
        pytrend = TrendReq()

        for x in Totallist:
            try:
                # Build payload and fetch data
                keywords = [x]
                pytrend.build_payload(kw_list=keywords, timeframe='today 3-m', geo='US')
                interest_over_time_df1 = pytrend.interest_over_time()

                if not interest_over_time_df1.empty:
                    # Save to CSV
                    today_date = datetime.today().strftime('%Y-%m-%d')
                    file_name = f"{today_date}_{x.replace(' ', '_')}.csv"
                    file_path = f"/tmp/{file_name}"
                    interest_over_time_df1.to_csv(file_path)

                    # Upload to GCS
                    upload_to_gcs(bucket_name, file_path, file_name)
                else:
                    st.warning(f"No data available for keyword: {x}")
            except Exception as e:
                st.error(f"Error processing keyword '{x}': {e}")
    else:
        st.error("Please provide both keywords and bucket name.")
