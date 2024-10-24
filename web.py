from flask import Flask, render_template, send_from_directory
import os

app = Flask(__name__)

# 定义图片目录路径
IMAGE_DIR = os.path.join(app.root_path, '', 'images')

@app.route('/')
def index():
    # 列出 images 目录下的所有文件
    images = sorted(os.listdir(IMAGE_DIR))

    return render_template('index.html', images=images)

@app.route('/static/images/<filename>')
def get_image(filename):
    return send_from_directory(IMAGE_DIR, filename)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=50005)
