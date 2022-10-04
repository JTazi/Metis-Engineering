import pandas as pd
import streamlit as st
from bs4 import BeautifulSoup as bs
from pymongo import MongoClient
import requests
import re
from st_aggrid import AgGrid, GridOptionsBuilder
from st_aggrid.shared import GridUpdateMode
#is this right?
import mtg_data

init_mongo()
db.cards = startup()

table_df = table_query_df()


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



selection = aggrid_interactive_table(df=table_df)
card_name = selection["selected_rows"][0]['name']

img_uri = image_df(card_name)

#aggrid returns dictionary with data and selected, selected being a list of selected rows
#i get ID of selected row, use that to get URI of image from image collection

if selection:
    #st.write("You selected:")
    #st.json(selection["selected_rows"])
    st.image(img_uri)
