import pickle
import streamlit as st
import requests
import dill
import os


def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def fetch_overview(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    return data['overview']

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []

    # getting the overview using movie_id
    global detail
    detail = fetch_overview(movies.iloc[distances[0][0]].movie_id) #finding the movie_id and calling fetch_overview with it

    for i in distances[0:7]:
        movie_id = movies.iloc[i[0]].movie_id
        # fetch the movie poster
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names,recommended_movie_posters, detail


st.header('Movie Recommender System')
with open(os.path.join(os.getcwd(), "movie_list.pkl"), "rb") as file_obj:
    movies = dill.load(file_obj)

with open(os.path.join(os.getcwd(), "similarity.pkl"), "rb") as file_obj:
    similarity = dill.load(file_obj)

movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

detail = 'None'

if st.button('Show Recommendation'):
    recommended_movie_names,recommended_movie_posters, detail = recommend(selected_movie)

    col1, col2 = st.columns([1,3])
    with col1:
        st.image(recommended_movie_posters[0])
    with col2:
        st.markdown(detail)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(recommended_movie_names[1])
        st.image(recommended_movie_posters[1])
    with col2:
        st.markdown(recommended_movie_names[2])
        st.image(recommended_movie_posters[2])

    with col3:
        st.markdown(recommended_movie_names[3])
        st.image(recommended_movie_posters[3])

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(recommended_movie_names[4])
        st.image(recommended_movie_posters[4])
    with col2:
        st.markdown(recommended_movie_names[5])
        st.image(recommended_movie_posters[5])
    with col3:
        st.markdown(recommended_movie_names[6])
        st.image(recommended_movie_posters[6])
    





