import pandas as pd
import streamlit as st
import numpy as np
from graphing import graphing_line_2v, graphing_line_1v


# Helper function 
def check_if_string_in_file(file_name, string_to_search):

    """ Check if any line in the file contains given string """
    # Open the file in read only mode
    with open(file_name, 'r') as read_obj:
        # Read all lines in the file one by one
        for line in read_obj:
            # For each line, check if line contains the string
            if string_to_search in line:
                return True
    return False

# ********************************************************************
# *************** Sales Function ************************************
# ********************************************************************
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
    col1, col2 = st.beta_columns(2)
    product_selection = col1.multiselect('product:', products, default=products)
    gender_selection = col2.multiselect('Gender', genders, default=genders)
    country_selection = st.multiselect('Countries:', country, default=country)
    masked_df = (df['Gender'].isin(gender_selection) & df['Product'].isin(product_selection) & df['Client Age'].between(*age_selection) & df['Country'].isin(country_selection) )
    number_of_results = df[masked_df].shape[0]

    # Pivot table creation 
    pivot_profit_df = df[masked_df].groupby(["Country", "Product"])[['Profit', 'Sale']].sum()
    pivot_count_df = df[masked_df].groupby(["Country", "Product"])[['Gender']].count()
# Draw the tables on the screen 
    st.markdown(f'*Available Results: {number_of_results}')
    with st.beta_expander(label='Data Table'):
        st.dataframe(df[masked_df])
# Pivot table using groupby in pandas 
    with st.beta_expander(label='Pivot Tables'):
        col1, col2 = st.beta_columns(2)
        col1.dataframe(pivot_profit_df)
        col2.dataframe(pivot_count_df)

# ********************************************************************
# *************** Gauges Function ************************************
# ********************************************************************

def Gauges_data(source_file, row=10):

    # Check if the data comma separated or not
    if check_if_string_in_file(source_file,  ','):
        sep = ','
    else:
        sep = '\t'

    df = pd.read_csv(source_file, sep=sep, header=None, skiprows=row
                     , names=['date', 'time', 'pressure', 'temperature'])
    df['date_time'] = df['date'] + " " + df['time']
    range_data = df.index.tolist()
    range_data_selection = st.slider('Range:', min_value=min(range_data),
                                     max_value=max(range_data),
                                     value=(min(range_data), max(range_data)))
    # Creating the masked df from the index
    df_lst = df[range_data_selection[0]:range_data_selection[1]]
    dx = graphing_line_2v(df_lst, 'date_time', 'pressure', 'temperature')
    # Showing the graphs 
    st.markdown(f'*Available Data: {df_lst.shape[0]}')
    st.markdown('Pressure Temperature Graph')

    with st.beta_expander(label='Table of Data'):
        st.markdown('Full Data Table')
        st.dataframe(df_lst)
    with st.beta_expander(label='Gauges Chart'):
        st.plotly_chart(dx)
    st.markdown(f'*Available Data: {df_lst.shape[0]}')

# ********************************************************************
# ************** MPFM Function ***************************************
# ********************************************************************

def MPFM_data(source_file):
    df = pd.read_csv(source_file, sep='\t')
    df.dropna(inplace=True, axis=1)
    # Masking
    range_data = df.index.tolist()
    range_data_selection = st.slider('Range:', min_value=min(range_data),
                                     max_value=max(range_data),
                                     value=(min(range_data), max(range_data)))
    # Creating the masked df from the index
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

    # Making the graphs
    ptd = graphing_line_2v(df_lst, 'Clock', 'Pressure', 'dP')
    oil_GOR = graphing_line_2v(df_lst, 'Clock', 'Std.OilFlowrate', 'GOR(std)')
    gas_oil = graphing_line_2v(df_lst, 'Clock', 'Std.OilFlowrate', 'Std.GasFlowrate')
    oil_water_cum = graphing_line_2v(df_lst, 'Clock', 'Std.AccumOilVol', 'AccumWaterVol')

    # Drawing the graphs
    st.markdown(f'*Available Data: {df_lst.shape[0]}')
    with st.beta_expander(label='Data Set'):
        st.dataframe(df_lst)
    st.markdown('Average Table')
    st.dataframe(summary)
    st.subheader('Summary of Data:')
    col1, col2, col3, col4 = st.beta_columns(4)
    col1.subheader(f'Oil rate: {int(avg_oilRate)}')
    col2.subheader(f'Water rate: {int(avg_waterRate)}')
    gas_rate_float = "{:.4f}".format(avg_std_gasRate)
    col3.subheader(f'Gas rate: {float(gas_rate_float)}')
    col4.subheader(f'GOR: {int(avg_GOR)}')

    # Making the graphs
    with st.beta_expander(label='Parameters Charts'):
        st.plotly_chart(ptd)
        st.plotly_chart(oil_GOR)
    with st.beta_expander(label='Flow Rate Charts'):
        st.plotly_chart(gas_oil)
        st.plotly_chart(oil_water_cum)
    st.markdown(f'*Available Data: {df_lst.shape[0]}')



