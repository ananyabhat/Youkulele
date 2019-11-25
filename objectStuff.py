#This class defines any classes used in my project

from tkinter import *

#This is a class for any button in the app
class Button1(object):
    def __init__(self, name, width, height, x, y, color = "pink2", fill = "white"):
        self.name = name
        self.width = width
        self.height = height
        self.color = color
        self.fill = fill
        self.x = x
        self.y = y
    
    def draw(self, canvas):
        canvas.create_rectangle(self.x, self.y, self.x + self.width, 
            self.y + self.height, fill = self.color, width = 0)
        canvas.create_text(self.x + self.width/2, self.y + self.height/2, 
            text = self.name, font="Helvetica 16 bold", fill=self.fill) 

#This is a class for any musical note in the app
class MusicNote(object):
    def __init__(self, name, pitch):
        self.name = name
        self.pitch = pitch

#This is a class defining a trie data structure. I took inspiration for this
#structure and definition from https://towardsdatascience.com/implementing-a-trie-data-structure-in-python-in-less-than-100-lines-of-code-a877ea23c1a1, but changed it to fit my project      
class TrieNode(object):
    
    def __init__(self, chord):
        self.chord = chord
        self.children = []
        # Is it the last character of the word.`
        self.progFinished = False
        # How many times this character appeared in the addition process
        self.counter = 1
        
    def __repr__(self):
        return self.chord    
    
