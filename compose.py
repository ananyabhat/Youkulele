import audioThings
from tkinter import *
import objectStuff
import learning
import generatingStuff
import setUpData

def init(data):
    setUpData.setUp(data)
    
def mousePressed(event, data):
    if data.margin3 <= event.y <= data.margin3 + data.buttonHeight:
        #if user clicked on major button, change selected to major
        if data.majorButton.x <= event.x <= data.majorButton.x + data.buttonWidth:
            data.majorButton.color = "paleVioletRed"
            data.minorButton.color = "pink2"
            data.singleButton.color = "pink2"
            data.mode = "majorScreen"
        #if user clicked on minor button, change selected to minor
        elif data.minorButton.x <= event.x <= data.minorButton.x + data.buttonWidth:
            data.majorButton.color = "pink2"
            data.minorButton.color = "paleVioletRed"
            data.singleButton.color = "pink2"
            data.mode = "minorScreen"
        #if user clicked on single button, change selected to single
        elif data.singleButton.x <= event.x <= data.singleButton.x + data.buttonWidth:
            data.majorButton.color = "pink2"
            data.minorButton.color = "pink2"
            data.singleButton.color = "paleVioletRed"
            data.mode = "singleScreen"
    elif (data.mode == "playSongScreen"): playSongScreenMousePressed(event,data)
    elif (data.mode == "majorScreen"): majorScreenMousePressed(event, data)
    elif (data.mode == "minorScreen"): minorScreenMousePressed(event, data)
    elif (data.mode == "singleScreen"): singleScreenMousePressed(event, data)
    elif (data.mode == "introScreen"): introScreenMousePressed(event,data)
    elif (data.mode == "learningScreen"): learningScreenMousePressed(event,data)

def keyPressed(event, data):
    if (data.mode == "learningScreen"):learningScreenKeyPressed(event,data)
    elif (data.mode == "playSongScreen"):playSongScreenKeyPressed(event,data)
    elif (data.mode == "majorScreen"): majorScreenKeyPressed(event, data)
    elif (data.mode == "minorScreen"): minorScreenKeyPressed(event, data)
    elif (data.mode == "singleScreen"): singleScreenKeyPressed(event, data)
    elif (data.mode == "introScreen"): introScreenKeyPressed(event,data)

def timerFired(data):
    if (data.mode == "learningScreen"): learningScreenTimerFired(data)
    elif (data.mode == "playSongScreen"): playSongScreenTimerFired(data)
    elif (data.mode == "majorScreen"): majorScreenTimerFired(data)
    elif (data.mode == "minorScreen"): minorScreenTimerFired(data)
    elif (data.mode == "singleScreen"): singleScreenTimerFired(data)
    elif (data.mode == "introScreen"): introScreenTimerFired(data)


def formatString(data):
    #converts data.song, which is a list, into a string
    result = ""
    for note in data.song:
        result += note + " "
    return result

def redrawAll(canvas, data):
    if data.mode == "introScreen":
        introScreenRedrawAll(canvas,data)
    else:
        if data.mode == "learningScreen":
            learningScreenRedrawAll(canvas,data)
        elif data.mode == "playSongScreen":
            playSongScreenRedrawAll(canvas,data)
        else:
            draw(canvas, data)
        
        
####################################
# intro screen mode
####################################
def introScreenMousePressed(event, data):
    #check if user clicked on start button
    x = data.startButton.x
    y = data.startButton.y
    if (x  <= event.x <= x + data.startButton.width) and \
    (y <= event.y <= y + data.startButton.height):
        data.mode = "majorScreen"

def introScreenKeyPressed(event, data):
    if event.keysym == "s":
        data.mode = "majorScreen"

def introScreenTimerFired(data):
    pass
    
def introScreenRedrawAll(canvas,data):
    #background image
    canvas.create_image(0,0,anchor="nw",image=data.background2)
    #brag a lil bit
    canvas.create_text(data.width/2 + data.margin2, data.height/2,  
    text= "The best, all-in-one ukulele composition and learning app", 
    fill="pink2", font = "Helvetica 16 bold")
    #instructions
    canvas.create_text(data.width/2 + data.margin2, data.height/2 + data.margin4, 
    text= "Press START or 's' to begin composing your song", 
    fill="paleVioletRed", font = "Helvetica 18 bold")
    data.startButton.draw(canvas)
    
        
####################################
# major chord screen mode
####################################

def majorScreenMousePressed(event, data):
    for button in data.buttons:
        if button.x <= event.x <= button.x + button.width:
            if button.y <= event.y <= button.y + button.height:
                data.selected = button.name
                #updates the canvas so that the sound plays at the same time
                #as the button turns green
                redrawAll(data.canvas, data)
                data.canvas.update()
                audioThings.play("sounds/chords/" + button.name + ".wav")
            

