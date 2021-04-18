import numpy as np
import cv2
import tkinter
from tkinter import *
from PIL import Image
import sys
f = open("archive/temporary.csv", "w")
cap = cv2.VideoCapture(0)

# actual number  =  number + 1
number = 0


def runn():
    cap = cv2.VideoCapture(0)

    i = 0
    while True:
        global number
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)

        grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        rect_img = grayFrame[100:400, 300:600]
        resized_image = cv2.resize(rect_img, (28, 28))

        frame = cv2.rectangle(frame, (300, 100), (600, 400), (255, 0, 0), 5)

        cv2.imshow('video gray', rect_img)
        cv2.imshow('video original', frame)

        if i < 160:
            resized_image = resized_image.reshape((1, 28, 28))
            resized_image = resized_image.flatten()
            ans = ','.join([str(i) for i in resized_image])
            ans = str(number) + "," + ans
            f.write(ans)
            f.write("\n")
            i += 1
        else:
            cap.release()
            cv2.destroyAllWindows()
            break

        if cv2.waitKey(1) == ord('q'):
            cap.release()
            cv2.destroyAllWindows()
            break

    number += 1


def helloCallBack():
    B['text'] = "Capture images for digit = "+str(number+2)
    runn()


root = tkinter.Tk()
root.title('Capture Images')
root.geometry("340x200")
root = Canvas(root, width=340, height=200)
root.pack(fill="both", expand=True)

text = "Capture images for digit = 1"
root.create_text(180, 40, fill="darkblue", font="Times 20 italic bold",
                 text="Capture Images")


B = tkinter.Button(
    root, text=text, fg='darkblue',
    font="Times 15 italic bold",  command=helloCallBack)
B.place(x=20, y=80)

root.mainloop()
