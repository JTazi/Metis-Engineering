# streamlit_app.py

import streamlit as st
import pymongo
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder
from st_aggrid.shared import GridUpdateMode

mana_dict = {"Red":"R", "Blue":"U", "White":"W", "Black":"B", "Green":"G", "Colorless":""}

#streamlit page config
st.set_page_config(
    layout="centered", page_icon='https://github.com/JTazi/Metis-Engineering/blob/901e6b1f820c12b29199ef635e835f4f2d395280/kisspng-magic-the-gathering-duels-of-the-planeswalker-magic-the-gathering-commander-5b1c8faf3cc9e6.955806671528598447249.png', page_title="MTG Table App"
)
st.title("MTG Table app")
st.write(
    """This app lets you sort and filter Magic the Gathering cards while also selecting a row for additional information"""
)

st.write("Go ahead, click on a row in the table below!")

#functions
# Uses st.experimental_singleton to only run once.
@st.experimental_singleton
def init_connection():
	#**st.secrets["mongo"]
	return pymongo.MongoClient('mongodb+srv://jtaz:mtg123!!!@mtgcluster.yrodbby.mongodb.net/?retryWrites=true&w=majority')

client = init_connection()

# Pull data from the collection.
# Uses st.experimental_memo to only rerun when the query changes or after 10 min.
@st.experimental_memo(ttl=1200)
def get_table_data(mana):
	db = client.mtg
	cursor = db.cards.find({'color_identity':mana_dict[mana_select]}, {'_id':0, 'name':1, 'cmc':1, 'type_line':1, 'power':1,'toughness':1,'set_name':1, 'rarity':1})
	table_data = list(cursor)  # make hashable for st.experimental_memo
	return table_data

@st.experimental_memo(ttl=600)  
def img_uri(card_name):
	db = client.mtg
	cursor = db.cards.find({'name':card_name},{'_id':0, 'image_uris':1})
	cur_list = list(cursor)
	image_uri = cur_list[0]['image_uris']['normal'] 
	return image_uri

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

#app code
# USer input on sidebar
mana_select = st.sidebar.selectbox(
    "What color mana do you want to see?",
    ("Red", "Blue", "White", "Black", "Green", "Colorless")
)	

table_data = get_table_data(mana_select)
df_table = pd.DataFrame(table_data)
		
selection = aggrid_interactive_table(df=df_table)

if selection:
	st.write("You selected:")
	card_name = selection["selected_rows"][0]['name']
	img_uri = img_uri(card_name)
	st.image(img_uri)
