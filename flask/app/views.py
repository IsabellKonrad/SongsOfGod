from flask import render_template, request, jsonify, url_for
from app import app
import json
import glob
import os.path
import subprocess
from time import gmtime, strftime


def make_songlist():
    g = open('songlist.txt', 'w')
    songs = sorted(glob.glob('../songs/*.tex'))
    for songpath in songs:
        if '_' not in songpath:
            h = open(songpath, 'r')
            content = h.read()
            h.close()
            song = songpath.replace('../songs/', '').replace('.tex', '')
            songname = content.split('begin{song}{')[1].split('}')[0]
            mode = content.split('tonart{')[1].split('}')[0]
            if mode.isupper():
                m = 'Dur'
            else:
                m = 'Moll'
            g.write(song + ':' + songname + ':' + m + '\n')
    g.close()


def get_songlist():
    if not os.path.isfile('songlist.txt'):
        make_songlist()
        songlist = get_songlist()
    else:
        f = open('songlist.txt', 'r')
        songlist = []
        for line in f:
            songlist.append([elem.strip() for elem in line.split(':')])
        f.close()
    return songlist


@app.route('/')
@app.route('/index')
def index():
    songlist = get_songlist()
    return render_template("index.html", songlist=songlist)


def get_lyrics(song, mode):
    songpath = '../songs/' + song + '_' + mode + '.tex'
    f = open(songpath, 'r')
    content = f.read()
    return content


def delete_pdfs_texs():
    all_pdfs = glob.glob('app/static/*.pdf')
    for pdf in all_pdfs:
        os.remove(pdf)
    all_texs = glob.glob('app/static/*.tex')
    for tex in all_texs:
        os.remove(tex)


def create_pdf(songs_and_modes):

    delete_pdfs_texs()
    latex_head_path = 'app/static/latex_head.txt'
    f = open(latex_head_path, 'r')
    latex_head = f.read()
    f.close()

    content = latex_head
    for song, mode in songs_and_modes:
        songpath = '../songs/' + song + '_' + mode
        content = content + '\n \\input{' + songpath + '}\n' 
    content = content + '\\end{multicols}\n\\end{document}'

    path = strftime("%Y%m%d_%H%M%S", gmtime())

    g = open('app/static/' + path + '.tex', 'w')
    g.write(content)
    g.close()

    subprocess.call(['pdflatex', 'app/static/' + path + '.tex'])
    os.remove(path + '.log')
    os.remove(path + '.aux')
    os.remove(path + '.out')
    os.rename(path + '.pdf', 'app/static/' + path + '.pdf')
    return path


@app.route('/getsong', methods=['GET', 'POST'])
def getsong():
    content = request.get_json(silent=True)
    songs_and_modes = zip(content["songs"], content["modes"])
    path = create_pdf(songs_and_modes)
    source_url = url_for('static', filename='./' + path + '.pdf')
    pdf_path = '<embed id="show_pdf" src="' + source_url + \
        '" width="600" height="700" type="application/pdf">'
    return jsonify({"path": pdf_path})