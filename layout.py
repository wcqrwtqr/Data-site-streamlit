import streamlit as st
import os
from helper import Sales_Data, Gauges_data, MPFM_data
from PIL import Image

st.set_page_config(page_title='Data analysis page', layout='wide')
st.title('Data Playground Web Page')
values = ['Choose Data','Sales Data', 'Gauges Data', 'MPFM Data']
default_ix = values.index('Choose Data')
window_ANTICOR = st.sidebar.selectbox('Selection Window', values, index=default_ix)

package_dir = os.path.dirname(os.path.abspath(__file__))
if window_ANTICOR == 'Choose Data':
    st.title('👈🏼 Choose data from menu bar')
    image = Image.open(os.path.join( package_dir,'Thumbnail/youtube.jpg'))
    st.subheader('About the website:')
    st.write('Select data type from the list to the side and explore who they change with built in handles All data are dummy data and there is several data in each page')
    st.write("You can find the data disused in my youtube channel and I've added the ")
    st.image(image, caption = 'youtube channel')

# Gauges
if window_ANTICOR == 'Gauges Data':
    values = ['Data 1', 'Data 2', 'Data 3', 'Data 4', 'Data 5', 'Data 6']
    default_ix = values.index('Data 1')
    x = st.selectbox('Select Different Data', values, index=default_ix)
    source_data = os.path.join(package_dir, f'Data/Gauges Data {values.index(x)}.txt')
    try:
        st.title('Down Hole Gauges Data')
        st.text('***Dummy Data only***')
        Gauges_data(source_data)
        col1, col2 = st.beta_columns(2)
        image = Image.open(os.path.join(package_dir,'Thumbnail/Gauges data thumbnail.jpg'))
        col1.image(image, caption='youtube', width=100)
        col2.markdown('See my youtube on this data: https://youtu.be/C6oz96OLCCg')
    except Exception:
        st.title('No Data available!!')
        st.subheader('Select previous data')

# Sales
if window_ANTICOR == 'Sales Data':
    source_data = os.path.join(package_dir, 'Data/Sales Data.xlsx')
    st.title('Sales Data')
    st.text('***Dummy Data only***')
    Sales_Data(source_data)
    col1, col2 = st.beta_columns(2)
    image = Image.open(os.path.join(package_dir,'Thumbnail/Pivot table thumbnail.jpg'))
    col1.image(image, caption='youtube', width=100)
    col2.markdown('See my youtube on this data:https://youtu.be/sctzeSaUL2')

# MPFM
if window_ANTICOR == 'MPFM Data':
    # selecting different files from a select box
    values = ['Data 1', 'Data 2', 'Data 3', 'Data 4', 'Data 5', 'Data 6', 'Data 7','Data 8' ]
    default_ix = values.index('Data 1')
    x = st.selectbox('Select Different Data' ,values, index=default_ix)
    source_data = os.path.join(package_dir, f'Data/MPFM Data {values.index(x)}.txt')
    try:
        st.title('Multiphase Meter Data')
        st.text('***Dummy Data only***')
        MPFM_data(source_data)
        col1, col2 = st.beta_columns(2)
        image = Image.open(os.path.join(package_dir,'Thumbnail/MPFM data thumbnail.jpg'))
        col1.image(image, caption='youtube', width=100)
        col2.markdown('See my youtube on this data:https://youtu.be/sctzeSaUL2c')
    except Exception:
        st.title('No Data available!!')
        st.subheader('Select previous data')




