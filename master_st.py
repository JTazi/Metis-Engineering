#import dependencies
from bs4 import BeautifulSoup as bs
from pymongo import MongoClient
import pandas as pd
import requests
import re
import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder
from st_aggrid.shared import GridUpdateMode

#define functions
def get_url():
	#get html code for scryfall bulk download page
	bulk_url = requests.get('https://scryfall.com/docs/api/bulk-data')
	#convert html to soup
	soup = bs(bulk_url.content, 'html.parser')
	#find URL for bulk download, two items after the table row title, "Default Cards"
	link = soup.find(text = "Default Cards").next.next
	#use regex to extract text between quotations. convert soup to string
	url = re.findall(r'"([^"]*)"', str(link))
	return url[0]
	
def get_api_data(url):
	#bulk download from api at url from get_url and return .json
	bulk = requests.get(url)
	mtg_lib = bulk.json()
	#return list of json objects, one for each card object from api
	return mtg_lib
	
def init_mongo():
	#create client instance
	return client = MongoClient()
	
def load_data(data)
	#load bulk json into mongodb, only do once every few months as new cards added
	# create cards database and assign to db
	db = client.mtg
	#create card collection in mtg database
	cards = db.cards
	#add cards json from request to cards collection
	cards.insert_many(mtg_lib)
	return db.cards

def table_query_df():
	cursor = db.cards.find({}, {'name':1, 'released_at':1, 'mana_cost':1, 'cmc':1, 'type_line':1, 'power':1,'toughness':1,'set_name':1, 'rarity':1})
	cur_list = list(cursor)
	df = pd.DataFrame(cur_list)
	return df
	
def image_df(card_name)
	cursor = db.cards.find({'name':card_name},{'image_uris':1})
	cur_list = list(cursor)
	image_uri = cur_list[0]['image_uris']['normal'] 
	return image_uri
	
def startup():
	url = get_url()
	sf_lib = get_api_data(url)
	db.cards = load_data(sf_lib)
	return db.cards
	
def aggrid_interactive_table(df: pd.DataFrame):
    """Creates an st-aggrid interactive table based on a dataframe.

    Args:
        df (pd.DataFrame]): Source dataframe

    Returns:
        dict: The selected row
    """
    options = GridOptionsBuilder.from_dataframe(
        table_df, enableRowGroup=True, enableValue=True, enablePivot=True
    )

    options.configure_side_bar()
    options.configure_selection("single")
    selection = AgGrid(
        table_df,
        enable_enterprise_modules=True,
        gridOptions=options.build(),
        theme="light",
        update_mode=GridUpdateMode.MODEL_CHANGED,
        allow_unsafe_jscode=True,
    )
    return selection	

#run code for data acquisition and streamlit app

init_mongo()
db.cards = startup()

table_df = table_query_df()

selection = aggrid_interactive_table(df=table_df)

card_name = selection["selected_rows"][0]['name']

img_uri = image_df(card_name)

#aggrid returns dictionary with data and selected, selected being a list of selected rows
#i get ID of selected row, use that to get URI of image from image collection

if selection:
    #st.write("You selected:")
    #st.json(selection["selected_rows"])
    st.image(img_uri)
