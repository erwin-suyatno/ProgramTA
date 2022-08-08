from __future__ import print_function
import cv2
import imutils
from imutils import face_utils
import tkinter as tk
from PIL import Image,ImageTk
import dlib
import time
from datetime import datetime

from gaze_tracking import GazeTracking


gaze = GazeTracking()
now = time.localtime()
counter = 666000
running = False
kanan = 0
kiri = 0
total = 0
pkanan = 0
pkiri = 0

pindahkanan= 0
pindahkiri = 0

def counter_label(label):
    def count():
        if running:
            global counter
            if counter == 666000:
                display = "Starting..."
            else:
                tt = datetime.fromtimestamp(counter)
                string = tt.strftime("%H:%M:%S")
                display = string
            label['text'] = display
            batas()
            label.after(1000, count)
            counter += 1
    count()

def batas():
    global pindahkiri
    global pindahkanan
    global kanan
    global kiri
    global total
    if gaze.is_right():
        if pindahkiri < 1 :
            kiri += 1
            print("kiri")
        pindahkiri += 1
    elif gaze.is_left():
        if pindahkanan < 1 :
            kanan += 1
            print("kanan")
        pindahkanan += 1
    elif gaze.is_center():
        pindahkanan = 0
        pindahkiri = 0
        print("tengah")
    total = kanan + kiri

def Start(label):
    global running
    running = True
    counter_label(label)
    Tblmulai['state'] = 'disabled'
    #stop['state'] = 'normal'
    Tblreset['state'] = 'normal'
    lblkanan['text'] = "0%"
    lblkiri['text'] = "0%"
    lblhasil['text'] = "Hasil"

def Reset(label):
    global counter
    global running
    global total
    global pkanan
    global pkiri
    counter = 666000
    Tblmulai['state'] = 'normal'
    # stop['state'] = 'disabled'
    Tblreset['state'] = 'normal'
    running = False
    pkanan = (kanan / total) * 100
    pkiri = (kiri / total) * 100
    pkanan = round(pkanan, 2)
    pkiri = round(pkiri, 2)

    lblkiri['text'] = str(pkiri) + "%"
    lblkanan['text'] = str(pkanan) + "%"

    if pkanan >= 60 :
        lblhasil['text'] = 'Bohong'
    else:
        lblhasil['text'] = 'Jujur'

    #masuk.delete(0,10)
def f_landmark():
    for face in faces:
        faceshape = landmark_predictor(img, face)
        faceshape = face_utils.shape_to_np(faceshape)  # convert to numpy array to be iterable
        for (x, y) in faceshape:
            cv2.circle(img, (x, y), 1, (0, 255, 0), 1)

def RoI_wajah():
    for (i, rect) in enumerate(faces):
        (x,y,w,h) = face_utils.rect_to_bb(rect)

        cv2.rectangle(img, (x,y),(x + w, y + h), (255, 255, 255), 2)

# windows aplikasi
windows = tk.Tk()
windows.geometry("1120x703+200+10")
windows.title("Deteksi Kbohongan")
windows.resizable(width=False, height=False)
tampilan = tk.PhotoImage(file="tampilan.png")
tampilan1 = tk.Label(windows, image=tampilan).place(x=0, y=0, relwidth=1, relheight=1)

# tombol mulai dan Stop
Tblmulai = tk.Button(windows, text="Mulai", bg="#E4842B", relief="flat",
                     cursor="hand2", command = lambda : Start(label) , width=10, height=1, font=("Calisto MT", 12, "bold"),)
Tblmulai.place(x=750, y=526)
Tblreset = tk.Button(windows, text="Stop", bg="#E4842B", relief="flat",
                     cursor="hand2", command = lambda : Reset(label), width=10, height=1, font=("Calisto MT", 12, "bold"),)
Tblreset.place(x=910, y=526)

#label waktu
label = tk.Label(windows, text="Welcome!",bg= "#F7C598", fg="black", font="Verdana 30 bold")
label.place(x=300, y=570)
"""
masuk = tk.Entry(windows)
masuk.place(x=900, y=110)
lblmasuk = tk.Label(windows, text="Nama  :  ", bg="#FB8D28", fg="black", font="Verdana 10 bold")
lblmasuk.place(x=830, y=110)
Tblmasuk = tk.Button(windows, text="oke", bg="#D6C096", relief="flat",
                     cursor="hand2", command = nama , width=6, height=1, font=("Calisto MT", 10, "bold"),)
Tblmasuk.place(x=1030, y=105)
"""
#label persen dan indikasi
lblkanan = tk.Label(windows, text="0%",bg= "#D6C096", fg="black", font="Verdana 30 bold")
lblkanan.place(x=750, y=185)
lblkiri = tk.Label(windows, text="0%",bg= "#D5C6A3", fg="black", font="Verdana 30 bold")
lblkiri.place(x=750, y=295)
lblhasil = tk.Label(windows, text="Hasil",bg= "#D5CDB0", fg="black", font="Verdana 24 bold")
lblhasil.place(x=750, y=410)

#video
frame_video = tk.Label(windows, bg="black")
frame_video.place(x=120, y=157)
face_detector = dlib.get_frontal_face_detector()
landmark_predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
video = cv2.VideoCapture(0)

while True:
    # Data mata
    img = video.read()[1]
    #img = cv2.flip(img, 1)
    img = imutils.resize(img, height=417)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    gaze.refresh(img)
    img = gaze.annotated_frame()
    nilai = gaze.horizontal_ratio()
    faces = face_detector(img, 1)
    # titik facial landmark
    f_landmark()
    # Roi wajah
    RoI_wajah()
    # muncul video
    img = Image.fromarray(img)
    img = ImageTk.PhotoImage(image=img)
    frame_video['image'] = img
    windows.update()
windows.mainloop()


