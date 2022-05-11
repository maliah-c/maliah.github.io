# -*- coding: utf-8 -*-
"""final.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1NgfdXXpVHSe1d9XV84o1UR0Y5jp9P2oP
"""

import sqlite3
from sqlite3 import connect
import pandas as pd
import numpy as np
import streamlit as st
from PIL import Image

image = Image.open('Logo-KDT-JU.webp')
st.title("Partner Search App")
st.image(image)


con = sqlite3.connect("ecsel_database.db")
df_countryList = pd.read_sql('SELECT countries.Country, countries.Acronym FROM countries', con)
df_projects = pd.read_sql('SELECT Projects.projectID, Projects.year, Projects.acronym FROM Projects', con)
df_participants = pd.read_sql('SELECT  organizations.projectID, organizations.country, organizations.shortName, organizations.name, organizations.activityType, organizations.organizationURL, organizations.ecContribution, organizations.projectAcronym FROM organizations ', con)
#df_participantLiat ()
print(df_countryList)
con.close()

# Country acronyms dictionary
country_acronyms = {'Belgium': 'BE','Bulgaria': 'BG', 'Czechia': 'CZ', 'Denmark': 'DK', 'Germany':
'DE', 'Estonia':'EE', 'Ireland':'IE', 'Greece':'EL', 'Spain': 'ES','France': 'FR', 'Croatia': 'HR', 'Italy': 'IT', 'Cyprus': 'CY', 
'Latvia':'LV', 'Lithuania': 'LT', 'Luxembourg': 'LU', 'Hungary': 'HU','Malta': 'MT','Netherlands': 'NL', 'Austria': 'AT',
'Poland': 'PL','Portugal':'PT', 'Romania': 'RO', 'Slovenia': 'SI', 'Slovakia':'SK', 'Finland': 'FI', 'Sweden':'SE'}

country = st.selectbox('pick', ['BE', 'BG', 'CZ', 'DK', 'DE', 'EE', 'IE','EL','ES','FR','HR','IT','CY','LV','LT','LU','HU','MT','NL','AT','PL','PT','RO','SI','SK','FI','SE'])

#country = df_countryList[df_countryList.Country == selection].Acronym.item()

#creating table with data specific to the selected country
df_new = df_participants[df_participants["country"] == country]
df_pryear = df_projects[["projectID", "year"]]
df_new = pd.merge(df_new, df_pryear, how ="left", on="projectID")
st.dataframe(df_new)

#create table by country selection, using sort_value to order the table in descending order, using .agg() to split ecContribution into two columns (count, sum)
con = sqlite3.connect("ecsel_database.db")
df_best = pd.read_sql(f'SELECT organizations.shortname, organizations.name, organizations.activityType, organizations.organizationURL, organizations.ecContribution, country  FROM organizations WHERE country="{country}" ORDER BY ecContribution DESC', con)


df_better = pd.read_sql(f'SELECT organizations.shortname, organizations.name, organizations.activityType, organizations.projectAcronym, country FROM organizations WHERE country="{country}"', con)

con.close()

st.dataframe(df_best)
st.dataframe(df_better)

csv_c = df_best.to_csv().encode('utf-8')
st.download_button(
     label="Download dataframe participants as CSV",
     data=csv_c,
     file_name=f'df.csv',
     mime='text/csv',)

csv_c2 = df_better.to_csv().encode('utf-8')
st.download_button(
     label="Download dataframe projects as CSV",
     data=csv_c2,
     file_name=f'df.csv',
     mime='text/csv',)

#bar graph
df_counterYear = df_new.groupby("year").sum().ecContribution
#df_counterYear.plot(kind = "bar", title = f"Total EU contribution in {country}")
st.bar_chart(df_counterYear)

