import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt 
import pandas as pd 

st.set_page_config(layout='wide')

header_html = """
<div style="background: -webkit-linear-gradient(45deg, #FF0000, #FF7F00, #FFFF00, #00FF00, #0000FF, #4B0082, #9400D3);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: 48px;
            text-align: center; /* Center the text horizontally */
            padding: 20px; /* Add padding for better visibility */
            ">
    Airbnb Analysis
</div>
"""

# Display the header HTML
st.markdown(header_html, unsafe_allow_html=True)

df = pd.read_csv("Airbnb_cleaned_data.csv", index_col='Unnamed: 0')

st.subheader("Total Number of Properties ")
st.markdown(f"<h1 style='text-align: center;'>{df.shape[0]}</h1>", unsafe_allow_html=True)

st.subheader("Total Number of Hosts ")
st.markdown(f"<h1 style='text-align: center;'>{df['host_name'].str.lower().value_counts().shape[0]}</h1>", unsafe_allow_html=True)

st.header("Locations of Properties")
fig = px.scatter_mapbox(df, lat='long', lon='lat', mapbox_style='open-street-map', zoom=1, height=600, width=1000)
fig.update_layout(mapbox_style="carto-positron")
st.plotly_chart(fig)

country_group =  df.groupby("country")
country_group.size().sort_values(ascending=False)
fig4 = px.bar(country_group.size(),x = country_group.size().sort_values(ascending=False).index, y= country_group.size().sort_values(ascending=False).values)
fig4.update_xaxes(title_text='Country')
fig4.update_yaxes(title_text='Number of Properties')
fig4.update_layout(title_text='Properties by Country')
fig4.update_layout(width = 1000, height = 500)
st.plotly_chart(fig4)
property_counts = df['property_type'].value_counts()

# Selecting the top 10 property types based on their counts
top_10_property_types = property_counts.head(15)


fig1 = px.bar(df,x = top_10_property_types.index, y= top_10_property_types.values)
fig1.update_xaxes(title_text='Property Type')
fig1.update_yaxes(title_text='Count')
fig1.update_layout(title_text='Top 15 Property Types')
fig1.update_layout(width = 1000, height = 600)
st.plotly_chart(fig1) 

col1, col2 = st.columns(2)


with col1:
    room = df['room_type'].value_counts()
    fig2 =  px.pie(df,names=room.index, values= room.values)
    fig2.update_layout(
    title_text='Room Types',
    legend=dict(
        orientation="v",  # Set orientation to horizontal
        yanchor="auto",  # Anchor legends to the bottom of the plot
        y=0,  # Adjust y position
        xanchor="center",  # Anchor legends to the right
        x=0 )) # Adjust x position
    st.plotly_chart(fig2)

with col2:
    bed = df['bed_type'].value_counts()
    fig3 = px.pie(df, names=bed.index, values=bed.values)
    fig3.update_layout(title_text='Bed Types', legend = dict(
        orientation="v",  # Set orientation to horizontal
        yanchor="auto",  # Anchor legends to the bottom of the plot
        y=0,  # Adjust y position
        xanchor="center",  # Anchor legends to the right
        x=0) )
    st.plotly_chart(fig3)


avg_country = country_group.mean().reset_index()
avg_country_price = avg_country.sort_values('price', ascending=False)

with col1:
    fig5 = px.line(avg_country_price, x='country', y='price', title='Price by Country')
    st.plotly_chart(fig5)

with col2:
    fig6 = px.line(avg_country_price, x='country', y='cleaning_fee', title='Cleaning Fee by Country')
    st.plotly_chart(fig6)
avg_country_rating = avg_country.sort_values('review_rating', ascending=False)

with col1:
    fig7 = px.line(avg_country_rating, x='country', y='review_rating', title='Average ratings by Country')
    st.plotly_chart(fig7)

with col2:
    fig8 = px.line(avg_country_rating, x='country', y='number_of_reviews', title='Number of reviews by Country')
    st.plotly_chart(fig8)

st.dataframe(avg_country)