from bs4 import BeautifulSoup as bs
from pymongo import MongoClient
import pandas as pd
import requests
import re

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
	cursor = db.cards.find({}, {'name':1, 'released_at':1, 'mana_cost':1, 'cmc':1,'type_line':1,'power':1,'toughness':1,'set_name':1, 'rarity':1})
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