def majorScreenKeyPressed(event, data):
    #adds note if you press return, undos the latest note added if you press u
    if event.keysym == "Return":
        data.song.append(data.selected)
        #if the song has no incomplete chord progressions, don't suggest anything
        if len(data.song) % 4 == 0:
            data.recs = []
        #if the song has incomplete chord progressions, suggest a chord
        else:
            #divide song by four to see how many complete chord progressions 
            #there are, and then multiply to get beginning of incomplete 
            #chord progression --> this is the starting index
            start = (len(data.song)//4)*4
            prog = data.song[start:]
            data.recs = generatingStuff.findProg(data.root, prog)
    if event.keysym == "u":
        if len(data.song) != 0:
            data.song.pop()
    if event.keysym == "l" :
        if len(data.song) != 0:
        #initialize note and notes to draw to first note of song
            data.note = data.song[0]
            data.notesToDraw = learning.getChords(data.note,data)
            data.mode = "learningScreen"
    elif event.keysym == "p":
        if len(data.song) != 0:
        #resets data.timer so that the animation plays from beginning again
            data.timer = -1
            data.mode = "playSongScreen"

def majorScreenTimerFired(data):
    pass

    
####################################
# minor chord screen mode
####################################

def minorScreenMousePressed(event, data):
    for button in data.buttons:
        if button.x <= event.x <= button.x + button.width:
            if button.y <= event.y <= button.y + button.height:
                data.selected = button.name
                #updates the canvas so that the sound plays at the same time
                #as the button turns green
                redrawAll(data.canvas, data)
                data.canvas.update()
                audioThings.play("sounds/chords/" + button.name + "m.wav")

def minorScreenKeyPressed(event, data):
    #adds note if you press return, undos the latest note added if you press u
    if event.keysym == "Return":
        data.song.append(data.selected + "m")
        #if the song has no incomplete chord progressions, don't suggest anything
        if len(data.song) % 4 == 0:
            data.recs = []
        #if the song has incomplete chord progressions, suggest a chord
        else:
            #divide song by four to see how many complete chord progressions 
            #there are, and then multiply to get beginning of incomplete 
            #chord progression --> this is the starting index
            start = (len(data.song)//4)*4
            prog = data.song[start:]
            data.recs = generatingStuff.findProg(data.root, prog)
    if event.keysym == "u":
        if len(data.song) != 0:
            data.song.pop()
    if event.keysym == "l" :
        if len(data.song) != 0:
        #initialize note and notes to draw to first note of song
            data.note = data.song[0]
            data.notesToDraw = learning.getChords(data.note,data)
            data.mode = "learningScreen"
    elif event.keysym == "p":
        if len(data.song) != 0:
        #resets data.timer so that the animation plays from beginning again
            data.timer = -1
            data.mode = "playSongScreen"
    
def minorScreenTimerFired(data):
    pass



####################################
# single note screen mode
####################################

def singleScreenMousePressed(event, data):
    for button in data.buttons:
        if button.x <= event.x <= button.x + button.width:
            if button.y <= event.y <= button.y + button.height:
                data.selected = button.name
                #updates the canvas so that the sound plays at the same time
                #as the button turns green
                redrawAll(data.canvas, data)
                data.canvas.update()
                audioThings.play("sounds/single/" + button.name + "(s).wav")

def singleScreenKeyPressed(event, data):
    #adds note if you press return, undos the latest note added if you press u
    if event.keysym == "Return":
        data.song.append(data.selected + "(s)")
        #if the song has no incomplete chord progressions, don't suggest anything
        if len(data.song) % 4 == 0:
            data.recs = []
        #if the song has incomplete chord progressions, suggest a chord
        else:
            #divide song by four to see how many complete chord progressions 
            #there are, and then multiply to get beginning of incomplete 
            #chord progression --> this is the starting index
            start = (len(data.song)//4)*4
            prog = data.song[start:]
            data.recs = generatingStuff.findProg(data.root, prog)
    if event.keysym == "u":
        if len(data.song) != 0:
            data.song.pop()
    if event.keysym == "l" :
        if len(data.song) != 0:
        #initialize note and notes to draw to first note of song
            data.note = data.song[0]
            data.notesToDraw = learning.getChords(data.note,data)
            data.mode = "learningScreen"
    elif event.keysym == "p":
        if len(data.song) != 0:
        #resets data.timer so that the animation plays from beginning again
            data.timer = -1
            data.mode = "playSongScreen"

def singleScreenTimerFired(data):
    pass
    
#####
# learning screen mode
#####
def learningScreenMousePressed(event, data):
    pass

def learningScreenKeyPressed(event, data):
    learning.keyPressed(event,data)

def learningScreenTimerFired(data):
    pass
    
def learningScreenRedrawAll(canvas,data):
    learning.redrawAll(canvas,data)
    #Instructions
    canvas.create_text(data.margin, data.margin2, 
        text="Press enter to move to the next chord", anchor = "nw",
        font = "Helvetica 16 italic", fill = "paleVioletRed")
    canvas.create_text(data.margin, data.margin2*2, 
        text="Press a to see how the chord is played", anchor = "nw",
        font = "Helvetica 16 italic", fill = "paleVioletRed")
    canvas.create_text(data.margin, data.margin2*3, 
        text="Press t to learn to play the current chord", anchor = "nw",
        font = "Helvetica 16 italic", fill = "paleVioletRed")
    canvas.create_text(data.width - data.margin, data.height - data.margin2, 
        text="Press m to return to composing your song", anchor = "e",
        font = "Helvetica 16 italic", fill = "paleVioletRed")
    #song
    song = formatString(data)
    canvas.create_text(data.margin, data.height-data.margin, fill = "paleVioletRed",
            text="Song: " + song, anchor = "nw", font = "Helvetica 18 bold italic")


    
###
# play song mode
####
def playSongScreenMousePressed(event, data):
    pass
    
def playSongScreenKeyPressed(event, data):
    if event.keysym == "l":
        data.mode = "learningScreen"
    else:
        learning.keyPressed(event,data)

def playSongScreenTimerFired(data):
    data.timer += 1
    #every 0.5 s, play the next note and update the screen so that it displays
    #the chord 
    if data.timer % 5 == 0:
        i = data.timer//5
        #ensures that the animation stops after it has played the song once
        if i < len(data.song):
            data.note = data.song[i%len(data.song)]
            data.notesToDraw = learning.getChords(data.note, data)
            playSongScreenRedrawAll(data.canvas, data)
            data.canvas.update()
            if "(s)" in data.note:
                audioThings.play("sounds/single/" + data.note + ".wav")
            else:
                audioThings.play("sounds/chords/" + data.note + ".wav")
            #reset screen so it is just the strings (bc otherwise the chord 
            #displays lay on top of each other)
            data.note = ""
            data.notesToDraw = []
            playSongScreenRedrawAll(data.canvas, data)
            data.canvas.update()
            
def playSongScreenRedrawAll(canvas,data):
    #display the note at top center of the screen
    canvas.create_text(data.width//2, data.margin3//2, text=data.note, 
    font="Arial 26 bold", fill="pink2")
    #draw the strings
    learning.drawStrings(canvas, data)
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
            canvas.create_oval(cx-data.circleSize, cy - data.circleSize, 
            cx + data.circleSize, cy + data.circleSize, fill = fill)
    #song
    song = formatString(data)
    canvas.create_text(data.margin, data.height-data.margin, fill = "paleVioletRed",
            text="Song: " + song, anchor = "nw", font = "Helvetica 18 bold italic")
    #instructions
    canvas.create_text(data.margin, data.margin2, 
        text="Press m to return to composing or l to learn your song!", anchor = "nw",
        font = "Helvetica 16 italic", fill = "paleVioletRed")

#draw func for major, minor, and single screen
def draw(canvas, data):
    #draws background
    canvas.create_image(0,0,anchor="nw",image=data.background1)
    #instructions
    canvas.create_text(data.margin, data.margin2, 
        text="Click a note and then press enter to add a chordnote to your song, press u to undo", anchor = "nw",
        font = "Helvetica 16 italic", fill = "paleVioletRed")
    canvas.create_text(data.margin, data.margin2*2, 
        text="Press l to learn your song", anchor = "nw",
        font = "Helvetica 16 italic", fill = "paleVioletRed")
    canvas.create_text(data.margin, data.margin2*3, 
        text="Press p to have the computer play your song!", anchor = "nw",
        font = "Helvetica 16 italic", fill = "paleVioletRed")
    #draws buttons for diff screens
    data.majorButton.draw(canvas)
    data.minorButton.draw(canvas)
    data.singleButton.draw(canvas)
    #draws all the buttons for chords/notes
    for button in data.buttons:
        if button.name == data.selected:
            button.color = "paleVioletRed"
        else:
            button.color = "pink2"
        button.draw(canvas)
    #draw the suggestion box
    margin = 40
    margin2 = 175
    width =125
    margin3 = 10
    margin4 = 30
    left = data.width - margin2
    top = data.height-data.margin3
    if len(data.recs) != 0:
        canvas.create_rectangle(left, top, left + width, 
        top + margin*len(data.recs) + margin3, fill = "lemonchiffon", width=0)
        canvas.create_text(left + margin3, top + margin3, 
        text="Suggestions:", font = "Helvetica 16 bold", anchor = "nw", fill="paleVioletRed")
        for i, rec in enumerate(data.recs):
            canvas.create_text(left + margin3, top + margin3 + margin4*(i+1),
            text = rec, font = "Helvetica 14 bold", fill ="paleVioletRed", anchor = "w")
        canvas.create_text(data.margin, data.height - data.margin2*3, 
            text="Don't know what chord to add next? Look at the suggestions box!", anchor = "nw",
            font = "Helvetica 16 italic", fill = "paleVioletRed")
    #draw song
    song = formatString(data)
    canvas.create_text(data.margin, data.height-data.margin*2, fill = "paleVioletRed",
            text="Song: " + song, anchor = "nw", font = "Helvetica 24 bold italic")
            
    
####################################
# use the run function as-is
####################################
#This is taken from the course lecture notes on time based animation
def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
    root = Tk()
    root.resizable(width=False, height=False) # prevents resizing window
    init(data)
    # create the root and the canvas
    data.canvas = Canvas(root, width=data.width, height=data.height)
    data.canvas.configure(bd=0, highlightthickness=0)
    data.canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, data.canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, data.canvas, data))
    timerFiredWrapper(data.canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run(700,500)

