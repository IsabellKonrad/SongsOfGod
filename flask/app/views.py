from flask import render_template, request, jsonify, url_for
from app import app
import json
import glob
import os.path
import subprocess


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


def create_pdf(song, mode):
    delete_pdfs_texs()

    songpath = '../songs/' + song + '_' + mode
    latex_head_path = 'app/static/latex_head.txt'
    f = open(latex_head_path, 'r')
    latex_head = f.read()
    f.close()

    content = latex_head + \
        '\n \\input{' + songpath + '}\n \\end{multicols}\n\\end{document}'

    tex_path = song + '_' + mode
    g = open('app/static/' + tex_path + '.tex', 'w')
    g.write(content)
    g.close()

    subprocess.call(['pdflatex', 'app/static/' + tex_path + '.tex'])
    os.remove(tex_path + '.log')
    os.remove(tex_path + '.aux')
    os.remove(tex_path + '.out')
    os.rename(tex_path + '.pdf', 'app/static/' + tex_path + '.pdf')


@app.route('/getsong', methods=['GET', 'POST'])
def getsong(song="hereiam"):
    content = request.get_json(silent=True)
    song = content["song"]
    mode = content["mode"]
    lyrics = get_lyrics(song, mode)
    create_pdf(song, mode)
    source_url = url_for('static', filename='./' + song + '_' + mode + '.pdf')
    tex_path = '<embed id="show_pdf" src="' + source_url + \
        '" width="600" height="700" type="application/pdf">'
    return jsonify({"song": song,
                    "lyrics": lyrics,
                    "path": tex_path
                    })
