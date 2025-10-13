import pandas as pd
import streamlit as st

dataset = pd.read_csv('https://www.irdx.com.br/media/uploads/paises.csv')

import streamlit as st
import plotly.express as px
import pandas as pd

fig = px.choropleth(dataset,
                    locations=dataset['iso3'],
                     color=dataset['nome'],
                     hover_name=dataset['nome'])
fig.update_layout(title= 'Mapa Coroplético dos Países',
                  geo_scope='world')
fig.show()

