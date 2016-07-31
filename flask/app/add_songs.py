import sys
import re

reload(sys)
sys.setdefaultencoding('utf-8')


def HorB(content):
    
    def get_distance(thischord,thatchord):
        chordvec = ['es','Ges','b','Des','f','As','c','Es','g','B','d','F','a','C',
        'e','G','h','D','fis','A','cis','E','gis','H','dis','Fis','ais','Cis','eis',
        'Gis', 'his', 'Dis']
        try:
            thisnumber = chordvec.index(thischord)
        except:
            return False
        thatnumber = chordvec.index(thatchord)
        return abs(thisnumber - thatnumber)

    def HtoB(thiscontent):
        def handle_h_in_chord(ccc):
            if '\\h' in ccc:
                cc = ccc.split('\\h')[0]
                ccrest = '\\h' + ccc.split('\\h')[1]
                ccc = cc.replace('h','*b')
                ccc = cc.replace('H','B')
                ccc = ccc + ccrest
            else:
                ccc = ccc.replace('h','*b')
                ccc = ccc.replace('H','B')
            return ccc
        content_list = thiscontent.split('[')
        contentB = content_list[0]
        for con in content_list[1:]:
            chord = con.split(']')[0]
            rest = con.split(']')[1]
            if '/' in chord:
                chord1 = chord.split('/')[0]
                chord1 = handle_h_in_chord(chord1)
                chord2 = chord.split('/')[1]
                chord2 = handle_h_in_chord(chord2)
                chord = chord1 + '/' + chord2
            else:
                chord = handle_h_in_chord(chord)
            contentB = contentB + '[' + chord + ']' + rest
        return contentB


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
        if 'B' not in chord and 'b' not in chord and 'H' not in chord and 'h' not in chord:
            chords.append(chord)
    sum_dist_H = 0
    sum_dist_h = 0
    sum_dist_B = 0
    sum_dist_b = 0
    for chord in chords:
        if get_distance(chord,'H') == False:
            return False
        sum_dist_H = sum_dist_H + get_distance(chord,'H')
        sum_dist_h = sum_dist_h + get_distance(chord,'h')
        sum_dist_B = sum_dist_B + get_distance(chord,'B')
        sum_dist_b = sum_dist_b + get_distance(chord,'b')
    if (sum_dist_H < sum_dist_b and sum_dist_H < sum_dist_B) or (sum_dist_h < sum_dist_b and sum_dist_h < sum_dist_B):
       content = content
    else:
        content = HtoB(content)
    return content


def makewdh(line):
    line = line.replace('(wdh)','wdh')
    line = line.replace('wdh','\\quad\\wdh')
    line = line.replace('(2x)','\\quad\\wdh')
    line = line.replace('2x','\\quad\\wdh')
    line = line.replace('(2X)','\\quad\\wdh')
    line = line.replace('2X','\\quad\\wdh')
    line = line.replace('(2 mal)','\\quad\\wdh')
    line = line.replace('2 mal','\\quad\\wdh')
    line = line.replace('(3x)','\\quad\\wdhh')
    line = line.replace('3x','\\quad\\wdhh')
    line = line.replace('(3X)','\\quad\\wdhh')
    line = line.replace('3X','\\quad\\wdhh')
    line = line.replace('(3 mal)','\\quad\\wdhh')
    line = line.replace('3 mal','\\quad\\wdhh')
    line = line.replace('(4x)','\\quad\\wdhhh')
    line = line.replace('4x','\\quad\\wdhhh')
    line = line.replace('(4X)','\\quad\\wdhhh')
    line = line.replace('4X','\\quad\\wdhhh')
    line = line.replace('(4 mal)','\\quad\\wdhhh')
    line = line.replace('4 mal','\\quad\\wdhhh')
    return line

def get_chords_lines(filename):
    f = open(filename,'r')
    special_lines = []
    for line in f:
        space_number = float(line.count(' '))/len(line)
        line = makewdh(line)
        if len(line.strip())==0:
            special_lines.append('eeee')
        elif space_number <= 0.4 and len(line.strip())>3:
            line = umlaute_to_numbers(line)
            special_lines.append('llll' + line)

        else:
            special_lines.append('cccc' + line)            
    return special_lines



