from bs4 import BeautifulSoup as bs
import requests
import re
from pymongo import MongoClient

#get html code for scryfall bulk download page
bulk_url = requests.get('https://scryfall.com/docs/api/bulk-data')

#convert html to soup
soup = bs(bulk_url.content, 'html.parser')

#find URL for bulk download, two items after the table row title, "Default Cards"
link = soup.find(text = "Default Cards").next.next

#use regex to extract text between quotations. convert soup to string
url = re.findall(r'"([^"]*)"', str(link))

#https://c2.scryfall.com/file/scryfall-bulk/default-cards/default-cards-20220928210728.json
#URL for bulk download of all english MTG card objects on scryfall
bulk = requests.get(url[0])
mtg_lib = bulk.json()


#create client instance connected to mongoDB atlas cloud db
client = MongoClient('mongodb+srv://jtaz:mtg123!!!@mtgcluster.yrodbby.mongodb.net/?retryWrites=true&w=majority')
db = client.mtg

#erase old collection
cards.drop()

#create/connect card collection in mtg database
cards = db.cards

#add cards json from request to cards collection
cards.insert_many(mtg_lib)
