#I have a lot of attributes for data, so this file sets up all those attributes
#to make the main file cleaner and easier to read

import objectStuff
from tkinter import *
import generatingStuff

def setUp(data):
    data.mode = "introScreen"
    data.background1 = PhotoImage(file="images/background.png")
    data.background2 = PhotoImage(file="images/background2.png")
    data.stop = False
    data.margin = 50
    data.margin2 = 20
    data.margin3 = 100
    data.margin4 = 25
    data.buttonWidth = 100
    data.buttonHeight = 50
    data.button2Size = 50
    data.buttons = []
    data.selected = 0
    data.song = []
    data.recs = []
    data.timer = -1
    data.canvas = None
    data.text = ""
    data.circleSize = 20
    data.counter = -1
    data.note = ""
    data.notesToDraw = []
    data.rows = 3
    data.cols = 5
    data.buttonNotes = ["c", "c#", "d", "d#", "e", "f", "f#", "g", 
    "g#", "a", "a#", "b"]
    data.strings = ["G","C","E", "A"]
    #this is a dictionary of the pitches of the 12 notes
    data.pitchesDict = {"c":262, "c#":278, "d":294, "d#":311, "e":330, 
    "f": 349, "f#":370, "g": 391, "g#":415, "a": 440, "a#": 466, "b": 494}
    #the list of values corresponds to the notes in the chords -- 0 means its 
    #an open chord, 1 means its on the first fret, etc. and the order of the
    #values is in order of the strings they are on (GCEA)     
    data.chords = {"c": [0,0,0,3], "c#": [1,1,1,4], "d": [2,2,2,0], 
    "d#": [0,3,3,1], "e": [1,4,0,2], "f": [ 2,0,1,0], "f#": [3,1,2,1], 
    "g": [0,2,3,2], "g#": [0,3,4,3], "a": [2,1,0,0], "a#": [3,2,1,1], 
    "b": [ 2,2,3,4], "cm": [0,3,3,3], "c#m": [1,1,0,4], "dm": [2,2,1,0], 
    "d#m": [3,3,2,1], "em": [0,4,3,2], "fm": [1,0,1,3], "f#m": [2,1,2,0], 
    "gm": [0,2,3,1], "g#m": [1,3,4,2], "am": [2,0,0,0], "a#m": [3,1,1,1], 
    "bm": [4,1,1,1]}
    #this is the placement/location of single notes on the uke strings
    data.singles = {"c(s)": (1,0), "c#(s)": (1,1) , "d(s)": (1,2), 
    "d#(s)": (1,3), "e(s)": (2,0), "f(s)": (2,1), "f#(s)": (2,2) , 
    "g(s)": (0,0), "g#(s)": (0,1), "a(s)": (3,0), "a#(s)": (3,1), 
    "b(s)": (3,2)}
    #this is a dict that corresponds notes (values) to a uke string (key)
    data.notes = {"g": ["g", "g#", "a", "a#", "b"], 
    "c": ["c", "c#", "d", "d#", "e"], "e": ["e","f","f#","g","g#"], 
    "a": ["a", "a#", "b", "c", "c#"]} 
    
    data.root = objectStuff.TrieNode('*')


    data.majorButton = objectStuff.Button1("major chords", data.buttonWidth, 
        data.buttonHeight, data.margin, data.margin3, color = "paleVioletRed") 
    data.minorButton = objectStuff.Button1("minor chords", data.buttonWidth, 
        data.buttonHeight, data.margin + data.width/3, data.margin3)
    data.singleButton = objectStuff.Button1("single notes", data.buttonWidth, 
        data.buttonHeight, data.margin + data.width*(2/3), data.margin3)
    data.startButton = objectStuff.Button1("START", 100, 50, 
    data.width/2, (data.height/2) + data.margin)
    
    
    createButtons(data)
    generatingStuff.setUpTrie(data.root)
    
def createButtons(data):
    #creates 12 buttons, split into 2 rows of 6 
    for i in range(len(data.buttonNotes)):
        if i <= 5:
            x = data.margin2 + (data.width/6)*i
            y = data.margin3 + data.buttonHeight + data.margin
        else:
            x = data.margin2 + (data.width/6)*(i - len(data.buttonNotes)//2 )
            y =  data.margin3 + data.buttonHeight + data.margin*2 + data.button2Size
        data.buttons.append(objectStuff.Button1(data.buttonNotes[i], 
                    data.button2Size, data.button2Size, x, y))