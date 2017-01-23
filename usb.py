import os
import shutil


def usbexport():
    source = "/home/pi/Desktop/"
    destination = "/media/pi/CRTEXPORT"
    #dest2="/media/pi/CRT/testing.text"
    #CHANGE NAME OF TANVI TO CRT AND THE PENDRIVE BEING CONNECTED SHOULD BE NAMED CRT
    for filename in os.listdir(source):
        if filename.endswith("exporting.dat"):
            shutil.move(source + filename,destination)
   
