from flask import Flask, request, jsonify, render_template, redirect, url_for,request
import pickle
import os
import python_speech_features
import soundfile
import librosa
import numpy as np
import ntpath
import wave
import pandas as pd
import tqdm
### Integrate HTML With Flask
### HTTP verb GET And POST

##Jinja2 template engine
dataset = pd.read_csv('./static/dataset.csv')

df = dataset.drop(columns=['id', 'name', 'artists', 'release_date', 'year'])
class Spotify_Recommendation():
    def __init__(self, dataset):
        self.dataset = dataset
    def recommend(self, songs, amount=1):
        print(dataset)
        distance = []
        song = self.dataset[(self.dataset.name.str.lower() == songs.lower())].head(1).values[0]
        rec = self.dataset[self.dataset.name.str.lower() != songs.lower()]
        for songs in rec.values:
            d = 0
            for col in np.arange(len(rec.columns)):
                if not col in [2, 7, 13, 15, 19]:
                    d = d + np.absolute(float(song[col]) - float(songs[col]))
            distance.append(d)
        rec['distance'] = distance
        rec = rec.sort_values('distance')
        columns = ['artists', 'name']
        return rec[columns][:amount]

app=Flask(__name__)

@app.route('/')
def welcome():
    return render_template('index.html')
list = []
@app.route('/submit',methods=['POST','GET'])
def submit():
    if request.method=='POST':
        songs = str(request.form['song'])
        number = int(request.form['number'])
        if songs == "" or number == "":
            return redirect(request.url)
    recommendations = Spotify_Recommendation(dataset)
    s = recommendations.recommend(songs, number)
    df = pd.DataFrame(s)
    for index, row in df.iterrows():
       list.append(row["artists"] + row["name"])
    return render_template('index.html',res=list)

if __name__=='__main__':
    app.run(debug=True)