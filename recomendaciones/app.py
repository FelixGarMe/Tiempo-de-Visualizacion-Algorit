from flask import Flask, render_template, jsonify, request
from flask_redis import FlaskRedis
import redis

app = Flask(__name__)
# Configuracion de la URL de Redis (momentaneamente de manera local)
app.config['REDIS_URL'] = 'redis://localhost:6379/'
# Objeto para interactuar con la BD de Redis
redis_store = FlaskRedis(app)
@app.route('/')
def index():
    # Lista de videos de YouTube con géneros, IDs, títulos y miniaturas
    videos = [
        {"id": 1, "title": "Video 1", "youtube_id": "dQw4w9WgXcQ", "thumbnail": "https://img.youtube.com/vi/dQw4w9WgXcQ/0.jpg", "genre": "Peliculas"},
        {"id": 2, "title": "Video 2", "youtube_id": "3JZ_D3ELwOQ", "thumbnail": "https://img.youtube.com/vi/3JZ_D3ELwOQ/0.jpg", "genre": "Gaming"},
        {"id": 3, "title": "Video 3", "youtube_id": "9bZkp7q19f0", "thumbnail": "https://img.youtube.com/vi/9bZkp7q19f0/0.jpg", "genre": "Musica"},
        {"id": 4, "title": "Video 4", "youtube_id": "eVTXPUF4Oz4", "thumbnail": "https://img.youtube.com/vi/eVTXPUF4Oz4/0.jpg", "genre": "Documentales"},
        {"id": 5, "title": "Video 5", "youtube_id": "C0DPdy98e4c", "thumbnail": "https://img.youtube.com/vi/C0DPdy98e4c/0.jpg", "genre": "Tecnologia"},
    ]
    return render_template('index.html', videos=videos)

@app.route('/save_watch_time', methods=['POST'])
def save_watch_time():
    data = request.get_json()
    video_id = data.get('video_id')
    watch_time = data.get('watch_time')
    total_time = data.get('total_time')
    genre = data.get('genre')
    # Salida
    print(f"Video ID: {video_id}, Watch Time: {watch_time}, Total Time: {total_time}, Genre: {genre}")
    # Guardar en Redis los datos obtenidos
    redis_key = f"{video_id}"
    redis_store.hset(redis_key, "watch_time", watch_time)
    redis_store.hset(redis_key, "genre", genre)
    return jsonify({"status": "success"})

if __name__ == '__main__':
    app.run(debug=True)
