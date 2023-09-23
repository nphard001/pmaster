"""
A quick image picker powered by ChatGPT
"""

from flask import Flask, render_template, send_from_directory, request, jsonify
import os
import json
import shutil
from loguru import logger

app = Flask(__name__)
image_folder = r"C:\dat\sdgen\XL01\0922face\ptest"
target_folder = r"C:\dat\sdgen\XL01\0922face"

# testing data
st = [{"a":5, "b":6}, {"x":-1, "y":0, "z":3.14}]
raw = r"""
.PHONY: gin
gin:
	@if [ ! -d "/active/codrive" ]; then \
		echo "Error: /active/codrive does not exist. NFS not mounted."; \
		exit 1; \
	fi
    """.strip()
uberlong = ("yolo"*1000)

@app.route('/')
def index():
    idata = [f for f in os.listdir(image_folder) if f.lower().endswith(('png', 'jpg', 'jpeg'))]
    idata = [
        {"filename": f, "info": f"{f}\n{uberlong}\nsome_extra_info1\nsome_extra_info2\nsome_extra_info3\n{json.dumps(st, indent=1)}\n{raw}"}
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
