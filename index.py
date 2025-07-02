import streamlit as st
import pickle

try:
    with open('movies_list.pkl', 'rb') as f:
        movies_list = pickle.load(f)
    my_movies = movies_list['title'].values

    with open('similarity.pkl', 'rb') as f:
        similarity = pickle.load(f)
except FileNotFoundError:
    st.error("Error: Make sure 'movies_list.pkl' and 'similarity.pkl' are in the same directory.")
    st.stop()

def recommendmemovies(moviename, number):
    if moviename not in movies_list['title'].values:
        return []

    movie_index = movies_list[movies_list['title'] == moviename].index[0]
    distances = similarity[movie_index]

    sorted_movies = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:number + 1]
    recommend_movies = []
    for i in sorted_movies:
        recommend_movies.append(movies_list.iloc[i[0]].title)
    return recommend_movies

if 'movie_chosen' not in st.session_state:
    st.session_state.movie_chosen = None
if 'recommend_button_clicked' not in st.session_state:
    st.session_state.recommend_button_clicked = False
if 'show_number_selection' not in st.session_state:
    st.session_state.show_number_selection = False
if 'number_of_movies_selected' not in st.session_state:
    st.session_state.number_of_movies_selected = None

st.title('Movie Recommender')

thechossenone = st.selectbox(
    'Choose a movie to see recommendations',
    my_movies,
    index=0,
    key='movie_selection'
)


if thechossenone != st.session_state.movie_chosen:
    st.session_state.movie_chosen = thechossenone
    st.session_state.show_number_selection = False
    st.session_state.recommend_button_clicked = False
    st.session_state.number_of_movies_selected = None
    st.rerun()
if st.button('Go ahead'):
    st.session_state.show_number_selection = True
    st.session_state.recommend_button_clicked = False 

if st.session_state.get('show_number_selection', False) and st.session_state.movie_chosen:
    numbers = list(range(1, 11))
    numberofmovies = st.selectbox(
        f'Choose the number of movies you want similar to {st.session_state.movie_chosen}',
        (numbers),
        key='num_movies_selection'
    )

    st.session_state.number_of_movies_selected = numberofmovies

    if st.button('Recommend'):
        st.session_state.recommend_button_clicked = True

if st.session_state.recommend_button_clicked and st.session_state.movie_chosen and st.session_state.number_of_movies_selected is not None:
    givenmovies = recommendmemovies(st.session_state.movie_chosen, st.session_state.number_of_movies_selected)
    if givenmovies:
        st.write('---')
        st.subheader(f'Movies Similar To "{st.session_state.movie_chosen}" Are:--')
        count = 1
        for movie in givenmovies:
            st.write(count,movie)
            count += 1
    else:
        st.write(f"Could not find recommendations for **{st.session_state.movie_chosen}**. Please try another movie or adjust the number of recommendations.")