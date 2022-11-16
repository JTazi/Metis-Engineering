# Metis-Engineering
Data Pipeline from api to app interface

## Summary:
The goal of this project was to ingest Magic the Gathering (MTG) card data into a database, extract the important pieces, and
display on an easy to use and interactive application. The data is scraped from Scryfall. using the BeautifulSoup and requests
library, stored in a Mongo database via Atlas, and interacted with through a streamlit app hosted on Streamlit Cloud.

**update_db.py** - a python script for pulling the html for the scryfall.com page that has the bulk download URL for MTG card data,
using beautiful soup to extract the URL, initiate a mongoclient on the MongoDB server, erase the old collection and replace with
the newest collection. New MTG cards are released every few months so this script is only needed 3-4 times a year.

**MTG_card_app.ipynb** - the jupyter notebook I used when troubleshooting or learning how to implement parts of the project, not needed
for final execution of project.

**bulk_json_ex** - an example of the data included for 1xdocument in the MTG cards collection. I used this to determine what columns to
include in my streamlit app.

**requirements.txt** - a required document for using streamlit cloud. This establishes which python libraries are needed to execute streamlit
app.

**test_st.py** - the python file for creating/running the streamlit application.

**.streamlit/secrets.toml** - a file used to communicate the mongodb host, port, username, password to allow my streamlit app to query the mongoDB.
