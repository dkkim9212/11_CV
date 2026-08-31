import cv2
import sys

cap1 = cv2.VideoCapture(0)

if not cap1.isOpened():
    print('카메라를 열 수 없습니다.')
    sys.exit()

    
width = int(cap1.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap1.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap1.get(cv2.CAP_PROP_FPS)

print('너비 :', width)
print('높이 :', height)
print('FPS :', fps)

print(f'녹화시작: {width}x{height}, {fps:.1f}FPS')
print('ESC 키를 누르면 녹화를 종료합니다.')


delay = max(1, round(1000 / fps))
stop = False
filter_mode = 0

while True:
    ret, frame = cap1.read()
    
    if not ret:
        break

    display_frame = frame.copy()

    if filter_mode == 1:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        display_frame = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)

    elif filter_mode == 2:
        display_frame = cv2.GaussianBlur(frame, (15, 15), 0)

    elif filter_mode == 3:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        edge = cv2.Canny(gray, 100, 200)
        display_frame = cv2.cvtColor(edge, cv2.COLOR_GRAY2BGR)


    cv2.imshow('camera', display_frame)


    key = cv2.waitKey(1) & 0xFF


    if key == ord('1'):
        filter_mode = 0

    elif key == ord('2'):
        filter_mode = 1

    elif key == ord('3'):
        filter_mode = 2

    elif key == ord('4'):
        filter_mode = 3

    elif key == 27:
        break


cap1.release()
cv2.destroyAllWindows()