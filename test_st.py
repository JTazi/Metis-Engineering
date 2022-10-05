# streamlit_app.py

import streamlit as st
import pymongo
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder
from st_aggrid.shared import GridUpdateMode

st.set_page_config(
    layout="centered", page_icon="🖱️", page_title="MTG Table App"
)
st.title("MTG Table app")
st.write(
    """This app lets you sort and filter Magic the Gathering cards while also selecting a row for additional information"""
)

st.write("Go ahead, click on a row in the table below!")

# Initialize connection.
# Uses st.experimental_singleton to only run once.
@st.experimental_singleton
def init_connection():
	#**st.secrets["mongo"]
	return pymongo.MongoClient('mongodb+srv://jtaz:mtg123!!!@mtgcluster.yrodbby.mongodb.net/?retryWrites=true&w=majority')

client = init_connection()

# Pull data from the collection.
# Uses st.experimental_memo to only rerun when the query changes or after 10 min.
@st.experimental_memo(ttl=600)
def get_table_data():
	db = client.mtg
	#'_id':0, 'name':1, 'released_at':1, 'mana_cost':1, 'cmc':1, 'type_line':1, 'power':1,'toughness':1,'set_name':1, 'rarity':1
	cursor = db.cards.find({}, {'_id':0, 'name':1, 'type_line':1})
	table_data = list(cursor)  # make hashable for st.experimental_memo
	return table_data

@st.experimental_memo(ttl=600)  
def img_uri(card_name):
	db = client.mtg
	cursor = db.cards.find({'name':card_name},{'_id':0, 'image_uris':1})
	cur_list = list(cursor)
	image_uri = cur_list[0]['image_uris']['normal'] 
	return image_uri

table_data = get_table_data()
df_table = pd.DataFrame(table_data)

def aggrid_interactive_table(df: pd.DataFrame):
    """Creates an st-aggrid interactive table based on a dataframe.
    Args:
        df (pd.DataFrame]): Source dataframe
    Returns:
        dict: The selected row
    """
    options = GridOptionsBuilder.from_dataframe(
        df, enableRowGroup=True, enableValue=True, enablePivot=True
    )

    options.configure_side_bar()

    options.configure_selection("single")
    selection = AgGrid(
        df,
        enable_enterprise_modules=True,
        gridOptions=options.build(),
        theme="alpine",
        update_mode=GridUpdateMode.MODEL_CHANGED,
        allow_unsafe_jscode=True,
    )

    return selection
  
selection = aggrid_interactive_table(df=df_table)

if selection:
	st.write("You selected:")
	#card_name = selection["selected_rows"][0]['name']
	#img_uri = img_uri(card_name)
	#st.image(img_uri)
