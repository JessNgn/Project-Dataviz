#! /bin/python
# -*- coding: utf-8 -*-
#
# DataVizProject.py
#
# Comment l'activité chirurgicale en cancérologie a-t-elle évoluée au cours des dernières années en France et comment améliorer la prise en charge des patients atteints du cancer?

__author__ = "Nhat-Vy Jessica NGUYEN"
__copyright__ = "Copyright 2023, DataVizProject 2023"
__credits__ = ["Nhat-Vy Jessica NGUYEN"]
__version__ = "0.0.1"
__maintainer__ = "Nhat-Vy Jessica NGUYEN"
__email__ = "nhat-vy-jessica.nguyen@efrei.net"
__status__ = "Research code"


# ----------------------------------------------- Librairies  ---------------------------------------------

from bs4 import BeautifulSoup
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import altair as alt
import plotly.graph_objects as go
import requests
from PIL import Image


# ----------------------------------------- Settings ---------------------------------------------

st.set_page_config(
    page_title="Cancer Chirurgie",
    page_icon=":syringe:", 
    layout="wide",
)


# ------------------------------ Récupération du lien (dynamique) ---------------------------------

def search_url():
    url = "https://www.data.gouv.fr/fr/datasets/activite-chirurgicale-en-cancerologie-par-localisation-tumorale/#/resources"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    links = soup.find_all('dd', class_="fr-text--sm fr-ml-0 fr-mt-0 fr-mb-2w text-overflow-ellipsis text-mention-grey")

    if links:
        for link in links:
            a_tag = link.find('a')
            if a_tag:
                first_href = a_tag['href']
                return first_href 
    else:
        return None

url = search_url()



@st.cache_data
def load_data(url):
    if url:
        data = pd.read_csv(url, header=0, encoding='ISO-8859-1',delimiter=';', skiprows=0)
        data = data.drop(0)

        numeric_columns = ['Dur_sej_moy', 'Dur_sej_max', 'Dur_sej_med', 'Dur_sej_min', 'Pat_chir_nbr', 'Pat_chir_pct', 'Hom_chir_nbr', 'Fem_chir_nbr']
        for colonne in numeric_columns:
            data[colonne] = data[colonne].str.replace(',', '.')
        data[numeric_columns] = data[numeric_columns].apply(pd.to_numeric, errors='coerce', downcast='float')

        return data
    else:
        return None

data = load_data(url)



# ---------------------------------- Side Bar / Presentattion -------------------------------------

st.sidebar.title(":hospital: Activité Chirurgicale en Cancérologie")
st.sidebar.markdown("---")

st.sidebar.caption("#datavz2023efrei")
st.sidebar.info("Développé par Jessica NGUYEN")


st.sidebar.markdown("---")
st.sidebar.write("*Où me trouver ?*")

st.sidebar.markdown('<a href="https://www.linkedin.com/in/jessica-nguyen-878a44225" style="color: #ADD8E6; text-decoration: none;">:link: Linkedin</a>', unsafe_allow_html=True)
st.sidebar.markdown('<a href="mailto:nhat-vy-jessica.nguyen@efrei.net" style="color: #ADD8E6; text-decoration: none;">:e-mail: nhat-vy-jessica.nguyen@efrei.net</a>', unsafe_allow_html=True)




# -------------------------------------------- Pages ----------------------------------------------

tab, tab1, tab2 = st.tabs(["Home", "Visualizations", "Find the Data"])


# ------------------------------------------ Page Home ---------------------------------------------

with tab:

    st.title(":syringe: Activité chirurgicale en cancérologie par localisation tumorale")
    st.write("Comment l'activité chirurgicale en cancérologie a-t-elle évoluée au cours des dernières années en France?")
    st.markdown('---')

    col1, col2 = st.columns(2)

    with col1:
        image = Image.open('image1.jpg')
        st.image(image)
    with col2:
        st.write('Notre site est spécialement conçu pour les médecins en cancérologie qui souhaitent comprendre comment l\'activité chirurgicale dans ce domaine évolue au fil du temps. Vous y trouverez des données pertinentes sur la durée de séjour à l\'hôpital, l\'évolution du nombre de patients, ainsi que des comparaisons par genre. Ces informations sont essentielles pour éclairer vos décisions cliniques et contribuer à l\'amélioration des soins en cancérologie.')

    
    st.write('***Rendez-vous sur l\'onglet "Visualizations" !***')
    st.markdown('---')

    st.subheader('Pour voir plus loin...')

    # Lien vers le site web
    st.write('*Site Web : Data visualization tools for exploring the global cancer burden :*')
    st.markdown('*[Source](https://gco.iarc.fr/today/home)*')
    web_page_url = 'https://gco.iarc.fr/today/home'
    st.markdown(f'<iframe src="{web_page_url}" width="725" height="450"></iframe>', unsafe_allow_html=True)
    
    st.markdown('<br>', unsafe_allow_html=True)

    # Lien vers la vidéo
    st.write('*Vidéo : Traitement chirurgical du cancer colorectal et développement de la chirurgie robotique :*')
    st.markdown('*[Source](https://www.youtube.com/watch?v=ZpXnunj1uqQ)*')
    video_url = 'https://www.youtube.com/watch?v=ZpXnunj1uqQ'
    st.video(video_url)



