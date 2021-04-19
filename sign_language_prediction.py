import tensorflow as tf
import tensorflow.keras
import cv2
import tkinter
from tkinter import *
import statistics
from statistics import mode

model = tensorflow.keras.models.load_model("sign_model.h5")
digit_array = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
digits = cv2.imread("archive/digits.png")
white = cv2.imread("archive/white.png")


def predict_letter(image):
    image = image.reshape((1, 28, 28, 1))
    res = model.predict(image)
    res = list(res[0])
    mx = max(res)
    return digit_array[res.index(mx)]


def view_signs():
    cv2.imshow('Sign Digits', digits)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def run_digit_recognition():
    cap = cv2.VideoCapture(0)
    history = [""]
    max_freq_array = ["" for _ in range(20)]
    freq_num = 0

    while True:
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)

        grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # grayFrame = cv2.bitwise_not(grayFrame)
        rect_img = grayFrame[100:400, 300:600]
        resized_image = cv2.resize(rect_img, (28, 28))

        # predict the sign
        ans_letter = predict_letter(resized_image)
        text = "Predicted Digit = " + ans_letter

        # to find the most accurate predicted sign
        max_freq_array[freq_num % 20] = ans_letter
        freq_num += 1
        current_best_number = mode(max_freq_array)
        if history[0] != current_best_number:
            history = [current_best_number] + history[:]

        white_temp = white.copy()
        cv2.putText(white_temp, "history",
                    (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (139, 0, 0), 2)
        cv2.putText(white_temp, ",".join(history),
                    (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (139, 0, 0),  2)
        cv2.imshow('Recorded Predictions', white_temp)

        # display captured images and grayscale
        frame = cv2.rectangle(frame, (300, 100), (600, 400), (139, 0, 0), 5)
        cv2.putText(frame, text,
                    (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (139, 0, 0),  2)

        cv2.imshow('Video gray', rect_img)
        cv2.imshow('Video original', frame)

        # outline predicted sign in the sign chart
        temp_ans = int(ans_letter)-1
        pt1x = int(1161 * temp_ans / 9)
        pt2x = int(1161 * (temp_ans + 1) / 9)
        digits_temp = digits.copy()
        digits_temp = cv2.rectangle(
            digits_temp, (pt1x, 0), (pt2x, 240), (0, 255, 0), 5)
        cv2.imshow('Digits Signs', digits_temp)

        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


def tkintercallback():
    run_digit_recognition()


def tkintercallback2():
    view_signs()


root = tkinter.Tk()
root.title('Sign Language Prediction')
root.geometry("757x501")
bg = PhotoImage(file="archive/bg.png")
root = Canvas(root, width=757, height=501)
root.pack(fill="both", expand=True)
root.create_image(0, 0, image=bg, anchor="nw")
root.create_text(370, 40, fill="darkblue", font="Times 30 italic bold",
                 text="Welcome to Sign Language Prediction")

B = Button(root, text="Predict Gesture", fg='darkblue',
           font="Times 27 italic bold", command=tkintercallback)
B2 = Button(root, text="View the Signs", fg='darkblue',
            font="Times 27 italic bold", command=tkintercallback2)

B.place(x=60, y=350)
B2.place(x=460, y=350)

root.mainloop()
