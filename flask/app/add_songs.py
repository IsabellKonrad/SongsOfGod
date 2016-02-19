import sys
import re

reload(sys)
sys.setdefaultencoding('utf-8')

def get_chords_lines(filename):
    f = open(filename,'r')
    special_lines = []
    for line in f:
        line = content_cleaning(line)
        space_number = float(line.count(' '))/len(line)
        if len(line.strip())==0:
            special_lines.append('eeee')
        elif space_number <= 0.4 and len(line.strip())>3:
            special_lines.append('llll' + line)
        else:
            special_lines.append('cccc' + line)            
    return special_lines


def handle_chord(chord):
    if 'moll' in chord:
        chord = chord.lower()
        chord = chord.replace('moll','')
    if 'm' in chord and not 'maj' in chord:
        chord = chord.lower()
        chord = chord.replace('m','')
    if '#' in chord:
        chord = chord.replace('#','is')
    if 'b' in chord:
        chord = chord.replace('b','*b')
    return chord

def chords_to_tuples(chord_line):
    chord_line = chord_line.strip('\n')
    indices = []
    isChord = False
    for i, ltr in enumerate(chord_line):
        if ltr != " " and isChord == False:
            isChord = True
            chord = ltr
            index = i
        elif ltr != " " and isChord == True:
            chord = chord + ltr
        elif ltr == " " and isChord == True:
            isChord = False
            indices.append((handle_chord(chord), index))
            chord = ''
    if chord:
        indices.append((handle_chord(chord), index))
    return indices



def handle_umlaute(line,chords):
    longer = chords[-1][1] - len(line)
    if longer > 0:
        line = line + " " * longer
    umlaute = [m.start() for m in re.finditer('"', line)]

    for umlaut in umlaute:
        umlaut = umlaut - 1
        chords_new = []
        for tup in chords:
            chord = tup[0]
            index = tup[1]
            if umlaut <= index:
                index = index + 2
            chords_new.append((chord, index))
        chords = chords_new

    sss = [m.start() for m in re.finditer('ss{}', line)]
    for ss in sss:
        ss = ss - 1
        chords_new = []
        for tup in chords:
            chord = tup[0]
            index = tup[1]
            if ss == index:
                index = index + 5
            if ss < index:
                index = index + 4
            chords_new.append((chord, index))
        chords = chords_new
    return line, chords



def inject_chords(line, chords):
    line, chords = handle_umlaute(line, chords)
    n = False
    if "\n" in line:
        line = line.strip('\n')
        n = True
    new_line = ''
   
    longer = chords[-1][1] - len(line)
    if longer > 0:
        line = line + " " * longer
    index_right = len(line)
    for tup in reversed(chords):
        chord = tup[0]
        index_left = tup[1]
        next_part = line[index_left:index_right]
        if len(next_part.strip())==0:
            new_line = '[' + chord + '|]{\quad}' + next_part + new_line
        elif len(next_part.strip()) < 2*len(chord):
            breakIndex = len(next_part.split(' ')[0])
            next_part = next_part[:breakIndex] + '}' + next_part[breakIndex:]
            new_line = '[' + chord + '|]{' + next_part + new_line
        else:
            new_line = '[' + chord + ']' + next_part + new_line
        index_right = index_left
    new_line = line[:index_right] + new_line
        
    if n:
        new_line = new_line + '\n'
    return new_line

def content_cleaning(input):
    input = input.replace("`","'")
    input = input.replace(u'\u00E4','\\"a')
    input = input.replace(u'\u00F6','\\"o')
    input = input.replace(u'\u00FC','\\"u')
    input = input.replace(u'\u00C4','\\"A')
    input = input.replace(u'\u00D6','\\"O')
    input = input.replace(u'\u00DC','\\"U')
    input = input.replace(u'\u00DF','\\ss{}')
    input = input.replace('\t','    ')
    return input

def txt2latex(filename, songtitle):
    special_lines = get_chords_lines(filename)

    line_line = ''
    chord_line = ''
    content = ''
    verse = 1
    chorus = 0
    bridge = 0
    for line in special_lines:
        if 'Verse' in line or 'verse' in line or 'VERSE' in line:
            content = content + "{\\bf %i.} " % verse
            line = ''
            verse = verse + 1
        if 'Chorus' in line or 'chorus' in line or 'CHORUS' in line:
            content = content + "\\begin{chorus}\n"
            line = ''
            chorus = 1
        if 'Bridge' in line or 'bridge' in line or 'BRIDGE' in line:
            content = content + "\\begin{bridge}\n"
            line = ''
            bridge = 1

        if 'llll' in line:
            if line_line:
                content = content + line_line
            line_line = line[4:]
        if 'cccc' in line:
            if line_line:
                content = content + line_line
                line_line = ''
            chord_line = line[4:]
        if line_line and chord_line:
            chords = chords_to_tuples(chord_line)
            new_line = inject_chords(line_line, chords)
            content = content + new_line
            line_line = ''
            chord_line = ''
        if 'eeee' in line:
            if chord_line:
                chords = chords_to_tuples(chord_line)
                new_line = inject_chords('',chords)
                content = content + new_line
                chord_line = ''
            if line_line:
                content = content + line_line
                line_line = ''
            if chorus:
                content = content + '\\end{chorus}\n'
                chorus = 0
            if bridge:
                content = content + '\\end{bridge}\n'
                bridge = 0
            content = content + '\n'
    if line_line:
        content = content + line_line
    if chord_line:
        chords = chords_to_tuples(chord_line)
        new_line = inject_chords('',chords)
        content = content + new_line
    if bridge:
        content = content + '\\end{bridge}\n'
        bridge = 0
    if chorus:
        content = content + '\\end{chorus}\n'
        chorus = 0

    content = content.replace('\n\n\n','\n\n\\bigskip\n\n')
    content = content_cleaning(content)
    name = filename.split('.')[0]
    content = '\\begin{song}{' + songtitle.strip() + '}\n\n' + content + '\n\\end{song}'
    g = open(name + '.txt','w')
    g.write(content)
    g.close()


if __name__ == '__main__':
    filename = sys.argv[1]
    songtitle = sys.argv[2]
    txt2latex(filename, songtitle)