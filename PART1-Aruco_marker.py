import cv2
import numpy as np
import cv2.aruco as aruco
import os
import math
from numpy import linalg

filename = 'Test.avi'
fps = 24.0
my_res = '720p'

imgx = 1280
imgy = 720

B1CX = 0
B1CY = 0
B1CVx = 0
B1CVy = -1
B2CX = 0
B2CY = 0
B2CVx = 0
B2CVy = -1
B3CX = 0
B3CY = 0
B3CVx = 0
B3CVy = -1
B4CX = 0
B4CY = 0
B4CVx = 0
B4CVy = -1
S1CX = imgx
S1CY = 0
S1CVx = 0
S1CVy = -1
S2CX = imgx
S2CY = 0
S2CVx = 0
S2CVy = -1
S3CX = imgx
S3CY = 0
S3CVx = 0
S3CVy = -1
S4CX = imgx
S4CY = 0
S4CVx = 0
S4CVy = -1
D1CX = imgx
D1CY = imgy
D1CVx = -1
D1CVy = 0
D2CX = imgx
D2CY = imgy
D2CVx = -1
D2CVy = 0
D3CX = imgx
D3CY = imgy
D3CVx = -1
D3CVy = 0
D4CX = imgx
D4CY = imgy
D4CVx = -1
D4CVy = 0
T1CX = 0
T1CY = imgy
T1CVx = 0
T1CVy = -1
T2CX = 0
T2CY = imgy
T2CVx = 0
T2CVy = -1
T3CX = 0
T3CY = imgy
T3CVx = 0
T3CVy = -1
T4CX = 0
T4CY = imgy
T4CVx = 0
T4CVy = -1
B1V = (0, -1)
B2V = (0, -1)
B3V = (0, -1)
B4V = (0, -1)
S1V = (0, -1)
S2V = (0, -1)
S3V = (0, -1)
S4V = (0, -1)
D1V = (-1, 0)
D2V = (-1, 0)
D3V = (1, 0)
D4V = (1, 0)
T1V = (0, -1)
T2V = (0, -1)
T3V = (0, -1)
T4V = (0, -1)

signal = "00"
buffer = 10
bufferAngle = 15


def unit_vector(vector):
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


def storeB1(x, y, vx, vy):
    global B1CX
    global B1CY
    global B1CVx
    global B1CVy
    global B1V
    B1CX = x  # x-value of B1 center
    B1CY = y  # y-value of B1 center
    B1CVx = vx  # x-value of B1 vector
    B1CVy = vy  # y-value of B1 vector
    B1C = (x, y)  # B1 center tuple
    B1V = (vx, vy)  # B1 vector tuple
    # print(B1CVx, B1CVy)


def storeB2(x, y, vx, vy):
    global B2CX
    global B2CY
    global B2CVx
    global B2CVy
    global B2V
    B2CX = x
    B2CY = y
    B2CVx = vx
    B2CVy = vy
    B2C = (x, y)
    B2V = (vx, vy)


def storeB3(x, y, vx, vy):
    global B3CX
    global B3CY
    global B3CVx
    global B3CVy
    global B3V
    B3CX = x
    B3CY = y
    B3CVx = vx
    B3CVy = vy
    B3C = (x, y)
    B3V = (vx, vy)


def storeB4(x, y, vx, vy):
    global B4CX
    global B4CY
    global B4CVx
    global B4CVy
    global B4V
    B4CX = x
    B4CY = y
    B4CVx = vx
    B4CVy = vy
    B4C = (x, y)
    B4V = (vx, vy)


def storeS1(x, y, vx, vy):
    global S1CX
    global S1CY
    global S1CVx
    global S1CVy
    global S1V
    S1CX = x
    S1CY = y
    S1CVx = vx
    S1CVy = vy
    S1C = (x, y)
    S1V = (vx, vy)


def storeS2(x, y, vx, vy):
    global S2CX
    global S2CY
    global S2CVx
    global S2CVy
    global S2V
    S2CX = x
    S2CY = y
    S2CVx = vx
    S2CVy = vy
    S2C = (x, y)
    S2V = (vx, vy)


def storeS3(x, y, vx, vy):
    global S3CX
    global S3CY
    global S3CVx
    global S3CVy
    global S3V
    S3CX = x
    S3CY = y
    S3CVx = vx
    S3CVy = vy
    S3C = (x, y)
    S3V = (vx, vy)


def storeS4(x, y, vx, vy):
    global S4CX
    global S4CY
    global S4CVx
    global S4CVy
    global S4V
    S4CX = x
    S4CY = y
    S4CVx = vx
    S4CVy = vy
    S4C = (x, y)
    S4V = (vx, vy)


def storeD1(x, y, vx, vy):
    global D1CX
    global D1CY
    global D1CVx
    global D1CVy
    global D1V
    D1CX = x
    D1CY = y
    D1CVx = vx
    D1CVy = vy
    D1C = (x, y)
    D1V = (vx, vy)


def storeD2(x, y, vx, vy):
    global D2CX
    global D2CY
    global D2CVx
    global D2CVy
    D2CX = x
    D2CY = y
    D2CVx = vx
    D2CVy = vy
    D2C = (x, y)
    D2V = (vx, vy)


def storeD3(x, y, vx, vy):
    global D3CX
    global D3CY
    global D3CVx
    global D3CVy
    global D3V
    D3CX = x
    D3CY = y
    D3CVx = vx
    D3CVy = vy
    D3C = (x, y)
    D3V = (vx, vy)


def storeD4(x, y, vx, vy):
    global D4CX
    global D4CY
    global D4CVx
    global D4CVy
    global D4V
    D4CX = x
    D4CY = y
    D4CVx = vx
    D4CVy = vy
    D4C = (x, y)
    D4V = (vx, vy)


def storeT1(x, y, vx, vy):
    global T1CX
    global T1CY
    global T1CVx
    global T1CVy
    global T1V
    T1CX = x
    T1CY = y
    T1CVx = vx
    T1CVy = vy
    T1C = (x, y)
    T1V = (vx, vy)


def storeT2(x, y, vx, vy):
    global T2CX
    global T2CY
    global T2CVx
    global T2CVy
    global T2V
    T2CX = x
    T2CY = y
    T2CVx = vx
    T2CVy = vy
    T2C = (x, y)
    T2V = (vx, vy)


def storeT3(x, y, vx, vy):
    global T3CX
    global T3CY
    global T3CVx
    global T3CVy
    global T3V
    T3CX = x
    T3CY = y
    T3CVx = vx
    T3CVy = vy
    T3C = (x, y)
    T3V = (vx, vy)


def storeT4(x, y, vx, vy):
    global T4CX
    global T4CY
    global T4CVx
    global T4CVy
    global T4V
    T4CX = x
    T4CY = y
    T4CVx = vx
    T4CVy = vy
    T4C = (x, y)
    T4V = (vx, vy)


def sendSignal(signal):
    print(signal)


