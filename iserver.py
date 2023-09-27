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
root_folder = r"C:\dat\sdgen\XL01"
target_folder = root_folder

@app.route('/', defaults={'subdir': ''})
@app.route('/<path:subdir>')
def index(subdir):
    image_folder = os.path.join(root_folder, subdir)

    def get_info(f, fast=False):
        if fast:
            return f"{f}", f"{f}"
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
        return "\n".join(outputs[1:]), "\n".join(outputs)

    idata = [
        {"filename": f}
        for f in os.listdir(image_folder) if f.lower().endswith(('png', 'jpg', 'jpeg'))
    ]

    for table in idata:
        info1, info2 = get_info(table["filename"], fast=False)
        table["info1"] = info1
        table["info2"] = info2
    return render_template('index.html', idata=idata, folder=image_folder, subdir=subdir)

@app.route('/image/<path:subdir>/<filename>')
def send_image(subdir, filename):
    send_from_dir = os.path.join(root_folder, subdir)
    return send_from_directory(send_from_dir, filename)

@app.route('/move_images', methods=['POST'])
def move_images():
    data = request.json
    selected_filenames = data.get('filenames', [])
    current_subdir = data.get('subdir', '')

    for filename in selected_filenames:
        src_path = os.path.join(root_folder, current_subdir, filename)
        dst_path = os.path.join(target_folder, filename)
        logger.info(f"<moving>\n{src_path}\n{dst_path}")
        shutil.move(src_path, dst_path)

    return jsonify({'message': 'Images moved successfully'})

if __name__ == '__main__':
    app.run(debug=False)
