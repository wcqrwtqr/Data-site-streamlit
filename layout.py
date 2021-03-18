import streamlit as st
import os
from helper import Sales_Data, Gauges_data, MPFM_data


st.set_page_config(page_title='Data analysis page')
st.header('Data Playground Web Page')
values = ['Choose Data','Sales Data', 'Gauges Data', 'MPFM Data']
default_ix = values.index('Choose Data')
window_ANTICOR = st.sidebar.selectbox('Selection Window', values, index=default_ix)

package_dir = os.path.dirname(os.path.abspath(__file__))
if window_ANTICOR == 'Choose Data':
    st.title('👈🏼 Choose data from menu bar')


if window_ANTICOR == 'Gauges Data':
    source_data = os.path.join(package_dir, 'Data/Gauges Data.txt')
    # st.subheader('Down Hole Gauges Data')
    st.text('***Dummy Data only***')
    Gauges_data(source_data)
    st.stop()

if window_ANTICOR == 'Sales Data':
    source_data = os.path.join(package_dir, 'Data/Sales Data.xlsx')
    # st.subheader('Marketing and Sales data')
    st.text('***Dummy Data only***')
    Sales_Data(source_data)
    st.stop()

if window_ANTICOR == 'MPFM Data':
    source_data = os.path.join(package_dir, 'Data/MPFM Data.txt')
    st.text('***Dummy Data only***')
    # st.subheader('Multi Phase Meter Data')
    MPFM_data(source_data)
    st.stop()


# bar_chart = px.bar(pivot_df, x='Profit', y='Sale', text='Sale',
#                    color_discrete_sequence=['#F63366']*len(pivot_df),
#                    template='plotly_white')
# st.plotly_chart(bar_chart)


