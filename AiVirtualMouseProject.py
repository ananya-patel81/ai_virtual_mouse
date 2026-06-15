import cv2
import numpy as np
import HandTrackingModule as htm
import time
import autopy
from pynput.mouse import Controller

# Initialize scroll controller
mouse = Controller()

# Settings
wCam, hCam = 640, 480
frameR = 100
smoothening = 7
scrollSpeed = 3

pTime = 0
plocX, plocY = 0, 0
clocX, clocY = 0, 0

prevScrollY = 0

# Camera
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

detector = htm.handDetector(maxHands=1)
wScr, hScr = autopy.screen.size()

while True:
    success, img = cap.read()
    if not success:
        continue

    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img)

    if len(lmList) != 0:

        x1, y1 = lmList[8][1:]   # index
        x2, y2 = lmList[12][1:]  # middle

        fingers = detector.fingersUp()

        cv2.rectangle(img, (frameR, frameR),
                      (wCam - frameR, hCam - frameR),
                      (255, 0, 255), 2)

        # 🖱️ Moving Mode (Index only)
        if fingers[1] == 1 and fingers[2] == 0:

            x3 = np.interp(x1, (frameR, wCam - frameR), (0, wScr))
            y3 = np.interp(y1, (frameR, hCam - frameR), (0, hScr))

            clocX = plocX + (x3 - plocX) / smoothening
            clocY = plocY + (y3 - plocY) / smoothening

            autopy.mouse.move(wScr - clocX, clocY)

            cv2.circle(img, (x1, y1), 15,
                       (255, 0, 255), cv2.FILLED)

            plocX, plocY = clocX, clocY

        # ✌️ Two Fingers Mode
        if fingers[1] == 1 and fingers[2] == 1:

            length, img, lineInfo = detector.findDistance(8, 12, img)

            # 👆 CLICK (fingers close)
            if length < 40:
                cv2.circle(img,
                           (lineInfo[4], lineInfo[5]),
                           15, (0, 255, 0), cv2.FILLED)
                autopy.mouse.click()

            # 🔽 SCROLL (fingers apart)
            else:
                y_avg = (y1 + y2) // 2

                if prevScrollY != 0:
                    diff = (y_avg - prevScrollY) / 5  # smoother scroll
                    mouse.scroll(0, -int(diff * scrollSpeed))

                prevScrollY = y_avg

        else:
            prevScrollY = 0  # reset when not scrolling

    # FPS display
    cTime = time.time()
    fps = 1 / (cTime - pTime) if (cTime - pTime) != 0 else 0
    pTime = cTime

    cv2.putText(img, str(int(fps)), (20, 50),
                cv2.FONT_HERSHEY_PLAIN, 3,
                (255, 0, 0), 3)

    cv2.imshow("AI Virtual Mouse", img)

    # Press ESC to exit
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()