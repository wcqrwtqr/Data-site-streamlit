import pandas as pd
import streamlit as st
import plotly.express as px
# import matplotlib.pyplot as plt
import numpy as np


def Sales_Data(source_file, sheet_name='data', column='A:I'):
    df = pd.read_excel(source_file, sheet_name='data', usecols='A:I')
    df.dropna(inplace=True)
    df['Sale'] = df['Price']*df['Qty']
    df['Profit'] = df['Sale']*df['Margin']/100
# Masks
    genders = ['Male', 'Female']
    products = df['Product'].unique().tolist()
    country = df['Country'].unique().tolist()
    ages = df['Client Age'].unique().tolist()
# webpage selections
    age_selection = st.slider('Age:', min_value=min(ages), max_value=max(ages), value=(min(ages), max(ages)))
    product_selection = st.multiselect('product:', products, default=products)
    country_selection = st.multiselect('Countries:', country, default=country)
    gender_selection = st.multiselect('Gender', genders, default=genders)
# mask
    # gender_mask = df['Gender'].isin(gender_selection)
    # product_mask = df['Product'].isin(product_selection)
    # country_mask = df['Country'].isin(country_selection)
    # age_mask = df['Client Age'].between(*age_selection)
# product_mask = df['Product'].isin(['A'])
    masked_df = (df['Gender'].isin(gender_selection) & df['Product'].isin(product_selection) & df['Client Age'].between(*age_selection) & df['Country'].isin(country_selection) )
    number_of_results = df[masked_df].shape[0]
    pivot_profit_df = df[masked_df].groupby(["Country", "Product"])[['Profit', 'Sale']].sum()
    pivot_count_df = df[masked_df].groupby(["Country", "Product"])[['Gender']].count()
# Draw the tables on the screen 
    st.markdown(f'*Available Results: {number_of_results}')
    st.dataframe(df[masked_df])
    col1, col2 = st.beta_columns(2)
    col1.dataframe(pivot_profit_df)
    col2.dataframe(pivot_count_df)

# ====================================================================

def Gauges_data(source_file, row=10):
    df = pd.read_csv(source_file, sep=',', header=None, skiprows=row
                     , names=['date', 'time', 'pm', 'elapse', 'pressure',
                     'temperature'])
    range_data = df['elapse'].unique().tolist()
    range_data_selection = st.slider('Range:', min_value=min(range_data),
                                     max_value=max(range_data),
                                     value=(min(range_data), max(range_data)))
    range_mask = df['elapse'].between(*range_data_selection)
    df_lst = df[range_mask]
    fig1 = px.scatter(df_lst['pressure'])
    fig2 = px.scatter(df_lst['temperature'])
    st.markdown(f'*Available Data: {df_lst.shape[0]}')
    st.plotly_chart(fig2)
    st.plotly_chart(fig1)
    st.dataframe(df_lst)
    st.markdown(f'*Available Data: {df_lst.shape[0]}')

# ====================================================================

def MPFM_data(source_file):
    df = pd.read_csv(source_file, sep='\t')
    df.dropna(inplace=True, axis=1)
    # Masking
    range_data = df.index.tolist()
    range_data_selection = st.slider('Range:', min_value=min(range_data),
                                     max_value=max(range_data),
                                     value=(min(range_data), max(range_data)))
    df_lst = df[range_data_selection[0]:range_data_selection[1]]
    # Averages calculation
    avg_P =             np.average(df_lst['Pressure'])
    avg_T =             np.average(df_lst['Temperature'])
    avg_dP =            np.average(df_lst['dP'])
    avg_oilRate =       np.average(df_lst['Std.OilFlowrate'])
    avg_waterRate =     np.average(df_lst['WaterFlowrate'])
    avg_std_gasRate =   np.average(df_lst['Std.GasFlowrate'])
    avg_act_gasRate =   np.average(df_lst['Act.GasFlowrate'])
    avg_GOR =           np.average(df_lst['GOR(std)'])
    avg_WC =            np.average(df_lst['Std.Watercut'])
    avg_oilSG =         np.average(df_lst['OilDensity'])
    avg_waterSG =       np.average(df_lst['WaterDensity'])
    avg_gasSG =         np.average(df_lst['GasDensity'])
    avg_liquid =        avg_oilRate + avg_waterRate
    API =               (141.5/(avg_oilSG/1000) - 131.5)
    start = df_lst['Clock'][range_data_selection[0]] + ' ' + df_lst['Date'][range_data_selection[0]]
    end = df_lst['Clock'][range_data_selection[1]-1] + ' ' + df_lst['Date'][range_data_selection[1]-1]
    # Making the dataframe
    dict_summary = {'Start Time': start,
                    'End Time': end, 'WHP': avg_P, 'WHT': avg_T,
                    'Diff dP': avg_dP, 'Oil Rate': avg_oilRate, 'Water Rate': avg_waterRate,
                    'Liquid Rate': avg_liquid, 'Gas Rate': avg_std_gasRate,
                    'Actual Gas Rate': avg_act_gasRate, 'Total GOR': avg_GOR,
                    'Gas SG': avg_gasSG, 'Oil SG': avg_oilSG, 'Oil API': API,
                    'BSW': avg_WC, 'Water SG' : avg_waterSG}
    summary = pd.DataFrame([dict_summary])
    # fig1 = px.scatter(df['Pressure'])
    fig1 = px.scatter(df_lst['Pressure'])
    st.markdown(f'*Available Data: {df_lst.shape[0]}')
    st.dataframe(df_lst)
    st.markdown('Summary')
    st.dataframe(summary)
    st.plotly_chart(fig1)





