#this file generates scales, keys, and popular chord progressions and defines
#the function used to generate recommendations for a chord to add

import objectStuff

#this creates a major scale based on the chromatic scale
def getMajorScale(keyNote):
    formula = [2,4,5,7,9, 11]
    scale = []
    scale.append(keyNote)
    for i in range(len(formula)):
        newNoteIndex = (chromaticScale[keyNote] + formula[i]) % 12
        if chromaticScaleLetters[newNoteIndex] == keyNote:
            break
        scale.append(chromaticScaleLetters[newNoteIndex])
    return scale

#this creates all major scales    
def createMajorScales():
    majorScales = {}
    for note in chromaticScaleLetters:
        majorScales[note] = getMajorScale(note)
    return majorScales

#this generates all the major keys
def generateMajorKeys():
    result = {}
    for scale in majorScales:
        key = {}
        i = -1
        for note in majorScales[scale]:
            i += 1
            chord = majorPattern[i]
            if chord == "major":
                key[i] = note
            elif chord == "minor": 
                key[i] = note + "m"
            elif chord == "diminished":
                continue
        result[scale] = key
    return result

#this rotates a list, placing the last item at the beginning    
def rotate(l):
    return l[-1:] + l[:-1]

#this generates all possible variations of a chord progression for a key    
def generateProgressions(keyNotes, a,b,c,d):
    s = set()
    prog1 = (keyNotes[a],keyNotes[b],keyNotes[c],keyNotes[d])
    prog1v2 = rotate(prog1)
    prog1v3 = rotate(prog1v2)
    prog1v4 = rotate(prog1v3)
    s.add(prog1)
    s.add(prog1v2)
    s.add(prog1v3)
    s.add(prog1v4)
    return s

#this generates all (popular) chord progressions for all keys
def generateChordProgressions():
    progressions = set()
    for key in majorKeys:
        keyNotes = majorKeys[key]
        #0, 4, 5, 3 refers to the popular chord progression I-V-vi-IV
        progressions.update(generateProgressions(keyNotes, 0,4,5,3))
    return progressions
    
#I took inspiration for this algorithm from https://towardsdatascience.com/implementing-a-trie-data-structure-in-python-in-less-than-100-lines-of-code-a877ea23c1a1, but changed it to add chords to a trie instead of chars 
def addNode(root, progression):
    node = root
    for chord in progression:
        foundInChild = False
        # Search for the chord in the children of the present `node`
        for child in node.children:
            if child.chord == chord:
                # We found it, increase the counter by 1 to keep track that 
                #another progression has it as well
                child.counter += 1
                # And point the node to the child that contains this chord
                node = child
                foundInChild = True
                break
        # We did not find it so add a new chlid
        if not foundInChild:
            newNode = objectStuff.TrieNode(chord)
            node.children.append(newNode)
            # And then point node to the new child
            node = newNode
    # Everything finished. Mark it as the end of a progression.
    node.progFinished = True
    
#I took inspiration for this algorithm from https://towardsdatascience.com/implementing-a-trie-data-structure-in-python-in-less-than-100-lines-of-code-a877ea23c1a1, but changed it to find chords in a progression instead of chars in a word
def findProg(root, progSoFar):
    """
    Check
      1. If the chord(s) exist 
    Return
      2.Sorted copy of child array (child from last node of prefix)
    """
    node = root
    # If the root node has no children, then return empty list because it means
    # we are trying to search in an empty trie
    if not root.children:
        return []
    # for each chord that we have 
    for chord in progSoFar:
        if "(s)" in chord:
            chord = chord.replace("(s)", "")
        chordNotFound = True
        # Search through all the children of the present node
        for child in node.children:
            if child.chord == chord:
                # We found the chord existing in the child.
                chordNotFound = False
                # Assign node as the child containing the last chord and break
                node = child
                break
            # Return False anyway when we did not find the chord.
        if chordNotFound:
            return []
    # If we went through everything and found the current progression of notes
    # we have, return the children of the last node, sorted in descending order
    sortedChildren =sorted(node.children, key=lambda x: x.counter, reverse=True)
    return sortedChildren
    
#set up the trie data structure!
def setUpTrie(root):
    for prog in progressions: 
        addNode(root, prog)
    
    
chromaticScaleLetters = ['c','c#','d','d#','e','f','f#','g','g#','a','a#','b']
chromaticScale = {'c':0,'c#':1,'d':2,'d#':3,'e':4,'f':5,'f#':6,'g':7,'g#':8,
                    'a':9,'a#':10,'b':11}
majorScales = createMajorScales()
majorPattern = ['major','minor','minor','major','major','minor','diminished']
majorKeys = generateMajorKeys()
progressions = generateChordProgressions()

 