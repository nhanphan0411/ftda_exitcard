import streamlit as st
import pandas as pd

teacher_path = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vQTCLXKUQ2TMFDdDpi0sjI5J_Cpg1uU19WlV2hytSFbl81GAhDiwt82rMq7kYjSv4w3YpbYk2UQCwEI/pub?gid=1804476502&single=true&output=csv'
student_path = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vQTCLXKUQ2TMFDdDpi0sjI5J_Cpg1uU19WlV2hytSFbl81GAhDiwt82rMq7kYjSv4w3YpbYk2UQCwEI/pub?gid=1265141036&single=true&output=csv'

st.set_page_config(layout="wide")
st.title('♦️ Exit Card Viewer')

st.write('All the submitted exit cards (or I may call Cards Against Memory Loss) will be collected here. Use this for your review while studying, or preparing for an interview.')
st.write('The site might be a bit slow to start. Please be patient 🥺')
mode = st.selectbox ('Choose a study mode', ["📖 Study with instructors' answers only", "✍🏼 Study your mistakes"])

def load_data(path):
    return pd.read_csv(path)

df = load_data(teacher_path)
df['Question ID'] = df['Question ID'].astype(int)

if mode == "📖 Study with instructors' answers only":
    col1, col2, col3 = st.columns((1, 1, 1))
    with col1:
        modules = ['Module 1 | SQL', 'Module 2 | Python']
        modules_ = st.multiselect('Module', modules)
    with col2: 
        weeks = list(range(1, 9))
        weeks_ =st.multiselect('Week', weeks)
    with col3:
        keywords = st.text_input('Keywords (separated by comma)')

    query_df = df.copy()
    if modules_ != []: 
        query_df = query_df[query_df['Module'].isin(modules_)]
    if weeks_ != []:
        query_df = query_df[query_df['Week'].isin(weeks_)]
    if keywords != '':
        keywords_ = list(map(lambda x: x.lower().strip(), keywords.split(',')))
        keywords_ = '|'.join(keywords_)
        query_df = query_df[query_df['Question'].str.lower().str.contains(keywords_) | query_df['Answer'].str.lower().str.contains(keywords_)]
    
    st.table(query_df)

if mode == "✍🏼 Study your mistakes":
    def load_student_data(path):
        sub = load_data(path)
        sub_ = sub.melt(id_vars=sub.columns[:5],
                        value_vars=sub.columns[5:],
                        var_name='ID',
                        value_name='Your Answer')

        sub_['Question ID'] = sub_['Question ID'].str.strip('Question ').astype('int')
        final = pd.merge(sub_, df, on=['Module', 'Week', 'Day', 'Question ID'], how='left')[['Name', 'Module', 'Week', 'Day', 'ID', 'Question', 'Your Answer', 'Answer']]
        
        final['Day'] = pd.Categorical(final['Day'], 
                                      categories=['Mon', 'Tue', 'Wed', 'Thu'],
                                      ordered=True)
        final.rename(columns={"Answer": "Instructor's Answer"}, inplace=True)
        return final
    
    final = load_student_data(student_path)

    col0, col1, col2, col3 = st.columns((2, 1, 1, 2))
    with col0: 
        name = st.selectbox('Your Name', final['Name'].unique())
    with col1:
        modules = ['Module 1 | SQL', 'Module 2 | Python']
        modules_ = st.multiselect('Module', modules)
    with col2: 
        weeks = list(range(1, 9))
        weeks_ =st.multiselect('Week', weeks)
    with col3:
        keywords = st.text_input('Keywords (separated by comma)')
    
    query_df = final.copy()
    query_df = query_df[query_df['Name']==name]

    if modules_ != []: 
        query_df = query_df[query_df['Module'].isin(modules_)]
    if weeks_ != []:
        query_df = query_df[query_df['Week'].isin(weeks_)]
    if keywords != '':
        keywords_ = list(map(lambda x: x.lower().strip(), keywords.split(',')))
        keywords_ = '|'.join(keywords_)
        query_df = query_df[query_df['Question'].str.lower().str.contains(keywords_) | query_df["Instructor's Answer"].str.lower().str.contains(keywords_)]

    st.table(query_df.sort_values(['Module', 'Week', 'Day', 'ID']))