def runLogicBOT1(img, p, operationNo, q):
    # BOT1 moving forward towards T1
    if operationNo == 0:

        cv2.line(img, (B1CX, B1CY), (T1CX, T1CY), (0, 255, 255), 2)
        # cv2.line(img, (T1CX-buffer, T1CY-buffer), (T1CX+buffer, T1CY-buffer), (255, 255, 0), 2)
        # cv2.line(img, (T1CX+buffer, T1CY-buffer), (T1CX+buffer, T1CY+buffer), (255, 255, 0), 2)
        # cv2.line(img, (T1CX+buffer, T1CY+buffer), (T1CX-buffer, T1CY+buffer), (255, 255, 0), 2)
        # cv2.line(img, (T1CX-buffer, T1CY+buffer), (T1CX-buffer, T1CY-buffer), (255, 255, 0), 2)

        cv2.line(img, (0, T1CY - buffer), (imgx, T1CY - buffer), (255, 255, 0), 2)
        cv2.line(img, (T1CX + buffer, 0), (T1CX + buffer, imgy), (255, 255, 0), 2)
        cv2.line(img, (imgx, T1CY + buffer), (0, T1CY + buffer), (255, 255, 0), 2)
        cv2.line(img, (T1CX - buffer, imgy), (T1CX - buffer, 0), (255, 255, 0), 2)

        if B1CX < T1CX - buffer and B1CY < T1CY - buffer:
            signal = "1H"  # Forward-Left
            sendSignal(signal)
            p = 0
            q = "BOT1"
            return p, q
        if B1CX > T1CX + buffer and B1CY < T1CY - buffer:
            signal = "1G"  # Forward-Right
            sendSignal(signal)
            p = 0
            q = "BOT1"
            return p, q
        if B1CX < T1CX - buffer and B1CY > T1CY + buffer:
            signal = "1J"  # Backward-Left
            sendSignal(signal)
            p = 0
            q = "BOT1"
            return p, q
        if B1CX > T1CX + buffer and B1CY > T1CY + buffer:
            signal = "1I"  # Backward-Right
            sendSignal(signal)
            p = 0
            q = "BOT1"
            return p, q
        if T1CX - buffer <= B1CX <= T1CX + buffer and B1CY < T1CY - buffer:
            signal = "1B"  # Forward
            sendSignal(signal)
            p = 0
            q = "BOT1"
            return p, q
        if T1CX - buffer <= B1CX <= T1CX + buffer and B1CY > T1CY + buffer:
            signal = "1C"  # Backward
            sendSignal(signal)
            p = 0
            q = "BOT1"
            return p, q
        if B1CX < T1CX - buffer and T1CY - buffer <= B1CY <= T1CY + buffer:
            signal = "1J"  # Backward-Left
            sendSignal(signal)
            p = 0
            q = "BOT1"
            return p, q
        if B1CX > T1CX + buffer and T1CY - buffer <= B1CY <= T1CY + buffer:
            signal = "1I"  # Backward-Right
            sendSignal(signal)
            p = 0
            q = "BOT1"
            return p, q
        if T1CX - buffer <= B1CX <= T1CX + buffer and T1CY - buffer <= B1CY <= T1CY + buffer:
            signal = "1A"  # Idle
            sendSignal(signal)
            p = 1
            q = "BOT1"
            return p, q

    # BOT1 moving turning at T1 towards D1
    if operationNo == 1:
        B1Vu = unit_vector(B1V)  # Making into unit vector
        D1Vu = unit_vector(D1V)  # Making into unit vector

        angle = angle_between(B1Vu, D1Vu)
        angleDeg = angle * 57.29577951326092812 // 1
        # print(angleDeg)

        Ux = math.cos(math.radians(bufferAngle)) * 100 // 1
        Uy = math.sin(math.radians(bufferAngle)) * 100 // 1
        # print(Ux, Uy)

        cv2.line(img, (B1CX, B1CY), (D1CX, D1CY), (0, 255, 255), 2)
        cv2.line(img, (B1CX, B1CY), (B1CX - int(Ux), B1CY - int(Uy)), (255, 255, 0), 2)
        cv2.line(img, (B1CX, B1CY), (B1CX - int(Ux), B1CY + int(Uy)), (255, 255, 0), 2)

        if angleDeg > bufferAngle:
            signal = "1D"  # Turn Right
            sendSignal(signal)
            p = 1
            q = "BOT1"
            return p, q
        elif angleDeg <= bufferAngle:
            signal = "1A"  # Idle
            sendSignal(signal)
            p = 2
            q = "BOT1"
            return p, q

    # BOT1 moving forward towards D1
    if operationNo == 2:

        cv2.line(img, (B1CX, B1CY), (D1CX, D1CY), (0, 255, 255), 2)
        # cv2.line(img, (D1CX - buffer, D1CY - buffer), (D1CX + buffer, D1CY - buffer), (255, 255, 0), 2)
        # cv2.line(img, (D1CX + buffer, D1CY - buffer), (D1CX + buffer, D1CY + buffer), (255, 255, 0), 2)
        # cv2.line(img, (D1CX + buffer, D1CY + buffer), (D1CX - buffer, D1CY + buffer), (255, 255, 0), 2)
        # cv2.line(img, (D1CX - buffer, D1CY + buffer), (D1CX - buffer, D1CY - buffer), (255, 255, 0), 2)

        cv2.line(img, (0, D1CY - buffer), (imgx, D1CY - buffer), (255, 255, 0), 2)
        cv2.line(img, (D1CX + buffer, 0), (D1CX + buffer, imgy), (255, 255, 0), 2)
        cv2.line(img, (imgx, D1CY + buffer), (0, D1CY + buffer), (255, 255, 0), 2)
        cv2.line(img, (D1CX - buffer, imgy), (D1CX - buffer, 0), (255, 255, 0), 2)

        if B1CX < D1CX - buffer and B1CY < D1CY - buffer:
            signal = "1J"  # Backward-Left
            sendSignal(signal)
            p = 2
            q = "BOT1"
            return p, q
        elif B1CX > D1CX + buffer and B1CY < D1CY - buffer:
            signal = "1H"  # Forward-Left
            sendSignal(signal)
            p = 2
            q = "BOT1"
            return p, q
        elif B1CX < D1CX - buffer and B1CY > D1CY + buffer:
            signal = "1I"  # Backward-Right
            sendSignal(signal)
            p = 2
            q = "BOT1"
            return p, q
        elif B1CX > D1CX + buffer and B1CY > D1CY + buffer:
            signal = "1G"  # Forward-Right
            sendSignal(signal)
            p = 2
            q = "BOT1"
            return p, q
        elif D1CX - buffer <= B1CX <= D1CX + buffer and B1CY < D1CY - buffer:
            signal = "1J"  # Backward-Left
            sendSignal(signal)
            p = 2
            q = "BOT1"
            return p, q
        elif D1CX - buffer <= B1CX <= D1CX + buffer and B1CY > D1CY + buffer:
            signal = "1I"  # Backward-Right
            sendSignal(signal)
            p = 2
            q = "BOT1"
            return p, q
        elif B1CX < D1CX - buffer and D1CY - buffer <= B1CY <= D1CY + buffer:
            signal = "1C"  # Backward
            sendSignal(signal)
            p = 2
            q = "BOT1"
            return p, q
        elif B1CX > D1CX + buffer and D1CY - buffer <= B1CY <= D1CY + buffer:
            signal = "1B"  # Forward
            sendSignal(signal)
            p = 2
            q = "BOT1"
            return p, q
        elif D1CX - buffer <= B1CX <= D1CX + buffer and D1CY - buffer <= B1CY <= D1CY + buffer:
            signal = "1A"  # Idle
            sendSignal(signal)
            p = 3
            q = "BOT1"
            return p, q

    # BOT1 dropping package
    if operationNo == 3:
        signal = "1F"
        sendSignal(signal)
        p = 4
        q = "BOT1"
        return p, q

    # BOT1 moving backwards towards T1
    if operationNo == 4:

        cv2.line(img, (B1CX, B1CY), (T1CX, T1CY), (0, 255, 255), 2)
        # cv2.line(img, (T1CX - buffer, T1CY - buffer), (T1CX + buffer, T1CY - buffer), (255, 255, 0), 2)
        # cv2.line(img, (T1CX + buffer, T1CY - buffer), (T1CX + buffer, T1CY + buffer), (255, 255, 0), 2)
        # cv2.line(img, (T1CX + buffer, T1CY + buffer), (T1CX - buffer, T1CY + buffer), (255, 255, 0), 2)
        # cv2.line(img, (T1CX - buffer, T1CY + buffer), (T1CX - buffer, T1CY - buffer), (255, 255, 0), 2)

        cv2.line(img, (0, T1CY - buffer), (imgx, T1CY - buffer), (255, 255, 0), 2)
        cv2.line(img, (T1CX + buffer, 0), (T1CX + buffer, imgy), (255, 255, 0), 2)
        cv2.line(img, (imgx, T1CY + buffer), (0, T1CY + buffer), (255, 255, 0), 2)
        cv2.line(img, (T1CX - buffer, imgy), (T1CX - buffer, 0), (255, 255, 0), 2)

        if B1CX < T1CX - buffer and B1CY < T1CY - buffer:
            signal = "1J"  # Backward-Left
            sendSignal(signal)
            p = 4
            q = "BOT1"
            return p, q
        elif B1CX > T1CX + buffer and B1CY < T1CY - buffer:
            signal = "1H"  # Forward-Left
            sendSignal(signal)
            p = 4
            q = "BOT1"
            return p, q
        elif B1CX < T1CX - buffer and B1CY > T1CY + buffer:
            signal = "1I"  # Backward-Right
            sendSignal(signal)
            p = 4
            q = "BOT1"
            return p, q
        elif B1CX > T1CX + buffer and B1CY > T1CY + buffer:
            signal = "1G"  # Forward-Right
            sendSignal(signal)
            p = 4
            q = "BOT1"
            return p, q
        elif T1CX - buffer <= B1CX <= T1CX + buffer and B1CY < T1CY - buffer:
            signal = "1H"  # Forward-Left
            sendSignal(signal)
            p = 4
            q = "BOT1"
            return p, q
        elif T1CX - buffer <= B1CX <= T1CX + buffer and B1CY > T1CY + buffer:
            signal = "1G"  # Forward-Right
            sendSignal(signal)
            p = 4
            q = "BOT1"
            return p, q
        elif B1CX < T1CX - buffer and T1CY - buffer <= B1CY <= T1CY + buffer:
            signal = "1C"  # Backward
            sendSignal(signal)
            p = 4
            q = "BOT1"
            return p, q
        elif B1CX > T1CX + buffer and T1CY - buffer <= B1CY <= T1CY + buffer:
            signal = "1B"  # Forward
            sendSignal(signal)
            p = 4
            q = "BOT1"
            return p, q
        elif T1CX - buffer <= B1CX <= T1CX + buffer and T1CY - buffer <= B1CY <= T1CY + buffer:
            signal = "1A"  # Idle
            sendSignal(signal)
            p = 5
            q = "BOT1"
            return p, q

    #  BOT1 moving turning at T1 towards S1
    if operationNo == 5:

        B1Vu = unit_vector(B1V)  # Making into unit vector
        S1Vu = unit_vector(S1V)  # Making into unit vector

        angle = angle_between(B1Vu, S1Vu)
        angleDeg = angle * 57.29577951326092812 // 1
        print(angleDeg)

        Ux = math.cos(math.radians(bufferAngle)) * 100 // 1
        Uy = math.sin(math.radians(bufferAngle)) * 100 // 1
        # print(Ux, Uy)

        cv2.line(img, (B1CX, B1CY), (S1CX, S1CY), (0, 255, 255), 2)
        cv2.line(img, (B1CX, B1CY), (B1CX + int(Uy), B1CY + int(Ux)), (255, 255, 0), 2)
        cv2.line(img, (B1CX, B1CY), (B1CX - int(Uy), B1CY + int(Ux)), (255, 255, 0), 2)

        if angleDeg > bufferAngle:
            signal = "1E"  # Turn Left
            sendSignal(signal)
            p = 5
            q = "BOT1"
            return p, q
        elif angleDeg <= bufferAngle:
            signal = "1A"  # Idle
            sendSignal(signal)
            p = 6
            q = "BOT1"
            return p, q

    # BOT1 moving backwards towards S1
    if operationNo == 6:

        cv2.line(img, (B1CX, B1CY), (S1CX, S1CY), (0, 255, 255), 2)
        # cv2.line(img, (S1CX - buffer, S1CY - buffer), (S1CX + buffer, S1CY - buffer), (255, 255, 0), 2)
        # cv2.line(img, (S1CX + buffer, S1CY - buffer), (S1CX + buffer, S1CY + buffer), (255, 255, 0), 2)
        # cv2.line(img, (S1CX + buffer, S1CY + buffer), (S1CX - buffer, S1CY + buffer), (255, 255, 0), 2)
        # cv2.line(img, (S1CX - buffer, S1CY + buffer), (S1CX - buffer, S1CY - buffer), (255, 255, 0), 2)

        cv2.line(img, (0, S1CY - buffer), (imgx, S1CY - buffer), (255, 255, 0), 2)
        cv2.line(img, (S1CX + buffer, 0), (S1CX + buffer, imgy), (255, 255, 0), 2)
        cv2.line(img, (imgx, S1CY + buffer), (0, S1CY + buffer), (255, 255, 0), 2)
        cv2.line(img, (S1CX - buffer, imgy), (S1CX - buffer, 0), (255, 255, 0), 2)

        if B1CX < S1CX - buffer and B1CY < S1CY - buffer:
            signal = "1H"  # Forward-Left
            sendSignal(signal)
            p = 6
            q = "BOT1"
            return p, q
        elif B1CX > S1CX + buffer and B1CY < S1CY - buffer:
            signal = "1G"  # Forward-Right
            sendSignal(signal)
            p = 6
            q = "BOT1"
            return p, q
        elif B1CX < S1CX - buffer and B1CY > S1CY + buffer:
            signal = "1J"  # Backward-Left
            sendSignal(signal)
            p = 6
            q = "BOT1"
            return p, q
        elif B1CX > S1CX + buffer and B1CY > S1CY + buffer:
            signal = "1I"  # Backward-Right
            sendSignal(signal)
            p = 6
            q = "BOT1"
            return p, q
        elif S1CX - buffer <= B1CX <= S1CX + buffer and B1CY < S1CY - buffer:
            signal = "1B"  # Forward
            sendSignal(signal)
            p = 6
            q = "BOT1"
            return p, q
        elif S1CX - buffer <= B1CX <= S1CX + buffer and B1CY > S1CY + buffer:
            signal = "1C"  # Backward
            sendSignal(signal)
            p = 6
            q = "BOT1"
            return p, q
        elif B1CX < S1CX - buffer and S1CY - buffer <= B1CY <= S1CY + buffer:
            signal = "1G"  # Forward-Left
            sendSignal(signal)
            p = 6
            return p, q
        elif B1CX > S1CX + buffer and S1CY - buffer <= B1CY <= S1CY + buffer:
            signal = "1G"  # Forward-Right
            sendSignal(signal)
            p = 6
            q = "BOT1"
            return p, q
        elif S1CX - buffer <= B1CX <= S1CX + buffer and S1CY - buffer <= B1CY <= S1CY + buffer:
            signal = "1A"  # Idle
            sendSignal(signal)
            p = 0
            q = "BOT2"
            return p, q


