# CineSuggest 🎬
Discover your next favorite movie with recommendations based on what you already love.

CineSuggest is a content-based movie recommender system built with Python and Scikit-learn. It analyzes a movie's plot, genre, cast, and crew to find and suggest other films with the most similar content. The entire project is deployed as an interactive web application using Streamlit.

This project is live and accessible at **[https://movierecotmdb.streamlit.app/](https://movierecotmdb.streamlit.app/)**

## 🧑‍💻 How to Run Locally

First, clone the repository:
```bash
https://github.com/harsh-c137/Movie-Recommender.git
cd Movie-Recommender
```
Next, get your free API key from The Movie Database (TMDB) here.
- Log in or create an account on [https://www.themoviedb.org/signup](https://www.themoviedb.org/signup)
- Generate the api key here: [https://www.themoviedb.org/subscription](https://www.themoviedb.org/subscription)

Then, create a `.streamlit` folder in the root directory. Inside it, create a file named `secrets.toml` and store your API key in the following format:
```toml
TMDB_API_KEY="your-api-key-here"
```

Finally, install the dependencies and launch the app:
```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

## 🔍 What Problem Does This Project Solve?

In an age of endless streaming options, users often face "choice paralysis" which is the difficulty of deciding what to watch next. Generic recommendations based on popularity often fail to capture individual tastes.

**CineSuggest** solves this by providing **content-based recommendations**. Instead of relying on what's popular, it performs a deep-dive into the attributes of a movie you like and finds others that share a similar DNA, leading to more relevant and personalized suggestions.

## ⚙️ Tech Stack

- **Python**: Core programming language.
- **Pandas**: For data manipulation and cleaning.
- **Scikit-learn**: For vectorization (`CountVectorizer`) and similarity calculation (`cosine_similarity`).
- **NLTK**: For Natural Language Processing tasks like stemming.
- **Streamlit**: For building and deploying the interactive user interface.
- **TMDB API**: Used to fetch movie posters and enhance the user experience.
- **Pickle**: For serializing and loading the pre-computed model artifacts.

## 🧩 The Pipeline

The recommendation engine is built through a multi-stage data processing pipeline:
1.  **Data Loading & Merging**: Two datasets (movies and credits) are loaded and merged into a single DataFrame. Both datasets can be donwloaded from Kaggle here: [https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata)
2.  **Feature Extraction**: Relevant features like `overview`, `genres`, `keywords`, `cast` (top 3), and `director` are extracted. Complex stringified columns are parsed to isolate key tags.
3.  **Corpus Creation**: All extracted textual features are combined into a single "tags" corpus for each movie, forming the basis for comparison.
4.  **Text Preprocessing**: The corpus is cleaned by lowercasing all text and applying **stemming** to normalize words (e.g., *action* and *actions* become the same token). Names are concatenated to be treated as single entities (e.g., "Sam Worthington" becomes "SamWorthington").
5.  **Vectorization**: The text corpus is converted into a numerical matrix using a Bag-of-Words model (`CountVectorizer`), where each movie is represented as a vector based on its word counts.
6.  **Similarity Calculation**: **Cosine similarity** is used to calculate the similarity score between every pair of movies, resulting in a comprehensive similarity matrix.
7.  **Recommendation UI**: The Streamlit app loads the pre-computed similarity matrix, takes a user's movie choice, and returns the top 5 most similar movies, fetching their posters via the TMDB API.

## 💡 Key Concepts Explained

**Why Content-Based Filtering?**

This method uses the intrinsic properties of items (in this case, movie attributes) to recommend other items with similar properties. It's effective because it doesn't require any user data, avoiding the "cold start" problem common in other recommender types.

**Why Cosine Similarity?**

Cosine similarity is ideal for text analysis because it measures the cosine of the angle between two vectors. This means it evaluates the *orientation* of the vectors, not their magnitude. For text, this is perfect as it tells us if two documents are talking about the same things, regardless of how long the documents are.

## 🚀 Future Plans

-   **Upgrade to TF-IDF**: Move from `CountVectorizer` to `TfidfVectorizer` to give more weight to rare and more significant keywords.
-   **Hybrid Recommender**: Incorporate collaborative filtering (based on user ratings) to create a more robust hybrid model.
-   **Enhanced UI**: Add more details to the results page, such as the movie's rating, overview, and a link to its TMDB page.
-   **Scalability**: For a larger dataset, migrate from pickle files to a database for storing and retrieving movie data and features.

## 📝 Note about deployment
This application is deployed on Streamlit Community Cloud. To ensure the application remains responsive and avoids being put to sleep by the hosting platform's resource management, this repository includes a simple GitHub Action [(.github/workflows/keep-awake.yml)](https://github.com/harsh-c137/Movie-Recommender/blob/main/.github/workflows/keep-awake.yaml) that sends a request to the app every 30 minutes.

## 🤝 Let's Collaborate

If you're interested in building data-driven applications or have ideas for this project, feel free to connect with me on [LinkedIn](https://www.linkedin.com/in/harsh-deshpande-v1/)
