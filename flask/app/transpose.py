import numpy as np
import os
import glob
import sys
import subprocess
import scipy

chords = ['Ces','as','Ges', 'es', 'Des', '*b', 'As', 'f', 'Es', 'c', 'B', 'g', 'F', 'd', 'C', 
          'a', 'G', 'e', 'D', 'h', 'A', 'fis', 'E', 'cis', 'H', 'gis', 'Fis', 'dis', 
          'Cis', 'ais', 'Gis', 'eis', 'Dis', 'his', 'Ais', 'fisis', 'Eis', 'cisis', 'His']

chords_jazz = ['Cb','Abm','Gb', 'Ebm', 'Db', 'Bbm', 'Ab', 'Fm', 'Eb', 'Cm', 'Bb', 'Gm', 'F', 'Dm', 'C', 
          'Am', 'G', 'Em', 'D', 'Bm', 'A', 'F#m', 'E', 'C#m', 'B', 'G#m', 'F#', 'D#m', 
          'C#', 'A#m', 'G#', 'E#m', 'D#', 'B#m', 'A#', 'F##m', 'E#', 'C##m', 'B#']

def chord_to_number(chord):
    if 'moll' in chord:
        chord = chord.lower()
        chord = chord.replace('moll','')
    if 'm' in chord and not 'maj' in chord:
        chord = chord.lower()
        chord = chord.replace('m','')
    if '#' in chord:
        chord = chord.replace('#','is')
    return chords.index(chord)

def get_mode(content):
    mode = content.split('tonart{')[1].split('}')[0]
    return mode 

def transpose_chord(old_chord, new_mode, old_mode, jazz):
    number = chord_to_number(old_chord)
    number = number - old_mode
    new_number = number + new_mode
    if jazz:
        new_chord = chords_jazz[new_number]
    else:
        new_chord = chords[new_number]
    return new_chord

def set_new_mode(content, new_mode, old_mode):
    return content.replace('%tonart{' + old_mode, '%tonart{' + new_mode)

def handle_inner(inner, new_mode_number, old_mode_number, jazz):
    if '\\' in inner:
        old_chord = inner.split('\\')[0]
        addendum = inner.split('\\')[1]
        new_chord = transpose_chord(old_chord, new_mode_number, old_mode_number, jazz)
        new_chord = new_chord + '\\' + addendum
    elif '|' in inner:
        old_chord = inner.replace('|','')
        new_chord = transpose_chord(old_chord, new_mode_number, old_mode_number, jazz)
        new_chord = new_chord + '|'
    else:
        new_chord = transpose_chord(inner, new_mode_number, old_mode_number, jazz)
    return new_chord

def transpose_song(content, new_mode, jazz=False):
    old_mode = get_mode(content)
    new_mode_number = chord_to_number(new_mode)
    old_mode_number = chord_to_number(old_mode)
    
    old_content = content.split('[')
    new_content = old_content[0]
    for part in old_content[1:]:
        inner = part.split(']')[0]
        inner = inner.strip() 
        if '/' in inner:
            old_chord1 = inner.split('/')[0]
            old_chord2 = inner.split('/')[1]
            new_chord1 = handle_inner(old_chord1, new_mode_number, old_mode_number, jazz)
            new_chord2 = handle_inner(old_chord2, new_mode_number, old_mode_number, jazz)
            new_chord = new_chord1 + '/' + new_chord2
        else:
            new_chord = handle_inner(inner, new_mode_number, old_mode_number, jazz)
        new_content = new_content + '[' + new_chord + ']' + part.split(']')[1]
    new_content = set_new_mode(new_content, new_mode, old_mode)
    return new_content

def transpose_all_songs_all_modes():
    mode_list_major = ['As', 'Es', 'B', 'F', 'C', 'G', 'D', 'A', 'E']
    mode_list_minor = ['f', 'c', 'g', 'd', 'a', 'e', 'h', 'fis','cis']

    for File in sorted(glob.glob('../../songs/*.tex')):
        f=open(File,'r')
        content = f.read()
        f.close()
        old_mode = get_mode(content)
        if old_mode.islower():
            mode_list = mode_list_minor
        else:
            mode_list = mode_list_major
            
        for new_mode in mode_list:
            new_content = transpose_song(content, new_mode)
            new_File = File.split('.tex')[0] + '_' + new_mode + '.tex'
            g = open(new_File,'w')
            g.write(new_content)
            g.close()


