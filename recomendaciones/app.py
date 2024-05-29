from flask import Flask, render_template, jsonify, request
from flask_redis import FlaskRedis
import pandas as pd
import numpy as np
import random
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

# Configuración de la URL de Redis (momentáneamente de manera local)
app.config['REDIS_URL'] = 'redis://localhost:6379/'
# Objeto para interactuar con la BD de Redis
redis_store = FlaskRedis(app)

# Lista de videos de YouTube con géneros, IDs, títulos y miniaturas
videos = [
    {"id": 1, "title": "Video 1", "youtube_id": "eVTXPUF4Oz4", "thumbnail": "https://img.youtube.com/vi/eVTXPUF4Oz4/0.jpg", "genres": ["Documental", "Terror", "VidaReal"], "watch_time": 12},
    {"id": 2, "title": "Video 2", "youtube_id": "eVTXPUF4Oz4", "thumbnail": "https://img.youtube.com/vi/eVTXPUF4Oz4/0.jpg", "genres": ["Pelicula", "VidaReal", "Supenso"], "watch_time": 10},
    {"id": 3, "title": "Video 3", "youtube_id": "eVTXPUF4Oz4", "thumbnail": "https://img.youtube.com/vi/eVTXPUF4Oz4/0.jpg", "genres": ["Tecnologia", "Informacion", "Documental"], "watch_time": 10},
    {"id": 4, "title": "Video 4", "youtube_id": "eVTXPUF4Oz4", "thumbnail": "https://img.youtube.com/vi/eVTXPUF4Oz4/0.jpg", "genres": ["Informacion", "Tecnologia", "Comedia"], "watch_time": 20},
    {"id": 5, "title": "Video 5", "youtube_id": "eVTXPUF4Oz4", "thumbnail": "https://img.youtube.com/vi/eVTXPUF4Oz4/0.jpg", "genres": ["Pelicula", "Comedia", "Fantasia"], "watch_time": 5},
    {"id": 6, "title": "Video 6", "youtube_id": "eVTXPUF4Oz4", "thumbnail": "https://img.youtube.com/vi/eVTXPUF4Oz4/0.jpg", "genres": ["CienciaFiccion", "Accion", "Aventura"], "watch_time": 5},
    {"id": 7, "title": "Video 7", "youtube_id": "eVTXPUF4Oz4", "thumbnail": "https://img.youtube.com/vi/eVTXPUF4Oz4/0.jpg", "genres": ["Documental", "Musica", "Informacion"], "watch_time": 2},
    {"id": 8, "title": "Video 8", "youtube_id": "eVTXPUF4Oz4", "thumbnail": "https://img.youtube.com/vi/eVTXPUF4Oz4/0.jpg", "genres": ["Drama", "Suspenso", "Terror"], "watch_time": 5},
    {"id": 9, "title": "Video 9", "youtube_id": "eVTXPUF4Oz4", "thumbnail": "https://img.youtube.com/vi/eVTXPUF4Oz4/0.jpg", "genres": ["Terror", "Comedia", "Documental"], "watch_time": 4},
    {"id": 10, "title": "Video 10", "youtube_id": "eVTXPUF4Oz4", "thumbnail": "https://img.youtube.com/vi/eVTXPUF4Oz4/0.jpg", "genres": ["Fantasia", "Aventuras", "Accion"], "watch_time": 14},
    {"id": 11, "title": "Video 11", "youtube_id": "eVTXPUF4Oz4", "thumbnail": "https://img.youtube.com/vi/eVTXPUF4Oz4/0.jpg", "genres": ["Accion", "Comedia", "Fantasia"], "watch_time": 11},
    {"id": 12, "title": "Video 12", "youtube_id": "eVTXPUF4Oz4", "thumbnail": "https://img.youtube.com/vi/eVTXPUF4Oz4/0.jpg", "genres": ["Romatica", "Comedia", "Drama"], "watch_time": 11},
    {"id": 13, "title": "Video 13", "youtube_id": "eVTXPUF4Oz4", "thumbnail": "https://img.youtube.com/vi/eVTXPUF4Oz4/0.jpg", "genres": ["Drama", "Supenso", "Accion"], "watch_time": 3},
]

# Convertir la lista de videos a un DataFrame
df = pd.DataFrame(videos)

# Función para limpiar y preparar el texto
def clean_text(text):
    return ' '.join(str(text).lower().replace(' ', '') for text in text)

df['genres'] = df['genres'].apply(clean_text)
df['title'] = df['title'].str.lower()

# Crear una matriz de características basada en los géneros
vectorizer = CountVectorizer()
genre_matrix = vectorizer.fit_transform(df['genres'])

# Calcular las similitudes de coseno entre los géneros
genre_similarities = cosine_similarity(genre_matrix)

# Función para obtener recomendaciones de videos basadas en el tiempo de visualización y el género
def get_video_recommendations(video_id):
    # Obtener el índice del video actual
    current_video_idx = df.index[df['id'] == video_id][0]
    
    # Calcular la similitud de género entre el video actual y todos los demás videos
    genre_similarity_scores = genre_similarities[current_video_idx]
    
    # Calcular el tiempo de visualización promedio para todos los videos
    average_watch_time = np.mean([video['watch_time'] for video in videos])
    
    # Calcular la puntuación de afinidad para cada video
    affinity_scores = []
    for idx, video in enumerate(videos):
        if idx != current_video_idx:
            watch_time = video['watch_time']
            genre_similarity_score = genre_similarity_scores[idx]
            affinity_score = watch_time * genre_similarity_score
            affinity_scores.append((video, affinity_score))
    
    # Ordenar las recomendaciones por la puntuación de afinidad en orden descendente
    sorted_recommendations = sorted(affinity_scores, key=lambda x: x[1], reverse=True)
    
    return [recommendation[0] for recommendation in sorted_recommendations]

@app.route('/')
def index():
    random_video = random.choice(videos)
    return render_template('index.html', video=random_video)

@app.route('/recommendations', methods=['POST'])
def recommendations():
    data = request.get_json()
    video_id = data.get('video_id')
    recommendations = get_video_recommendations(video_id)
    
    # Preparar la respuesta con títulos y thumbnails
    response = [{"title": video['title'], "thumbnail": video['thumbnail'], "youtube_id": video['youtube_id']} for video in recommendations]
    
    return jsonify(response)

@app.route('/save_watch_time', methods=['POST'])
def save_watch_time():
    data = request.get_json()
    video_id = data.get('video_id')
    watch_time = data.get('watch_time')
    total_time = data.get('total_time')
    genre = data.get('genre')
    # Salida para verificar que los datos llegan correctamente
    print(f"Video ID: {video_id}, Watch Time: {watch_time}, Total Time: {total_time}, Genre: {genre}")
    # Guardar en Redis los datos obtenidos
    redis_key = f"video:{video_id}"
    redis_store.hset(redis_key, "watch_time", watch_time)
    redis_store.hset(redis_key, "genre", genre)
    return jsonify({"status": "success"})

@app.route('/get_recommendations/<int:video_id>', methods=['GET'])
def get_recommendations(video_id):
    recommendations = get_video_recommendations(video_id)
    return jsonify(recommendations)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True, threaded=True)