def runLogicBOT2(img, p, operationNo, q):
    # BOT2 moving forward towards T2
    if operationNo == 0:

        cv2.line(img, (B2CX, B2CY), (T2CX, T2CY), (0, 255, 255), 2)
        # cv2.line(img, (T2CX-buffer, T2CY-buffer), (T2CX+buffer, T2CY-buffer), (255, 255, 0), 2)
        # cv2.line(img, (T2CX+buffer, T2CY-buffer), (T2CX+buffer, T2CY+buffer), (255, 255, 0), 2)
        # cv2.line(img, (T2CX+buffer, T2CY+buffer), (T2CX-buffer, T2CY+buffer), (255, 255, 0), 2)
        # cv2.line(img, (T2CX-buffer, T2CY+buffer), (T2CX-buffer, T2CY-buffer), (255, 255, 0), 2)

        cv2.line(img, (0, T2CY - buffer), (imgx, T2CY - buffer), (255, 255, 0), 2)
        cv2.line(img, (T2CX + buffer, 0), (T2CX + buffer, imgy), (255, 255, 0), 2)
        cv2.line(img, (imgx, T2CY + buffer), (0, T2CY + buffer), (255, 255, 0), 2)
        cv2.line(img, (T2CX - buffer, imgy), (T2CX - buffer, 0), (255, 255, 0), 2)

        if B2CX < T2CX - buffer and B2CY < T2CY - buffer:
            signal = "2H"  # Forward-Left
            sendSignal(signal)
            p = 0
            q = "BOT2"
            return p, q
        if B2CX > T2CX + buffer and B2CY < T2CY - buffer:
            signal = "2G"  # Forward-Right
            sendSignal(signal)
            p = 0
            q = "BOT2"
            return p, q
        if B2CX < T2CX - buffer and B2CY > T2CY + buffer:
            signal = "2J"  # Backward-Left
            sendSignal(signal)
            p = 0
            q = "BOT2"
            return p, q
        if B2CX > T2CX + buffer and B2CY > T2CY + buffer:
            signal = "2I"  # Backward-Right
            sendSignal(signal)
            p = 0
            q = "BOT2"
            return p, q
        if T2CX - buffer <= B2CX <= T2CX + buffer and B2CY < T2CY - buffer:
            signal = "2B"  # Forward
            sendSignal(signal)
            p = 0
            q = "BOT2"
            return p, q
        if T2CX - buffer <= B2CX <= T2CX + buffer and B2CY > T2CY + buffer:
            signal = "2C"  # Backward
            sendSignal(signal)
            p = 0
            q = "BOT2"
            return p, q
        if B2CX < T2CX - buffer and T2CY - buffer <= B2CY <= T2CY + buffer:
            signal = "2J"  # Backward-Left
            sendSignal(signal)
            p = 0
            q = "BOT2"
            return p, q
        if B2CX > T2CX + buffer and T2CY - buffer <= B2CY <= T2CY + buffer:
            signal = "2I"  # Backward-Right
            sendSignal(signal)
            p = 0
            q = "BOT2"
            return p, q
        if T2CX - buffer <= B2CX <= T2CX + buffer and T2CY - buffer <= B2CY <= T2CY + buffer:
            signal = "2A"  # Idle
            sendSignal(signal)
            p = 1
            q = "BOT2"
            return p, q

    # BOT2 moving turning at T2 towards D2
    if operationNo == 1:
        B2Vu = unit_vector(B2V)  # Making into unit vector
        D2Vu = unit_vector(D2V)  # Making into unit vector

        angle = angle_between(B2Vu, D2Vu)
        angleDeg = angle * 57.29577952326092822 // 1
        # print(angleDeg)

        Ux = math.cos(math.radians(bufferAngle)) * 100 // 1
        Uy = math.sin(math.radians(bufferAngle)) * 100 // 1
        # print(Ux, Uy)

        cv2.line(img, (B2CX, B2CY), (D2CX, D2CY), (0, 255, 255), 2)
        cv2.line(img, (B2CX, B2CY), (B2CX - int(Ux), B2CY - int(Uy)), (255, 255, 0), 2)
        cv2.line(img, (B2CX, B2CY), (B2CX - int(Ux), B2CY + int(Uy)), (255, 255, 0), 2)

        if angleDeg > bufferAngle:
            signal = "2D"  # Turn Right
            sendSignal(signal)
            p = 1
            q = "BOT2"
            return p, q
        elif angleDeg <= bufferAngle:
            signal = "2A"  # Idle
            sendSignal(signal)
            p = 2
            q = "BOT2"
            return p, q

    # BOT2 moving forward towards D2
    if operationNo == 2:

        cv2.line(img, (B2CX, B2CY), (D2CX, D2CY), (0, 255, 255), 2)
        # cv2.line(img, (D2CX - buffer, D2CY - buffer), (D2CX + buffer, D2CY - buffer), (255, 255, 0), 2)
        # cv2.line(img, (D2CX + buffer, D2CY - buffer), (D2CX + buffer, D2CY + buffer), (255, 255, 0), 2)
        # cv2.line(img, (D2CX + buffer, D2CY + buffer), (D2CX - buffer, D2CY + buffer), (255, 255, 0), 2)
        # cv2.line(img, (D2CX - buffer, D2CY + buffer), (D2CX - buffer, D2CY - buffer), (255, 255, 0), 2)

        cv2.line(img, (0, D2CY - buffer), (imgx, D2CY - buffer), (255, 255, 0), 2)
        cv2.line(img, (D2CX + buffer, 0), (D2CX + buffer, imgy), (255, 255, 0), 2)
        cv2.line(img, (imgx, D2CY + buffer), (0, D2CY + buffer), (255, 255, 0), 2)
        cv2.line(img, (D2CX - buffer, imgy), (D2CX - buffer, 0), (255, 255, 0), 2)

        if B2CX < D2CX - buffer and B2CY < D2CY - buffer:
            signal = "2J"  # Backward-Left
            sendSignal(signal)
            p = 2
            q = "BOT2"
            return p, q
        elif B2CX > D2CX + buffer and B2CY < D2CY - buffer:
            signal = "2H"  # Forward-Left
            sendSignal(signal)
            p = 2
            q = "BOT2"
            return p, q
        elif B2CX < D2CX - buffer and B2CY > D2CY + buffer:
            signal = "2I"  # Backward-Right
            sendSignal(signal)
            p = 2
            q = "BOT2"
            return p, q
        elif B2CX > D2CX + buffer and B2CY > D2CY + buffer:
            signal = "2G"  # Forward-Right
            sendSignal(signal)
            p = 2
            q = "BOT2"
            return p, q
        elif D2CX - buffer <= B2CX <= D2CX + buffer and B2CY < D2CY - buffer:
            signal = "2J"  # Backward-Left
            sendSignal(signal)
            p = 2
            q = "BOT2"
            return p, q
        elif D2CX - buffer <= B2CX <= D2CX + buffer and B2CY > D2CY + buffer:
            signal = "2I"  # Backward-Right
            sendSignal(signal)
            p = 2
            q = "BOT2"
            return p, q
        elif B2CX < D2CX - buffer and D2CY - buffer <= B2CY <= D2CY + buffer:
            signal = "2C"  # Backward
            sendSignal(signal)
            p = 2
            q = "BOT2"
            return p, q
        elif B2CX > D2CX + buffer and D2CY - buffer <= B2CY <= D2CY + buffer:
            signal = "2B"  # Forward
            sendSignal(signal)
            p = 2
            q = "BOT2"
            return p, q
        elif D2CX - buffer <= B2CX <= D2CX + buffer and D2CY - buffer <= B2CY <= D2CY + buffer:
            signal = "2A"  # Idle
            sendSignal(signal)
            p = 3
            q = "BOT2"
            return p, q

    # BOT2 dropping package
    if operationNo == 3:
        signal = "2F"
        sendSignal(signal)
        p = 4
        q = "BOT2"
        return p, q

    # BOT2 moving backwards towards T2
    if operationNo == 4:

        cv2.line(img, (B2CX, B2CY), (T2CX, T2CY), (0, 255, 255), 2)
        # cv2.line(img, (T2CX - buffer, T2CY - buffer), (T2CX + buffer, T2CY - buffer), (255, 255, 0), 2)
        # cv2.line(img, (T2CX + buffer, T2CY - buffer), (T2CX + buffer, T2CY + buffer), (255, 255, 0), 2)
        # cv2.line(img, (T2CX + buffer, T2CY + buffer), (T2CX - buffer, T2CY + buffer), (255, 255, 0), 2)
        # cv2.line(img, (T2CX - buffer, T2CY + buffer), (T2CX - buffer, T2CY - buffer), (255, 255, 0), 2)

        cv2.line(img, (0, T2CY - buffer), (imgx, T2CY - buffer), (255, 255, 0), 2)
        cv2.line(img, (T2CX + buffer, 0), (T2CX + buffer, imgy), (255, 255, 0), 2)
        cv2.line(img, (imgx, T2CY + buffer), (0, T2CY + buffer), (255, 255, 0), 2)
        cv2.line(img, (T2CX - buffer, imgy), (T2CX - buffer, 0), (255, 255, 0), 2)

        if B2CX < T2CX - buffer and B2CY < T2CY - buffer:
            signal = "2J"  # Backward-Left
            sendSignal(signal)
            p = 4
            q = "BOT2"
            return p, q
        elif B2CX > T2CX + buffer and B2CY < T2CY - buffer:
            signal = "2H"  # Forward-Left
            sendSignal(signal)
            p = 4
            q = "BOT2"
            return p, q
        elif B2CX < T2CX - buffer and B2CY > T2CY + buffer:
            signal = "2I"  # Backward-Right
            sendSignal(signal)
            p = 4
            q = "BOT2"
            return p, q
        elif B2CX > T2CX + buffer and B2CY > T2CY + buffer:
            signal = "2G"  # Forward-Right
            sendSignal(signal)
            p = 4
            q = "BOT2"
            return p, q
        elif T2CX - buffer <= B2CX <= T2CX + buffer and B2CY < T2CY - buffer:
            signal = "2H"  # Forward-Left
            sendSignal(signal)
            p = 4
            q = "BOT2"
            return p, q
        elif T2CX - buffer <= B2CX <= T2CX + buffer and B2CY > T2CY + buffer:
            signal = "2G"  # Forward-Right
            sendSignal(signal)
            p = 4
            q = "BOT2"
            return p, q
        elif B2CX < T2CX - buffer and T2CY - buffer <= B2CY <= T2CY + buffer:
            signal = "2C"  # Backward
            sendSignal(signal)
            p = 4
            q = "BOT2"
            return p, q
        elif B2CX > T2CX + buffer and T2CY - buffer <= B2CY <= T2CY + buffer:
            signal = "2B"  # Forward
            sendSignal(signal)
            p = 4
            q = "BOT2"
            return p, q
        elif T2CX - buffer <= B2CX <= T2CX + buffer and T2CY - buffer <= B2CY <= T2CY + buffer:
            signal = "2A"  # Idle
            sendSignal(signal)
            p = 5
            q = "BOT2"
            return p, q

    #  BOT2 moving turning at T2 towards S2
    if operationNo == 5:

        B2Vu = unit_vector(B2V)  # Making into unit vector
        S2Vu = unit_vector(S2V)  # Making into unit vector

        angle = angle_between(B2Vu, S2Vu)
        angleDeg = angle * 57.29577952326092822 // 2
        print(angleDeg)

        Ux = math.cos(math.radians(bufferAngle)) * 100 // 1
        Uy = math.sin(math.radians(bufferAngle)) * 100 // 1
        # print(Ux, Uy)

        cv2.line(img, (B2CX, B2CY), (S2CX, S2CY), (0, 255, 255), 2)
        cv2.line(img, (B2CX, B2CY), (B2CX + int(Uy), B2CY + int(Ux)), (255, 255, 0), 2)
        cv2.line(img, (B2CX, B2CY), (B2CX - int(Uy), B2CY + int(Ux)), (255, 255, 0), 2)

        if angleDeg > bufferAngle:
            signal = "2E"  # Turn Left
            sendSignal(signal)
            p = 5
            q = "BOT2"
            return p, q
        elif angleDeg <= bufferAngle:
            signal = "2A"  # Idle
            sendSignal(signal)
            p = 6
            q = "BOT2"
            return p, q

    # BOT2 moving backwards towards S2
    if operationNo == 6:

        cv2.line(img, (B2CX, B2CY), (S2CX, S2CY), (0, 255, 255), 2)
        # cv2.line(img, (S2CX - buffer, S2CY - buffer), (S2CX + buffer, S2CY - buffer), (255, 255, 0), 2)
        # cv2.line(img, (S2CX + buffer, S2CY - buffer), (S2CX + buffer, S2CY + buffer), (255, 255, 0), 2)
        # cv2.line(img, (S2CX + buffer, S2CY + buffer), (S2CX - buffer, S2CY + buffer), (255, 255, 0), 2)
        # cv2.line(img, (S2CX - buffer, S2CY + buffer), (S2CX - buffer, S2CY - buffer), (255, 255, 0), 2)

        cv2.line(img, (0, S2CY - buffer), (imgx, S2CY - buffer), (255, 255, 0), 2)
        cv2.line(img, (S2CX + buffer, 0), (S2CX + buffer, imgy), (255, 255, 0), 2)
        cv2.line(img, (imgx, S2CY + buffer), (0, S2CY + buffer), (255, 255, 0), 2)
        cv2.line(img, (S2CX - buffer, imgy), (S2CX - buffer, 0), (255, 255, 0), 2)

        if B2CX < S2CX - buffer and B2CY < S2CY - buffer:
            signal = "2H"  # Forward-Left
            sendSignal(signal)
            p = 6
            q = "BOT2"
            return p, q
        elif B2CX > S2CX + buffer and B2CY < S2CY - buffer:
            signal = "2G"  # Forward-Right
            sendSignal(signal)
            p = 6
            q = "BOT2"
            return p, q
        elif B2CX < S2CX - buffer and B2CY > S2CY + buffer:
            signal = "2J"  # Backward-Left
            sendSignal(signal)
            p = 6
            q = "BOT2"
            return p, q
        elif B2CX > S2CX + buffer and B2CY > S2CY + buffer:
            signal = "2I"  # Backward-Right
            sendSignal(signal)
            p = 6
            q = "BOT2"
            return p, q
        elif S2CX - buffer <= B2CX <= S2CX + buffer and B2CY < S2CY - buffer:
            signal = "2B"  # Forward
            sendSignal(signal)
            p = 6
            q = "BOT2"
            return p, q
        elif S2CX - buffer <= B2CX <= S2CX + buffer and B2CY > S2CY + buffer:
            signal = "2C"  # Backward
            sendSignal(signal)
            p = 6
            q = "BOT2"
            return p, q
        elif B2CX < S2CX - buffer and S2CY - buffer <= B2CY <= S2CY + buffer:
            signal = "2H"  # Forward-Left
            sendSignal(signal)
            p = 6
            return p, q
        elif B2CX > S2CX + buffer and S2CY - buffer <= B2CY <= S2CY + buffer:
            signal = "2G"  # Forward-Right
            sendSignal(signal)
            p = 6
            q = "BOT2"
            return p, q
        elif S2CX - buffer <= B2CX <= S2CX + buffer and S2CY - buffer <= B2CY <= S2CY + buffer:
            signal = "2A"  # Idle
            sendSignal(signal)
            p = 0
            q = "BOT3"
            return p, q