def handle_chord(chord):
    def help_with_chords(thechord):
        thechord = thechord.strip()
        if 'moll' in thechord:
            thechord = thechord.lower()
            thechord = thechord.replace('moll','')
        if 'm' in thechord and not 'maj' in thechord:
            thechord = thechord.lower()
            thechord = thechord.replace('m','')
        if '#' in thechord:
            thechord = thechord.replace('#','is')
        # all chords H, h, B, b, Bb, bb are overwritten with H, h. We check H, h or B, b in HorB.
        if len(thechord)>1:
            if ('B' in thechord[0:1] or 'b' in thechord[0:1]) and 'b' not in thechord[1:2]:
                thechord = thechord.replace('B','H')
                thechord = thechord.replace('b','h')
        else:
            thechord = thechord.replace('B','H')
            thechord = thechord.replace('b','h')
        if len(thechord)>1:
            if 'b' in thechord[1:2]:
                if 'a' in thechord[0:1] or 'e' in thechord[0:1] or 'A' in thechord[0:1] or 'E' in thechord[0:1]:
                    thechord = thechord[:1] + 's' + thechord[2:]
                elif 'b' in thechord[0:1]:
                    thechord = 'h' + thechord[2:]
                elif 'B' in thechord[0:1]:
                    thechord = 'H' + thechord[2:]
                else:
                    thechord = thechord[:1] + 'es' + thechord[2:]

        if len(thechord)>3:
            if 'is' in thechord[1:3] or 'es' in thechord[1:3]:
                thechord = thechord[0:3] + '\\h{' + thechord[3:] + '}'
            elif 's' in thechord[1:2] and 'sus' not in thechord[1:4]:
                thechord = thechord[0:2] + '\\h{' + thechord[2:] + '}'
            else:
                thechord = thechord[0:1] + '\\h{' + thechord[1:] + '}'
        if len(thechord)==3:
            if 'is' in thechord[1:3] or 'es' in thechord[1:3]:
                thechord = thechord
            elif 's' in thechord[1:2]:
                thechord = thechord[0:2] + '\\h{' + thechord[2:] + '}'
            else:
                thechord = thechord[0:1] + '\\h{' + thechord[1:] + '}'
        if len(thechord)==2:
            if 's' in thechord[1:2]:
                thechord = thechord
            else:
                thechord = thechord[0:1] + '\\h{' + thechord[1:] + '}'
        return thechord

    if '/' in chord:
        chord1 = chord.split('/')[0]
        chord2 = chord.split('/')[1]
        chord1 = help_with_chords(chord1)
        chord2 = help_with_chords(chord2)
        chord = chord1 + '/' + chord2
    else:
        chord = help_with_chords(chord)    
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
    umlaute = [m.start() for m in re.finditer('%', line)]
    umlaute = umlaute + [m.start() for m in re.finditer('5', line)]
    umlaute = umlaute + [m.start() for m in re.finditer('6', line)]
    umlaute = umlaute + [m.start() for m in re.finditer('7', line)]
    umlaute = umlaute + [m.start() for m in re.finditer('8', line)]
    umlaute = umlaute + [m.start() for m in re.finditer('9', line)]

    for umlaut in umlaute:
        umlaut = umlaut - 1
        chords_new = []
        for tup in chords:
            chord = tup[0]
            index = tup[1]
            if umlaut+1 == index:
                index = index + 1
            chords_new.append((chord, index))
        chords = chords_new

    sss = [m.start() for m in re.finditer('0', line)]
    for ss in sss:
        ss = ss - 1
        chords_new = []
        for tup in chords:
            chord = tup[0]
            index = tup[1]
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
            new_line = '[' + chord + '|]{\quad}' + content_cleaning(next_part) + new_line
        elif len(next_part.strip()) < 2*len(chord):
            breakIndex = len(next_part.split(' ')[0])
            next_part = next_part[:breakIndex] + '}' + next_part[breakIndex:]
            new_line = '[' + chord + '|]{' + content_cleaning(next_part) + new_line
        else:
            new_line = '[' + chord + ']' + content_cleaning(next_part) + new_line
        index_right = index_left
    new_line = content_cleaning(line[:index_right]) + new_line
        
    if n:
        new_line = new_line + '\n'
    return new_line