# -------------------------------------- Page Visualizations ---------------------------------------

with tab1:

    # ------------------------------------------ Intro ----------------------------------------

    st.subheader(":stethoscope: Tendances en cancérologie par localisation tumorale")

    selected_localisation = st.selectbox('Sélectionnez une localisation tumorale', data['Loc'].unique())
    selected_year = st.selectbox('Sélectionnez une année', data['Ann'].unique())


    filtered_data = data[(data['Loc'] == selected_localisation) & (data['Ann'] == selected_year)]

    st.markdown('<br>', unsafe_allow_html=True)
    st.write("En", selected_year, "pour la localisation", selected_localisation, " : ")
    st.write("Durée moyenne de séjour :", filtered_data['Dur_sej_moy'].values[0])
    st.write("Nombre total de patients traités par chirurgie en MCO :", filtered_data['Pat_chir_nbr'].values[0])

    st.markdown("---")


    # -------------------------- Répartition nombre chirurgie ---------------------------------


    # Pie chart

    total = data['Pat_chir_nbr'].sum()

    data_grouped_Loc = data.copy()
    data_grouped_Loc = data_grouped_Loc.groupby('Loc')['Pat_chir_nbr'].sum().reset_index()
    data_grouped_Loc['Loc'] = data_grouped_Loc.apply(lambda row: row['Loc'] if row['Pat_chir_nbr'] / total >= 0.02 else 'Autres', axis=1)
    data_grouped_Loc = data_grouped_Loc.groupby('Loc')['Pat_chir_nbr'].sum().reset_index()
    pastel_colors = ["#FF6B6B", "#98F6B0", "#FFD700", "#C3B1E1", "#FFA07A"]

    colors = pastel_colors + px.colors.qualitative.Pastel1
    
    fig = px.pie(data_grouped_Loc, names='Loc', values='Pat_chir_nbr', title='Répartition des Chirurgies par Localisation Tumorale',
                color_discrete_sequence=colors)

    fig.update_layout(height=800, width=800)
    st.plotly_chart(fig)



    # ----------------------------------- Durée Séjour ----------------------------------------

    st.markdown("---")
    st.subheader(":male-doctor: Evolution de la durée de séjour en chirurgie")

    # ------------

    selected_location = st.selectbox('Sélectionner une localisation tumorale', data['Loc'].unique(), key='dmoy_key')
    filtered_data = data[data['Loc'] == selected_location]

    # Selectbox pour la sélection du type de graphique
    plot_choice = st.selectbox("Sélectionnez le type de graphique :", ["Line Chart", "Bar Chart"])
    
    st.markdown('<br>', unsafe_allow_html=True)
    st.markdown("**Durée moyenne pour une localisation tumorale**")

    if plot_choice == "Line Chart":
        fig = px.line(filtered_data, x='Ann', y='Dur_sej_moy')
        st.plotly_chart(fig)
    elif plot_choice == "Bar Chart":
        st.bar_chart(filtered_data.set_index('Ann')['Dur_sej_moy'])




    # ------------------------- Nombre Chirurgies / Nombre Patients ---------------------------

    st.markdown("---")
    st.markdown('<br>', unsafe_allow_html=True)
    st.subheader(":adhesive_bandage: Evolution du nombre de patients traités en chirurgie")
 
    # ------------


    # Filtrer les données par localisation tumorale
    selected_location = st.selectbox('Sélectionner une localisation tumorale', data['Loc'].unique())
    filtered_data = data[data['Loc'] == selected_location]

    # Selectbox pour la sélection du type de graphique
    plot_choice = st.selectbox("Sélectionnez le type de graphique :", ["Line Chart", "Bar Chart"], key='plot_choice')
    st.markdown('<br>', unsafe_allow_html=True)
    st.markdown("**Nombre total de patients pour une localisation tumorale**")

    if plot_choice == "Line Chart":
        fig = px.line(filtered_data, x='Ann', y='Pat_chir_nbr')
        st.plotly_chart(fig)
    elif plot_choice == "Bar Chart":
        st.bar_chart(filtered_data.set_index('Ann')['Pat_chir_nbr'])


    # ------------

    st.markdown("---")

    # Filtrer les données par année
    selected_year = st.selectbox('Sélectionner une année', data['Ann'].unique())
    filtered_data = data[data['Ann'] == selected_year]

    # Graphique en barres pour le nombre de chirurgies par localisation tumorale
    fig = px.bar(filtered_data, x='Loc', y='Pat_chir_nbr', title=f'Nombre de Chirurgies par Localisation Tumorale en {selected_year}')
    st.plotly_chart(fig)


    # ------------

    st.markdown("---")

    datagrouped = data.groupby('Ann')['Pat_chir_nbr'].sum().reset_index()

    # Graphique en ligne pour l'évolution du nombre total de patients traités par année
    fig = px.line(datagrouped, x='Ann', y='Pat_chir_nbr', title='Évolution du Nombre Total de Patients Traités par Année')
    st.plotly_chart(fig)




    # ----------------------------------------- Genres ----------------------------------------


    st.markdown("---")
    st.subheader(":couple: Comparaison par genre")

    # ------------

    localisations = data['Loc'].unique()
    selected_localisation = st.selectbox("Sélectionnez une localisation tumorale", localisations, key="unique_key")
    # Filtrer les données en fonction de la localisation sélectionnée
    filtered_data = data[data['Loc'] == selected_localisation]

    fig = go.Figure(data=[
    go.Bar(name='Hommes', x=filtered_data['Ann'], y=filtered_data['Hom_chir_nbr']),
    go.Bar(name='Femmes', x=filtered_data['Ann'], y=filtered_data['Fem_chir_nbr'])
    ])

    fig.update_layout(barmode='stack', xaxis_title='Année', yaxis_title='Nombre de patients', title='Nombre de patients par genre par année')
    st.plotly_chart(fig)        

    # ------------

    st.markdown("---")
    st.markdown("**Comparaison par genres des durée de séjour maximale**")

    # Par ordre alphabétiuqe
    data['Catégorie'] = data['Loc'].str[0]
    catégories_uniques = data['Catégorie'].unique()
    catégorie_sélectionnée = st.selectbox("Sélectionnez une catégorie", catégories_uniques)

    data_filtré = data[data['Catégorie'] == catégorie_sélectionnée]

    # Graphique basé sur les données filtrées
    fig1 = px.bar(data_filtré, x='Loc', y='Dur_sej_max', color='Hom_chir_nbr', title=f'Durée de Séjour Maximale ({catégorie_sélectionnée}) par Type de Cancer et Genre')
    fig2 = px.bar(data_filtré, x='Loc', y='Dur_sej_max', color='Fem_chir_nbr', title=f'Durée de Séjour Maximale ({catégorie_sélectionnée}) par Type de Cancer et Genre')

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig1, use_container_width= True)
    with col2:
        st.plotly_chart(fig2, use_container_width= True)


    # ------------

    st.markdown("---")

    maladie_select = st.selectbox("Sélectionnez une location tumorale", data['Loc'].unique(), key = "select_maladie")
    data_catégorie = data[data['Loc'] == maladie_select]
    total_femmes = data_catégorie['Fem_chir_nbr'].sum()
    total_hommes = data_catégorie['Hom_chir_nbr'].sum()

    gender_data = pd.DataFrame({'Gender': ['Femmes', 'Hommes'],
                                'Count': [total_femmes, total_hommes]})
    

    # Pie chart avec Plotly Express
    fig = px.pie(gender_data, names='Gender', values='Count', title=f"Répartition par genre pour la localisation tumorale : {maladie_select}")
    # Etiquettes (pourcentages)
    fig.update_traces(textinfo='percent+label', marker=dict(colors=['#FF8080', '#FFCF96']))
    st.plotly_chart(fig)
        

    # ------------

    st.markdown("---")
    st.markdown("**Comparaison des genres par type de cancer**")


    fig1 = px.bar(data, x='Loc', y='Hom_chir_nbr', title='Hommes par Type de Cancer')

    fig2 = px.bar(data, x='Loc', y='Fem_chir_nbr', title='Femmes par Type de Cancer')
    fig2.update_traces(marker_color='pink')

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig1, use_container_width=True)
    with col2:
        st.plotly_chart(fig2, use_container_width=True)


    # ------------ st.radio

    st.markdown("---")

    choice = st.radio('Choisir le style de graphique', ['Stack', 'Grouped'])

    if choice == 'Stack':

        # Filtrer les données par année
        selected_year = st.selectbox('Sélectionner une année', data['Ann'].unique(), key='stack_key')
        filtered_data = data[data['Ann'] == selected_year]

        # Graphique en barres empilées pour comparer le nombre de chirurgies pour les hommes et les femmes
        fig2 = px.bar(filtered_data, x='Loc', y=['Hom_chir_nbr', 'Fem_chir_nbr'], title=f'Comparaison des Chirurgies pour Hommes et Femmes en {selected_year}')
        st.plotly_chart(fig2)

    elif choice == 'Grouped':

        annees = data["Ann"].unique()
        selected_annees = st.multiselect("Sélectionnez les années", annees, annees, key='grouped_key') 

        df_hommes_loc = data[data["Ann"].isin(selected_annees)].groupby('Loc')['Hom_chir_nbr'].sum().reset_index()
        df_femmes_loc = data[data["Ann"].isin(selected_annees)].groupby('Loc')['Fem_chir_nbr'].sum().reset_index()
        fig_genre_loc = go.Figure()


        fig_genre_loc.add_trace(go.Bar(x=df_hommes_loc['Loc'], y=df_hommes_loc['Hom_chir_nbr'], name='Hommes', marker_color="light blue"))
        fig_genre_loc.add_trace(go.Bar(x=df_femmes_loc['Loc'], y=df_femmes_loc['Fem_chir_nbr'], name='Femmes'))
        fig_genre_loc.update_traces(marker_color="#EF9595", selector={"name": "Femmes"})
        fig_genre_loc.update_layout(title='Evolution nombre de patients en fonction du genre et de la location tumorale', barmode='group', xaxis_tickangle=-45, width=800, height=800, bargap=0, bargroupgap=0.1)

        st.plotly_chart(fig_genre_loc)



