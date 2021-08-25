import cv2
import numpy as np
import cv2.aruco as aruco
import os
import math
import time
from numpy import linalg
import serial

filename = 'Test.avi'
fps = 15.0
my_res = '720p'

imgx = 1280
imgy = 720

signal = "00"
buffer = 50
bufferAngle = 10


class Store:
    def __init__(self, x, y, vx, vy, name, misc, turn, num):
        self.x = x
        self.y = y
        self.name = name
        self.misc = misc
        self.vx = vx
        self.vy = vy
        self.v = (vx, vy)
        self.c = (x, y)
        self.turn = turn
        self.num = num

    def StoreNew(self, x, y, vx, vy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.v = (vx, vy)
        self.c = (x, y)


B1 = Store(0, 0, 0, -1, "B1", ("BOT1", "BOT2"), ("13", "14"), 1)
B2 = Store(0, 0, 0, -1, "B2", ("BOT2", "BOT3"), ("23", "24"), 2)
B3 = Store(0, 0, 0, -1, "B3", ("BOT3", "BOT4"), ("34", "33"), 3)
B4 = Store(0, 0, 0, -1, "B4", ("BOT4", "BOTend"), ("44", "43"), 4)

S1 = Store(imgx, 0, 0, -1, "S1", (), (), 1)
S2 = Store(imgx, 0, 0, -1, "S2", (), (), 2)
S3 = Store(imgx, 0, 0, -1, "S3", (), (), 3)
S4 = Store(imgx, 0, 0, -1, "S4", (), (), 4)

D1 = Store(imgx, imgy, -1, 0, "D1", (), (), 1)
D2 = Store(imgx, imgy, -1, 0, "D2", (), (), 2)
D3 = Store(imgx, imgy, -1, 0, "D3", (), (), 3)
D4 = Store(imgx, imgy, -1, 0, "D4", (), (), 4)

T1 = Store(0, imgy, 0, -1, "T1", (), (), 1)
T2 = Store(0, imgy, 0, -1, "T2", (), (), 2)
T3 = Store(0, imgy, 0, -1, "T3", (), (), 3)
T4 = Store(0, imgy, 0, -1, "T4", (), (), 4)


def unit_vector(vector):
    vector = np.array(vector)
    return vector / np.linalg.norm(vector)


def angle_between(v1, v2):
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))


def change_res(cap, width, height):
    cap.set(3, width)
    cap.set(4, height)


STD_Dim = {
    "480p": (640, 480),
    "720p": (1280, 720),
    "1080p": (1920, 1080),
    "4k": (3840, 2160),
}


def get_dims(cap, res='720p'):
    width, height = STD_Dim['480p']
    if res in STD_Dim:
        width, height = STD_Dim[res]
    change_res(cap, width, height)
    return width, height


def ids_rids(arg1):
    switch = {
        "[0]": "FKMP0001",
        "[1]": "FKMP0002",
        "[2]": "FKMP0003",
        "[3]": "FKMP0004",
        "[4]": "S1",
        "[5]": "S2",
        "[6]": "S3",
        "[7]": "S4",
        "[8]": "D1",
        "[9]": "D2",
        "[10]": "D3",
        "[11]": "D4",
        "[12]": "T1",
        "[13]": "T2",
        "[14]": "T3",
        "[15]": "T4",
    }

    return switch.get(arg1)


def countdown():
    elapsed_time = time.time() - start_time
    global elapsed_time_min
    global elapsed_time_sec
    global elapsed_time_millisec
    elapsed_time_min = elapsed_time // 60
    elapsed_time_sec = elapsed_time % 60
    elapsed_time_millisec = ((elapsed_time_sec * 1000) % 1000) // 1

    return f"{int(elapsed_time_min):02d}:{int(elapsed_time_sec):02d}:{int(elapsed_time_millisec):03d}"


VIDEO_TYPE = {
    'avi': cv2.VideoWriter_fourcc(*'XVID')
}


def get_video_type(filename):
    filename, ext = os.path.splitext(filename)
    if ext in VIDEO_TYPE:
        return VIDEO_TYPE[ext]
    return VIDEO_TYPE['avi']


def runBOTstart(p, q):
    if cv2.waitKey(10) & 0xFF == ord('l'):
        global start_time
        start_time = time.time()
        p = 0
        q = "BOT1"

    return p, q


