import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")
st.title('✍🏼 Exit Card Viewer')

# st.write('All the submitted exit cards (or I may call Cards Against Memory Loss) will be collected here. Use this for your review while studying, or preparing for an interview. The site might be a bit slow to start. Please be patient 🥺')
# mode = st.selectbox ('Choose a study mode', ["📖 Study with instructors' answers only", "✍🏼 Study your mistakes"])
cohort = st.sidebar.selectbox('', ["--- Choose a Course ---", "SOUTH SANDWICH", "FULL-TIME DATA SCIENCE"])

if cohort == "--- Choose a Course ---":
    st.markdown('*Please specify your course*')

else: 
    if cohort == "SOUTH SANDWICH":
        teacher_path = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vSXDs6_lRFR96clhKRa-D3a3wX1qTP2DCEzDX4P8-bS4kwu9ldyqIJQC3UTHJ5F4vSNhyjAJMjHGTgf/pub?gid=1724394138&single=true&output=csv'
        student_path = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vSXDs6_lRFR96clhKRa-D3a3wX1qTP2DCEzDX4P8-bS4kwu9ldyqIJQC3UTHJ5F4vSNhyjAJMjHGTgf/pub?gid=648124414&single=true&output=csv'
        student_list = {'614c3afc8570b1001f6aca3d':'Phạm Thị Thu Huyền',
                '614c3afd8406f200212b9ecd':'Tô Minh Hằng',
                '614c3aff8406f200212b9ed1':'Hà Lê',
                '614c3b008406f200212b9ed5':'Nguyễn Cửu Quỳnh Vy',
                '614c3b018406f200212b9ed9':'Trịnh Nguyễn Thảo Nguyên',
                '614c3b028406f200212b9edd':'Nguyễn Hà Yên',
                '614c3b038406f200212b9ee1':'Trương Hoàng Đông',
                '614c3b048406f200212b9ee5':'Nguyễn Thị Thanh Ngọc',
                '614c3b058406f200212b9ee9':'Vũ Thị Kim Hương',
                '614c3b068406f200212b9eed':'Vũ Thị Hương Ly',
                '614c3b078406f200212b9ef1':'Nguyễn Đức Anh',
                '614c3b088406f200212b9ef5':'Trần Đức Hiệp',
                '614c3b098406f200212b9ef9':'Đặng Diệu Thạch Thảo',
                '614c3b0a8406f200212b9efd':'Phan Công Hội',
                '614c3b0b8406f200212b9f01':'Nguyễn Hoàng Đỗ Quyên',
                '614c3b0c8406f200212b9f05':'Lê Huy Vỹ',
                '614c3b0e8406f200212b9f09':'Trần Thị Li Li',
                '6151511994a921001fca057b':'Dương Hoàng Yến'}
    
    elif cohort == "FULL-TIME DATA SCIENCE":
        teacher_path = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vQTCLXKUQ2TMFDdDpi0sjI5J_Cpg1uU19WlV2hytSFbl81GAhDiwt82rMq7kYjSv4w3YpbYk2UQCwEI/pub?gid=1804476502&single=true&output=csv'
        student_path ='https://docs.google.com/spreadsheets/d/e/2PACX-1vQTCLXKUQ2TMFDdDpi0sjI5J_Cpg1uU19WlV2hytSFbl81GAhDiwt82rMq7kYjSv4w3YpbYk2UQCwEI/pub?gid=1265141036&single=true&output=csv'
        student_list = {"618c9eaff63bc8001f0faa08": "Trang Thanh Le",
                        "618c9eb0f63bc8001f0faa0a": "Nguyễn Thị Bích Trân",
                        "618c9eb0f63bc8001f0faa0c": "Lý Công Thành",
                        "618c9eb1f63bc8001f0faa0e": "Nguyễn Cửu Quỳnh Vy",
                        "618c9eb1f63bc8001f0faa10": "Vũ Thị Hương Ly",
                        "618c9eb1f63bc8001f0faa12": "Âu Trường Hi",
                        "618c9eb2f63bc8001f0faa14": "Nguyễn Ngọc Hoài Nguyễn",
                        "618c9eb2f63bc8001f0faa16": "Bùi Thị Thanh Thủy",
                        "618c9eb3f63bc8001f0faa18": "Đào Phương Thế Luân",
                        "618c9eb3f63bc8001f0faa1a": "Nguyen Tien Dung",
                        "618c9eb4f63bc8001f0faa1c": "Đinh Thị Thu Hà",
                        "618c9eb4f63bc8001f0faa1e": "Lâm Minh Hoa",
                        "618c9eb5f63bc8001f0faa20": "Nguyễn Minh Trí",
                        "618c9eb5f63bc8001f0faa22": "Huỳnh Dương Mỹ Hương",
                        "618c9eb5f63bc8001f0faa24": "Phan Hạ Uyên",
                        "6195f9a6295c9b001fd74084": "Duy Nghi"}

    mode = st.sidebar.selectbox('CHOOSE STUDY MODE', ["📖 Study with instructors' answers only", "✍🏼 Study your mistakes"])

    def load_data(path):
        return pd.read_csv(path)

    df = load_data(teacher_path)
    df[['Week', 'ID']] = df[['Week', 'ID']].astype(int)

    if mode == "📖 Study with instructors' answers only":
        col1, col2 = st.columns((1, 2))
        with col1: 
            weeks = list(range(1, 9))
            weeks_ = st.sidebar.multiselect('CHOOSE WEEK', weeks)
        with col2:
            keywords = st.sidebar.text_input('SEARCH BY KEYWORDS (separated by comma)')

        query_df = df.copy()
        if weeks_ != []:
            query_df = query_df[query_df['Week'].isin(weeks_)]
        if keywords != '':
            keywords_ = list(map(lambda x: x.lower().strip(), keywords.split(',')))
            keywords_ = '|'.join(keywords_)
            query_df = query_df[query_df['Question'].str.lower().str.contains(keywords_) | query_df['Answer'].str.lower().str.contains(keywords_)]
        
        st.table(query_df)

    if mode == "✍🏼 Study your mistakes":
        weeks = list(range(1, 10))
        weeks_ = st.sidebar.multiselect('CHOOSE WEEK', weeks)
        keywords = st.sidebar.text_input('SEARCH BY KEYWORDS (separated by comma)')

        def load_student_data(path):
            sub = load_data(path)
    
            sub_ = sub.melt(id_vars=sub.columns[:4],
                            value_vars=sub.columns[4:],
                            var_name='ID',
                            value_name='Your Answer')

            sub_['ID'] = sub_['ID'].str.strip('Question ')
            sub_[['Week', 'ID']] = sub_[['Week', 'ID']].astype('int')
            final = pd.merge(sub_, df, on=['Week', 'Day', 'ID'], how='left')[['Name', 'Week', 'Day', 'ID', 'Question', 'Your Answer', 'Answer']]
            
            final['Day'] = pd.Categorical(final['Day'], categories=['Mon', 'Tue', 'Wed', 'Thu', 'Fri'], ordered=True)
            final.rename(columns={"Answer": "Instructor's Answer"}, inplace=True)
            return final
        
        final = load_student_data(student_path)

        col1, col2 = st.columns((2, 1))
        with col1: 
            name_id = st.text_input('INPUT YOUR STUDENT ID - for example: 614c3b0b8406f200212b947').strip()
        if name_id in student_list.keys():
            st.markdown(f'🙌🏻 {student_list[name_id]}')
    
        query_df = final.copy()
        if name_id in student_list.keys(): 
            name = student_list[name_id]
            query_df = query_df[query_df['Name']==name]
            if weeks_ != []:
                query_df = query_df[query_df['Week'].isin(weeks_)]
            if keywords != '':
                keywords_ = list(map(lambda x: x.lower().strip(), keywords.split(',')))
                keywords_ = '|'.join(keywords_)
                query_df = query_df[query_df['Question'].str.lower().str.contains(keywords_) | query_df["Instructor's Answer"].str.lower().str.contains(keywords_)]
            st.table(query_df.iloc[:, 1:].sort_values(['Week', 'Day', 'ID']).reset_index(drop=True))
        else: 
            st.markdown('*Please input a correct ID*')

        
