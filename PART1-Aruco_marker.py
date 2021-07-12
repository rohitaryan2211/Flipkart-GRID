import cv2
import numpy as np
import cv2.aruco as aruco
import os

filename = 'Test.avi'
fps = 24.0
my_res = '720p'
BOT = "BOT1"
p = 0


B1CX = 0
B1CY = 0
B1CVx = 0
B1CVy = 0
B2CX = 1
B2CY = 1
B2CVx = 1
B2CVy = 1
B3CX = 2
B3CY = 2
B3CVx = 2
B3CVy = 2
B4CX = 3
B4CY = 3
B4CVx = 3
B4CVy = 3
S1CX = 4
S1CY = 4
S1CVx = 4
S1CVy = 4
S2CX = 5
S2CY = 5
S2CVx = 5
S2CVy = 5
S3CX = 6
S3CY = 6
S3CVx = 6
S3CVy = 6
S4CX = 7
S4CY = 7
S4CVx = 7
S4CVy = 7
D1CX = 8
D1CY = 8
D1CVx = 8
D1CVy = 8
D2CX = 9
D2CY = 9
D2CVx = 9
D2CVy = 9
D3CX = 10
D3CY = 10
D3CVx = 10
D3CVy = 10
D4CX = 11
D4CY = 11
D4CVx = 11
D4CVy = 11
T1CX = 12
T1CY = 12
T1CVx = 12
T1CVy = 12
T2CX = 13
T2CY = 13
T2CVx = 13
T2CVy = 13
T3CX = 14
T3CY = 14
T3CVx = 14
T3CVy = 14
T4CX = 15
T4CY = 15
T4CVx = 15
T4CVy = 15
signal = "00"
buffer = 10




def change_res(cap, width, height):
    cap.set(3,width)
    cap.set(4,height)

STD_Dim = {
    "480p": (640,480),
    "720p": (1280,720),
    "1080p": (1920,1080),
    "4k": (3840,2160),
}

def get_dims(cap, res='720p'):
    width, height = STD_Dim['480p']
    if res in STD_Dim:
        width, height = STD_Dim[res]
    change_res(cap, width,height)
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
    B1CX = x                    #x-value of B1 center
    B1CY = y                    #y-value of B1 center
    B1CVx = vx                  #x-value of B1 vector
    B1CVy = vy                  #y-value of B1 vector
    B1C = (x, y)                #B1 center tuple
    B1V = (vx, vy)              #B1 vector tuple
    # print(B1CVx, B1CVy)

def storeB2(x, y, vx, vy):
    global B2CX
    global B2CY
    global B2CVx
    global B2CVy
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
    T4CX = x
    T4CY = y
    T4CVx = vx
    T4CVy = vy
    T4C = (x, y)
    T4V = (vx, vy)

def sendSignal(signal):
    print(signal)


def runLogicBOT1(img, p):


    if(p == 0):                             ###BOT1 moving forward towards T1

        cv2.line(img, (B1CX, B1CY), (T1CX, T1CY), (0, 255, 255), 2)
        cv2.line(img, (T1CX-buffer, T1CY-buffer), (T1CX+buffer, T1CY-buffer), (255, 255, 0), 2)
        cv2.line(img, (T1CX+buffer, T1CY-buffer), (T1CX+buffer, T1CY+buffer), (255, 255, 0), 2)
        cv2.line(img, (T1CX+buffer, T1CY+buffer), (T1CX-buffer, T1CY+buffer), (255, 255, 0), 2)
        cv2.line(img, (T1CX-buffer, T1CY+buffer), (T1CX-buffer, T1CY-buffer), (255, 255, 0), 2)


        if(B1CX < T1CX-buffer and B1CY < T1CY-buffer):
            signal = "1H"                     #Forward-Left
            sendSignal(signal)
        elif(B1CX > T1CX+buffer and B1CY < T1CY-buffer):
            signal = "1G"                     #Forward-Right
            sendSignal(signal)
        elif(B1CX < T1CX-buffer and B1CY > T1CY+buffer):
            signal = "1J"                     #Backward-Left
            sendSignal(signal)
        elif(B1CX > T1CX+buffer and B1CY > T1CY+buffer):
            signal = "1I"                     #Backward-Right
            sendSignal(signal)
        elif (B1CX > T1CX-buffer and B1CX < T1CX+buffer and B1CY < T1CY-buffer):
            signal = "1B"                     #Forward
            sendSignal(signal)
        elif (B1CX > T1CX-buffer and B1CX < T1CX+buffer and B1CY > T1CY+buffer):
            signal = "1C"                     #Backward
            sendSignal(signal)
        elif (B1CX < T1CX-buffer and B1CY > T1CY-buffer and B1CY < T1CY+buffer):
            signal = "1J"
            sendSignal(signal)
        elif (B1CX > T1CX+buffer and B1CY > T1CY-buffer and B1CY < T1CY+buffer):
            signal = "1I"
            sendSignal(signal)
        elif(B1CX > T1CX-buffer and B1CX < T1CX+buffer and B1CY > T1CY-buffer and B1CY < T1CY+buffer):
            signal = "1A"                    #Idle
            sendSignal(signal)




    # elif(a==1):                             ###BOT1 moving turning at T1
    #     if():




def findArucoMarkers(img, MarkerSize=5, totalMarkers=250, draw=True):
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    key = getattr(aruco, f'DICT_{MarkerSize}X{MarkerSize}_{totalMarkers}')
    arucoDict = aruco.Dictionary_get(key)
    arucoParam = aruco.DetectorParameters_create()
    corners, ids, rejected = aruco.detectMarkers(imgGray, arucoDict, parameters=arucoParam)
    # print(ids)
    cv2.rectangle(imgGray, (10, 10), (100, 100), color=(255, 0, 0), thickness=3)

    if draw:
        aruco.drawDetectedMarkers(img, corners)

    for (i, b) in enumerate(corners):

        c1 = (b[0][0][0], b[0][0][1])
        c2 = (b[0][1][0], b[0][1][1])
        c3 = (b[0][2][0], b[0][2][1])
        c4 = (b[0][3][0], b[0][3][1])
        v = (int(c1[0])-int(c4[0]), int(c1[1])-int(c4[1]))
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
        cv2.line(img, (x, y), (x+(int(v[0])//2), y+(int(v[1])//2)), (255, 0, 0), 2)
        img = cv2.putText(img, arg2, (x-10, y+20), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA)




VIDEO_TYPE = {
    'avi': cv2.VideoWriter_fourcc(*'XVID')
}

def get_video_type(filename):
    filename,ext = os.path.splitext(filename)
    if ext in VIDEO_TYPE:
        return VIDEO_TYPE[ext]
    return VIDEO_TYPE['avi']



def main():
    cap = cv2.VideoCapture(0)
    dims = get_dims(cap, res= my_res)
    video_type_cv2 = get_video_type(filename)


    # rec = cv2.VideoWriter(filename,video_type_cv2, fps, dims)

    while True:
        success, img = cap.read()
        findArucoMarkers(img)

        if BOT == "BOT1":
            runLogicBOT1(img, p)

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