import pickle
import streamlit as st
import requests

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=b319dc85b5ee3be45947deb65c99bc0e&language=en-US".format(movie_id)
    response = requests.get(url)
    movie_data_json = response.json()
    poster_path = movie_data_json['poster_path']
    full_poster_path = "https://image.tmdb.org/t/p/original/" + poster_path

    return full_poster_path

def recommend_similar(movie_name):

    original_idx_in_movies = movies[movies['title']==movie_name].index[0]
    distances = sorted(enumerate(similarity[original_idx_in_movies]), reverse=True, key=lambda x: x[1])
    
    reco_list = []
    reco_list_posters = []

    for pair in distances[1:6]:
        reco_idx_in_matrix = pair[0]
        movie_id = movies.iloc[reco_idx_in_matrix].id

        reco_list.append(movies.iloc[reco_idx_in_matrix].title)
        reco_list_posters.append(fetch_poster(movie_id))

    return reco_list, reco_list_posters


st.header("Movie Recommendation System using ML")
movies = pickle.load(open('artifacts/movies.pkl', 'rb'))
similarity = pickle.load(open('artifacts/similarity.pkl', 'rb'))

movie_list = movies['title'].values
selected_movie = st.selectbox(
    'Select a movie to get recommendation',
    movie_list
    )

if st.button('Show Reco'):
    recommended_movies_name, recommended_movies_poster_fpath = recommend_similar(selected_movie)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommended_movies_name[0])
        st.image(recommended_movies_poster_fpath[0])
    with col2:
        st.text(recommended_movies_name[1])
        st.image(recommended_movies_poster_fpath[1])
    with col3:
        st.text(recommended_movies_name[2])
        st.image(recommended_movies_poster_fpath[2])
    with col4:
        st.text(recommended_movies_name[3])
        st.image(recommended_movies_poster_fpath[3])
    with col5:
        st.text(recommended_movies_name[4])
        st.image(recommended_movies_poster_fpath[4])
