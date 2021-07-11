import cv2
import numpy as np
import cv2.aruco as aruco
import os

filename = 'Test.avi'
fps = 24.0
my_res = '720p'

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

def findArucoMarkers(img, MarkerSize=5, totalMarkers=250, draw=True):
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    key = getattr(aruco,f'DICT_{MarkerSize}X{MarkerSize}_{totalMarkers}')
    arucoDict = aruco.Dictionary_get(key)
    arucoParam = aruco.DetectorParameters_create()
    corners, ids, rejected = aruco.detectMarkers(imgGray, arucoDict, parameters=arucoParam)
    # print(ids)
    cv2.rectangle(imgGray, (10, 10), (100, 100), color=(255, 0, 0), thickness=3)

    if draw:
        aruco.drawDetectedMarkers(img,corners)

    for (i, b) in enumerate(corners):

        c1 = (b[0][0][0], b[0][0][1])
        c2 = (b[0][1][0], b[0][1][1])
        c3 = (b[0][2][0], b[0][2][1])
        c4 = (b[0][3][0], b[0][3][1])
        v = (int(c1[0])-int(c4[0]),int(c1[1])-int(c4[1]))
        x = int((c1[0] + c2[0] + c3[0] + c4[0]) / 4)
        y = int((c1[1] + c2[1] + c3[1] + c4[1]) / 4)



        print(ids[i],v)
        # print(c1)
        # print(c2)
        # print(c3)
        # print(c4)
        # print(v)

        arg1 = str(ids[i])
        arg2 = ids_rids(arg1)

        cv2.line(img, (int(c1[0]),int(c1[1])), (int(c2[0]),int(c2[1])), (0, 255, 0), 2)
        cv2.line(img, (int(c2[0]),int(c2[1])), (int(c3[0]),int(c3[1])), (0, 255, 0), 2)
        cv2.line(img, (int(c3[0]),int(c3[1])), (int(c4[0]),int(c4[1])), (0, 255, 0), 2)
        cv2.line(img, (int(c4[0]),int(c4[1])), (int(c1[0]),int(c1[1])), (0, 255, 0), 2)
        cv2.line(img,(x,y),(x+(int(v[0])//2),y+(int(v[1])//2)),(255,0,0),2)
        img = cv2.putText(img, arg2, (x+50, y), cv2.FONT_HERSHEY_COMPLEX,
                            0.5, (0, 0, 255), 1, cv2.LINE_AA)


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
        # rec.write(img)
        cv2.imshow("Image",img)
        cv2.waitKey(1)

        if cv2.waitKey(20) & 0xFF == ord('q'):
            rec.release()
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()