import streamlit as st
import pandas as pd
import os
from io import BytesIO

st.set_page_config(page_title="Data Sweeper",layout='wide')

#title and description
st.title("Data Sweeper")
st.write("Transform your files between CSV and Sxcel formats with built-in data cleaning and visuallization Creating the project for quater 3")

#file uploader
uploaded_file = st.file_uploader("uploaded your files (accepts CSV or Excel):", type=["csv","xlsx"], accept_multiple_files=(True))

if uploaded_file:
    for file in uploaded_file:
        file_ext = os.path.splitext(file.name)[-1].lower()
        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"unsupported file type: {file_ext}")
            continue  

        #file detail
         
        st.write("Preview the head of the Dataframe")
        st.dataframe(df.head())   

        #data cleaning options
        st.subheader("Data Cleaning Options")
        if st.checkbox(f"Clean data for{file.name}"):
            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"Remove duplicates from the file : {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.write("Duplicates removed!")  

            with col2:
                if st.button(f"Fill missing value for {file.name}"):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())        
                    st.write("Missing value have been filled!")

        st.subheader("Select Columns to Keep")  
        columns = st.multiselect(f"Choose colums for {file.name}",df.columns, default=df.columns)
        df = df[columns]

        #data visualization
        st.subheader("Data Visualization")
        if st.checkbox(f"Show Visualization for {file.name}"):
            st.bar_chart(df.select_dtypes(include='number').iloc[:, :2])

        #convertion options
        st.subheader("Covertion Optiona")
        convertion_type = st.radio(f"Convert {file.name} to:", ["csv" , "Excel"],key=file.name )
        if st.button(f"Convert{file.name}"):
            buffer = BytesIO()
            if convertion_type == "csv":
                df.to_csv(buffer, index=False)
                file_name = file.name.replace(file_ext, ".csv")
                mine_type = "text/csv"

            elif convertion_type == "Excel":
                df.to_excel(buffer, index=False)
                file_name = file.name.replace(file_ext, ".xlsx")
                mine_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"    
            buffer.seek(0)

            st.download_button(
                label=f"Download {file.name} as {convertion_type}",
                data=buffer,
                file_name=file_name,
                mime=mine_type
            )    

st.success("All file processed successfully!")            



