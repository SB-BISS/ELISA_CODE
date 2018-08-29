import Structures
import numpy
import pickle
import numpy as np
import pandas as pd
from keras.models import Sequential
from keras.layers import Dense
from keras.wrappers.scikit_learn import KerasClassifier
from keras.utils import np_utils
from keras.layers import Dropout
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.preprocessing import LabelEncoder
from keras.optimizers import SGD
from sklearn.pipeline import Pipeline
from pyAudioAnalysis import audioBasicIO
from pyAudioAnalysis import audioFeatureExtraction
import os
import re
import matplotlib.pyplot as plt
from sklearn.externals import joblib
import array
from pydub import AudioSegment
from pydub.utils import get_array_type
import pandas as pd
from matplotlib import pyplot as plt


class EmotionExtractor:


        def __init__(self, filename_baseline,filename_mean_sd):
            self.structure = Structures.Structures(3, 34, 7, 256)
            self.my_attention_network = self.structure.structure_11_cnn_attention_dot()
            #load weights
            self.my_attention_network.load_weights(filename_baseline)
            self.dictionary =   pickle.load(open(filename_mean_sd, "rb"))
            self.mean_train = self.dictionary.get("mean")
            self.sd_train = self.dictionary.get("sd")

        def extract_features(self, file_path):
            [Fs, x] = audioBasicIO.readAudioFile(file_path)

            x = audioBasicIO.stereo2mono(x)  # necessary conversion for pyaudio analysis
            features = audioFeatureExtraction.stFeatureExtraction(x, Fs, 0.05 * Fs, 0.025 * Fs)
            features = np.mean(features, axis=1)
            features = np.asarray(features).reshape(len(features), -1).transpose()
            # features_complete = np.append(features_complete, features, axis=0)
            return features  # _complete

        def extract_features2(self, Fs, x):
            x = audioBasicIO.stereo2mono(x)  # necessary conversion for pyaudio analysis
            # print len(x)

            # they must be 24k samples
            # coef = int(np.floor(len(x)/48000))

            # x = x[range(0,len(x),6)]
            # print len(x)
            # Fs=16000
            
            
            
            features = audioFeatureExtraction.stFeatureExtraction(x, Fs, 0.05 * Fs, 0.025 * Fs)
            if len(features) == 0:
                features = np.zeros((34,2))
 
            features = np.mean(features, axis=1)
            features = np.asarray(features).reshape(len(features), -1).transpose()
            # features_complete = np.append(features_complete, features, axis=0)
            return features  # _complete

        def split_song(self, song):
            mydict = []
            convers = []

            for i in range(3000, len(song), 3000):
                # print i
                splitting = song[i - 3000:i]  # first three seconds
                bit_depth = splitting.sample_width * 16
                # print splitting.frame_rate
                array_type = get_array_type(bit_depth)
                numeric_array = array.array(array_type, splitting._data)
                numeric_array = numeric_array.tolist()
                features = self.extract_features2(splitting.frame_rate, np.asarray(numeric_array))[0]
                features_transformed = (features - self.mean_train) / self.sd_train
                convers.append(features_transformed)
                if len(convers) == 3:
                    prediction = self.my_attention_network.predict(np.array([convers]))[0]
                    # print prediction
                    mydict.append({"Anger": prediction[0], "Disgust": prediction[1], "Fear": prediction[3],
                                   "Happiness": prediction[5], "Neutral": prediction[6], "Sadness": prediction[2],
                                   "Surprise": prediction[4]})
                    convers.pop(0)

            data_frame_emotions = pd.DataFrame.from_dict(mydict)
            return data_frame_emotions


        def split_single_song(self, song,splits):
          
            mydict = []
            convers = []
           
            #increment = 3000
            #if len(song)< 9000:
            increment = int(float(len(song))/splits)

            for i in range(increment,len(song)+increment, increment):
                # print i
                splitting = song[i-increment:i]  # first incremement seconds
                bit_depth = splitting.sample_width * 8
                
                # print splitting.frame_rate
                array_type = get_array_type(bit_depth)
              
                
                numeric_array = array.array(array_type, splitting._data)
                numeric_array = numeric_array.tolist()
                features = self.extract_features2(splitting.frame_rate, np.asarray(numeric_array))[0]
                features_transformed = (features - self.mean_train) / self.sd_train
                convers.append(features_transformed)
                
                if len(convers) == 3:
                    
                    prediction = self.my_attention_network.predict(np.array([convers]))[0]
            
                    mydict.append({"Anger": prediction[0], "Disgust": prediction[1], "Fear": prediction[3],
                                   "Happiness": prediction[5], "Neutral": prediction[6], "Sadness": prediction[2],
                                   "Surprise": prediction[4]})
                    #convers.pop(0)
                    

            data_frame_emotions = pd.DataFrame.from_dict(mydict)
            return data_frame_emotions