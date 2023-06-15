import streamlit as st
import seaborn as sns
from streamlit_extras.no_default_selectbox import selectbox
import pandas as pd
import matplotlib.pyplot as plt

web_apps = st.sidebar.selectbox("Select Web Apps", ["Summary","Exploratory Data Analysis"])

with st.sidebar:
    uploaded_file = st.sidebar.file_uploader("Choose a file")
    

if web_apps == "Summary":
    st.title("Hello Reader!")
    st.markdown('Welcome to my app where we can do some simple data analysis for you. Upload a file and pick a Web App to get started!')
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.markdown('Cool! You have uploaded a file! Here are some preliminary pieces of information')
        st.write("This uploaded dataset has the dimensions", df.shape,'.')
        st.write('This data set has ',df.size, 'pieces of data!')
        if df.size > 1000:
            st.markdown('*Good luck working with that lol*')
        st.markdown('**GREAT**, now let us do some analysis. From the side bar click the _Exploratory Data Analysis_ to find more information about your dataset.')

elif web_apps == "Exploratory Data Analysis":
    if uploaded_file is not None:
        #Can be used wherever a "file-line" object is accepted:
        st.title('Welcome to the EDA')
        df = pd.read_csv(uploaded_file)
        show_df = st.checkbox("Show Data Frame", key="disabled")

        if show_df:
            st.write('Here is your data!!')
            st.write(df)

        st.header('Indepth Analysis')
        st.write('Ok now lets get into the nitty gritty')
        column_type = st.selectbox('Select Data Type',
                                           ("Numerical","Categorical"))
        
        if column_type == "Numerical":
            numerical_column = st.sidebar.selectbox(
                'Select a Column', df.select_dtypes(include = ['int64','float64']).columns)

            st.write(df.describe())
            #graph
            sort_categorical = selectbox('Categorical variable to sort by',
                                                df.select_dtypes(include=['object']).columns)
            
            main_title = st.text_input('Set Title', 'Stacked Kernel density estimation')
            xtitle = st.text_input('Set x-axis Title', numerical_column)

            ax = sns.displot(df, x=numerical_column, hue = sort_categorical,kind="kde", fill = True, multiple="stack")
            ax.set(xlabel=xtitle, ylabel='Proportion')
            plt.title(main_title)

            st.pyplot(ax)
            filename = "plot.png"
            ax.savefig(filename, dpi = 300)

            with open("plot.png", "rb") as file:
                btn = st.download_button(
                    label="Download image",
                    data = file,
                    file_name = "flower.png",
                    mime="image/png"
                )
        #If the column selected is categorical, display in a table the proportions of each category level, and create a customized barplot
        if column_type == "Categorical":
            categorical_column = st.sidebar.selectbox(
                'Select a Column', df.select_dtypes(include = ['object']).columns)
            categorical_data = pd.DataFrame(df[categorical_column].value_counts())
            st.write(categorical_data)
            
            col1, col2, col3 = st.columns([3,3,2],gap="medium")
            with col1:
                chart_height = st.slider(
                    'Chart height', min_value = 100, max_value=1000, step = 10, value = 400)
            with col2:
                chart_width = st.slider(
                    'Chart Width', min_value=200, max_value=2000, step=10, value = 800)
            with col3:    
                use_container = st.checkbox('Use the container width?')
                
            st.bar_chart(categorical_data,use_container_width=use_container,height=chart_height, width=chart_width)