def umlaute_to_numbers(input):
    input = input.replace("`","'")
    input = input.replace(u'\u00E4','%')
    input = input.replace(u'\u00F6','5')
    input = input.replace(u'\u00FC','6')
    input = input.replace(u'\u00C4','7')
    input = input.replace(u'\u00D6','8')
    input = input.replace(u'\u00DC','9')
    input = input.replace(u'\u00DF','0')
    input = input.replace('\t','    ')
    return input

def content_cleaning(input):
    input = input.replace('%','\\"a')
    input = input.replace('5','\\"o')
    input = input.replace('6','\\"u')
    input = input.replace('7','\\"A')
    input = input.replace('8','\\"O')
    input = input.replace('9','\\"U')
    input = input.replace('0','\\ss{}')
    return input

def title_cleaning(input):
    input = input.replace("`","'")
    input = input.replace(u'\u00E4','ae')
    input = input.replace(u'\u00F6','oe')
    input = input.replace(u'\u00FC','ue')
    input = input.replace(u'\u00C4','Ae')
    input = input.replace(u'\u00D6','Oe')
    input = input.replace(u'\u00DC','Ue')
    input = input.replace(u'\u00DF','ss')
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
        if 'verse' in line.lower() or 'vers' in line.lower():
            if 'end' in line.lower() or 'ende' in line.lower():
                pass
            else:
                content = content + "{\\bf %i.} " % verse
                line = ''
                verse = verse + 1
        if 'chorus' in line.lower():
            if 'end' in line.lower() or 'ende' in line.lower():
                content = content[:-4] + content[-4:-1].strip('\n') + "\\end{chorus}\n"
                line = ''
                chorus = 0
            else:
                content = content + "\\begin{chorus}\n"
                line = ''
                chorus = 1
        if 'bridge' in line.lower():
            if 'end' in line.lower() or 'ende' in line.lower():
                line=''
                content = content[:-4] + content[-4:-1].strip('\n') + "\\end{bridge}\n"
            else:
                content = content + "\\begin{bridge}\n"
                line = ''
                bridge = 0

        if 'llll' in line:
            if line_line:
                content = content + content_cleaning(line_line)
            line_line = line[4:]
        if 'cccc' in line:
            if line_line:
                content = content + content_cleaning(line_line)
                line_line = ''
            chord_line = line[4:]
        if line_line and chord_line:
            try:
                chords = chords_to_tuples(chord_line)
            except:
                return False
            new_line = inject_chords(line_line, chords)
            content = content + new_line
            line_line = ''
            chord_line = ''
        if 'eeee' in line:
            if chord_line:
                try:
                    chords = chords_to_tuples(chord_line)
                except:
                    return False
                new_line = inject_chords('',chords)
                content = content + new_line
                chord_line = ''
            if line_line:
                content = content + content_cleaning(line_line)
                line_line = ''
            content = content + '\n'
    if line_line:
        content = content + content_cleaning(line_line)
    if chord_line:
        try:
            chords = chords_to_tuples(chord_line)
        except:
            return False
        new_line = inject_chords('',chords)
        content = content + new_line
    if bridge:
        content = content + '\\end{bridge}\n'
        bridge = 0
    if chorus:
        content = content + '\\end{chorus}\n'
        chorus = 0

    content = content.replace('\n\n\n','\n\n\\bigskip\n\n')
    name = filename.split('.')[0]
    songtitle = title_cleaning(songtitle).strip()
    content = '\\begin{song}{' + songtitle + '}\n\n' + content + '\n\\end{song}'
    content = HorB(content)
    if content == False:
        return False
    g = open(name + '.txt','w')
    g.write(content)
    g.close()
    return True


if __name__ == '__main__':
    filename = sys.argv[1]
    songtitle = sys.argv[2]
    txt2latex(filename, songtitle)