import streamlit as st
import requests
import googleapiclient.discovery

# Function to get anime details from AniList API
def get_anime_details(anime_name):
    query = """
    query ($animeName: String) {
        Media (search: $animeName, type: ANIME) {
            title {
                romaji
                english
                native
            }
            coverImage {
                large
            }
            description
            genres
            episodes
            averageScore
            trending
            siteUrl
        }
    }
    """
    variables = {'animeName': anime_name}
    url = 'https://graphql.anilist.co'
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.post(url, headers=headers, json={'query': query, 'variables': variables})
    data = response.json()

    if 'data' in data and data['data']['Media']:
        anime = data['data']['Media']
        title = anime['title']['romaji'] if anime['title']['romaji'] else anime['title']['native']
        cover_image = anime['coverImage']['large']
        description = anime['description']
        genres = ", ".join(anime['genres'])
        episodes = anime['episodes']
        average_score = anime['averageScore']
        trending = anime['trending']
        url = anime['siteUrl']
        return {
            'title': title,
            'cover_image': cover_image,
            'description': description,
            'genres': genres,
            'episodes': episodes,
            'average_score': average_score,
            'trending': trending,
            'url': url
        }
    else:
        return None

# Function to get anime recommendations by genre
def get_anime_recommendations(genre):
    query = """
    query ($genre: String) {
        Page (perPage: 10) {
            media (genre: $genre, type: ANIME) {
                title {
                    romaji
                    english
                }
                coverImage {
                    large
                }
                siteUrl
            }
        }
    }
    """
    variables = {'genre': genre}
    url = 'https://graphql.anilist.co'
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.post(url, headers=headers, json={'query': query, 'variables': variables})
    data = response.json()

    if 'data' in data and data['data']['Page']['media']:
        return data['data']['Page']['media']
    else:
        return []

# Function to get anime trailer from YouTube using API
def get_anime_trailer(anime_name):
    api_key = "AIzaSyDfcpbArjlrGiEGc9x5W4CNHjPCPkOU6aU"  # Replace with your YouTube API key
    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)
    request = youtube.search().list(
        part="snippet",
        q=f"{anime_name} trailer",
        type="video",
        videoDuration="short"
    )
    response = request.execute()
    if 'items' in response:
        trailer_video = response['items'][0]
        video_id = trailer_video['id']['videoId']
        return f"https://www.youtube.com/watch?v={video_id}"
    else:
        return None

# Streamlit app layout
st.set_page_config(page_title="Anime Search & Recommendations", page_icon="🎭")

# Title and Description
st.markdown("<h1 style='text-align: center; color: red; font-weight: bold; text-decoration: underline;'>ANIME_DV</h1>", unsafe_allow_html=True)
st.write("Search for your favorite anime and get recommendations!")

# Dark Mode Toggle
dark_mode = st.sidebar.checkbox('Enable Dark Mode', value=False)
moon_icon = "🌙" if dark_mode else "☀️"
st.sidebar.markdown(f"{moon_icon} Dark Mode")

# Set theme based on dark_mode toggle
if dark_mode:
    st.markdown("""
        <style>
        body {
            background-color: #121212;
            color: white;
        }
        .stApp {
            background-color: #121212;
        }
        h1, h2, h3, h4, h5, h6, .stTextInput, .stSelectbox, .stButton, .stMarkdown {
            color: white !important;
        }
        .stButton>button {
            background-color: #333;
            color: white;
        }
        .stTextInput>div>input {
            background-color: #333;
            color: white;
        }
        .stTextArea>div>textarea {
            background-color: #333;
            color: white;
        }
        .stSelectbox>div>div>input {
            background-color: #333;
            color: white;
        }
        .stMarkdown {
            color: white;
        }
        .stImage img {
            border-radius: 5px;
        }
        .stTextInput>label {
            color: white;
        }
        .stSelectbox>label {
            color: white;
        }
        </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
        <style>
        body {
            background-color: white;
            color: black;
        }
        .stApp {
            background-color: white;
        }
        h1, h2, h3, h4, h5, h6, .stTextInput, .stSelectbox, .stButton, .stMarkdown {
            color: black !important;
        }
        .stButton>button {
            background-color: #f0f0f0;
            color: black;
        }
        .stTextInput>div>input {
            background-color: #f0f0f0;
            color: black;
        }
        .stTextArea>div>textarea {
            background-color: #f0f0f0;
            color: black;
        }
        .stSelectbox>div>div>input {
            background-color: #f0f0f0;
            color: black;
        }
        .stMarkdown {
            color: black;
        }
        .stImage img {
            border-radius: 5px;
        }
        .stTextInput>label {
            color: black;
        }
        .stSelectbox>label {
            color: black;
        }
        </style>
    """, unsafe_allow_html=True)

# Anime search section
anime_name = st.text_input("Enter the anime you want to search:")
if anime_name:
    anime_details = get_anime_details(anime_name)
    if anime_details:
        st.image(anime_details['cover_image'], width=200)
        st.subheader(f"Title: {anime_details['title']}")
        st.write(f"Genres: {anime_details['genres']}")
        st.write(f"Episodes: {anime_details['episodes']}")
        st.write(f"Score: {anime_details['average_score']}")
        st.write(f"Description: {anime_details['description']}")
        st.markdown(f"[More Info]({anime_details['url']})")
        
        # Fetch and display trailer
        trailer_url = get_anime_trailer(anime_name)
        if trailer_url:
            st.subheader("Watch Trailer:")
            st.markdown(f"[Click here to watch the trailer]( {trailer_url} )")
        else:
            st.write("Trailer not found.")

# Genre-based recommendations section
selected_genre = st.selectbox("Select Genre for Recommendations", ["Action", "Adventure", "Comedy", "Drama", "Fantasy", "Horror", "Romance", "Sci-Fi"])
if st.button('Get Anime Recommendations'):
    recommendations = get_anime_recommendations(selected_genre)
    if recommendations:
        st.subheader(f"Recommendations for Genre: {selected_genre}")
        for anime in recommendations:
            st.image(anime['coverImage']['large'], width=100)
            st.write(anime['title']['romaji'])
            st.markdown(f"[More Info]({anime['siteUrl']})")
    else:
        st.write("No anime found in this genre.")
