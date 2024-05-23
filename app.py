from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

@app.route('/')
def index():
    # Lista de videos de YouTube con géneros, IDs, títulos y miniaturas
    videos = [
        {"id": 1, "title": "Video 1", "youtube_id": "dQw4w9WgXcQ", "thumbnail": "https://img.youtube.com/vi/dQw4w9WgXcQ/0.jpg", "genre": "Películas"},
        {"id": 2, "title": "Video 2", "youtube_id": "3JZ_D3ELwOQ", "thumbnail": "https://img.youtube.com/vi/3JZ_D3ELwOQ/0.jpg", "genre": "Gaming"},
        {"id": 3, "title": "Video 3", "youtube_id": "9bZkp7q19f0", "thumbnail": "https://img.youtube.com/vi/9bZkp7q19f0/0.jpg", "genre": "Música"},
        {"id": 4, "title": "Video 4", "youtube_id": "eVTXPUF4Oz4", "thumbnail": "https://img.youtube.com/vi/eVTXPUF4Oz4/0.jpg", "genre": "Documentales"},
        {"id": 5, "title": "Video 5", "youtube_id": "C0DPdy98e4c", "thumbnail": "https://img.youtube.com/vi/C0DPdy98e4c/0.jpg", "genre": "Tecnología"},
    ]
    return render_template('index.html', videos=videos)

@app.route('/save_watch_time', methods=['POST'])
def save_watch_time():
    data = request.get_json()
    video_id = data.get('video_id')
    watch_time = data.get('watch_time')
    total_time = data.get('total_time')
    # Salida
    print(f"Video ID: {video_id}, Watch Time: {watch_time}, Total Time: {total_time}")
    return jsonify({"status": "success"})

if __name__ == '__main__':
    app.run(debug=True)
