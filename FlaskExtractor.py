#!flask/bin/python
from flask import Flask
import jsonify
import EmotionExtractor.EmotionExtractor
import os
from flask import Flask, request, redirect, url_for
from werkzeug.utils import secure_filename
from pydub import AudioSegment

app = Flask(__name__)

UPLOAD_FOLDER = './'
ALLOWED_EXTENSIONS = set(['mp3'])

em = EmotionExtractor('./baseline.npy','baselnine_mean_sd.pickle')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/extract_song',methods=['GET', 'POST'])
def extract_song():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            #flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            #flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            song = AudioSegment.from_mp3(filename)
            data_frame_emotions = em.split_single_song(song)
            return jsonify(data_frame_emotions)

    return "{}"

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


if __name__ == '__main__':
    app.run(debug=True)