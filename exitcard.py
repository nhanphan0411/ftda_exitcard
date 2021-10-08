import streamlit as st
import pandas as pd

st.title('Exit Card Viewer')
df = pd.read_csv('https://docs.google.com/spreadsheets/d/e/2PACX-1vQTCLXKUQ2TMFDdDpi0sjI5J_Cpg1uU19WlV2hytSFbl81GAhDiwt82rMq7kYjSv4w3YpbYk2UQCwEI/pub?gid=1804476502&single=true&output=csv', 
                 )
col1, col2, col3 = st.beta_columns((1, 1, 1))
with col1:
    modules = ['Module 1 | SQL', 'Module 2 | Python']
    modules_ = st.multiselect('Module', modules)
with col2: 
    weeks = list(range(1, 9))
    weeks_ =st.multiselect('Week', weeks)
with col3:
    keywords = st.text_input('Keywords (separated by comma)')
    keywords_ = list(map(lambda x: x.lower().strip(), keywords.split(',')))
    keywords_ = '|'.join(keywords_)

query_df = df.copy()
if modules_ != []: 
    query_df = query_df[query_df['Module'].isin(modules_)]
if weeks_ != []:
    query_df = query_df[query_df['Week'].isin(weeks_)]
if keywords != None:
    query_df = query_df[query_df['Question'].str.lower().str.contains(keywords_) | query_df['Answer'].str.lower().str.contains(keywords_)]

st.table(query_df)

# def convert_df(df):
# # IMPORTANT: Cache the conversion to prevent computation on every rerun
#     return df.to_csv().encode('utf-8')
# csv = convert_df(query_df)

# st.download_button(label="Download data as CSV", data=csv, file_name='exitcards.csv', mime='text/csv')