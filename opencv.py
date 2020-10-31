import cv2
import keyboard

############### Tracker Types #####################

tracker = cv2.TrackerBoosting_create()
# tracker = cv2.TrackerMIL_create()
# tracker = cv2.TrackerKCF_create()
# tracker = cv2.TrackerTLD_create()
# tracker = cv2.TrackerMedianFlow_create()
# tracker = cv2.TrackerCSRT_create()
# tracker = cv2.TrackerMOSSE_create()

########################################################

cap = cv2.VideoCapture(0)
# TRACKER INITIALIZATION

success, frame = cap.read()
bbox = cv2.selectROI("Tracking", frame, False)
tracker.init(frame, bbox)
cur_x = 0
cur_y = 0


def key_presser(img, a, b):

    global cur_x, cur_y
    print(f"{a} {b}----{cur_x} {cur_y}")
    print(f"{a} {b}")

    while cur_x < a:
        keyboard.press("left")
        cur_x += 1
        print("x+")
    while cur_x > a:
        keyboard.press("right")
        cur_x -= 1
        print("x-")
    if b == 1:
        print("down")
        keyboard.press("down")
    if b == -1:
        print("up")
        keyboard.press("up")
    cur_x = 0






def drawBox(img, bbox):
    x, y, w, h = int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])
    cv2.rectangle(img, (x, y), ((x + w), (y + h)), (255, 0, 255), 3, 3)
    p = x + (int(w/2))
    q = y + int(h/2)

    a = 0
    b = 0
    if p >= 0 and p <= 213:
        a = -1
    elif p>213 and p<= 2*213:
        a = 0
    else:
        a = 1

    if q>=0 and q<= 160:
        b = -1
    elif q>160 and q <= 2*160:
        b = 0
    else:
        b = 1

    cv2.putText(img, f"position:{a} {b}", (450, 400), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 255), 2)
    key_presser(img, a, b)

    cv2.rectangle(img, (0, 0), (213, 160), (0, 0, 255), 1, 1)
    cv2.rectangle(img, (213, 0), (2*213, 160), (0, 0, 255), 1, 1)
    cv2.rectangle(img, (2*213, 0), (3*213, 160), (0, 0, 255), 1, 1)

    cv2.rectangle(img, (0, 160), (213, 2*160), (0, 0, 255), 1, 1)
    cv2.rectangle(img, (213, 1*160), (2 * 213, 2*160), (0, 0, 255), 1, 1)
    cv2.rectangle(img, (2 * 213, 1*160), (3 * 213, 2*160), (0, 0, 255), 1, 1)

    cv2.rectangle(img, (0, 2*160), (213, 3*160), (0, 0, 255), 1, 1)
    cv2.rectangle(img, (213, 2*160), (2 * 213, 3*160), (0, 0, 255), 1, 1)
    cv2.rectangle(img, (2 * 213, 2*160), (3 * 213, 3*160), (0, 0, 255), 1, 1)
    cv2.putText(img, f"position:{x+int(w/2)} {y+int(h/2)}", (50, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 255), 2);

    cv2.circle(img, (x+int(w/2), y+int(h/2)), 10, (255, 255, 0), thickness=10, lineType=8, shift=0)
    cv2.putText(img, "Tracking", (100, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)


while True:

    timer = cv2.getTickCount()
    success, img = cap.read()
    success, bbox = tracker.update(img)

    if success:
        drawBox(img, bbox)
    else:
        cv2.putText(img, "Lost", (100, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    cv2.rectangle(img, (15,15), (200,90), (255,0,255), 2)
    cv2.putText(img, "Fps:", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 255), 2)
    cv2.putText(img, "Status:", (20, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 255), 2)

    fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)
    if fps > 60:
        myColor = (20, 230, 20)
    elif fps > 20:
        myColor = (230, 20, 20)
    else:
        myColor = (20, 20, 230)
    cv2.putText(img, str(int(fps)), (75, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, myColor, 2);

    cv2.imshow("Tracking", img)
    if cv2.waitKey(1) and 0xff == ord('q'):
        break