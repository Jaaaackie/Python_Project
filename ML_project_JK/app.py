import pickle
import streamlit as st
from tmdbv3api import Movie, TMDb

movie = Movie()
tmdb = TMDb()
tmdb.api_key = '52849df673603b39d0679318138dbfb2'
# api : Wenn ein Programm dem Server um Daten bittet, gibt der Server die entsprechenden Daten zurück.
#       Dies ermöglicht die Kommunikation zwischen dem Programm und dem Server.
# https://www.themoviedb.org/settings/api

tmdb.language = 'de-DE' # Informationen auf Deutsch abrufen

# Die "get_recommendations()"-Funktion, die im Jupyter Notebook definiert wurde, nahm "title" und "cosine_sim" als Parameter an.
# Hier ist "cosine_sim" jedoch  im globalen Bereich deklariert, daher nehmen wir nur "title" als Parameter.
def get_recommendations(title):
    # Den Index des Films im Gesatmdatensatz anhand des Titels ermitteln
    idx = movies[movies['title'] == title].index[0]
    # den Film in den Daten der "movies"-Datei ("title"), dessen Titel dem übergebenen Titel entspricht, finden
    # Der Index in der "movies"-Datei = Der Index im Gesamtdatensatz
    # Wir suchen also den Film mit dem übergebenen Titel in der "title"-Spalte der "movies"-Datei 
    # und speichern den Index in einer Variable "idx"
    # Da "movies[movies['title] == title].index" ein Array ist, müssen wir den 0. Index nehmen!

    # Die Daten aus der Kosinusähnlichkeitsmatrix("cosine_sim") für den index "idx" in der Form (idx, Ähnlichkeit) abrufen
    sim_scores = list(enumerate(cosine_sim[idx]))
    # Wir verwenden die "cosine_sim" direkt aus dem globalen Bereich und die Daten an den "cosine_sim" entsprechenden Indizes
    # Wenn wir nur die Ähnlichkeit nehmen, wissen wir nicht, welcher Index dazugehört. Daher holen wir die Paare (idx, Ähnlichkeit) mit "enumerate"

    # Die Ergebnisse nach Kosinus-Ähnlichkeit absteigend sortieren
    sim_scores = sorted(sim_scores, key = lambda x: x[1], reverse = True)

    # Die 10 empfohlenen Filme ohne den Film seblst (Kosinusähnlichkeit = 1) auswählen anhand Slicing
    sim_scores = sim_scores[1:11]

    # Die Indizes der 10 empfohlenen Filme extrahieren
    movie_indices = [i[0] for i in sim_scores]    

    # Anhand der Indizes die Filmtitel abrufen
    images = []
    titles = []
    for i in movie_indices:
        id = movies['id'].iloc[i] # Die Film-"id" zum Index i abrufen
        details = movie.details(id) # Die Details des Films mit der "id" über die "details()"-Methode des "movie"-Objekts vom TMDb abrufen
        
        image_path = details['poster_path'] # details.poster_path, Das Poster-Pfad-Feld aus den "details"

        if image_path:
            # Ref.: https://developer.themoviedb.org/docs/image-basics
           image_path = 'https://image.tmdb.org/t/p/w500' + image_path
          
        else:
            image_path = 'no_image.jpg'
        
        images.append(image_path)
        titles.append(details['title'])
        # Wir haben den Filmtitel bereits als Parameter an "get_recommendations()" übergeben.
        # Der Grund, warum wir ihn hier noch einmal abrufen, ist, dass alle unsere Daten bisher auf Englisch sind.
        # Mit der Spracheinstellung können wir jedoch auch Deutsche Filmtitel abrufen.

    return images, titles

movies = pickle.load(open('movies.pickle', 'rb')) # Die Daten mit den Film-"id"s und -"title" sind hier gespeichert
cosine_sim = pickle.load(open('cosine_sim.pickle', 'rb'))

st.set_page_config(layout =  'wide') # Layout auf breit setzen
st.header('Toastflix') # Titel

# Auf der Seite kann der Nutzer einen Filmtitel auswählen und dann einen Button drücken, um eine Inhaltsbasierte Empfehlungsliste ähnlicher Filme zu sehen

# Die Filmliste aus den Daten extrahieren und als Dropdown-Auswahl anbieten
movie_list = movies['title'].values
# "movie_list" als Optionen für ein Dropdown-Menü verwenden, das ausgewählte Element wird in der Variable "title" gespeichert
title = st.selectbox('Bitte wählen Sie einen Film aus, den Sie mögen', movie_list)
# Event beim Klick auf den Empfehlungs-Button
if st.button('Empfehlen'):
    with st.spinner('Bitte warten...'): # Ladebalken (Progress Bar) unter dem Button
        images, titles = get_recommendations(title)

        idx = 0 # Index für die 10 empfohlenen Filme (Poster & Titel)
        for i in range(0, 2): # 2 Zeilen (0, 1)
            cols = st.columns(5) # 5 Spalten pro Zeile
            for col in cols:
                col.image(images[idx]) # "image" in die Spalte einfügen
                col.write(titles[idx]) # "title" in die Spalte einfügen
                idx += 1

# App im Terminal starten : streamlit run app.py