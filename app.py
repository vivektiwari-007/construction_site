from flask import Flask, render_template, request, send_from_directory
import os, shutil
from ultralytics import YOLO
from moviepy.editor import *

app = Flask(__name__)

# Set the path for the uploaded images
UPLOAD_FOLDER = 'media'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

img = os.path.join('static', 'Image', 'predict')
print('img',img)

current_path = os.getcwd()
static_path = os.path.join(current_path, 'static', 'Image','predict')
media_path = os.path.join(current_path, 'media')
print("static_path",static_path)
print("media_path",media_path)

@app.route('/')
def upload_file():
    return render_template('upload.html')


#create delete file or folder function
def delete_file():
    if os.path.exists(static_path):
        for filename in os.listdir(static_path):
            file_path = os.path.join(static_path, filename)
            try:
                if os.path.isfile(file_path):
                    os.system('sudo rm {}'.format(file_path))
                elif os.path.isdir(file_path):
                    os.system('sudo rm -r {}'.format(file_path))
            except Exception as e:
                print(f"Error: {e}")
        print("All files and folders have been deleted.")
    else:
        print(f"The folder {static_path} does not exist.")
    if os.path.exists(media_path):
        for filename in os.listdir(media_path):
            file_path = os.path.join(media_path, filename)
            try:
                if os.path.isfile(file_path):
                    os.system('sudo rm {}'.format(file_path))
                elif os.path.isdir(file_path):
                    os.system('sudo rm -r {}'.format(file_path))
            except Exception as e:
                print(f"Error: {e}")
        print("All files and folders have been deleted.")
    else:
        print(f"The folder {media_path} does not exist.")


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp4'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/uploader', methods=['GET', 'POST'])
def upload_file_result():
    if request.method == 'POST':
        delete_file()
        f = request.files['file']
        if f.filename == '':
            return render_template('error.html', error_message="File not selected")
        if f and allowed_file(f.filename):
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], f.filename)
            size_bytes = os.path.getsize(file_path)
            size_mb = size_bytes / (1024 * 1024)
            if size_mb > 2:
                return render_template('error.html', error_message="Please upload less then 2 mb of file")
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
                    return render_template('error.html', error_message="File does not supported")
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
            return render_template('error.html', error_message="File does not supported")
        return render_template('error.html', error_message="File does not supported")

    if request.method == 'GET':
        path = f'{current_path}\\runs\detect'
        print("path",path)
        return render_template('result.html', file_path=path)

if __name__ == '__main__':
    app.run(host='0.0.0.0')