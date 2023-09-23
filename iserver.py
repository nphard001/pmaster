"""
A quick image picker powered by ChatGPT
"""

from flask import Flask, render_template, send_from_directory, request, jsonify
import os
import shutil
from loguru import logger

app = Flask(__name__)
image_folder = r"C:\dat\sdgen\XL01\0922face\ptest"
target_folder = r"C:\dat\sdgen\XL01\0922face"

@app.route('/')
def index():
    images = [f for f in os.listdir(image_folder) if f.lower().endswith(('png', 'jpg', 'jpeg'))]
    images.sort()

    return render_template('index.html', images=images, folder=image_folder)

@app.route('/image/<path:filename>')
def send_image(filename):
    return send_from_directory(image_folder, filename)

@app.route('/move_images', methods=['POST'])
def move_images():
    data = request.json  # 從 request 對象中獲取 JSON 數據
    selected_filenames = data.get('filenames', [])  # 使用正確的方式獲取 'filenames'
    for filename in selected_filenames:
        src_path = os.path.join(image_folder, filename)
        dst_path = os.path.join(target_folder, filename)
        logger.info(f"<moving>\n{src_path}\n{dst_path}")
        shutil.move(src_path, dst_path)

    return jsonify({'message': 'Images moved successfully'})

if __name__ == '__main__':
    app.run(debug=False)
