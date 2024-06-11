from flask import Flask, request, send_file
from PIL import Image
import numpy as np
import tensorflow as tf
import tensorflow_hub as hub
import io

app = Flask(__name__)

# ESRGANのモデルをロード
model = hub.load("https://tfhub.dev/captain-pool/esrgan-tf2/1")

@app.route('/')
def index():
    return send_file('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    img = Image.open(file.stream).convert('RGB')

    # 画像を超解像処理
    img_array = np.array(img).astype(np.float32) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    result = model(img_array)
    result = tf.clip_by_value(result, 0, 1)
    result = tf.squeeze(result).numpy()
    result = (result * 255).astype(np.uint8)

    result_img = Image.fromarray(result)
    img_byte_arr = io.BytesIO()
    result_img.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)

    return send_file(img_byte_arr, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)
