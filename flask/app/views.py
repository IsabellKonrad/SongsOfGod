from flask import render_template, request, jsonify, url_for
from app import app
import json
import glob
import os
import sys
import os.path
import subprocess
from time import gmtime, strftime
from transpose import transpose_song
reload(sys)
sys.setdefaultencoding('utf-8')


if 'ubuntu' in os.getcwd():
    # on AWS server where cwd is not set properly. Hence this workaround
    os.chdir('/home/ubuntu/SongsOfGod/flask')

# def make_umlaute(input):
#    input = input.replace('ae', u'\u00e4')
#    input = input.replace('oe', u'\u00f6')
#    input = input.replace('ue', u'\u00fc')
#    input = input.replace('Ae', u'\u00c4')
#    input = input.replace('Oe', u'\u00d6')
#    input = input.replace('Ue', u'\u00dc')
#    return input


def make_songlist():
    g = open('songlist.txt', 'w')
    songs = sorted(glob.glob('../songs/*.tex'))
    for songpath in songs:
        h = open(songpath, 'r')
        content = h.read()
        h.close()
        song = songpath.replace('../songs/', '').replace('.tex', '')
        songname = content.split('begin{song}{')[1].split('}')[0]
        mode = content.split('tonart{')[1].split('}')[0]
        #g.write(song + ':' + make_umlaute(songname) + ':' + mode + '\n')
        g.write(song + ':' + songname + ':' + mode + '\n')
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


@app.route('/editor')
def editor():
    return render_template("editor.html")


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


def create_pdf(songs_and_modes, jazz):

    delete_pdfs_texs()
    latex_head_path = 'app/static/latex_head.txt'
    f = open(latex_head_path, 'r')
    latex_head = f.read()
    f.close()

    content = latex_head
    for song, mode in songs_and_modes:
        songpath = '../songs/' + song + '.tex'
        g = open(songpath, 'r')
        song_content = g.read()
        g.close()
        song_content = transpose_song(song_content, mode, jazz)
        content = content + '\n' + song_content + '\n'

    content = content + '\\end{multicols}\n\\end{document}'

    path = strftime("%Y%m%d_%H%M%S", gmtime())

    h = open('app/static/' + path + '.tex', 'w')
    h.write(content)
    h.close()

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
    jazz = content["jazz"]
    path = create_pdf(songs_and_modes, jazz)
    source_url = url_for('static', filename='./' + path + '.pdf')
    print source_url
    pdf_path = '<embed id="show_pdf" src="' + source_url + \
        '" width="600" height="700" type="application/pdf">'
    return jsonify({"path": pdf_path})
