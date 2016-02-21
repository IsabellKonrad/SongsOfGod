import re
import numpy as np
import os
import json
import glob
import argparse
import sys
import subprocess
import scipy
import pandas as pd
from sklearn.multiclass import OneVsRestClassifier
from sklearn.svm import SVC
from sklearn.cross_validation import train_test_split
from sklearn.metrics import classification_report
import pickle


chords_X = ['Ces','as','Ges', 'es', 'Des', '*b', 'As', 'f', 'Es', 'c', 'B', 'g', 'F', 'd', 'C', 
          'a', 'G', 'e', 'D', 'h', 'A', 'fis', 'E', 'cis', 'H', 'gis', 'Fis', 'dis', 
          'Cis', 'ais', 'Gis', 'eis', 'Dis', 'his', 'Ais', 'fisis', 'Eis', 'cisis', 'His']
nX = len(chords_X)
chords_Y = ['As', 'Es', 'B', 'F', 'C', 'G', 'D', 'A', 'E', 'f', 'c', 'g', 'd', 'a', 'e', 'h', 'fis','cis']
nY = len(chords_Y)

def chord_to_number_X(chord):
    if 'moll' in chord:
        chord = chord.lower()
        chord = chord.replace('moll','')
    if 'm' in chord and not 'maj' in chord:
        chord = chord.lower()
        chord = chord.replace('m','')
    if '#' in chord:
        chord = chord.replace('#','is')
    return chords_X.index(chord)


def get_x_vec(content):
    content_list = content.split('[')
    chords = []
    for con in content_list[1:]:
        chord = con.split(']')[0]
        if '/' in chord:
            chord = chord.split('/')[0]
        if '\\' in chord:
            chord = chord.split('\\')[0]
        if '|' in chord:
            chord = chord.replace('|','')
        chords.append(chord)
    
    x_vec = np.zeros(shape=(1,nX))
    for chord in chords:
        number = chord_to_number_X(chord)
        x_vec[0][number] += 1
    return x_vec



def use_classifier(content):
    x_vec = get_x_vec(content)
    x_vec = x_vec.astype(int)
    x_vec = np.reshape(x_vec,(1,nX))
    clf = pickle.load(open("../classifier/classifier.bin", "rb"))

    y_suggest = list(clf.predict_proba(x_vec)[0])
    mode_number1 = max(y_suggest)
    mode1 = chords_Y[y_suggest.index(mode_number1)]
    y_suggest[y_suggest.index(mode_number1)] = 0
    mode_number2 = max(y_suggest)
    mode2 = chords_Y[y_suggest.index(mode_number2)]

    return mode1, mode2
    

def mode_to_song(song_name, mode):
    g = open(song_name,'r')
    content = g.read()
    g.close()
    lines = content.split('\n')
    done = 0
    new_content = ''
    for c_line in lines:
        if done == 1:
            new_line = '%tonart{' + mode + '}'
            new_content = new_content + new_line + '\n'
            done = -1
        if '\\begin{song}' in c_line:
            done = 1
        new_content = new_content + c_line + '\n'
    g = open(song_name,'w')
    g.write(new_content)
    g.close()

