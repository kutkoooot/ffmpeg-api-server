from flask import Flask, request, send_file
import subprocess
import os
import uuid

app = Flask(__name__)
UPLOAD_FOLDER = '/tmp'

@app.route('/merge', methods=['POST'])
def merge():
    image = request.files['image']
    audio = request.files['audio']
    
    scene_id = str(uuid.uuid4())
    image_path = os.path.join(UPLOAD_FOLDER, f"{scene_id}.jpg")
    audio_path = os.path.join(UPLOAD_FOLDER, f"{scene_id}.mp3")
    video_path = os.path.join(UPLOAD_FOLDER, f"{scene_id}.mp4")

    image.save(image_path)
    audio.save(audio_path)

    ffmpeg_cmd = [
        'ffmpeg',
        '-loop', '1',
        '-i', image_path,
        '-i', audio_path,
        '-c:v', 'libx264',
        '-tune', 'stillimage',
        '-c:a', 'aac',
        '-b:a', '192k',
        '-shortest',
        '-pix_fmt', 'yuv420p',
        video_path
    ]

    subprocess.run(ffmpeg_cmd, check=True)

    return send_file(video_path, mimetype='video/mp4')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
