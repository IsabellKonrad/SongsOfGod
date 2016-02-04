from extractFunctions import chords_to_tuples, inject_chords

def test_chords_to_tuples_1():
    line = " A\n"
    expect = [("A", 1)]
    res = chords_to_tuples(line)
    print(expect, res)
    assert expect == res
    
def test_chords_to_tuples_2():
    line = "A   "
    expect = [("A", 0)]
    res = chords_to_tuples(line)
    print(expect, res)
    assert expect == res
    
def test_chords_to_tuples_3():
    line = "A   B"
    expect = [("A", 0), ("B", 4)]
    res = chords_to_tuples(line)
    print(expect, res)
    assert expect == res

def test_chords_to_tuples_4():
    line = "Am   B"
    expect = [("Am", 0), ("B", 5)]
    res = chords_to_tuples(line)
    print(expect, res)
    assert expect == res

def test_chords_to_tuples_5():
    line = "Am Bm Cm"
    expect = [("Am", 0), ("Bm", 3), ("Cm", 6)]
    res = chords_to_tuples(line)
    print(expect, res)
    assert expect == res


def test_inject_chords_1():
    chords = [("Am", 0), ("Bm", 3), ("Cm", 7)]
    line = "I will love you"
    expect = "[Am]I w[Bm]ill [Cm]love you"
    res = inject_chords(line, chords)
    print(expect, res)
    assert expect == res

def test_inject_chords_2():
    chords = [("Am", 0), ("Am", 3), ("Am", 7)]
    line = "I will love you"
    expect = "[Am]I w[Am]ill [Am]love you"
    res = inject_chords(line, chords)
    print(expect, res)
    assert expect == res

def test_inject_chords_3():
    chords = [("Am", 0), ("Bm", 3), ("Cm", 7)]
    line = "I will love you\n"
    expect = "[Am]I w[Bm]ill [Cm]love you\n"
    res = inject_chords(line, chords)
    print(expect, res)
    assert expect == res

def test_inject_chords_4():
    chords = [("Am", 0), ("G#/Fis", 3), ("Bb\\h{maj7}", 12)]
    line = "I will love you\n"
    expect = "[Am]I w[G#/Fis]ill love [Bb\\h{maj7}]you\n"
    res = inject_chords(line, chords)
    print(expect, res)
    assert expect == res

def test_inject_chords_5():
    chords = [("Am", 0), ("Bm", 7), ("Cm", 12), ("F",16), ("G",19)]
    line = "I will love you\n"
    expect = "[Am]I will [Bm]love [Cm]you [F]   [G]\n"
    res = inject_chords(line, chords)
    print(expect, res)
    assert expect == res