def runLogicBOT3(img, p, operationNo, q):
    # BOT3 moving forward towards T3
    if operationNo == 0:

        cv2.line(img, (B3CX, B3CY), (T3CX, T3CY), (0, 255, 255), 2)
        # cv2.line(img, (T3CX-buffer, T3CY-buffer), (T3CX+buffer, T3CY-buffer), (255, 255, 0), 2)
        # cv2.line(img, (T3CX+buffer, T3CY-buffer), (T3CX+buffer, T3CY+buffer), (255, 255, 0), 2)
        # cv2.line(img, (T3CX+buffer, T3CY+buffer), (T3CX-buffer, T3CY+buffer), (255, 255, 0), 2)
        # cv2.line(img, (T3CX-buffer, T3CY+buffer), (T3CX-buffer, T3CY-buffer), (255, 255, 0), 2)

        cv2.line(img, (0, T3CY - buffer), (imgx, T3CY - buffer), (255, 255, 0), 2)
        cv2.line(img, (T3CX + buffer, 0), (T3CX + buffer, imgy), (255, 255, 0), 2)
        cv2.line(img, (imgx, T3CY + buffer), (0, T3CY + buffer), (255, 255, 0), 2)
        cv2.line(img, (T3CX - buffer, imgy), (T3CX - buffer, 0), (255, 255, 0), 2)

        if B3CX < T3CX - buffer and B3CY < T3CY - buffer:
            signal = "3H"  # Forward-Left
            sendSignal(signal)
            p = 0
            q = "BOT3"
            return p, q
        if B3CX > T3CX + buffer and B3CY < T3CY - buffer:
            signal = "3G"  # Forward-Right
            sendSignal(signal)
            p = 0
            q = "BOT3"
            return p, q
        if B3CX < T3CX - buffer and B3CY > T3CY + buffer:
            signal = "3J"  # Backward-Left
            sendSignal(signal)
            p = 0
            q = "BOT3"
            return p, q
        if B3CX > T3CX + buffer and B3CY > T3CY + buffer:
            signal = "3I"  # Backward-Right
            sendSignal(signal)
            p = 0
            q = "BOT3"
            return p, q
        if T3CX - buffer <= B3CX <= T3CX + buffer and B3CY < T3CY - buffer:
            signal = "3B"  # Forward
            sendSignal(signal)
            p = 0
            q = "BOT3"
            return p, q
        if T3CX - buffer <= B3CX <= T3CX + buffer and B3CY > T3CY + buffer:
            signal = "3C"  # Backward
            sendSignal(signal)
            p = 0
            q = "BOT3"
            return p, q
        if B3CX < T3CX - buffer and T3CY - buffer <= B3CY <= T3CY + buffer:
            signal = "3J"  # Backward-Left
            sendSignal(signal)
            p = 0
            q = "BOT3"
            return p, q
        if B3CX > T3CX + buffer and T3CY - buffer <= B3CY <= T3CY + buffer:
            signal = "3I"  # Backward-Right
            sendSignal(signal)
            p = 0
            q = "BOT3"
            return p, q
        if T3CX - buffer <= B3CX <= T3CX + buffer and T3CY - buffer <= B3CY <= T3CY + buffer:
            signal = "3A"  # Idle
            sendSignal(signal)
            p = 1
            q = "BOT3"
            return p, q

    # BOT3 moving turning at T3 towards D3
    if operationNo == 1:
        B3Vu = unit_vector(B3V)  # Making into unit vector
        D3Vu = unit_vector(D3V)  # Making into unit vector

        angle = angle_between(B3Vu, D3Vu)
        angleDeg = angle * 57.29577952326092822 // 1
        print(angleDeg)

        Ux = math.cos(math.radians(bufferAngle)) * 100 // 1
        Uy = math.sin(math.radians(bufferAngle)) * 100 // 1
        # print(Ux, Uy)

        cv2.line(img, (B3CX, B3CY), (D3CX, D3CY), (0, 255, 255), 2)
        cv2.line(img, (B3CX, B3CY), (B3CX + int(Ux), B3CY - int(Uy)), (255, 255, 0), 2)
        cv2.line(img, (B3CX, B3CY), (B3CX + int(Ux), B3CY + int(Uy)), (255, 255, 0), 2)

        if angleDeg > bufferAngle:
            signal = "3E"  # Turn Left
            sendSignal(signal)
            p = 1
            q = "BOT3"
            return p, q
        elif angleDeg <= bufferAngle:
            signal = "3A"  # Idle
            sendSignal(signal)
            p = 2
            q = "BOT3"
            return p, q

    # BOT3 moving forward towards D3
    if operationNo == 2:

        cv2.line(img, (B3CX, B3CY), (D3CX, D3CY), (0, 255, 255), 2)
        # cv2.line(img, (D3CX - buffer, D3CY - buffer), (D3CX + buffer, D3CY - buffer), (255, 255, 0), 2)
        # cv2.line(img, (D3CX + buffer, D3CY - buffer), (D3CX + buffer, D3CY + buffer), (255, 255, 0), 2)
        # cv2.line(img, (D3CX + buffer, D3CY + buffer), (D3CX - buffer, D3CY + buffer), (255, 255, 0), 2)
        # cv2.line(img, (D3CX - buffer, D3CY + buffer), (D3CX - buffer, D3CY - buffer), (255, 255, 0), 2)

        cv2.line(img, (0, D3CY - buffer), (imgx, D3CY - buffer), (255, 255, 0), 2)
        cv2.line(img, (D3CX + buffer, 0), (D3CX + buffer, imgy), (255, 255, 0), 2)
        cv2.line(img, (imgx, D3CY + buffer), (0, D3CY + buffer), (255, 255, 0), 2)
        cv2.line(img, (D3CX - buffer, imgy), (D3CX - buffer, 0), (255, 255, 0), 2)

        if B3CX < D3CX - buffer and B3CY < D3CY - buffer:
            signal = "3G"  # Forward-Right
            sendSignal(signal)
            p = 2
            q = "BOT3"
            return p, q
        elif B3CX > D3CX + buffer and B3CY < D3CY - buffer:
            signal = "3I"  # Backward-Right
            sendSignal(signal)
            p = 2
            q = "BOT3"
            return p, q
        elif B3CX < D3CX - buffer and B3CY > D3CY + buffer:
            signal = "3H"  # Forward-Left
            sendSignal(signal)
            p = 2
            q = "BOT3"
            return p, q
        elif B3CX > D3CX + buffer and B3CY > D3CY + buffer:
            signal = "3J"  # Backward-Left
            sendSignal(signal)
            p = 2
            q = "BOT3"
            return p, q
        elif D3CX - buffer <= B3CX <= D3CX + buffer and B3CY < D3CY - buffer:
            signal = "3I"  # Backward-Right
            sendSignal(signal)
            p = 2
            q = "BOT3"
            return p, q
        elif D3CX - buffer <= B3CX <= D3CX + buffer and B3CY > D3CY + buffer:
            signal = "3J"  # Backward-Left
            sendSignal(signal)
            p = 2
            q = "BOT3"
            return p, q
        elif B3CX < D3CX - buffer and D3CY - buffer <= B3CY <= D3CY + buffer:
            signal = "3B"  # Forward
            sendSignal(signal)
            p = 2
            q = "BOT3"
            return p, q
        elif B3CX > D3CX + buffer and D3CY - buffer <= B3CY <= D3CY + buffer:
            signal = "3C"  # Backward
            sendSignal(signal)
            p = 2
            q = "BOT3"
            return p, q
        elif D3CX - buffer <= B3CX <= D3CX + buffer and D3CY - buffer <= B3CY <= D3CY + buffer:
            signal = "3A"  # Idle
            sendSignal(signal)
            p = 3
            q = "BOT3"
            return p, q

    # BOT3 dropping package
    if operationNo == 3:
        signal = "3F"
        sendSignal(signal)
        p = 4
        q = "BOT3"
        return p, q

    # BOT3 moving backwards towards T3
    if operationNo == 4:

        cv2.line(img, (B3CX, B3CY), (T3CX, T3CY), (0, 255, 255), 2)
        # cv2.line(img, (T3CX - buffer, T3CY - buffer), (T3CX + buffer, T3CY - buffer), (255, 255, 0), 2)
        # cv2.line(img, (T3CX + buffer, T3CY - buffer), (T3CX + buffer, T3CY + buffer), (255, 255, 0), 2)
        # cv2.line(img, (T3CX + buffer, T3CY + buffer), (T3CX - buffer, T3CY + buffer), (255, 255, 0), 2)
        # cv2.line(img, (T3CX - buffer, T3CY + buffer), (T3CX - buffer, T3CY - buffer), (255, 255, 0), 2)

        cv2.line(img, (0, T3CY - buffer), (imgx, T3CY - buffer), (255, 255, 0), 2)
        cv2.line(img, (T3CX + buffer, 0), (T3CX + buffer, imgy), (255, 255, 0), 2)
        cv2.line(img, (imgx, T3CY + buffer), (0, T3CY + buffer), (255, 255, 0), 2)
        cv2.line(img, (T3CX - buffer, imgy), (T3CX - buffer, 0), (255, 255, 0), 2)

        if B3CX < T3CX - buffer and B3CY < T3CY - buffer:
            signal = "3G"  # Forward-Right
            sendSignal(signal)
            p = 4
            q = "BOT3"
            return p, q
        elif B3CX > T3CX + buffer and B3CY < T3CY - buffer:
            signal = "3I"  # Backward-Right
            sendSignal(signal)
            p = 4
            q = "BOT3"
            return p, q
        elif B3CX < T3CX - buffer and B3CY > T3CY + buffer:
            signal = "3H"  # Forward-Left
            sendSignal(signal)
            p = 4
            q = "BOT3"
            return p, q
        elif B3CX > T3CX + buffer and B3CY > T3CY + buffer:
            signal = "3J"  # Backward-Left
            sendSignal(signal)
            p = 4
            q = "BOT3"
            return p, q
        elif T3CX - buffer <= B3CX <= T3CX + buffer and B3CY < T3CY - buffer:
            signal = "3G"  # Forward-Right
            sendSignal(signal)
            p = 4
            q = "BOT3"
            return p, q
        elif T3CX - buffer <= B3CX <= T3CX + buffer and B3CY > T3CY + buffer:
            signal = "3H"  # Forward-Left
            sendSignal(signal)
            p = 4
            q = "BOT3"
            return p, q
        elif B3CX < T3CX - buffer and T3CY - buffer <= B3CY <= T3CY + buffer:
            signal = "3B"  # Forward
            sendSignal(signal)
            p = 4
            q = "BOT3"
            return p, q
        elif B3CX > T3CX + buffer and T3CY - buffer <= B3CY <= T3CY + buffer:
            signal = "3C"  # Backward
            sendSignal(signal)
            p = 4
            q = "BOT3"
            return p, q
        elif T3CX - buffer <= B3CX <= T3CX + buffer and T3CY - buffer <= B3CY <= T3CY + buffer:
            signal = "3A"  # Idle
            sendSignal(signal)
            p = 5
            q = "BOT3"
            return p, q

    #  BOT3 moving turning at T3 towards S3
    if operationNo == 5:

        B3Vu = unit_vector(B3V)  # Making into unit vector
        S3Vu = unit_vector(S3V)  # Making into unit vector

        angle = angle_between(B3Vu, S3Vu)
        angleDeg = angle * 57.29577952326092822 // 1
        print(angleDeg)

        Ux = math.cos(math.radians(bufferAngle)) * 100 // 1
        Uy = math.sin(math.radians(bufferAngle)) * 100 // 1
        # print(Ux, Uy)

        cv2.line(img, (B3CX, B3CY), (S3CX, S3CY), (0, 255, 255), 2)
        cv2.line(img, (B3CX, B3CY), (B3CX + int(Uy), B3CY + int(Ux)), (255, 255, 0), 2)
        cv2.line(img, (B3CX, B3CY), (B3CX - int(Uy), B3CY + int(Ux)), (255, 255, 0), 2)

        if angleDeg > bufferAngle:
            signal = "3D"  # Turn Right
            sendSignal(signal)
            p = 5
            q = "BOT3"
            return p, q
        elif angleDeg <= bufferAngle:
            signal = "3A"  # Idle
            sendSignal(signal)
            p = 6
            q = "BOT3"
            return p, q

    # BOT3 moving backwards towards S3
    if operationNo == 6:

        cv2.line(img, (B3CX, B3CY), (S3CX, S3CY), (0, 255, 255), 2)
        # cv2.line(img, (S3CX - buffer, S3CY - buffer), (S3CX + buffer, S3CY - buffer), (255, 255, 0), 2)
        # cv2.line(img, (S3CX + buffer, S3CY - buffer), (S3CX + buffer, S3CY + buffer), (255, 255, 0), 2)
        # cv2.line(img, (S3CX + buffer, S3CY + buffer), (S3CX - buffer, S3CY + buffer), (255, 255, 0), 2)
        # cv2.line(img, (S3CX - buffer, S3CY + buffer), (S3CX - buffer, S3CY - buffer), (255, 255, 0), 2)

        cv2.line(img, (0, S3CY - buffer), (imgx, S3CY - buffer), (255, 255, 0), 2)
        cv2.line(img, (S3CX + buffer, 0), (S3CX + buffer, imgy), (255, 255, 0), 2)
        cv2.line(img, (imgx, S3CY + buffer), (0, S3CY + buffer), (255, 255, 0), 2)
        cv2.line(img, (S3CX - buffer, imgy), (S3CX - buffer, 0), (255, 255, 0), 2)

        if B3CX < S3CX - buffer and B3CY < S3CY - buffer:
            signal = "3H"  # Forward-Left
            sendSignal(signal)
            p = 6
            q = "BOT3"
            return p, q
        elif B3CX > S3CX + buffer and B3CY < S3CY - buffer:
            signal = "3G"  # Forward-Right
            sendSignal(signal)
            p = 6
            q = "BOT3"
            return p, q
        elif B3CX < S3CX - buffer and B3CY > S3CY + buffer:
            signal = "3J"  # Backward-Left
            sendSignal(signal)
            p = 6
            q = "BOT3"
            return p, q
        elif B3CX > S3CX + buffer and B3CY > S3CY + buffer:
            signal = "3I"  # Backward-Right
            sendSignal(signal)
            p = 6
            q = "BOT3"
            return p, q
        elif S3CX - buffer <= B3CX <= S3CX + buffer and B3CY < S3CY - buffer:
            signal = "3B"  # Forward
            sendSignal(signal)
            p = 6
            q = "BOT3"
            return p, q
        elif S3CX - buffer <= B3CX <= S3CX + buffer and B3CY > S3CY + buffer:
            signal = "3C"  # Backward
            sendSignal(signal)
            p = 6
            q = "BOT3"
            return p, q
        elif B3CX < S3CX - buffer and S3CY - buffer <= B3CY <= S3CY + buffer:
            signal = "3H"  # Forward-Left
            sendSignal(signal)
            p = 6
            return p, q
        elif B3CX > S3CX + buffer and S3CY - buffer <= B3CY <= S3CY + buffer:
            signal = "3G"  # Forward-Right
            sendSignal(signal)
            p = 6
            q = "BOT3"
            return p, q
        elif S3CX - buffer <= B3CX <= S3CX + buffer and S3CY - buffer <= B3CY <= S3CY + buffer:
            signal = "3A"  # Idle
            sendSignal(signal)
            p = 0
            q = "BOT4"
            return p, q

