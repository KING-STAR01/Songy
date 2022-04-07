#!/usr/bin/python3 main.py
import os.path
import tkinter
from tkinter import filedialog
import SongDownload
import movieLists
from functools import partial
from entrywidget import *
import threading
import time


def frame(root, side):
    w = Frame(root)
    w.pack(side=side, expand=NO, fill=X)
    return w


def button(root, side, text, command=None):
    b = Button(root, text=text, command=command)
    b.configure(height=2, width=20)
    b.pack(side=side, expand=NO, fill=X)
    return b


movienamesobj = movieLists.GetNames()
MOVIELIST = movienamesobj.movielist
movielinksobj = movieLists.GetLinks()
MOVIELINKS = movielinksobj.movielinkslist


class Songy(Tk):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mainFrame()
        self.mainloop()
        self.filepath = os.path.curdir

    def getPath(self):

        dir_name = filedialog.askdirectory()
        self.filepath = dir_name

    def clear(self):
        self.entry.delete(0, tkinter.END)

    def driverSearch(self):

        thread = threading.Thread(target=self.search)
        thread.start()
        # thread.join()

    def driverDownloadAll(self):
        thread = threading.Thread(target=self.downloadAll)
        thread.start()

    def driverDownload(self,moviesongs,quality,id,path):
        thread = threading.Thread(target = moviesongs.download,args=(quality,id,path))
        thread.start()

    def mainFrame(self):

        self.title("Songy")
        self.geometry(f'{self.winfo_screenwidth()}x{self.winfo_screenheight()}')
        # self.resizable(False, False)

        label = Label(self, text="SONGY", font=("Times", "24", "bold italic"), height=2)
        label.pack(side=TOP, expand=NO, fill=X)

        searchFrame = frame(self, TOP)
        self.display = StringVar()
        large_font = ('Verdana', 26)
        self.entry = AutocompleteEntry(MOVIELIST, searchFrame)
        self.entry.focus()

        b2 = button(searchFrame, RIGHT, "CLEAR", self.clear)
        b2.configure(font=("Times", "14", "bold"))

        b1 = button(searchFrame, RIGHT, "SELECT FOLDER", self.getPath)
        b1.configure(font=("Times", "14", "bold"))

        b = button(searchFrame, RIGHT, "SEARCH", self.driverSearch)
        b.configure(font=("Times", "14", "bold"))

        self.entry.pack(side=TOP, expand=NO, fill=X)

        # for displaying and downloading songs

        self.songsFrame = frame(self, TOP)

        self.canvas = Canvas(self.songsFrame, height=850)
        self.scrollbar = Scrollbar(self.songsFrame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        bb = Button(self.songsFrame, text="DOWNLOAD ALL", command=partial(self.driverDownloadAll))
        bb.configure(width=15, height=3, background="cyan")
        bb.pack(side=BOTTOM)
        self.songsFrame.pack(pady=20)

    def downloadAll(self):
        if (self.entry.get() == ''):
            tkinter.messagebox.showinfo("Error....!", "please enter a movie name")
            return False
        if self.filepath is None:
            tkinter.messagebox.showinfo("Error....!", "please a folder to download")
            return False

        ind = MOVIELIST.index(self.entry.get())
        url = MOVIELINKS[ind]
        moviesongs = SongDownload.SongDownload(url)

        for i in moviesongs.songsNormal:

            thread = threading.Thread(target=moviesongs.download, args=(1, moviesongs.songsNormal.index(i), self.filepath))
            time.sleep(0.4)
            thread.start()

        return True

    def search(self):

        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        if (self.entry.get() == ''):
            tkinter.messagebox.showinfo("ALERT...!!.", "please enter a movie name")
            return False
        if self.filepath is None:
            tkinter.messagebox.showinfo("ALERT...!!.", "Please select a folder to download")
            return False

        ind = MOVIELIST.index(self.entry.get())
        url = MOVIELINKS[ind]
        moviesongs = SongDownload.SongDownload(url)

        for i in moviesongs.songsNormal:
            print(moviesongs.songsNormal.index(i), i)
            sFrame = frame(self.scrollable_frame, TOP)
            Button(sFrame, text="Download",
                   command=partial(self.driverDownload, moviesongs, 1, moviesongs.songsNormal.index(i), self.filepath)).pack(
                side=RIGHT)

            # if possible implement quality based downloading 128, 320 kbps

            l = Label(sFrame, text=moviesongs.songsNormalNames[moviesongs.songsNormal.index(i)])
            l.configure(height=5, font=("Times", 16))
            l.pack(side=LEFT, padx=5)
        return True


if __name__ == '__main__':
    # print(MOVIELIST)
    obj = Songy()
