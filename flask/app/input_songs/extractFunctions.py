def get_chords_lines(filename):
    f = open(filename,'r')
    
    this_line = False
    special_lines = []
    
    for i, line in enumerate(f):
        zahl = i
        space_number = float(line.count(' '))/len(line)
        if this_line and len(line.strip())>0:
            special_lines.append('llll' + line)
            this_line = False
            zahl = -1
        if space_number > 0.4:
            this_line = True
            special_lines.append('cccc' + line)
            zahl = -1
        if zahl != -1:
            special_lines.append('eeee')
            
    return special_lines

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
            indices.append((chord, index))
            chord = ''
    if chord:
        indices.append((chord, index))
    return indices


def inject_chords(line, chords):
    n = False
    if "\n" in line:
        line = line.strip('\n')
        n = True
        
    new_line = ''
    index_right = len(line)
    longer = chords[-1][1] - index_right
    if longer > 0:
        line = line + " " * longer
        
    for tup in reversed(chords):
        chord = tup[0]
        index_left = tup[1]
        next_part = line[index_left:index_right]
        if len(next_part.strip())==0:
            new_line = '[' + chord + '|]{\ }' + next_part + new_line
        elif len(next_part) < 2*len(chord):
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


def txt2latex(filename):
    special_lines = get_chords_lines(filename)

    line_line = ''
    chord_line = ''
    content = ''
    for line in special_lines:
        if 'llll' in line:
            line_line = line[4:]
        if 'cccc' in line:
            chord_line = line[4:]
        if len(line_line)>0 and len(chord_line)>0:
            chords = chords_to_tuples(chord_line)
            new_line = inject_chords(line_line, chords)
            content = content + new_line
            line_line = ''
            chord_line = ''
        if 'eeee' in line:
            content = content + '\n'
    name = filename.split('.')[0]
    content = '\\begin{song}{' + name[0].upper() + name[1:] + '}\n' + content + '\end{song}'
    g = open(name + '.tex','w')
    g.write(content.replace("´","'").replace('’',"'").replace("`","'"))
    g.close()