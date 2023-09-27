"""
A quick image picker powered by ChatGPT
"""

from flask import Flask, render_template, send_from_directory, request, jsonify
import os
import json
import shutil
from loguru import logger
from pmaster.core.img import *

app = Flask(__name__)
image_folder = r"C:\dat\sdgen\XL01\simpleBG\rawUpperExt\part2"
target_folder = r"C:\dat\sdgen\XL01\simpleBG"


@app.route('/')
def index():
    def get_info(f, fast=False):
        if fast:
            return f"{f}"
        s0 = read_pstring(os.path.join(image_folder, f))
        data = parse_pstring(s0)
        p1 = data['pos'].strip().replace(", ", ",")
        p1 = ",".join([part.strip() for part in p1.split(',')])
        p1 = p1.replace(",", ", ")
        outputs = [
            f"<Positive> {p1}",
            f"<File> {f}"
        ]
        if data['score'] > 0:
            outputs.append(f"<Score> {data['score']}")
        return "\n".join(outputs)
    fast_flag = False # turn-on if too many files
    idata = [
        {"filename": f,
         "info": f"{get_info(f, fast=fast_flag)}"}
        for f in os.listdir(image_folder) if f.lower().endswith(('png', 'jpg', 'jpeg'))
    ]
    return render_template('index.html', idata=idata, folder=image_folder)


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
