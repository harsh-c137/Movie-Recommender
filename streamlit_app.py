import pickle
import streamlit as st
import requests

# --- Page Configuration ---
st.set_page_config(
    page_title="CineSuggest Movie Recommender",
    page_icon="🎬",
    layout="wide"
)

# --- Custom CSS for Styling ---
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

st.markdown("""
<style>
.movie-title {
    font-size: 16px;
    font-weight: bold;
    color: #FFFFFF; /* White text for better contrast on dark theme */
    text-align: center;
    height: 60px; /* Fixed height to ensure alignment */
    overflow: hidden;
    text-overflow: ellipsis;
    display: -webkit-box;
    -webkit-line-clamp: 2; /* Limit to 2 lines */
    -webkit-box-orient: vertical;
}
.stButton>button {
    width: 100%;
    border-radius: 20px;
    background-color: #FF4B4B;
}
</style>
""", unsafe_allow_html=True)


# --- Data Loading (Cached for Performance) ---
@st.cache_data
def load_data():
    """Loads the movie data and similarity matrix from pickle files."""
    try:
        movies = pickle.load(open('artifacts/movies.pkl', 'rb'))
        similarity = pickle.load(open('artifacts/similarity.pkl', 'rb'))
        return movies, similarity
    except FileNotFoundError:
        st.error("Model files not found. Please ensure 'artifacts/movies.pkl' and 'artifacts/similarity.pkl' exist.")
        return None, None

movies, similarity = load_data()

# --- API Call to TMDB ---
def fetch_poster(movie_id):
    """Fetches the movie poster path from the TMDB API."""
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=b319dc85b5ee3be45947deb65c99bc0e&language=en-US"
        response = requests.get(url)
        response.raise_for_status()  # Raises an exception for 4XX/5XX errors
        movie_data_json = response.json()
        poster_path = movie_data_json.get('poster_path')
        if poster_path:
            full_poster_path = "https://image.tmdb.org/t/p/w500/" + poster_path
            return full_poster_path
        else:
            return "https://via.placeholder.com/500x750.png?text=No+Poster+Available" # Placeholder
    except requests.exceptions.RequestException as e:
        st.warning(f"Could not fetch poster for movie ID {movie_id}: {e}")
        return "https://via.placeholder.com/500x750.png?text=API+Error" # Placeholder for API error

# --- Recommendation Logic ---
def recommend_similar(movie_name):
    """Recommends 5 similar movies based on the selected movie."""
    try:
        original_idx_in_movies = movies[movies['title'] == movie_name].index[0]
        distances = sorted(enumerate(similarity[original_idx_in_movies]), reverse=True, key=lambda x: x[1])

        reco_list = []
        reco_list_posters = []

        for pair in distances[1:6]:  # Start from 1 to skip the movie itself
            reco_idx_in_matrix = pair[0]
            movie_id = movies.iloc[reco_idx_in_matrix].id

            reco_list.append(movies.iloc[reco_idx_in_matrix].title)
            reco_list_posters.append(fetch_poster(movie_id))

        return reco_list, reco_list_posters
    except IndexError:
        st.error(f"Movie '{movie_name}' not found in the dataset.")
        return [], []

# --- UI Layout ---
st.markdown("<h1 style='text-align: center; color: #FF4B4B;'>CineSuggest 🍿</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #FFFFFF;'>Find Your Next Favorite Movie</h3>", unsafe_allow_html=True)

if movies is not None:
    movie_list = movies['title'].values
    selected_movie = st.selectbox(
        'Type or select a movie you like from the dropdown below:',
        movie_list
    )

    if st.button('Get Recommendations'):
        with st.spinner('Finding similar movies for you...'):
            recommended_movies_name, recommended_movies_poster = recommend_similar(selected_movie)
        
        if recommended_movies_name:
            st.subheader("Here are your recommendations:")
            
            cols = st.columns(5)
            for i in range(5):
                with cols[i]:
                    st.markdown(f"<p class='movie-title'>{recommended_movies_name[i]}</p>", unsafe_allow_html=True)
                    st.image(recommended_movies_poster[i])

