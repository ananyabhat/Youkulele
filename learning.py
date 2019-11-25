#This file defines the functions for the learning screen

import audioThings
from tkinter import *
import objectStuff
import atexit

#checks if user played right pitch
def checkPitch(note, data):
    marginOfError = 10
    data.text = "Listening..."
    redrawAll(data.canvas, data)
    data.canvas.update()
    audioThings.record("sounds/fileToCheck.wav")
    pitch = audioThings.findDomFreq("sounds/fileToCheck.wav")
    if pitch > note.pitch + marginOfError or pitch < note.pitch - marginOfError:
        return False
    return True

#getCellBounds is taken from the course lecture notes on Event-based animation   
def getCellBounds(row, col, data):
    # returns (x0, y0, x1, y1) corners/bounding box of given cell in grid
    # to help draw strings
    gridWidth  = data.width - 2*data.margin3
    gridHeight = data.height - 2*data.margin3
    columnWidth = gridWidth / data.cols
    rowHeight = gridHeight / data.rows
    x0 = data.margin3 + col * columnWidth
    x1 = data.margin3 + (col+1) * columnWidth
    y0 = data.margin3 + row * rowHeight
    y1 = data.margin3 + (row+1) * rowHeight
    return (x0, y0, x1, y1)
    
def getLocation(row, col, data):
    # returns (x0, x1, y0) of given cell in grid to help place notes
    gridWidth  = data.width - 2*data.margin3
    gridHeight = data.height - 2*data.margin3
    columnWidth = gridWidth / data.cols
    rowHeight = gridHeight / data.rows
    x0 = data.margin3 + col * columnWidth
    x1 = data.margin3 + (col + 1) * columnWidth
    y0 = data.margin3 + row * rowHeight
    return (x0, x1, y0)

#draws 4 strings by drawing a 3x4 grid and corresponding string letters (GCEA)       
def drawStrings(canvas, data):
    for row in range(data.rows):
        for col in range(data.cols):
            (x0, y0, x1, y1) = getCellBounds(row, col, data)
            if col == 0 and row %2  == 0:
                canvas.create_text(x0 - data.margin4, y0, text=data.strings[row],
                       font="Arial 26 bold", fill="paleVioletRed", anchor = "e")
                canvas.create_text(x0 - data.margin4, y1, text=data.strings[row + 1],
                       font="Arial 26 bold", fill="paleVioletRed", anchor = "e")
            canvas.create_rectangle(x0, y0, x1, y1, fill=None, width = 2)

#returns a list of the notes in a chord        
def getChords(note, data):
    result = []
    #if its a single note, then get the note from singles list 
    if "(s)" in note:
        row = data.singles[note][0]
        col = data.singles[note][1]
        (x0, x1, y0) = getLocation(row, col, data) 
        #if its an open chord, meaning col = 0, then the note should be 
        #displayed as text, which is why object type is text
        if col == 0:
            fill = "paleVioletRed"
            objectType = "textSingle" 
        #otherwise, display note as a red circle
        else:
            #places circle in the middle so it looks like its on a fret 
            x0 = (x0 + x1) /2
            fill = "pink"
            objectType = "circle"
        result.append([x0, y0, fill, objectType, note])
    else:
        #get each note in the chord
        chordNotes = data.chords[note]
        for i, chordNote in enumerate(chordNotes):
            row = i
            col = chordNote
            (x0, x1, y0) = getLocation(row, col, data) 
            #if its an open chord, meaning col = 0, then the note should be 
            #displayed as text, which is why object type is text
            if col == 0:
                fill = "paleVioletRed"
                objectType = "text"
            #otherwise, display note as a red circle
            else: 
                #places circle in the middle so it looks like its on a fret 
                x0 = (x0 + x1) /2
                fill = "pink"
                objectType = "circle"
            result.append([x0, y0, fill, objectType, note])
    return result

#performs animation for a chord
def playChordAnimation(note, data):
    #get each note in the chord
    chordNotes = data.chords[note]
    #this is a list of the file names for the notes in the chords
    chordsLst = ["sounds/g/" + data.notes["g"][chordNotes[0]] + ".wav",
                "sounds/c/" + data.notes["c"][chordNotes[1]] + ".wav",
                "sounds/e/" + data.notes["e"][chordNotes[2]] + ".wav",
                "sounds/a/" + data.notes["a"][chordNotes[3]] + ".wav"]
    #turns note green, plays note, then turns back to red
    for i, chordNote in enumerate(data.notesToDraw):
        initialColor = chordNote[2]
        chordNote[2] = "lawn green"
        #updates the canvas so that the sound plays at the same time
        #instead of processing all audio before changing canvas
        redrawAll(data.canvas, data)
        data.canvas.update()
        audioThings.play(chordsLst[i])
        chordNote[2] = initialColor
        redrawAll(data.canvas, data)
        data.canvas.update()
        