def runLogicBOT4(img, p, operationNo, q):
    # BOT4 moving forward towards T4
    if operationNo == 0:

        cv2.line(img, (B4CX, B4CY), (T4CX, T4CY), (0, 255, 255), 2)
        # cv2.line(img, (T4CX-buffer, T4CY-buffer), (T4CX+buffer, T4CY-buffer), (255, 255, 0), 2)
        # cv2.line(img, (T4CX+buffer, T4CY-buffer), (T4CX+buffer, T4CY+buffer), (255, 255, 0), 2)
        # cv2.line(img, (T4CX+buffer, T4CY+buffer), (T4CX-buffer, T4CY+buffer), (255, 255, 0), 2)
        # cv2.line(img, (T4CX-buffer, T4CY+buffer), (T4CX-buffer, T4CY-buffer), (255, 255, 0), 2)

        cv2.line(img, (0, T4CY - buffer), (imgx, T4CY - buffer), (255, 255, 0), 2)
        cv2.line(img, (T4CX + buffer, 0), (T4CX + buffer, imgy), (255, 255, 0), 2)
        cv2.line(img, (imgx, T4CY + buffer), (0, T4CY + buffer), (255, 255, 0), 2)
        cv2.line(img, (T4CX - buffer, imgy), (T4CX - buffer, 0), (255, 255, 0), 2)

        if B4CX < T4CX - buffer and B4CY < T4CY - buffer:
            signal = "4H"  # Forward-Left
            sendSignal(signal)
            p = 0
            q = "BOT4"
            return p, q
        if B4CX > T4CX + buffer and B4CY < T4CY - buffer:
            signal = "4G"  # Forward-Right
            sendSignal(signal)
            p = 0
            q = "BOT4"
            return p, q
        if B4CX < T4CX - buffer and B4CY > T4CY + buffer:
            signal = "4J"  # Backward-Left
            sendSignal(signal)
            p = 0
            q = "BOT4"
            return p, q
        if B4CX > T4CX + buffer and B4CY > T4CY + buffer:
            signal = "4I"  # Backward-Right
            sendSignal(signal)
            p = 0
            q = "BOT4"
            return p, q
        if T4CX - buffer <= B4CX <= T4CX + buffer and B4CY < T4CY - buffer:
            signal = "4B"  # Forward
            sendSignal(signal)
            p = 0
            q = "BOT4"
            return p, q
        if T4CX - buffer <= B4CX <= T4CX + buffer and B4CY > T4CY + buffer:
            signal = "4C"  # Backward
            sendSignal(signal)
            p = 0
            q = "BOT4"
            return p, q
        if B4CX < T4CX - buffer and T4CY - buffer <= B4CY <= T4CY + buffer:
            signal = "4J"  # Backward-Left
            sendSignal(signal)
            p = 0
            q = "BOT4"
            return p, q
        if B4CX > T4CX + buffer and T4CY - buffer <= B4CY <= T4CY + buffer:
            signal = "4I"  # Backward-Right
            sendSignal(signal)
            p = 0
            q = "BOT4"
            return p, q
        if T4CX - buffer <= B4CX <= T4CX + buffer and T4CY - buffer <= B4CY <= T4CY + buffer:
            signal = "4A"  # Idle
            sendSignal(signal)
            p = 1
            q = "BOT4"
            return p, q

    # BOT4 moving turning at T4 towards D4
    if operationNo == 1:
        B4Vu = unit_vector(B4V)  # Making into unit vector
        D4Vu = unit_vector(D4V)  # Making into unit vector

        angle = angle_between(B4Vu, D4Vu)
        angleDeg = angle * 57.29577952326092822 // 1
        # print(angleDeg)

        Ux = math.cos(math.radians(bufferAngle)) * 100 // 1
        Uy = math.sin(math.radians(bufferAngle)) * 100 // 1
        # print(Ux, Uy)

        cv2.line(img, (B4CX, B4CY), (D4CX, D4CY), (0, 255, 255), 2)
        cv2.line(img, (B4CX, B4CY), (B4CX + int(Ux), B4CY - int(Uy)), (255, 255, 0), 2)
        cv2.line(img, (B4CX, B4CY), (B4CX + int(Ux), B4CY + int(Uy)), (255, 255, 0), 2)

        if angleDeg > bufferAngle:
            signal = "4E"  # Turn Left
            sendSignal(signal)
            p = 1
            q = "BOT4"
            return p, q
        elif angleDeg <= bufferAngle:
            signal = "4A"  # Idle
            sendSignal(signal)
            p = 2
            q = "BOT4"
            return p, q

    # BOT4 moving forward towards D4
    if operationNo == 2:

        cv2.line(img, (B4CX, B4CY), (D4CX, D4CY), (0, 255, 255), 2)
        # cv2.line(img, (D4CX - buffer, D4CY - buffer), (D4CX + buffer, D4CY - buffer), (255, 255, 0), 2)
        # cv2.line(img, (D4CX + buffer, D4CY - buffer), (D4CX + buffer, D4CY + buffer), (255, 255, 0), 2)
        # cv2.line(img, (D4CX + buffer, D4CY + buffer), (D4CX - buffer, D4CY + buffer), (255, 255, 0), 2)
        # cv2.line(img, (D4CX - buffer, D4CY + buffer), (D4CX - buffer, D4CY - buffer), (255, 255, 0), 2)

        cv2.line(img, (0, D4CY - buffer), (imgx, D4CY - buffer), (255, 255, 0), 2)
        cv2.line(img, (D4CX + buffer, 0), (D4CX + buffer, imgy), (255, 255, 0), 2)
        cv2.line(img, (imgx, D4CY + buffer), (0, D4CY + buffer), (255, 255, 0), 2)
        cv2.line(img, (D4CX - buffer, imgy), (D4CX - buffer, 0), (255, 255, 0), 2)

        if B4CX < D4CX - buffer and B4CY < D4CY - buffer:
            signal = "4G"  # Forward-Right
            sendSignal(signal)
            p = 2
            q = "BOT4"
            return p, q
        elif B4CX > D4CX + buffer and B4CY < D4CY - buffer:
            signal = "4I"  # Backward-Right
            sendSignal(signal)
            p = 2
            q = "BOT4"
            return p, q
        elif B4CX < D4CX - buffer and B4CY > D4CY + buffer:
            signal = "4H"  # Forward-Left
            sendSignal(signal)
            p = 2
            q = "BOT4"
            return p, q
        elif B4CX > D4CX + buffer and B4CY > D4CY + buffer:
            signal = "4J"  # Backward-Left
            sendSignal(signal)
            p = 2
            q = "BOT4"
            return p, q
        elif D4CX - buffer <= B4CX <= D4CX + buffer and B4CY < D4CY - buffer:
            signal = "4I"  # Backward-Right
            sendSignal(signal)
            p = 2
            q = "BOT4"
            return p, q
        elif D4CX - buffer <= B4CX <= D4CX + buffer and B4CY > D4CY + buffer:
            signal = "4J"  # Backward-Left
            sendSignal(signal)
            p = 2
            q = "BOT4"
            return p, q
        elif B4CX < D4CX - buffer and D4CY - buffer <= B4CY <= D4CY + buffer:
            signal = "4B"  # Forward
            sendSignal(signal)
            p = 2
            q = "BOT4"
            return p, q
        elif B4CX > D4CX + buffer and D4CY - buffer <= B4CY <= D4CY + buffer:
            signal = "4C"  # Backward
            sendSignal(signal)
            p = 2
            q = "BOT4"
            return p, q
        elif D4CX - buffer <= B4CX <= D4CX + buffer and D4CY - buffer <= B4CY <= D4CY + buffer:
            signal = "4A"  # Idle
            sendSignal(signal)
            p = 3
            q = "BOT4"
            return p, q

    # BOT4 dropping package
    if operationNo == 3:
        signal = "4F"
        sendSignal(signal)
        p = 4
        q = "BOT4"
        return p, q

    # BOT4 moving backwards towards T4
    if operationNo == 4:

        cv2.line(img, (B4CX, B4CY), (T4CX, T4CY), (0, 255, 255), 2)
        # cv2.line(img, (T4CX - buffer, T4CY - buffer), (T4CX + buffer, T4CY - buffer), (255, 255, 0), 2)
        # cv2.line(img, (T4CX + buffer, T4CY - buffer), (T4CX + buffer, T4CY + buffer), (255, 255, 0), 2)
        # cv2.line(img, (T4CX + buffer, T4CY + buffer), (T4CX - buffer, T4CY + buffer), (255, 255, 0), 2)
        # cv2.line(img, (T4CX - buffer, T4CY + buffer), (T4CX - buffer, T4CY - buffer), (255, 255, 0), 2)

        cv2.line(img, (0, T4CY - buffer), (imgx, T4CY - buffer), (255, 255, 0), 2)
        cv2.line(img, (T4CX + buffer, 0), (T4CX + buffer, imgy), (255, 255, 0), 2)
        cv2.line(img, (imgx, T4CY + buffer), (0, T4CY + buffer), (255, 255, 0), 2)
        cv2.line(img, (T4CX - buffer, imgy), (T4CX - buffer, 0), (255, 255, 0), 2)

        if B4CX < T4CX - buffer and B4CY < T4CY - buffer:
            signal = "4G"  # Forward-Right
            sendSignal(signal)
            p = 4
            q = "BOT4"
            return p, q
        elif B4CX > T4CX + buffer and B4CY < T4CY - buffer:
            signal = "4I"  # Backward-Right
            sendSignal(signal)
            p = 4
            q = "BOT4"
            return p, q
        elif B4CX < T4CX - buffer and B4CY > T4CY + buffer:
            signal = "4H"  # Forward-Left
            sendSignal(signal)
            p = 4
            q = "BOT4"
            return p, q
        elif B4CX > T4CX + buffer and B4CY > T4CY + buffer:
            signal = "4J"  # Backward-Left
            sendSignal(signal)
            p = 4
            q = "BOT4"
            return p, q
        elif T4CX - buffer <= B4CX <= T4CX + buffer and B4CY < T4CY - buffer:
            signal = "4G"  # Forward-Right
            sendSignal(signal)
            p = 4
            q = "BOT4"
            return p, q
        elif T4CX - buffer <= B4CX <= T4CX + buffer and B4CY > T4CY + buffer:
            signal = "4H"  # Forward-Left
            sendSignal(signal)
            p = 4
            q = "BOT4"
            return p, q
        elif B4CX < T4CX - buffer and T4CY - buffer <= B4CY <= T4CY + buffer:
            signal = "4B"  # Forward
            sendSignal(signal)
            p = 4
            q = "BOT4"
            return p, q
        elif B4CX > T4CX + buffer and T4CY - buffer <= B4CY <= T4CY + buffer:
            signal = "4C"  # Backward
            sendSignal(signal)
            p = 4
            q = "BOT4"
            return p, q
        elif T4CX - buffer <= B4CX <= T4CX + buffer and T4CY - buffer <= B4CY <= T4CY + buffer:
            signal = "4A"  # Idle
            sendSignal(signal)
            p = 5
            q = "BOT4"
            return p, q

    #  BOT4 moving turning at T4 towards S4
    if operationNo == 5:

        B4Vu = unit_vector(B4V)  # Making into unit vector
        S4Vu = unit_vector(S4V)  # Making into unit vector

        angle = angle_between(B4Vu, S4Vu)
        angleDeg = angle * 57.29577952326092822 // 1
        print(angleDeg)

        Ux = math.cos(math.radians(bufferAngle)) * 100 // 1
        Uy = math.sin(math.radians(bufferAngle)) * 100 // 1
        # print(Ux, Uy)

        cv2.line(img, (B4CX, B4CY), (S4CX, S4CY), (0, 255, 255), 2)
        cv2.line(img, (B4CX, B4CY), (B4CX + int(Uy), B4CY + int(Ux)), (255, 255, 0), 2)
        cv2.line(img, (B4CX, B4CY), (B4CX - int(Uy), B4CY + int(Ux)), (255, 255, 0), 2)

        if angleDeg > bufferAngle:
            signal = "4D"  # Turn Right
            sendSignal(signal)
            p = 5
            q = "BOT4"
            return p, q
        elif angleDeg <= bufferAngle:
            signal = "4A"  # Idle
            sendSignal(signal)
            p = 6
            q = "BOT4"
            return p, q

    # BOT4 moving backwards towards S4
    if operationNo == 6:

        cv2.line(img, (B4CX, B4CY), (S4CX, S4CY), (0, 255, 255), 2)
        # cv2.line(img, (S4CX - buffer, S4CY - buffer), (S4CX + buffer, S4CY - buffer), (255, 255, 0), 2)
        # cv2.line(img, (S4CX + buffer, S4CY - buffer), (S4CX + buffer, S4CY + buffer), (255, 255, 0), 2)
        # cv2.line(img, (S4CX + buffer, S4CY + buffer), (S4CX - buffer, S4CY + buffer), (255, 255, 0), 2)
        # cv2.line(img, (S4CX - buffer, S4CY + buffer), (S4CX - buffer, S4CY - buffer), (255, 255, 0), 2)

        cv2.line(img, (0, S4CY - buffer), (imgx, S4CY - buffer), (255, 255, 0), 2)
        cv2.line(img, (S4CX + buffer, 0), (S4CX + buffer, imgy), (255, 255, 0), 2)
        cv2.line(img, (imgx, S4CY + buffer), (0, S4CY + buffer), (255, 255, 0), 2)
        cv2.line(img, (S4CX - buffer, imgy), (S4CX - buffer, 0), (255, 255, 0), 2)

        if B4CX < S4CX - buffer and B4CY < S4CY - buffer:
            signal = "4H"  # Forward-Left
            sendSignal(signal)
            p = 6
            q = "BOT4"
            return p, q
        elif B4CX > S4CX + buffer and B4CY < S4CY - buffer:
            signal = "4G"  # Forward-Right
            sendSignal(signal)
            p = 6
            q = "BOT4"
            return p, q
        elif B4CX < S4CX - buffer and B4CY > S4CY + buffer:
            signal = "4J"  # Backward-Left
            sendSignal(signal)
            p = 6
            q = "BOT4"
            return p, q
        elif B4CX > S4CX + buffer and B4CY > S4CY + buffer:
            signal = "4I"  # Backward-Right
            sendSignal(signal)
            p = 6
            q = "BOT4"
            return p, q
        elif S4CX - buffer <= B4CX <= S4CX + buffer and B4CY < S4CY - buffer:
            signal = "4B"  # Forward
            sendSignal(signal)
            p = 6
            q = "BOT4"
            return p, q
        elif S4CX - buffer <= B4CX <= S4CX + buffer and B4CY > S4CY + buffer:
            signal = "4C"  # Backward
            sendSignal(signal)
            p = 6
            q = "BOT4"
            return p, q
        elif B4CX < S4CX - buffer and S4CY - buffer <= B4CY <= S4CY + buffer:
            signal = "4H"  # Forward-Left
            sendSignal(signal)
            p = 6
            return p, q
        elif B4CX > S4CX + buffer and S4CY - buffer <= B4CY <= S4CY + buffer:
            signal = "4G"  # Forward-Right
            sendSignal(signal)
            p = 6
            q = "BOT4"
            return p, q
        elif S4CX - buffer <= B4CX <= S4CX + buffer and S4CY - buffer <= B4CY <= S4CY + buffer:
            signal = "4A"  # Idle
            sendSignal(signal)
            p = 0
            q = "BOTend"
            return p, q




