import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import numpy as np

def graphing (df,x, ym, ys):
    """ Graphing function for two values

    :param df: Dataframe
    :type df: string
    :param x: Dataframe for axis x
    :type x: string
    :param ym: Dataframe for axis y primary
    :type ym: string
    :param ys: Dataframe for axis y secondary
    :type ys: string

    :returns: graph object
    :rtype: figure """

    xt =  df[x]
    yp = df[ym]
    yt = df[ys]
    # Making the graph for the two values
    fig_n = make_subplots(specs=[[{'secondary_y': True}]])
    fig_n.update_layout(title_text=ym + ' ' + ys + ' ' + 'Graph')
    fig_n.update_xaxes(title_text=x)
    fig_n.update_yaxes(title_text=ym, secondary_y=False)
    fig_n.update_yaxes(title_text=ys, secondary_y=True)
    fig_n.add_trace(go.Scatter(x=xt, y=yp, mode='lines', name=ym), secondary_y=False)
    fig_n.add_trace(go.Scatter(x=xt, y=yt, mode='lines', name=ys), secondary_y=True)
    return fig_n




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
# product_mask = df['Product'].isin(['A'])
    masked_df = (df['Gender'].isin(gender_selection) & df['Product'].isin(product_selection) & df['Client Age'].between(*age_selection) & df['Country'].isin(country_selection) )
    number_of_results = df[masked_df].shape[0]
    pivot_profit_df = df[masked_df].groupby(["Country", "Product"])[['Profit', 'Sale']].sum()
    pivot_count_df = df[masked_df].groupby(["Country", "Product"])[['Gender']].count()
# Draw the tables on the screen 
    st.markdown(f'*Available Results: {number_of_results}')
    st.dataframe(df[masked_df])
# Pivot table using groupby in pandas 
    st.markdown('Pivot tables')
    col1, col2 = st.beta_columns(2)
    col1.dataframe(pivot_profit_df)
    col2.dataframe(pivot_count_df)

# bar_chart = px.bar(pivot_count_df, x='Profit', y='Sale', text='Sale',
#                    color_discrete_sequence=['#F63366']*len(pivot_df),
#                    template='plotly_white')
# st.plotly_chart(bar_chart)
# ********************************************************************
# *************** Gauges Function ************************************
# ********************************************************************

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

# ====================================================================
# Plotly graphs
# ====================================================================

    x = df_lst['elapse']
    yp = df_lst['pressure']
    yt = df_lst['temperature']

    # Making the graph for the two values
    fig_n = make_subplots(specs=[[{'secondary_y': True}]])
    fig_n.update_layout(title_text='Pressure vs Temperature')
    fig_n.update_xaxes(title_text='Time lapse')
    fig_n.update_yaxes(title_text='Pressure /psi', secondary_y=False)
    fig_n.update_yaxes(title_text='Temperature /F', secondary_y=True)
    fig_n.add_trace(go.Scatter(x=x, y=yt, mode='lines', name='Temperature'), secondary_y=True)
    fig_n.add_trace(go.Scatter(x=x, y=yp, mode='lines', name='Pressure'), secondary_y=False)

    dx = graphing(df_lst, 'elapse', 'pressure', 'temperature')


# ====================================================================
# Showing the graphs 
# ====================================================================
    st.markdown(f'*Available Data: {df_lst.shape[0]}')
    st.markdown('Pressure Temperature Graph')
    # st.plotly_chart(fig_n)
    st.plotly_chart(dx)
    st.markdown('Full Data Table')
    st.dataframe(df_lst)
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
    # fig1 = px.scatter(df_lst['Pressure'])


# ====================================================================
# Plotly graphs
# ====================================================================
    ptd = graphing(df_lst, 'Clock', 'Pressure', 'dP')
    oil_GOR = graphing(df_lst, 'Clock', 'Std.OilFlowrate', 'GOR(std)')

    st.markdown(f'*Available Data: {df_lst.shape[0]}')
    st.dataframe(df_lst)
    st.markdown('Average Table')
    st.dataframe(summary)
    st.plotly_chart(ptd)
    if st.button('make oil grapgh'):
        st.plotly_chart(oil_GOR)
    st.markdown(f'*Available Data: {df_lst.shape[0]}')



