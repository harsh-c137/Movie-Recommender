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

    .footer {
        text-align: center;
        padding: 1.5rem 0;
        margin-top: 2rem;
        border-top: 1px solid #dee2e6;
        color: #6c757d;
    }

        .social-links {
        margin-top: 0.5rem;
    }
    
    .social-links a {
        margin: 0 10px;
        text-decoration: none;
        font-size: 1.2rem;
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
st.markdown("""
<div class="footer">
    <h3>Impressed with AskVault? 🚀</h3>
    <p>Let's collaborate on your next AI project! I specialize in building intelligent applications that solve real business problems.</p>
    <div class="social-links">
        <a href="https://www.github.com/harsh-c137" target="_blank">
            <img src="https://cdn.jsdelivr.net/gh/simple-icons/simple-icons/icons/github.svg" alt="GitHub Icon" width="20" height="20"> GitHub
        </a>
        <a href="https://www.linkedin.com/in/harsh-deshpande-v1/" target="_blank">
            <img src="https://www.svgrepo.com/show/157006/linkedin.svg" alt="LinkedIn Icon" width="20" height="20"> LinkedIn
        </a>
    </div>
</div>
""", unsafe_allow_html=True)