def runBOTend(q):
    if cv2.waitKey(10) & 0xFF == ord('b'):
        q = "BOTend"

    return q


# Arduino Serial Communication
arduino = serial.Serial(port='COM3', baudrate=9600, timeout=.1)


def sendSignal(signal):
    print(f"Signal : {signal}")
    print("___________________________________")
    arduino.write(bytes(signal, 'utf-8'))


def runLogicBOT(B, S, T, D, img, operationNo):
    # BOT moving forward towards T
    if operationNo == 0:

        cv2.line(img, (B.x, B.y), (T.x, T.y), (0, 255, 255), 2)
        # cv2.line(img, (T.x-buffer, T.y-buffer), (T.x+buffer, T.y-buffer), (255, 255, 0), 2)
        # cv2.line(img, (T.x+buffer, T.y-buffer), (T.x+buffer, T.y+buffer), (255, 255, 0), 2)
        # cv2.line(img, (T.x+buffer, T.y+buffer), (T.x-buffer, T.y+buffer), (255, 255, 0), 2)
        # cv2.line(img, (T.x-buffer, T.y+buffer), (T.x-buffer, T.y-buffer), (255, 255, 0), 2)

        cv2.line(img, (0, T.y - buffer), (imgx, T.y - buffer), (255, 255, 0), 2)
        cv2.line(img, (T.x + buffer, 0), (T.x + buffer, imgy), (255, 255, 0), 2)
        cv2.line(img, (imgx, T.y + buffer), (0, T.y + buffer), (255, 255, 0), 2)
        cv2.line(img, (T.x - buffer, imgy), (T.x - buffer, 0), (255, 255, 0), 2)

        if B.x < T.x - buffer and B.y < T.y - buffer:
            signal = f"{B.num}7"  # Forward-Left
            sendSignal(signal)
            return 0, B.misc[0]
        if B.x > T.x + buffer and B.y < T.y - buffer:
            signal = f"{B.num}6"  # Forward-Right
            sendSignal(signal)
            return 0, B.misc[0]
        if B.x < T.x - buffer and B.y > T.y + buffer:
            signal = f"{B.num}9"  # Backward-Left
            sendSignal(signal)
            return 0, B.misc[0]
        if B.x > T.x + buffer and B.y > T.y + buffer:
            signal = f"{B.num}8"  # Backward-Right
            sendSignal(signal)
            return 0, B.misc[0]
        if T.x - buffer <= B.x <= T.x + buffer and B.y < T.y - buffer:
            signal = f"{B.num}1"  # Forward
            sendSignal(signal)
            return 0, B.misc[0]
        if T.x - buffer <= B.x <= T.x + buffer and B.y > T.y + buffer:
            signal = f"{B.num}2"  # Backward
            sendSignal(signal)
            return 0, B.misc[0]
        if B.x < T.x - buffer and T.y - buffer <= B.y <= T.y + buffer:
            signal = f"{B.num}9"  # Backward-Left
            sendSignal(signal)
            return 0, B.misc[0]
        if B.x > T.x + buffer and T.y - buffer <= B.y <= T.y + buffer:
            signal = f"{B.num}8"  # Backward-Right
            sendSignal(signal)
            return 0, B.misc[0]
        if T.x - buffer <= B.x <= T.x + buffer and T.y - buffer <= B.y <= T.y + buffer:
            signal = f"{B.num}0"  # Idle
            sendSignal(signal)
            return 1, B.misc[0]

    # BOT1 moving turning at T1 towards D1
    if operationNo == 1:
        B1Vu = unit_vector(B.v)  # Making into unit vector
        D1Vu = unit_vector(D.v)  # Making into unit vector

        # print(B.v)

        angle = angle_between(B1Vu, D1Vu)
        angleDeg = angle * 57.29577951326092812 // 1
        # print(angleDeg)

        Ux = math.cos(math.radians(bufferAngle)) * 100 // 1
        Uy = math.sin(math.radians(bufferAngle)) * 100 // 1
        # print(Ux, Uy)

        cv2.line(img, (B.x, B.y), (D.x, D.y), (0, 255, 255), 2)
        if B.name == "B1" or "B2":
            cv2.line(img, (B.x, B.y), (B.x - int(Ux), B.y - int(Uy)), (255, 255, 0), 2)
            cv2.line(img, (B.x, B.y), (B.x - int(Ux), B.y + int(Uy)), (255, 255, 0), 2)
        if B.name == "B3" or "B4":
            cv2.line(img, (B.x, B.y), (B.x + int(Ux), B.y - int(Uy)), (255, 255, 0), 2)
            cv2.line(img, (B.x, B.y), (B.x + int(Ux), B.y + int(Uy)), (255, 255, 0), 2)

        if angleDeg > bufferAngle:
            signal = B.turn[0]  # Turn Right
            sendSignal(signal)
            return 1, B.misc[0]
        elif angleDeg <= bufferAngle:
            signal = f"{B.num}0"  # Idle
            sendSignal(signal)
            return 2, B.misc[0]

    # BOT1 moving forward towards D1
    if operationNo == 2:

        cv2.line(img, (B.x, B.y), (D.x, D.y), (0, 255, 255), 2)
        # cv2.line(img, (D.x - buffer, D.y - buffer), (D.x + buffer, D.y - buffer), (255, 255, 0), 2)
        # cv2.line(img, (D.x + buffer, D.y - buffer), (D.x + buffer, D.y + buffer), (255, 255, 0), 2)
        # cv2.line(img, (D.x + buffer, D.y + buffer), (D.x - buffer, D.y + buffer), (255, 255, 0), 2)
        # cv2.line(img, (D.x - buffer, D.y + buffer), (D.x - buffer, D.y - buffer), (255, 255, 0), 2)

        cv2.line(img, (0, D.y - buffer), (imgx, D.y - buffer), (255, 255, 0), 2)
        cv2.line(img, (D.x + buffer, 0), (D.x + buffer, imgy), (255, 255, 0), 2)
        cv2.line(img, (imgx, D.y + buffer), (0, D.y + buffer), (255, 255, 0), 2)
        cv2.line(img, (D.x - buffer, imgy), (D.x - buffer, 0), (255, 255, 0), 2)

        if B.name == "B1" or "B2":
            if B.x < D.x - buffer and B.y < D.y - buffer:
                signal = f"{B.num}9"  # Backward-Left
                sendSignal(signal)
                return 2, B.misc[0]
            elif B.x > D.x + buffer and B.y < D.y - buffer:
                signal = f"{B.num}7"  # Forward-Left
                sendSignal(signal)
                return 2, B.misc[0]
            elif B.x < D.x - buffer and B.y > D.y + buffer:
                signal = f"{B.num}8"  # Backward-Right
                sendSignal(signal)
                return 2, B.misc[0]
            elif B.x > D.x + buffer and B.y > D.y + buffer:
                signal = f"{B.num}6"  # Forward-Right
                sendSignal(signal)
                return 2, B.misc[0]
            elif D.x - buffer <= B.x <= D.x + buffer and B.y < D.y - buffer:
                signal = f"{B.num}9"  # Backward-Left
                sendSignal(signal)
                return 2, B.misc[0]
            elif D.x - buffer <= B.x <= D.x + buffer and B.y > D.y + buffer:
                signal = f"{B.num}8"  # Backward-Right
                sendSignal(signal)
                return 2, B.misc[0]
            elif B.x < D.x - buffer and D.y - buffer <= B.y <= D.y + buffer:
                signal = f"{B.num}2"  # Backward
                sendSignal(signal)
                return 2, B.misc[0]
            elif B.x > D.x + buffer and D.y - buffer <= B.y <= D.y + buffer:
                signal = f"{B.num}1"  # Forward
                sendSignal(signal)
                return 2, B.misc[0]
            elif D.x - buffer <= B.x <= D.x + buffer and D.y - buffer <= B.y <= D.y + buffer:
                signal = f"{B.num}0"  # Idle
                sendSignal(signal)
                return 3, B.misc[0]

        if B.name == "B3" or "B4":
            if B.x < D.x - buffer and B.y < D.y - buffer:
                signal = f"{B.num}6"  # Forward-Right
                sendSignal(signal)
                return 2, B.misc[0]
            elif B.x > D.x + buffer and B.y < D.y - buffer:
                signal = f"{B.num}8"  # Backward-Right
                sendSignal(signal)
                return 2, B.misc[0]
            elif B.x < D.x - buffer and B.y > D.y + buffer:
                signal = f"{B.num}7"  # Forward-Left
                sendSignal(signal)
                return 2, B.misc[0]
            elif B.x > D.x + buffer and B.y > D.y + buffer:
                signal = f"{B.num}9"  # Backward-Left
                sendSignal(signal)
                return 2, B.misc[0]
            elif D.x - buffer <= B.x <= D.x + buffer and B.y < D.y - buffer:
                signal = f"{B.num}8"  # Backward-Right
                sendSignal(signal)
                return 2, B.misc[0]
            elif D.x - buffer <= B.x <= D.x + buffer and B.y > D.y + buffer:
                signal = f"{B.num}9"  # Backward-Left
                sendSignal(signal)
                return 2, B.misc[0]
            elif B.x < D.x - buffer and D.y - buffer <= B.y <= D.y + buffer:
                signal = f"{B.num}1"  # Forward
                sendSignal(signal)
                return 2, B.misc[0]
            elif B.x > D.x + buffer and D.y - buffer <= B.y <= D.y + buffer:
                signal = f"{B.num}2"  # Backward
                sendSignal(signal)
                return 2, B.misc[0]
            elif D.x - buffer <= B.x <= D.x + buffer and D.y - buffer <= B.y <= D.y + buffer:
                signal = f"{B.num}0"  # Idle
                sendSignal(signal)
                return 3, B.misc[0]

    # BOT1 dropping package
    if operationNo == 3:
        signal = f"{B.num}5"
        sendSignal(signal)
        return 4, B.misc[0]

    # BOT1 moving backwards towards T1
    if operationNo == 4:

        cv2.line(img, (B.x, B.y), (T.x, T.y), (0, 255, 255), 2)
        # cv2.line(img, (T.x - buffer, T.y - buffer), (T.x + buffer, T.y - buffer), (255, 255, 0), 2)
        # cv2.line(img, (T.x + buffer, T.y - buffer), (T.x + buffer, T.y + buffer), (255, 255, 0), 2)
        # cv2.line(img, (T.x + buffer, T.y + buffer), (T.x - buffer, T.y + buffer), (255, 255, 0), 2)
        # cv2.line(img, (T.x - buffer, T.y + buffer), (T.x - buffer, T.y - buffer), (255, 255, 0), 2)

        cv2.line(img, (0, T.y - buffer), (imgx, T.y - buffer), (255, 255, 0), 2)
        cv2.line(img, (T.x + buffer, 0), (T.x + buffer, imgy), (255, 255, 0), 2)
        cv2.line(img, (imgx, T.y + buffer), (0, T.y + buffer), (255, 255, 0), 2)
        cv2.line(img, (T.x - buffer, imgy), (T.x - buffer, 0), (255, 255, 0), 2)

        if B.name == "B1" or "B2":
            if B.x < T.x - buffer and B.y < T.y - buffer:
                signal = f"{B.num}9"  # Backward-Left
                sendSignal(signal)
                return 4, B.misc[0]
            elif B.x > T.x + buffer and B.y < T.y - buffer:
                signal = f"{B.num}7"  # Forward-Left
                sendSignal(signal)
                return 4, B.misc[0]
            elif B.x < T.x - buffer and B.y > T.y + buffer:
                signal = f"{B.num}8"  # Backward-Right
                sendSignal(signal)
                return 4, B.misc[0]
            elif B.x > T.x + buffer and B.y > T.y + buffer:
                signal = f"{B.num}6"  # Forward-Right
                sendSignal(signal)
                return 4, B.misc[0]
            elif T.x - buffer <= B.x <= T.x + buffer and B.y < T.y - buffer:
                signal = f"{B.num}7"  # Forward-Left
                sendSignal(signal)
                return 4, B.misc[0]
            elif T.x - buffer <= B.x <= T.x + buffer and B.y > T.y + buffer:
                signal = f"{B.num}6"  # Forward-Right
                sendSignal(signal)
                return 4, B.misc[0]
            elif B.x < T.x - buffer and T.y - buffer <= B.y <= T.y + buffer:
                signal = f"{B.num}2"  # Backward
                sendSignal(signal)
                return 4, B.misc[0]
            elif B.x > T.x + buffer and T.y - buffer <= B.y <= T.y + buffer:
                signal = f"{B.num}1"  # Forward
                sendSignal(signal)
                return 4, B.misc[0]
            elif T.x - buffer <= B.x <= T.x + buffer and T.y - buffer <= B.y <= T.y + buffer:
                signal = f"{B.num}0"  # Idle
                sendSignal(signal)
                return 5, B.misc[0]

        if B.name == "B3" or "B4":
            if B.x < T.x - buffer and B.y < T.y - buffer:
                signal = f"{B.num}6"  # Forward-Right
                sendSignal(signal)
                return 4, B.misc[0]
            elif B.x > T.x + buffer and B.y < T.y - buffer:
                signal = f"{B.num}8"  # Backward-Right
                sendSignal(signal)
                return 4, B.misc[0]
            elif B.x < T.x - buffer and B.y > T.y + buffer:
                signal = f"{B.num}7"  # Forward-Left
                sendSignal(signal)
                return 4, B.misc[0]
            elif B.x > T.x + buffer and B.y > T.y + buffer:
                signal = f"{B.num}9"  # Backward-Left
                sendSignal(signal)
                return 4, B.misc[0]
            elif T.x - buffer <= B.x <= T.x + buffer and B.y < T.y - buffer:
                signal = f"{B.num}6"  # Forward-Right
                sendSignal(signal)
                return 4, B.misc[0]
            elif T.x - buffer <= B.x <= T.x + buffer and B.y > T.y + buffer:
                signal = f"{B.num}7"  # Forward-Left
                sendSignal(signal)
                return 4, B.misc[0]
            elif B.x < T.x - buffer and T.y - buffer <= B.y <= T.y + buffer:
                signal = f"{B.num}1"  # Forward
                sendSignal(signal)
                return 4, B.misc[0]
            elif B.x > T.x + buffer and T.y - buffer <= B.y <= T.y + buffer:
                signal = f"{B.num}2"  # Backward
                sendSignal(signal)
                return 4, B.misc[0]
            elif T.x - buffer <= B.x <= T.x + buffer and T.y - buffer <= B.y <= T.y + buffer:
                signal = f"{B.num}0"  # Idle
                sendSignal(signal)
                return 5, B.misc[0]

    #  BOT1 moving turning at T1 towards S1
    if operationNo == 5:

        B1Vu = unit_vector(B.v)  # Making into unit vector
        S1Vu = unit_vector(S.v)  # Making into unit vector

        angle = angle_between(B1Vu, S1Vu)
        angleDeg = angle * 57.29577951326092812 // 1
        # print(angleDeg)

        Ux = math.cos(math.radians(bufferAngle)) * 100 // 1
        Uy = math.sin(math.radians(bufferAngle)) * 100 // 1
        # print(Ux, Uy)

        cv2.line(img, (B.x, B.y), (S.x, S.y), (0, 255, 255), 2)
        if B.name == "B1" or "B2":
            cv2.line(img, (B.x, B.y), (B.x + int(Uy), B.y + int(Ux)), (255, 255, 0), 2)
            cv2.line(img, (B.x, B.y), (B.x - int(Uy), B.y + int(Ux)), (255, 255, 0), 2)
        if B.name == "B3" or "B4":
            cv2.line(img, (B.x, B.y), (B.x + int(Uy), B.y + int(Ux)), (255, 255, 0), 2)
            cv2.line(img, (B.x, B.y), (B.x - int(Uy), B.y + int(Ux)), (255, 255, 0), 2)

        if angleDeg > bufferAngle:
            signal = B.turn[1]  # Turn Left
            sendSignal(signal)
            return 5, B.misc[0]
        elif angleDeg <= bufferAngle:
            signal = f"{B.num}0"  # Idle
            sendSignal(signal)
            return 6, B.misc[0]

    # BOT1 moving backwards towards S1
    if operationNo == 6:

        cv2.line(img, (B.x, B.y), (S.x, S.y), (0, 255, 255), 2)
        # cv2.line(img, (S.x - buffer, S.y - buffer), (S.x + buffer, S.y - buffer), (255, 255, 0), 2)
        # cv2.line(img, (S.x + buffer, S.y - buffer), (S.x + buffer, S.y + buffer), (255, 255, 0), 2)
        # cv2.line(img, (S.x + buffer, S.y + buffer), (S.x - buffer, S.y + buffer), (255, 255, 0), 2)
        # cv2.line(img, (S.x - buffer, S.y + buffer), (S.x - buffer, S.y - buffer), (255, 255, 0), 2)

        cv2.line(img, (0, S.y - buffer), (imgx, S.y - buffer), (255, 255, 0), 2)
        cv2.line(img, (S.x + buffer, 0), (S.x + buffer, imgy), (255, 255, 0), 2)
        cv2.line(img, (imgx, S.y + buffer), (0, S.y + buffer), (255, 255, 0), 2)
        cv2.line(img, (S.x - buffer, imgy), (S.x - buffer, 0), (255, 255, 0), 2)

        if B.x < S.x - buffer and B.y < S.y - buffer:
            signal = f"{B.num}7"  # Forward-Left
            sendSignal(signal)
            return 6, B.misc[0]
        elif B.x > S.x + buffer and B.y < S.y - buffer:
            signal = f"{B.num}6"  # Forward-Right
            sendSignal(signal)
            return 6, B.misc[0]
        elif B.x < S.x - buffer and B.y > S.y + buffer:
            signal = f"{B.num}9"  # Backward-Left
            sendSignal(signal)
            return 6, B.misc[0]
        elif B.x > S.x + buffer and B.y > S.y + buffer:
            signal = f"{B.num}8"  # Backward-Right
            sendSignal(signal)
            return 6, B.misc[0]
        elif S.x - buffer <= B.x <= S.x + buffer and B.y < S.y - buffer:
            signal = f"{B.num}1"  # Forward
            sendSignal(signal)
            return 6, B.misc[0]
        elif S.x - buffer <= B.x <= S.x + buffer and B.y > S.y + buffer:
            signal = f"{B.num}2"  # Backward
            sendSignal(signal)
            return 6, B.misc[0]
        elif B.x < S.x - buffer and S.y - buffer <= B.y <= S.y + buffer:
            signal = f"{B.num}7"  # Forward-Left
            sendSignal(signal)
            return 6, B.misc[0]
        elif B.x > S.x + buffer and S.y - buffer <= B.y <= S.y + buffer:
            signal = f"{B.num}6"  # Forward-Right
            sendSignal(signal)
            return 6, B.misc[0]
        elif S.x - buffer <= B.x <= S.x + buffer and S.y - buffer <= B.y <= S.y + buffer:
            signal = f"{B.num}0"  # Idle
            sendSignal(signal)
            return 0, B.misc[1]


