import cv2
import numpy as np
import os
import time

cap = cv2.VideoCapture(0)
NDIM=10000
media= np.ones([NDIM,480,640],dtype=np.uint8)
print(media.shape)

MAX_MATCHES = 2000
GOOD_MATCH_PERCENT = 0.5

WINDOW=100
media_movel_homography = np.zeros([1,WINDOW])

def alignImages(im1, im2):
    # Convert images to grayscale
    im1Gray = cv2.cvtColor(im1, cv2.COLOR_BGR2GRAY)
    im2Gray = cv2.cvtColor(im2, cv2.COLOR_BGR2GRAY)

    # Detect ORB features and compute descriptors.
    orb = cv2.ORB_create(MAX_MATCHES)
    keypoints1, descriptors1 = orb.detectAndCompute(im1Gray, None)
    keypoints2, descriptors2 = orb.detectAndCompute(im2Gray, None)

    # Match features.
    matcher = cv2.DescriptorMatcher_create(cv2.DESCRIPTOR_MATCHER_BRUTEFORCE_HAMMING)
    matches = matcher.match(descriptors1, descriptors2, None)

    # Sort matches by score
    matches.sort(key=lambda x: x.distance, reverse=False)

    # Remove not so good matches
    numGoodMatches = int(len(matches) * GOOD_MATCH_PERCENT)
    matches = matches[:numGoodMatches]
    #print(str(numGoodMatches))

    # Draw top matches
    #imMatches = cv2.drawMatches(im1, keypoints1, im2, keypoints2, matches, None)
    #cv2.imwrite("matches.jpg", imMatches)

    # Extract location of good matches
    points1 = np.zeros((len(matches), 2), dtype=np.float32)
    points2 = np.zeros((len(matches), 2), dtype=np.float32)

    for i, match in enumerate(matches):
        points1[i, :] = keypoints1[match.queryIdx].pt
        points2[i, :] = keypoints2[match.trainIdx].pt

    # Find homography
    try:
        h, mask = cv2.findHomography(points1, points2, cv2.RANSAC)
    except:
        h=0
        pass


    # Use homography
    height, width, channels = im2.shape
    try:
        im1Reg = cv2.warpPerspective(im1, h, (width, height))
        cv2.imshow('frame3', im1Reg)
    except:
        im1Reg=im1
        pass

    return im1Reg, h


def media_homography(new_value):
    global  media_movel_homography
    global WINDOW

    for n in range(WINDOW-1,1,-1):
        media_movel_homography[0,n]= media_movel_homography[0,n-1]

    media_movel_homography[0, 0] = new_value
    media_mov= np.sum(media_movel_homography)/6
    media_mov=np.std(media_movel_homography)


    return media_mov


while True:
    ret,frame = cap.read()
    #print(frame.shape)
    #gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

    #ret, frame = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

    # Read reference image
    refFilename = "Golden_ref_old.jpeg"
    #print("Reading reference image : ", refFilename)
    imReference = cv2.imread(refFilename, cv2.IMREAD_COLOR)

    # The estimated homography will be stored in h.
    imReg, h = alignImages(frame, imReference)

    try:
        res=media_homography(np.linalg.det(h))
        fonte = cv2.FONT_HERSHEY_SIMPLEX


        print(res)
        nome = str(res) + ".jpg"
        if (res > 0.05)  and (res < 0.15):
            cv2.putText(frame, "OK", (15, 65), fonte, 1, (255, 255, 255), 2, cv2.LINE_AA)
            cv2.imwrite(nome, change)
            cv2.imshow('frame3', change)
        else:
            cv2.putText(frame, "NOK", (15, 65), fonte, 1, (255, 255, 255), 2, cv2.LINE_AA)
    except:
        print("NULL homography")
        pass

    #fonte = cv2.FONT_HERSHEY_SIMPLEX
    #cv2.putText(frame,str(h), (15, 65), fonte, 0.3, (255, 255, 255), 2, cv2.LINE_AA)

    #cv2.imwrite("Golden_ref3.jpeg", frame)

    ref_gray = cv2.cvtColor(imReference, cv2.COLOR_BGR2GRAY)
    frame_gray2 = cv2.cvtColor(imReg, cv2.COLOR_BGR2GRAY)
    change = cv2.absdiff(ref_gray, frame_gray2)
    ret, change = cv2.threshold(change, 80, 255, cv2.THRESH_BINARY)
    mask = cv2.imread("mascara1.jpg", 0)

    nome=str(res)+".jpg"



    cv2.imshow('frame2', frame)
    #cv2.imshow('frame3', change)

    masked = cv2.multiply(change, (mask // 255))
    cv2.imshow('frame4', masked)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyALLWindows()