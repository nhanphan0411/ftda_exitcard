from tkinter import NONE
import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")
st.title('✍🏼 Exit Card Viewer')

# ----- COHORT INFORMATION -----
# teacher_path: path to the google sheet of teacher's answers
# student_path: path to the google sheet of student's submissions
# To get the linke, on Google Sheet, go to File - Share - Publish to Web, and publish each sheet separately  
cohort_info = {"SOUTH SANDWICH": {'teacher_path': 'https://docs.google.com/spreadsheets/d/e/2PACX-1vSXDs6_lRFR96clhKRa-D3a3wX1qTP2DCEzDX4P8-bS4kwu9ldyqIJQC3UTHJ5F4vSNhyjAJMjHGTgf/pub?gid=1724394138&single=true&output=csv',
                                  'student_path': 'https://docs.google.com/spreadsheets/d/e/2PACX-1vSXDs6_lRFR96clhKRa-D3a3wX1qTP2DCEzDX4P8-bS4kwu9ldyqIJQC3UTHJ5F4vSNhyjAJMjHGTgf/pub?gid=648124414&single=true&output=csv',
                                  'student_id_path': 'https://docs.google.com/spreadsheets/d/e/2PACX-1vQ5spaMba1n1-NjaUFGB_QJQW4vzGfwFrIcOtKDn3pUbOh8ZgRh2Kj6OxMrv5De9FeaFIC9Kce0zOqB/pub?gid=1980741304&single=true&output=csv'},
               "FTDS-1": {'teacher_path': 'https://docs.google.com/spreadsheets/d/e/2PACX-1vQTCLXKUQ2TMFDdDpi0sjI5J_Cpg1uU19WlV2hytSFbl81GAhDiwt82rMq7kYjSv4w3YpbYk2UQCwEI/pub?gid=1804476502&single=true&output=csv',
                          'student_path': 'https://docs.google.com/spreadsheets/d/e/2PACX-1vQTCLXKUQ2TMFDdDpi0sjI5J_Cpg1uU19WlV2hytSFbl81GAhDiwt82rMq7kYjSv4w3YpbYk2UQCwEI/pub?gid=1265141036&single=true&output=csv',
                          'student_id_path': 'https://docs.google.com/spreadsheets/d/e/2PACX-1vSzVO404kgSELEVmQuwrhk7ewMhNMAHV9ruE7T-9wY9CTdfvyc56pDhNL8LoP60L7Tid5JhvKFXRmB4/pub?gid=1333273843&single=true&output=csv'},
               "FTDS-2": {'teacher_path': 'https://docs.google.com/spreadsheets/d/e/2PACX-1vT8Efm2EghlRA4_86rQ0xsS7IjL6NF4uXAQQY7yzP3XZHIm-88GhvQ32prWAq48MY5fLJc0YiEWP0sO/pub?gid=19745885&single=true&output=csv',
                          'student_path': 'https://docs.google.com/spreadsheets/d/e/2PACX-1vT8Efm2EghlRA4_86rQ0xsS7IjL6NF4uXAQQY7yzP3XZHIm-88GhvQ32prWAq48MY5fLJc0YiEWP0sO/pub?gid=791858605&single=true&output=csv',
                          'student_id_path': 'https://docs.google.com/spreadsheets/d/e/2PACX-1vTqEfaWeSwxaiS8v1fqjF7Acctu0nvdG-IWeBLQeWaZJxgeSBV-dqHV7LOEqtNYVIKsqTPTBZpHJWa-/pub?gid=638124590&single=true&output=csv'}
              }


cohort = st.sidebar.selectbox('CHOOSE COHORT', ["--- Choose a Course ---", "SOUTH SANDWICH", "FTDS-1", "FTDS-2"])

if cohort == "--- Choose a Course ---":
    st.markdown('*Please specify your course*')

else: 
    teacher_path = cohort_info[cohort]['teacher_path']
    student_path = cohort_info[cohort]['student_path']
    
    student_id_path = cohort_info[cohort]['student_id_path']
    student_list = pd.read_csv(student_id_path).set_index('cohortMemberId')

    weeks = list(range(1, 10))
    weeks_ = st.sidebar.multiselect('CHOOSE WEEK', weeks)
    keywords = st.sidebar.text_input('SEARCH BY KEYWORDS (separated by comma)')

    # ------ GET TEACHER'S ANSWERS ------
    df = pd.read_csv(teacher_path)
    df[['Week', 'ID']] = df[['Week', 'ID']].astype(int)

    # ------ GET STUDENT'S ANSWERS ------
    def load_student_data(path):
        data = pd.read_csv(path)

        # From FTDS-2, start using email instead of name like previous cohort 
        # Extract name from email 
        if 'Name' not in data.columns:
            name_dict = student_list.set_index('email')
            data['Name'] = data['Email Address'].apply(lambda x: name_dict.loc[x, 'name'])
            data = data.loc[:, ['Timestamp', 'Name', 'Week', 'Day', 'Question 1', 'Question 2', 'Question 3', 'Question 4', 'Question 5', 'Question 6']]
        
        # Transform student table 
        data_ = data.melt(id_vars=data.columns[:4],
                        value_vars=data.columns[4:],
                        var_name='ID',
                        value_name='Your Answer')
        data_['ID'] = data_['ID'].str.strip('Question ')
        data_[['Week', 'ID']] = data_[['Week', 'ID']].astype('int')
        final = pd.merge(data_, df, on=['Week', 'Day', 'ID'], how='left')[['Name', 'Week', 'Day', 'ID', 'Question', 'Your Answer', 'Answer']]
        final['Day'] = pd.Categorical(final['Day'], categories=['Mon', 'Tue', 'Wed', 'Thu', 'Fri'], ordered=True)
        final.rename(columns={"Answer": "Instructor's Answer"}, inplace=True)
        return final
    
    query_df = load_student_data(student_path)

    col1, col2 = st.columns((2, 1))
    with col1: 
        name_id = st.text_input('INPUT YOUR STUDENT ID - for example: 614c3b0b8406f200212b947').strip()
    
    if name_id in student_list.index:
        name = student_list.loc[name_id, 'name']
        st.markdown(f'🙌🏻 {name}')

        query_df = query_df[query_df['Name']==name]

        if weeks_ != []:
            query_df = query_df[query_df['Week'].isin(weeks_)]
        if keywords != '':
            keywords_ = list(map(lambda x: x.lower().strip(), keywords.split(',')))
            keywords_ = '|'.join(keywords_)
            query_df = query_df[query_df['Question'].str.lower().str.contains(keywords_) | query_df["Instructor's Answer"].str.lower().str.contains(keywords_)]
        
        st.table(query_df.iloc[:, 1:].sort_values(['Week', 'Day', 'ID']).reset_index(drop=True).dropna())
    
    elif name_id != '' and name_id not in student_list.index:
        st.markdown('*Your Student ID is not correct.*')

        