def findArucoMarkers(img, MarkerSize=5, totalMarkers=250, draw=True):
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    key = getattr(aruco, f'DICT_{MarkerSize}X{MarkerSize}_{totalMarkers}')
    arucoDict = aruco.Dictionary_get(key)
    arucoParam = aruco.DetectorParameters_create()
    corners, ids, rejected = aruco.detectMarkers(imgGray, arucoDict, parameters=arucoParam)
    # print(ids)
    # cv2.rectangle(imgGray, (10, 10), (100, 100), color=(255, 0, 0), thickness=3)

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
            storeB1(x, y, vx, vy)
        elif arg2 == "FKMP0002":
            storeB2(x, y, vx, vy)
        elif arg2 == "FKMP0003":
            storeB3(x, y, vx, vy)
        elif arg2 == "FKMP0004":
            storeB4(x, y, vx, vy)
        elif arg2 == "S1":
            storeS1(x, y, vx, vy)
        elif arg2 == "S2":
            storeS2(x, y, vx, vy)
        elif arg2 == "S3":
            storeS3(x, y, vx, vy)
        elif arg2 == "S4":
            storeS4(x, y, vx, vy)
        elif arg2 == "D1":
            storeD1(x, y, vx, vy)
        elif arg2 == "D2":
            storeD2(x, y, vx, vy)
        elif arg2 == "D3":
            storeD3(x, y, vx, vy)
        elif arg2 == "D4":
            storeD4(x, y, vx, vy)
        elif arg2 == "T1":
            storeT1(x, y, vx, vy)
        elif arg2 == "T2":
            storeT2(x, y, vx, vy)
        elif arg2 == "T3":
            storeT3(x, y, vx, vy)
        elif arg2 == "T4":
            storeT4(x, y, vx, vy)

        cv2.line(img, (int(c1[0]), int(c1[1])), (int(c2[0]), int(c2[1])), (0, 255, 0), 2)
        cv2.line(img, (int(c2[0]), int(c2[1])), (int(c3[0]), int(c3[1])), (0, 255, 0), 2)
        cv2.line(img, (int(c3[0]), int(c3[1])), (int(c4[0]), int(c4[1])), (0, 255, 0), 2)
        cv2.line(img, (int(c4[0]), int(c4[1])), (int(c1[0]), int(c1[1])), (0, 255, 0), 2)
        cv2.line(img, (x, y), (x + (int(v[0]) // 2), y + (int(v[1]) // 2)), (255, 0, 0), 2)
        img = cv2.putText(img, arg2, (x - 10, y + 20), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA)


VIDEO_TYPE = {
    'avi': cv2.VideoWriter_fourcc(*'XVID')
}


def get_video_type(filename):
    filename, ext = os.path.splitext(filename)
    if ext in VIDEO_TYPE:
        return VIDEO_TYPE[ext]
    return VIDEO_TYPE['avi']


def main():
    cap = cv2.VideoCapture(0)
    dims = get_dims(cap, res=my_res)
    video_type_cv2 = get_video_type(filename)

    p = 6
    operationNo = 6
    BOT = "BOT4"
    q = "BOT4"

    # rec = cv2.VideoWriter(filename,video_type_cv2, fps, dims)

    while True:
        success, img = cap.read()

        global imgx
        global imgy
        imgx = img.shape[1]
        imgy = img.shape[0]

        findArucoMarkers(img)

        if BOT == "BOT1":
            p, q = runLogicBOT1(img, p, operationNo, q)
        if BOT == "BOT2":
            p, q = runLogicBOT2(img, p, operationNo, q)
        if BOT == "BOT3":
            p, q = runLogicBOT3(img, p, operationNo, q)
        if BOT == "BOT4":
            p, q = runLogicBOT4(img, p, operationNo, q)
        if BOT == "BOTend":
            pass


        operationNo = p
        BOT = q

        # print(p, operationNo, BOT)

        # rec.write(img)
        cv2.imshow("Image", img)
        cv2.waitKey(1)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            # rec.release()
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
