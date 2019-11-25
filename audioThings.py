#this function defines all audio-related functions, such as playing and recording audio
import pyaudio
import wave
from tkinter import *
from scipy.fftpack import fft, fftfreq
from scipy.io import wavfile
import numpy as np


### playing note ##

#This is from Tara Stentz's pyaudio demo code
def play(file):
    CHUNK = 1024
    wf = wave.open(file, 'rb')
    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)
    data = wf.readframes(CHUNK)
    while len(data) > 0:
        stream.write(data)
        data = wf.readframes(CHUNK)
    stream.stop_stream()
    stream.close()
    p.terminate()

### recording a note ###    
#This is from Tara Stentz's pyaudio demo code
def record(outputFile):
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    RECORD_SECONDS = 1

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("* recording")

    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("* done recording")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(outputFile, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    
##detecting pitch##
#This is my own code
#This detects the dominant pitch of a file
def findDomFreq(filename):
    samplerate, data = wavfile.read(filename)
    data = data[:,0]
    datafft = abs(fft(data))
    return np.argmax(datafft)



