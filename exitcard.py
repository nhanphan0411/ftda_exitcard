import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")
st.title('✍🏼 Exit Card Viewer')

# st.write('All the submitted exit cards (or I may call Cards Against Memory Loss) will be collected here. Use this for your review while studying, or preparing for an interview. The site might be a bit slow to start. Please be patient 🥺')
# mode = st.selectbox ('Choose a study mode', ["📖 Study with instructors' answers only", "✍🏼 Study your mistakes"])
cohort = st.sidebar.selectbox('', ["--- Choose a Course ---", "SOUTH SANDWICH", "FTDA"])

if cohort == "--- Choose a Course ---":
    st.markdown('*Please specify your course*')

else: 
    mode = st.sidebar.selectbox('CHOOSE STUDY MODE', ["📖 Study with instructors' answers only", "✍🏼 Study your mistakes"])
    if cohort == "SOUTH SANDWICH":
        teacher_path = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vSXDs6_lRFR96clhKRa-D3a3wX1qTP2DCEzDX4P8-bS4kwu9ldyqIJQC3UTHJ5F4vSNhyjAJMjHGTgf/pub?gid=1724394138&single=true&output=csv'
        student_path = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vSXDs6_lRFR96clhKRa-D3a3wX1qTP2DCEzDX4P8-bS4kwu9ldyqIJQC3UTHJ5F4vSNhyjAJMjHGTgf/pub?gid=648124414&single=true&output=csv'
    elif cohort == "FTDA":
        teacher_path = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vQTCLXKUQ2TMFDdDpi0sjI5J_Cpg1uU19WlV2hytSFbl81GAhDiwt82rMq7kYjSv4w3YpbYk2UQCwEI/pub?gid=1804476502&single=true&output=csv'
        student_path='https://docs.google.com/spreadsheets/d/e/2PACX-1vQTCLXKUQ2TMFDdDpi0sjI5J_Cpg1uU19WlV2hytSFbl81GAhDiwt82rMq7kYjSv4w3YpbYk2UQCwEI/pub?gid=1265141036&single=true&output=csv'

    def load_data(path):
        return pd.read_csv(path)

    df = load_data(teacher_path)
    df[['Week', 'ID']] = df[['Week', 'ID']].astype(int)

    if mode == "📖 Study with instructors' answers only":
        col1, col2 = st.columns((1, 2))
        # with col1:
        #     modules = ['Module 1 | SQL', 'Module 2 | Python']
        #     modules_ = st.multiselect('Module', modules)
        with col1: 
            weeks = list(range(1, 9))
            weeks_ = st.sidebar.multiselect('CHOOSE WEEK', weeks)
        with col2:
            keywords = st.sidebar.text_input('SEARCH BY KEYWORDS (separated by comma)')

        query_df = df.copy()
        # if modules_ != []: 
        #     query_df = query_df[query_df['Module'].isin(modules_)]
        if weeks_ != []:
            query_df = query_df[query_df['Week'].isin(weeks_)]
        if keywords != '':
            keywords_ = list(map(lambda x: x.lower().strip(), keywords.split(',')))
            keywords_ = '|'.join(keywords_)
            query_df = query_df[query_df['Question'].str.lower().str.contains(keywords_) | query_df['Answer'].str.lower().str.contains(keywords_)]
        
        st.table(query_df)

    if mode == "✍🏼 Study your mistakes":
        print(df.info())
        def load_student_data(path):
            sub = load_data(path)
    
            sub_ = sub.melt(id_vars=sub.columns[:4],
                            value_vars=sub.columns[4:],
                            var_name='ID',
                            value_name='Your Answer')

            sub_['ID'] = sub_['ID'].str.strip('Question ')
            sub_[['Week', 'ID']] = sub_[['Week', 'ID']].astype('int')
            # final = pd.merge(sub_, df, on=['Module', 'Week', 'Day', 'ID'], how='left')[['Name', 'Module', 'Week', 'Day', 'ID', 'Question', 'Your Answer', 'Answer']]
            final = pd.merge(sub_, df, on=['Week', 'Day', 'ID'], how='left')[['Name', 'Week', 'Day', 'ID', 'Question', 'Your Answer', 'Answer']]
            
            final['Day'] = pd.Categorical(final['Day'], categories=['Mon', 'Tue', 'Wed', 'Thu'], ordered=True)
            final.rename(columns={"Answer": "Instructor's Answer"}, inplace=True)
            return final
        
        final = load_student_data(student_path)

        col1, col2, col3 = st.columns((1, 1, 2))
        with col1: 
            name = st.sidebar.selectbox('YOUR NAME', final['Name'].unique())
        # with col1:
        #     modules = ['Module 1 | SQL', 'Module 2 | Python']
        #     modules_ = st.multiselect('Module', modules)
        with col2: 
            weeks = list(range(3, 10))
            weeks_ = st.sidebar.multiselect('CHOOSE WEEK', weeks)
        with col3:
            keywords = st.sidebar.text_input('SEARCH BY KEYWORDS (separated by comma)')
        
        query_df = final.copy()
        query_df = query_df[query_df['Name']==name]

        # if modules_ != []: 
        #     query_df = query_df[query_df['Module'].isin(modules_)]
        if weeks_ != []:
            query_df = query_df[query_df['Week'].isin(weeks_)]
        if keywords != '':
            keywords_ = list(map(lambda x: x.lower().strip(), keywords.split(',')))
            keywords_ = '|'.join(keywords_)
            query_df = query_df[query_df['Question'].str.lower().str.contains(keywords_) | query_df["Instructor's Answer"].str.lower().str.contains(keywords_)]

        # st.table(query_df.sort_values(['Module', 'Week', 'Day', 'ID']))
        st.table(query_df.iloc[:, 1:].sort_values(['Week', 'Day', 'ID']).reset_index(drop=True))
