import pickle
from flask import Flask, request, render_template
import logging

with open(r"C:\Users\rajay\Documents\movies_correct.pkl", 'rb') as file:
    df, similarity = pickle.load(file)

app = Flask(__name__)


logging.basicConfig(level=logging.DEBUG)

def recommend(movie, df, similarity, n_recommendations=5):
    movie = movie.strip().lower()
    df['title_lower'] = df['title'].str.lower()

    if movie not in df['title_lower'].values:
        return []
    
    movie_index = df[df['title_lower'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:n_recommendations + 1]
    
    recommended_movies = [df.iloc[i[0]].title for i in movies_list]
    
    return recommended_movies

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    movie = request.form['movie']
    logging.debug(f"User input: {movie}")
    recommendations = recommend(movie, df, similarity)
    logging.debug(f"Recommendations: {recommendations}")
    return render_template('index.html', recommendations=recommendations, movie=movie)

if __name__ == '__main__':
    app.run(debug=True)
