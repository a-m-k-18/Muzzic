from tkinter import *
import tkinter.messagebox
from pygame import mixer
from tkinter import filedialog
from mutagen.mp3 import MP3
from tkinter import ttk
from ttkthemes import themed_tk as tk
import time
import threading
import os

root = tk.ThemedTk()
root.get_themes()
root.set_theme("plastik")

statusbar = ttk.Label(root , text = "Welcome to Muzzic" , relief = SUNKEN)
statusbar.pack(side = BOTTOM , fill_ = X)
# THE MENU BAR
menubar = Menu(root)
root.config(menu=menubar)

playlist = []

def browseFile():
    global filename_path
    filename_path = filedialog.askopenfilename()
    addToPlaylist(filename_path)

def addToPlaylist(filename):
    filename = os.path.basename(filename)
    index = 0
    playlistbox.insert(index, filename)
    playlist.insert(index , filename_path)
    index +=1

def delSong():
    selectedSong = playlistbox.curselection()
    selectedSong = int(selectedSong[0])
    playlistbox.delete(selectedSong)
    playlist.pop(selectedSong)

# MENU BAR CONTENTS
#
submenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="File", menu=submenu)
submenu.add_command(label="Open", command=browseFile)
submenu.add_command(label="Exit", command=root.destroy)


def about_us():
    tkinter.messagebox.showinfo("Muzzic", "Created by Aravind M Krishnan , NIT Puducherry")


submenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Help", menu=submenu)
submenu.add_command(label="About Us", command=about_us)

mixer.init()  # Intitializing the mixer


root.title("Muzzic")

leftFrame = Frame(root)
leftFrame.pack(side = LEFT)

playlistbox = Listbox(leftFrame)
playlistbox.pack()

rightFrame = Frame(root)
rightFrame.pack()

topFrame = Frame(rightFrame)
topFrame.pack()

lengthLabel = ttk.Label(topFrame, text="Total Time : -- : --")
lengthLabel.pack(pady = 5)

currentTimeLabel = ttk.Label(topFrame, text="Remaining Time : -- : --" , relief = GROOVE)
currentTimeLabel.pack()

addBtn = ttk.Button(leftFrame , text = "+ ADD" , command = browseFile)
addBtn.pack(side = LEFT)

delBtn = ttk.Button(leftFrame , text = "+ DEL" , command = delSong)
delBtn.pack()


def showDetails(playSong):

    audio = MP3(playSong)
    totalLength = audio.info.length
    mins , secs = divmod(totalLength , 60)
    mins = round(mins)
    secs = round(secs)
    timeformat = '{:02d}:{:02d}'.format(mins, secs)
    lengthLabel['text'] = "Total Length" + ' - ' + timeformat

    t1 = threading.Thread(target= startCount , args = (totalLength , ))
    t1.start()

def startCount(t):
    global paused
    while t and mixer.music.get_busy():
        if paused:
            continue
        else:
            mins, secs = divmod(t, 60)
            mins = round(mins)
            secs = round(secs)
            timeformat = '{:02d}:{:02d}'.format(mins, secs)
            currentTimeLabel['text'] = "Remaining Time " + ' - ' + timeformat
            time.sleep(1)
            t -= 1

def playMusic():
    global paused
    if paused:
        mixer.music.unpause()
        statusbar['text'] = "Music Resumed"
        paused = FALSE
    else:
        try:
            stopMusic()
            time.sleep(1)
            selectedSong = playlistbox.curselection()
            selectedSong = int(selectedSong[0])
            playIt = playlist[selectedSong]
            mixer.music.load(playIt)
            mixer.music.play()
            statusbar['text'] = "Playing Music " + ' ' + os.path.basename(playIt)
            showDetails(playIt)
        except:
            tkinter.messagebox.showerror('File not found ', 'Muzzic could not find the file.')

def stopMusic():
    mixer.music.stop()
    statusbar['text'] = "Music Stopped"

def setVol(val):
    volume = float(val) / 100
    mixer.music.set_volume(volume)

paused = FALSE

def pauseMusic():
    global paused
    paused = TRUE
    mixer.music.pause()
    statusbar['text'] = "Music Paused"

def rewindMusic():
    playMusic()
    statusbar['text'] = "Music Rewinded"

muted = FALSE

def muteMusic():
    global muted
    if muted:
        mixer.music.set_volume(0.5)
        volumeBtn.configure(image=volumePhoto)
        scale.set(50)
        muted = FALSE
    else:
        mixer.music.set_volume(0)
        volumeBtn.configure(image = mutePhoto)
        scale.set(0)
        muted = TRUE

middleFrame  = Frame(rightFrame)
middleFrame.pack(padx = 10, pady = 10)

playPhoto = PhotoImage(file="images/baseline_play_circle_filled_black_48dp.png")
playBtn = ttk.Button(middleFrame, image=playPhoto, command=playMusic)
playBtn.grid(row = 0 , column =0  ,padx = 10)

stopPhoto = PhotoImage(file="images/baseline_stop_black_48dp.png")
stopBtn = ttk.Button(middleFrame, image=stopPhoto, command=stopMusic)
stopBtn.grid(row = 0 , column =1  ,padx = 10)

pausePhoto = PhotoImage(file="images/baseline_pause_circle_filled_black_48dp.png")
pauseBtn = ttk.Button(middleFrame, image=pausePhoto, command=pauseMusic)
pauseBtn.grid(row = 0 , column =2  ,padx = 10)

rewindPhoto = PhotoImage(file="images/baseline_fast_rewind_black_48dp.png")
rewindBtn = ttk.Button(middleFrame, image=rewindPhoto, command=rewindMusic)
rewindBtn.grid(row = 0 , column = 3 , padx = 10)

bottomFrame  = Frame(rightFrame)
bottomFrame.pack(padx = 10, pady = 10)

mutePhoto = PhotoImage(file="images/baseline_volume_mute_black_18dp.png")
volumePhoto = PhotoImage(file = "images/baseline_volume_up_black_18dp.png")
volumeBtn = ttk.Button(bottomFrame, image = volumePhoto, command=muteMusic)
volumeBtn.grid(row = 0 , column = 0 , padx = 10)

scale = Scale(bottomFrame, from_=0, to=100, orient=HORIZONTAL, command=setVol)
scale.set(50)
mixer.music.set_volume(50)
scale.grid(row = 0 , column = 1 , padx =30 , pady = 15)


def onClosing():
    tkinter.messagebox.showinfo('Bye' , 'Thanks for using Muzzic')
    root.destroy()

root.protocol("WM_DELETE_WINDOW" , onClosing)
root.mainloop()