# --- Footer with Social Links ---
st.markdown("---")

# Centered text and icons
st.markdown(
    """
    <div style="text-align: center;">
        <p>Connect with me</p>
        <a href="https://www.linkedin.com/in/harsh-deshpande-v1/" target="_blank">
            <img src="data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIiBzdHJva2U9IndoaXRlIiBzdHJva2Utd2lkdGg9IjIiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIgY2xhc3M9ImZlYXRoZXIgZmVhdGhlci1saW5rZWRpbiI+PHBhdGggZD0iTTE2IDhhNiA2IDAgMCAxIDYgNnY3aC00di03YTMgMyAwIDAgMC0zLTMgMyAzIDAgMCAwLTMgM3Y3SDV2LTdjMC0zLjMxIDEuNDEtNyA2LTd6Ij48L3BhdGg+PHJlY3QgeD0iMiIgeT0iOSIgd2lkdGg9IjQiIGhlaWdodD0iMTIiPjwvcmVjdD48Y2lyY2xlIGN4PSI0IiBjeT0iNCIgcj0iMiI+PC9jaXJjbGU+PC9zdmc+" width="30" height="30" style="margin: 0 10px;">
        </a>
        <a href="https://github.com/harsh-c137" target="_blank">
            <img src="data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIiBzdHJva2U9IndoaXRlIiBzdHJva2Utd2lkdGg9IjIiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIgY2xhc3M9ImZlYXRoZXIgZmVhdGhlci1naXRodWIiPjxwYXRoIGQ9Ik05IDljLTEuMjcgMS4yNy0yLjA5IDIuODYtMiA1IDAgMy41OCAyLjkxIDYuNSAxLjQyIDcuOS0xLjQxIDEuNC0zLjUzIDEuNTktNS41OSA2LjQxLTIuMDYtNC44Mi0xLjk4LTkuMjYgLjA5LTEzLjUxQzYuODggMCAxMiAwIDEyIDBjMy4xMSAwIDUuMTIgMS42NCA1LjkyIDQuMzhDMjAgNi4xIDIwIDExLjM0IDIwIDExLjM0djEuMzZjMCAuODEtLjY3IDEuNDctMS40NyAxLjQ3SDE4LjVjLS44MSAwLTEuNDctLjY3LTEuNDctMS40N3YtMy4zOWMwLS44MS0uNjctMS40Ny0xLjQ3LTEuNDdoLTEuMDNjLS44MSAwLTEuNDcuNjctMS40NyAxLjQ3djUuNTlDMTEuNDEgMjAgMTAuMjcgMjAgOSAyMGMtMS4yNyAwLTIuNDYtMS4xNy0yLjQ2LTIuNjIgMC0uNDEuMDMtMS4zOS4yOS0yLjM4IDAgMC0xLjA3LjY3LTEuMDctMi4xNyAwLTMgMi40Ni0yLjQ2IDIuNDYtMi40NnptMC0zLjE3YzAgMS4zOC0xLjEyIDIuNS0yLjUgMi41UzQgNy4yMSA0IDUuODMgNS4xMiAzLjMzIDYuNSAzLjMzIDkgNC40NSA5IDUuODN6bTggMGMwIDEuMzgtMS4xMiAyLjUtMi41IDIuNVMxMi41IDcuMjEgMTIuNSA1LjgzaC0xLjA0YzAgMS4zOC0xLjEyIDIuNS0yLjUgMi41UzYgNy4yMSA2IDUuODN2LS44NGMwLTEuMzggMS4xMi0yLjUgMi41LTIuNVMxMSA0LjQ1IDExIDUuODN2Ljg0YzAgMS4zOCAxLjEyIDIuNSAyLjUgMi41czIuNS0xLjEyIDIuNS0yLjV2LS44NGMwLTEuMzggMS4xMi0yLjUgMi41LTIuNVMxOSA0LjQ1IDE5IDUuODN2Ljg0eiI+PC9wYXRoPjwvc3ZnPg==" width="30" height="30" style="margin: 0 10px;">
        </a>
    </div>
    """
    , unsafe_allow_html=True
)
