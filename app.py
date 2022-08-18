from flask import Flask, render_template, request
from utils import *


app  = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        upload_file = request.files['image_name']
        filename = upload_file.filename
        path_save = os.path.join(UPLOAD_PATH, filename)
        upload_file.save(path_save)
        text = OCR(path_save, filename)
        return render_template('index.html', upload=True, upload_image=filename, text=text)
    return render_template('index.html', upload=False)


if __name__ == "__main__":
    app.run(host=HOST, port=PORT)