# ---------------------------------------- Page Find Data -----------------------------------------

with tab2:

    st.markdown('**Pour télécharger la base de données, rendez-vous sur :**')
    st.markdown('*https://www.data.gouv.fr/fr/datasets/5a8c1d46c751df748508e58f/#/resources*')

    column_descriptions = {
    "Ann": "Année de référence",
    "Loc": "Lieux du cancer",
    "Dur_sej_moy": "Durée moyenne du séjour en jours",
    "Dur_sej_max": "Durée maximale du séjour en jours",
    "Dur_sej_med": "Durée médiane du séjour en jours",
    "Dur_sej_min": "Durée minimale du séjour en jours",
    "Pat_chir_nbr": "Nombre total de patients traités par chirurgie en mode ambulatoire (MCO)",
    "Pat_chir_pct": "Répartition en pourcentage du nombre total de patients traités par chirurgie en mode ambulatoire (MCO)",
    "Hom_chir_nbr": "Nombre d'hommes traités par chirurgie en mode ambulatoire (MCO)",
    "Fem_chir_nbr": "Nombre de femmes traitées par chirurgie en mode ambulatoire (MCO)"
    }


    # ------------ description

    st.markdown('<br>', unsafe_allow_html=True)
    st.write("Description de la dataset :")
    st.table(pd.DataFrame(column_descriptions.items(), columns=["Colonne", "Description"]))


    # ------------ data et utilisation

    st.markdown('<br>', unsafe_allow_html=True)
    st.write("Voici un aperçu des données et leurs utilisations :")

    st.dataframe(data)

    # ------------  

    selected_localisation = st.selectbox("Sélectionnez une localisation tumorale", localisations, key="unique_keys")
    filtered_data = data[data['Loc'] == selected_localisation]

    col1, col2 = st.columns(2)

    with col1:
        localisations = data['Loc'].unique()
        st.markdown("**Evolution de l'activité chirurgicale en cancérologie entre 2011 et 2016**")
        fig1, ax = plt.subplots()
        ax.plot(filtered_data['Ann'], filtered_data['Dur_sej_moy'])
        ax.set_xlabel("Année")
        ax.set_ylabel("Durée moyenne de séjour (en jours)")
        st.pyplot(fig1, use_container_width= True)

    with col2:
            
        st.markdown("**Répartition des patients par genre pour une localisation tumorale**")

        annee = filtered_data['Ann'].to_list()
        hommes = filtered_data['Hom_chir_nbr'].to_list()
        femmes = filtered_data['Fem_chir_nbr'].to_list()

        # Création du graphique à barres empilées avec Matplotlib
        fig2, ax = plt.subplots(figsize=(6, 4.5))
        ax.bar(annee, hommes, label="Hommes")
        ax.bar(annee, femmes, label="Femmes", bottom=hommes)
        ax.set_xlabel("Année")
        ax.set_ylabel("Nombre de patients")
        ax.legend(title="Genre")
        st.pyplot(fig2, use_container_width= True)



