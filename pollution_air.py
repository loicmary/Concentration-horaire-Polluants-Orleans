import streamlit as st
import pandas as pd
import pydeck as pdk
import plotly.express as px
import functions
st.set_page_config(layout="wide")
st.title('Concentration horaire des polluants - Air ambiant - Orléans Métropole')

dataframe = pd.read_csv('concentration-horaire-des-polluants-air-ambiant-ligair-orleans-metropole.csv', sep=';')
final_dataframe = functions.preprocessing(dataframe)


with st.container():
    col1, col2 = st.columns(2)

    with col2:
        month = st.number_input(label='Mois',
                                min_value=1,
                                max_value=12,
                                step=1,
                                value=8)

        day = st.number_input(label='Jour',
                                min_value=1,
                                max_value=31,
                                step=1,
                                value=16)

        hour = st.number_input(label='Heure',
                                min_value=0,
                                max_value=23,
                                step=1,
                                value=17)

        molecule = st.radio(label = 'Molecule',
                            options = ['NO', 'PM10', 'PM2.5', 'O3', 'NO2'],
                            index=0)

    with col1:
        st.subheader(f"Concentration de {molecule} (µg/m3) le 2023-0{month}-{day} à {hour}:00")
        st.pydeck_chart(pdk.Deck(
            map_style=None,
            initial_view_state=pdk.ViewState(
                latitude=47.837765,
                longitude=1.944658,
                zoom=11,
                pitch=50,
            ),
            layers=[
                
                pdk.Layer(
                    "ColumnLayer",
                    data=functions.filtered_dataframe(final_dataframe, month, day, hour, molecule),
                    get_position=["longitude", "latitude"],
                    get_elevation="valeur",
                    elevation_scale=100,
                    radius=300,
                    get_radius=200,
                    pickable=True,
                    elevation_range = [0,200],
                    get_fill_color=[240, 0 , 240],
                    auto_highlight=True,
                )]  
        ))


with st.container():
    col1, col2 = st.columns(2)

    with col2 :

        type_graphe = st.selectbox(
            label = 'type graphe',
            options =('graphe complet', 
                      'Moyenne polluants' 
                      ))
        if type_graphe == 'graphe complet':

            ville = st.selectbox(
                label = 'ville',
                options =('Marigny-les-Usages', 'Orléans', 'Saint-Jean-de-la-Ruelle'))
            
            if ville == 'Orléans':
                station = st.selectbox(
                    label = 'station',
                    options =('Gambetta', 'La_Source-CNRS'))
                
                
                molecule2 = st.radio(label = 'Molecule2',
                                    options = list(final_dataframe[(final_dataframe['nom_com']==ville) & (final_dataframe['nom_station']==station)]['nom_poll'].unique()),
                                    index=0)
                
            elif ville == 'Marigny-les-Usages':
                station = 'Marigny-les-usages'

                molecule2 = st.radio(label = 'Molecule2',
                                    options = list(final_dataframe[(final_dataframe['nom_com']==ville) & (final_dataframe['nom_station']==station)]['nom_poll'].unique()),
                                    index=0)
            
            else :
                station = 'St-Jean-de-la-Ruelle'

                molecule2 = st.radio(label = 'Molecule2',
                                    options = list(final_dataframe[(final_dataframe['nom_com']==ville) & (final_dataframe['nom_station']==station)]['nom_poll'].unique()),
                                    index=0)


            
        
            with col1 :
                fig = px.line(final_dataframe[(final_dataframe['nom_com']==ville) & (final_dataframe['nom_station']==station) & (final_dataframe['nom_poll']==molecule2)].sort_values(by='date_debut'),
                            x="date_debut", 
                            y="valeur",
                            labels= {"valeur":"concentration (µg/m3)"},
                            title=f"Concentration de {molecule2} à la station {station} ({ville})")

                st.plotly_chart(fig)

        else :
            with col1 :
                mean_df = final_dataframe.groupby(['date_debut','nom_com','nom_station'])['valeur'].mean().reset_index().sort_values(by='date_debut')
                fig = px.line(mean_df, x="date_debut", 
                              y="valeur", 
                              color="nom_station",
                              labels = {'valeur':'concentration moyenne (µg/m3)'},
                              title='Concentration moyenne de l\'ensemble des polluants')
                st.plotly_chart(fig)
            
            
    
    
