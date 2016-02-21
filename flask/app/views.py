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
from add_songs import txt2latex
from find_mode import use_classifier, mode_to_song
reload(sys)
sys.setdefaultencoding('utf-8')


if 'ubuntu' in os.getcwd():
    # on AWS server where cwd is not set properly. Hence this workaround
    os.chdir('/home/ubuntu/SongsOfGod/flask')


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


def delete_pdfs_texs_txts():
    all_pdfs = glob.glob('app/static/*.pdf')
    for pdf in all_pdfs:
        os.remove(pdf)
    all_texs = glob.glob('app/static/*.tex')
    for tex in all_texs:
        os.remove(tex)
    all_txts = glob.glob('app/static/*.txt')
    for txt in all_txts:
        os.remove(txt)


def create_pdf(songs_and_modes, jazz):
    latex_head_path = 'app/static/latex_head'
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
    delete_pdfs_texs_txts()
    content = request.get_json(silent=True)
    songs_and_modes = zip(content["songs"], content["modes"])
    jazz = content["jazz"]
    path = create_pdf(songs_and_modes, jazz)
    source_url = url_for('static', filename='./' + path + '.pdf')
    pdf_path = '<embed id="show_pdf" src="' + source_url + \
        '" width="600" height="700" type="application/pdf">'
    return jsonify({"path": pdf_path})



def create_pdf_check(songpath):
    latex_head_path = 'app/static/latex_head_check'
    f = open(latex_head_path, 'r')
    latex_head_check = f.read()
    f.close()
    g = open(songpath,'r')
    song_content = g.read()
    g.close()
    content = latex_head_check + song_content + '\n}\n\n\\end{document}'
    path = strftime("%Y%m%d_%H%M%S", gmtime())
    h = open('app/static/' + path + '.tex', 'w')
    h.write(content)
    h.close()
    latex_success = subprocess.call(['pdflatex', 'app/static/' + path + '.tex'])
    latex_success = 1-latex_success
    os.remove(path + '.log')
    os.remove(path + '.aux')
    os.remove(path + '.out')
    os.rename(path + '.pdf', 'app/static/' + path + '.pdf')
    return path, latex_success

def title_cleaning(input):
    print input
    input = input.strip().lower()
    input = input.replace(' ','')
    input = input.replace("`",'')
    input = input.replace("'",'')
    input = input.replace(u'\u00E4','ae')
    input = input.replace(u'\u00F6','oe')
    input = input.replace(u'\u00FC','ue')
    input = input.replace(u'\u00C4','Ae')
    input = input.replace(u'\u00D6','Oe')
    input = input.replace(u'\u00DC','Ue')
    input = input.replace(u'\u00DF','ss')
    return input

@app.route('/checksong', methods=['GET', 'POST'])
def checksong():
    delete_pdfs_texs_txts()
    content = request.get_json(silent=True)
    songtitle = content["songtitle"]
    songpath = 'app/static/' + title_cleaning(songtitle)
    songcontent = content["songcontent"]
    f = open(songpath + '.txt','w')
    f.write(songcontent)
    f.close()
    txt2latex(songpath + '.txt', songtitle)
    g = open(songpath + '.txt','r')
    songcontent = g.read()
    g.close()
    mode1, mode2 = use_classifier(songcontent)
    path, latex_success = create_pdf_check(songpath + '.txt')
    source_url = url_for('static', filename='./' + path + '.pdf')
    pdf_path = '<embed id="show_pdf_check" style="margin-top: 2%" src="' + source_url + \
        '" width="350" height="530"  type="application/pdf">'
    return jsonify({"path": pdf_path, "latex_success": latex_success, "mode1": mode1, "mode2": mode2})


@app.route('/savesong', methods=['GET', 'POST'])
def savesong():
    content = request.get_json(silent=True)
    mode = content["mode"]
    songtitle = content["songtitle"]
    songpath = 'app/static/' + title_cleaning(songtitle) + '.txt'
    mode_to_song(songpath,mode)
    os.rename(songpath, '../songs/' + title_cleaning(songtitle) + '.tex')
    make_songlist()
    return jsonify({"success": True})

