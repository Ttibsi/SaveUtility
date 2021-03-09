#!/usr/bin/env python3

'''
Programmed by Ash Isbitt
Version - 1.0
'''

# import modules
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import ctypes
import os
import platform
import sys
import shutil
import datetime

#global variables
dir_Name = ""
finalVal = ""
totalSize = 0
totalSize_bytes = 0
intFileCount_bytes = 0

##################################################################

'''
FUNCTION: testPrint
PURPOSE: Allow the developer to test buttons functionality before
their functions are complete
PARAMETERS: NULL
'''

def testPrint():
    print("test")

##################################################################

'''
FUNCTION: inPath
PURPOSE: Collate functions for btn_inPath to run
PARAMETERS:
    - entry - entrybox used to store path
'''

def inPath(entry):
    global dir_Name
    
    setPath(entry)
    getFileCount(dir_Name)

##################################################################
    
'''
FUNCTION: setPath
PURPOSE: Allows the user to define a specific path
PARAMETERS:
    - entry - entrybox used to store paths
'''

# https://stackoverflow.com/questions/25282883/how-can-i-use-the-output-from-tkfiledialog-askdirectory-to-fill-a-tkinter-entry

def setPath(entry):
    try:
        global dir_Name
        dir_Name = filedialog.askdirectory()
        print(dir_Name)
        
        entry.insert(0, str(dir_Name))
        return 
    except Exception as e:
        print("Error: setPath")
        print(e)

##################################################################

'''
FUNCTION: getFileCount
PURPOSE: Count the number of files in a directory (including subdirectories)
PARAMETERS:
    - dir_Name - User's specified directory

SRC: https://stackoverflow.com/questions/29769181/count-the-number-of-folders-in-a-directory-and-subdirectories
Created by jonrsharpe
Modified by Ash Isbitt
'''

def getFileCount(dir_Name):
    files = 0
    global totalSize
    global totalSize_bytes

    #collate the number of files in a directory and all subdirectories
    for dirpath, dirnames, filenames in os.walk(dir_Name):
        files += len(filenames)
        print(files)

        #get the total file size of all selected files
        for f in filenames:
            fp = os.path.join(dirpath, f)
            totalSize += os.path.getsize(fp)

    print(totalSize)
           
    lbl_inCount.config(text="Files to Move: " + str(int(files)))
    convertedSize = byteConverter(totalSize)
    lbl_inSize.config(text="Total size: " + str(convertedSize))

    totalSize_bytes = int(totalSize)
    
##################################################################

'''
FUNCTION: byteConverter
PURPOSE: To take an integer as bytes and divide until a human readable value
        is created
PARAMETERS:
    - byteCount - the value in bytes of free space on a given directory
'''

def byteConverter(byteCount):
    byteCount = byteCount
    sizeListIndex = 0
    sizeList = ["bytes",
                "KB",
                "MB",
                "GB",
                "TB"]

    #convert a value down from bytes to a readable value
    while byteCount >= 1024 and sizeListIndex < (len(sizeList)-1):
        byteCount /= 1024
        sizeListIndex += 1

    #set the value to 2 D.P.
    finalVal = "{0:.2f}".format(byteCount)
    print(finalVal + " " + sizeList[sizeListIndex])
    return( finalVal + " " + sizeList[sizeListIndex])

##################################################################
    
'''
FUNCTION: getEmptySpace
PURPOSE: Detect how much empty storage is available on a selected external drive
PARAMETERS:
    - dirname - the directory to evaluate

https://stackoverflow.com/questions/51658/cross-platform-space-remaining-on-volume-using-python

written by Frankovskyi Bogdan
'''

def getEmptySpace(dirname):

    global finalVal
    global intFileCount_bytes
    
    """Return folder/drive free space (in megabytes)."""
    if platform.system() == 'Windows':
        free_bytes = ctypes.c_ulonglong(0)
        ctypes.windll.kernel32.GetDiskFreeSpaceExW(ctypes.c_wchar_p(dirname), None, None, ctypes.pointer(free_bytes))
        finalVal = byteConverter(intFileCount)
        lbl_outFreeSpace.config(text="Free space on disk: " + finalVal)
    else:
        st = os.statvfs(dirname)
        intFileCount = int(st.f_bavail * st.f_frsize)
        finalVal = byteConverter(intFileCount)
        lbl_outFreeSpace.config(text="Free space on disk: " + finalVal)

    intFileCount_bytes = int(intFileCount)
##################################################################

'''
FUNCTION: outPath
PURPOSE: Collate functions for btn_outPath to run
PARAMETERS:
    - entry_outPath - the entrybox used to store the path
'''

def outPath(entry_outPath):
    global dir_Name

    setPath(entry_outPath)
    getEmptySpace(dir_Name)

##################################################################

'''
FUNCTION: prereqChecks
PURPOSE: To check user input before executing file move functions
PARAMETERES: NULL
'''

def prereqChecks():
    print ("prereq")

    global finalVal
    global totalSize

    #check if both entry boxes have paths
    if not len(entry_inPath.get()) == 0 and not len(entry_outPath.get()) == 0:
        # check if destination has enough space
        if int(totalSize_bytes) <= intFileCount_bytes:
            print("execute")
            execute()
        else:
            messagebox.showinfo("Alert", 'Not enough space in selected output')
    else:
        messagebox.showinfo("Alert", "Choose locations")

##################################################################

'''
FUNCTION: execute
PURPOSE: Create a new folder in the destination location and copy over all files from
    source location
PARAMETERES: NULL
'''

def execute():
    print("confirm")

    #get current date
    dt = str(datetime.datetime.now().date())
    print(dt)

    if platform.system() == 'Windows':
        dirJoin = "\\"
    else:
        dirJoin = "/"
    
    #get locations
    src = entry_inPath.get()
    dest = (entry_outPath.get() + dirJoin + dt)
    print(dest)

##    #create new folder
##    if not os.path.exists(dest):
##        print("Creating directory")
##        os.makedirs(dest)
##    else:
##        print("dir exists")

    #copy files over
    shutil.copytree(src, dest)
    messagebox.showinfo("success!", "file copying complete")
    
##################################################################

#create TK interface
root = Tk()
root.resizable(False, False)
root.title("SaveUtility V1.0")

#create widgets
lbl_inPath = Label(root, text = "Source Location")
lbl_outPath = Label(root, text = "Destination Location")
entry_inPath = Entry(root)
entry_outPath = Entry(root)
btn_inPath = Button(root, text='>', command=lambda:inPath(entry_inPath))
btn_outPath = Button(root, text='>', command=lambda:outPath(entry_outPath))
lbl_inCount = Label(root, text="Files to Move: ")
lbl_inSize = Label(root, text="Total size: ")
lbl_outFreeSpace = Label(root, text="Free space on disk: ")
btn_execute = Button(root, text="Execute", command=prereqChecks)

#grid placement
lbl_inPath.grid(row=0, sticky=E)
lbl_outPath.grid(row=1, sticky=E)
entry_inPath.grid(row=0,column=1)
entry_outPath.grid(row=1,column=1)
btn_inPath.grid(row=0,column=2)
btn_outPath.grid(row=1,column=2)
lbl_inCount.grid(row=2, columnspan=2)
lbl_inSize.grid(row=3, columnspan=2)
lbl_outFreeSpace.grid(row=4, columnspan=2)
btn_execute.grid(row=5,columnspan=2)

##################################################################

# run interface
root.mainloop()
