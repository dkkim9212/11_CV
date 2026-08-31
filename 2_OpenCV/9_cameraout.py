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

fourcc = cv2.VideoWriter_fourcc(*"XVID")
out = cv2.VideoWriter("camera.avi", fourcc, fps, (width, height))


print(f'녹화시작: {width}x{height}, {fps:.1f}FPS')
print('ESC 키를 누르면 녹화를 종료합니다.')


delay = max(1, round(1000 / fps))
stop = False


while True:
    ret, frame = cap1.read()
    if not ret:
        break
    if frame.shape[1] != width or frame.shape[0] != height:
        frame = cv2.resize(frame, (width, height))
    out.write(frame)
    cv2.imshow('camera', frame)
    if cv2.waitKey(delay) == 27:
        break




cap1.release()
cv2.destroyAllWindows()