#performs animation for a single note
def playSingleAnimation(note, data):
    noteSound = "sounds/single/" + note + ".wav"
    for i, chordNote in enumerate(data.notesToDraw):
        initialColor = chordNote[2]
        chordNote[2] = "lawn green"
        #updates the canvas so that the sound plays at the same time
        #instead of processing all audio before changing canvas
        redrawAll(data.canvas, data)
        data.canvas.update()
        audioThings.play(noteSound)
        chordNote[2] = initialColor
        redrawAll(data.canvas, data)
        data.canvas.update()

#performs animation for learning a chord
def learningAnimation(note,data):
    chordNotes = data.chords[note]
    chordsLst = ["sounds/g/" + data.notes["g"][chordNotes[0]] + ".wav",
                "sounds/c/" + data.notes["c"][chordNotes[1]] + ".wav",
                "sounds/e/" + data.notes["e"][chordNotes[2]] + ".wav",
                "sounds/a/" + data.notes["a"][chordNotes[3]] + ".wav"]
    notes = [data.notes["g"][chordNotes[0]],data.notes["c"][chordNotes[1]],
    data.notes["e"][chordNotes[2]], data.notes["a"][chordNotes[3]]]
    #for each note in the chord, play the animation for the note
    for i, chordNote in enumerate(data.notesToDraw):
        animation(notes[i], chordNote, data, chordsLst[i])

#performs animation for learning a single note        
def learnSingleAnimation(note, data):
    noteSound = "sounds/single/" + note + ".wav"
    #play the animation for the note
    if data.stop == False:
        for i, chordNote in enumerate(data.notesToDraw):
            animation(note, chordNote, data, noteSound)

#recursive function makes the note to be played green, plays the note,
#then calls testNote to check if player played the note correctly — if so, 
#change color back to red and move on; otherwise, calls itself again        
def animation(note, chordNote, data, sound): 
    initialColor = chordNote[2]
    chordNote[2] = "lawn green"
    redrawAll(data.canvas, data)
    data.canvas.update()
    audioThings.play(sound)
    #removes "(s)" from a note if its single note bc (s) is not in pitchdict
    if "(s)" in note:
        note = note.replace("(s)", "")
    #base case
    if testNote(note,data):
        chordNote[2] = initialColor
        redrawAll(data.canvas, data)
        data.canvas.update()
    #recursive case
    else:
        if data.stop == False:
            chordNote[2] = initialColor
            redrawAll(data.canvas, data)
            data.canvas.update()
            animation(note, chordNote, data, sound)
        else:
            chordNote[2] = initialColor
            redrawAll(data.canvas, data)
            data.canvas.update()
                
    
#changes text to good job and returns true if user played correct note, 
#or changes text to try again and returns false if user did not
def testNote(note,data):
    chosenNote = objectStuff.MusicNote(note, data.pitchesDict[note])
    if checkPitch(chosenNote, data):
        data.text = "Good Job!"
        return True
    else:
        data.text = "Try Again."
        return False
    
def keyPressed(event,data):
        #moves onto next note in song
        if event.keysym == "Return":
            data.counter += 1
            data.note = data.song[data.counter%len(data.song)]
            data.notesToDraw = getChords(data.note, data)
            data.text = ""
        #plays animation
        if event.keysym == "a":
            if "(s)" in data.note:
                playSingleAnimation(data.note, data)
            else:
                playChordAnimation(data.note, data)
        #plays learning animation
        if event.keysym == "t":
            data.stop = False
            if "(s)" in data.note:
                learnSingleAnimation(data.note, data)
            else:
                learningAnimation(data.note, data)
        if event.keysym == "m":
            data.mode = "majorScreen"
        if event.keysym == "s":
            data.stop = True

def redrawAll(canvas, data):  
    #display the note at top center of the screen  
    canvas.create_text(data.width//2, data.margin3//2, text=data.note, font="Arial 26 bold", fill="paleVioletRed")
    #draw text for learning animation ("listening...", "good job", etc.)
    canvas.create_text(data.width//2, data.height - data.margin3 + data.margin4, 
    text=data.text,font="Arial 26 bold", fill="paleVioletRed")
    #draw the strings
    drawStrings(canvas, data)
    #for each note in the chord, draw either circle or text (text is if its an
    #open chord) 
    for i, chordNote in enumerate(data.notesToDraw):
        (cx, cy, fill, objectType, note) = chordNote
        if objectType == "text":
                canvas.create_text(cx - data.margin4, cy, text=data.strings[i],
                       font="Arial 26 bold", fill=fill, anchor = "e")
        elif objectType == "textSingle":
                canvas.create_text(cx - data.margin4, cy, text=note[0].upper(),
                       font="Arial 26 bold", fill=fill, anchor = "e")
        else:
            canvas.create_oval(cx-data.circleSize, cy - data.circleSize, cx + data.circleSize, cy + data.circleSize, fill = fill)
        