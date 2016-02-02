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


chords_X = ['Ces','as','Ges', 'es', 'Des', 'b', 'As', 'f', 'Es', 'c', 'B', 'g', 'F', 'd', 'C', 
          'a', 'G', 'e', 'D', 'h', 'A', 'fis', 'E', 'cis', 'H', 'gis', 'Fis', 'dis', 
          'Cis', 'ais', 'Gis', 'eis', 'Dis', 'his', 'Ais', 'fisis', 'Eis', 'cisis', 'His']
nX = len(chords_X)
chords_Y = ['As', 'Es', 'B', 'F', 'C', 'G', 'D', 'A', 'E', 'f', 'c', 'g', 'd', 'a', 'e', 'h', 'fis','cis']
nY = len(chords_Y)

def chord_to_number_X(chord):
    if 'moll' in chord:
        chord = chord.lower()
        chord = chord.replace('moll','')
    if '#' in chord:
        chord = chord.replace('#','is')
    return chords_X.index(chord)

#########  Make Classifier #############

def chord_to_number_Y(chord):
    if 'moll' in chord:
        chord = chord.lower()
        chord = chord.replace('moll','')
    if '#' in chord:
        chord = chord.replace('#','is')
    return chords_Y.index(chord)

def get_mode(content):
    mode = content.split('tonart{')[1]
    mode = mode.split('}')[0]
    y_vec = np.zeros(shape=(1,nY))
    number = chord_to_number_Y(mode)
    y_vec[0][number] += 1
    return y_vec

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

def make_X_Y():
    Files = glob.glob('../songs/*.tex')
    X = np.zeros(shape=(0,nX))
    Y = np.zeros(shape=(0,nY))
    for File in Files:
        f=open(File)
        content = f.read()
        if 'tonart' in content:
            x_vec = get_x_vec(content)
            X = np.append(X,x_vec,0)
            y_vec = get_mode(content)
            Y = np.append(Y,y_vec,0)
    return X,Y


def make_classifier():
    test_size=0
    X, y = make_X_Y()
    X_train, X_test, y_train, y_test = train_test_split(X, y,test_size=test_size)
    X_train = X_train.astype(int)
    X_test = X_test.astype(int)
    y_train = y_train.astype(int)
    y_test = y_test.astype(int)
    clf = OneVsRestClassifier(SVC(kernel='linear', class_weight='auto', probability=True))
    clf.fit(X_train, y_train)
    y_suggest = clf.predict_proba(X_test)
    nn = 0
    n = 0
    for y_s, y_t in zip(y_suggest, y_test):
        s1 = chords_Y[np.argmax(y_s)]
        y_s[np.argmax(y_s)]=0
        s2 = chords_Y[np.argmax(y_s)]
        t = chords_Y[np.argmax(y_t)]        
        print 'Suggest: ' + s1 + ' or ' + s2 + '  Real: ' + t
        n = n+1
        if s1==t:
            nn = nn+1
    if n>0:
        print 'Accuracy is ' + str(float(nn)/n)
    #print classification_report(clf.predict(X_test), y_test)
    pickle.dump(clf, open("classifier.bin", "wb"))   


##############  Use Classifiert   #####################

def make_X():
    Files = sorted(glob.glob('../songs/*.tex'))
    X = np.zeros(shape=(0,nX))
    Files_list = []
    for File in Files:
        f=open(File)
        content = f.read()
        if 'tonart' not in content:
            x_vec = get_x_vec(content)
            X = np.append(X,x_vec,0)
            Files_list.append(File)
    return X, Files_list

def use_classifier():
    X, Files_list = make_X()
    X = X.astype(int)
    clf = pickle.load(open("classifier.bin", "rb"))
    f = open('result.txt','w')
    for x_vec, File in zip(X, Files_list):
        x_vec = np.reshape(x_vec,(1,nX))
        y_suggest = list(clf.predict_proba(x_vec)[0])
        mode_number1 = max(y_suggest)
        mode1 = chords_Y[y_suggest.index(mode_number1)]
        y_suggest[y_suggest.index(mode_number1)] = 0
        mode_number2 = max(y_suggest)
        mode2 = chords_Y[y_suggest.index(mode_number2)]
        f.write('%0.2f: %s,  ' % (mode_number1, mode1))
        f.write('%0.2f: %s,  ' % (mode_number2, mode2))
        f.write('   ')
        f.write(File.split('/')[1].split('.tex')[0])
        f.write('\n')

    f.close()
    

def mode_to_song(song_name, mode):
    g = open('../songs/' + song_name + '.tex','r')
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
    return new_content

def set_suggested_mode():
    f = open('result.txt','r')
    for line in f:
        song_name = line.split(',')[-1].strip()
        mode = line.split(',')[0].split(':')[1].strip()
        new_content = mode_to_song(song_name, mode)
                    
        h = open('../songs/' + line.split(',')[-1].strip() + '-s.tex','w')
        h.write(new_content) 
        h.close()
    f.close()