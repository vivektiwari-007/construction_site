from flask import Flask, render_template, request, send_from_directory
import os
from ultralytics import YOLO
from moviepy.editor import *

app = Flask(__name__)

# Set the path for the uploaded images
UPLOAD_FOLDER = 'media'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

img = os.path.join('static', 'Image', 'predict')
print('img',img)

current_path = os.getcwd()

@app.route('/')
def upload_file():
    return render_template('upload.html')


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp4'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/uploader', methods=['GET', 'POST'])
def upload_file_result():
    if request.method == 'POST':
        f = request.files['file']
        if f.filename == '':
            return render_template('error.html')
        if f and allowed_file(f.filename):
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], f.filename)
            f.save(file_path)
            model = YOLO(f'{current_path}\models\\best.pt')
            # results = model.predict(file_path, save=True, imgsz=320, conf=0.5, project=f"{current_path}/static/Image/", exist_ok=True,stream=True)
            results = model.predict(file_path, save=True, imgsz=320, conf=0.5, project=f"{current_path}/static/Image/", exist_ok=True)
            if results:
                image_file = ""
                video_file = ""
                message = []
                if f.filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}:
                    image_file = os.path.join(img, f.filename)
                elif f.filename.rsplit('.', 1)[1].lower() in {'mp4'}:
                    filename = f"{f.filename[0]}.avi"
                    avi_file = os.path.join(img, filename)
                    clip = VideoFileClip(avi_file)
                    mp4_file = os.path.join(img, f.filename)
                    clip.write_videofile(mp4_file)
                    video_file = os.path.join(img, f.filename)
                else:
                    return render_template('error.html')
                # for result in results:
                #     values = result.boxes.cls
                #     integer_value = values.int()
                #     if 5 in integer_value:
                #         if 4 in integer_value:
                #             print("Not wearing safety west")
                #         if 2 in integer_value:
                #             print("Not wearing Hardhat")
                #         if 3 in integer_value:
                #             print("Not wearing mask")
                # print(video_file,"video_file")
                return render_template('result.html',  image_filename=image_file, video_filename=video_file)
            return render_template('error.html')
        return render_template('error.html')

    if request.method == 'GET':
        path = f'{current_path}\\runs\detect'
        print("path",path)
        return render_template('result.html', file_path=path)

if __name__ == '__main__':
    app.run(host='0.0.0.0')