def findArucoMarkers(img, MarkerSize=5, totalMarkers=250, draw=True):
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    key = getattr(aruco, f'DICT_{MarkerSize}X{MarkerSize}_{totalMarkers}')
    arucoDict = aruco.Dictionary_get(key)
    arucoParam = aruco.DetectorParameters_create()
    corners, ids, rejected = aruco.detectMarkers(imgGray, arucoDict, parameters=arucoParam)
    # print(ids)

    if BOT == "BOTstart":
        cv2.rectangle(img, (imgx - 190, 20), (imgx - 10, 60), color=(255, 255, 255), thickness=2)
        image = cv2.putText(img, "00:00:000", (imgx - 180, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2,
                            cv2.LINE_AA)
    elif BOT == "BOTend":
        cv2.rectangle(img, (imgx - 190, 20), (imgx - 10, 60), color=(255, 255, 255), thickness=2)
        image = cv2.putText(img,
                            f"{int(elapsed_time_min):02d}:{int(elapsed_time_sec):02d}:{int(elapsed_time_millisec):03d}",
                            (imgx - 180, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
    else:
        cv2.rectangle(img, (imgx - 190, 20), (imgx - 10, 60), color=(255, 255, 255), thickness=2)
        image = cv2.putText(img, countdown(), (imgx - 180, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2,
                            cv2.LINE_AA)

    if draw:
        aruco.drawDetectedMarkers(img, corners)

    for (i, b) in enumerate(corners):

        c1 = (b[0][0][0], b[0][0][1])
        c2 = (b[0][1][0], b[0][1][1])
        c3 = (b[0][2][0], b[0][2][1])
        c4 = (b[0][3][0], b[0][3][1])
        v = (int(c1[0]) - int(c4[0]), int(c1[1]) - int(c4[1]))
        vx = int(c1[0]) - int(c4[0])
        vy = int(c1[1]) - int(c4[1])
        x = int((c1[0] + c2[0] + c3[0] + c4[0]) / 4)
        y = int((c1[1] + c2[1] + c3[1] + c4[1]) / 4)

        # print(ids[i], v)
        # print(c1)
        # print(c2)
        # print(c3)
        # print(c4)
        # print(v)

        arg1 = str(ids[i])
        arg2 = ids_rids(arg1)

        if arg2 == "FKMP0001":
            B1.StoreNew(x, y, vx, vy)
        elif arg2 == "FKMP0002":
            B2.StoreNew(x, y, vx, vy)
        elif arg2 == "FKMP0003":
            B3.StoreNew(x, y, vx, vy)
        elif arg2 == "FKMP0004":
            B4.StoreNew(x, y, vx, vy)
        elif arg2 == "S1":
            S1.StoreNew(x, y, vx, vy)
        elif arg2 == "S2":
            S2.StoreNew(x, y, vx, vy)
        elif arg2 == "S3":
            S3.StoreNew(x, y, vx, vy)
        elif arg2 == "S4":
            S4.StoreNew(x, y, vx, vy)
        elif arg2 == "D1":
            D1.StoreNew(x, y, vx, vy)
        elif arg2 == "D2":
            D2.StoreNew(x, y, vx, vy)
        elif arg2 == "D3":
            D3.StoreNew(x, y, vx, vy)
        elif arg2 == "D4":
            D4.StoreNew(x, y, vx, vy)
        elif arg2 == "T1":
            T1.StoreNew(x, y, vx, vy)
        elif arg2 == "T2":
            T2.StoreNew(x, y, vx, vy)
        elif arg2 == "T3":
            T3.StoreNew(x, y, vx, vy)
        elif arg2 == "T4":
            T4.StoreNew(x, y, vx, vy)

        cv2.line(img, (int(c1[0]), int(c1[1])), (int(c2[0]), int(c2[1])), (0, 255, 0), 2)
        cv2.line(img, (int(c2[0]), int(c2[1])), (int(c3[0]), int(c3[1])), (0, 255, 0), 2)
        cv2.line(img, (int(c3[0]), int(c3[1])), (int(c4[0]), int(c4[1])), (0, 255, 0), 2)
        cv2.line(img, (int(c4[0]), int(c4[1])), (int(c1[0]), int(c1[1])), (0, 255, 0), 2)
        cv2.line(img, (x, y), (x + (int(v[0]) // 2), y + (int(v[1]) // 2)), (255, 0, 0), 2)
        img = cv2.putText(img, arg2, (x - 10, y + 20), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA)


def main():
    cap = cv2.VideoCapture(3)
    dims = get_dims(cap, res=my_res)
    video_type_cv2 = get_video_type(filename)

    p = 0
    operationNo = 0
    global BOT
    BOT = "BOTstart"
    q = "BOTstart"

    rec = cv2.VideoWriter(filename,video_type_cv2, fps, dims)

    while True:
        success, img = cap.read()

        global imgx
        global imgy
        imgx = img.shape[1]
        imgy = img.shape[0]

        findArucoMarkers(img)

        q = runBOTend(q)

        operationNo = p
        BOT = q

        if BOT == "BOTstart":
            p, q = runBOTstart(p, q)
        if BOT == "BOT1":
            p, q = runLogicBOT(B1, S1, T1, D1, img, operationNo)
        if BOT == "BOT2":
            p, q = runLogicBOT(B2, S2, T2, D2, img, operationNo)
        if BOT == "BOT3":
            p, q = runLogicBOT(B3, S3, T3, D3, img, operationNo)
        if BOT == "BOT4":
            p, q = runLogicBOT(B4, S4, T4, D4, img, operationNo)
        if BOT == "BOTend":
            pass

        # print(p, operationNo, BOT)

        rec.write(img)
        cv2.imshow("Image", img)
        cv2.waitKey(1)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            rec.release()
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
