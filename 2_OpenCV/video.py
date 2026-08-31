import cv2
import sys

woman = cv2.VideoCapture("./movies/woman.mp4")
sea = cv2.VideoCapture("./movies/sea.mp4")

hsv = cv2.cvtColor(woman, cv2.COLOR_BGR2HSV)

if not woman.isOpened():
    print('동영상을 불러올 수 없습니다.')
    sys.exit()
if not sea.isOpened():
    print('동영상을 불러올 수 없습니다.')
    sys.exit()

print('동영상 로드 성공!')

width = int(woman.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(woman.get(cv2.CAP_PROP_FRAME_HEIGHT))
frame_count = int(woman.get(cv2.CAP_PROP_FRAME_COUNT))
fps = woman.get(cv2.CAP_PROP_FPS)

print('너비 :', width)
print('높이 :', height)
print('프레임 수 :', frame_count)
print('FPS :', fps)

width2 = int(sea.get(cv2.CAP_PROP_FRAME_WIDTH))
height2 = int(sea.get(cv2.CAP_PROP_FRAME_HEIGHT))
frame_count2 = int(sea.get(cv2.CAP_PROP_FRAME_COUNT))
fps2 = sea.get(cv2.CAP_PROP_FPS)



print('너비 :', width2)
print('높이 :', height2)
print('프레임 수 :', frame_count2)
print('FPS :', fps2)

lower_green = (40, 150, 0)
upper_green = (100, 255, 255)
green_mask = cv2.inRange(hsv, lower_green, upper_green)


fourcc = cv2.VideoWriter_fourcc(*"XVID")
out = cv2.VideoWriter("mix.avi", fourcc, fps, (width, height))

delay = max(1, round(1000 / fps)) if fps > 0 else 40

while True:
    ret, frame = woman.read()

    if not ret:
        break

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_green = (50, 150, 0)
    upper_green = (90, 255, 255)

    green_mask = cv2.inRange(hsv, lower_green, upper_green)

    cv2.imshow('frame', frame)
    cv2.imshow('green_mask', green_mask)

    if cv2.waitKey(30) == 27:
        break

while True:
    # ret : 프레임을 정상적으로 읽었는지 여부
    # frame : 읽어온 한 장의 영상 프레임(numpy 배열)
    ret, frame = woman.read()
    if not ret:
        break
    cv2.imshow("frame", frame)
    if cv2.waitKey(delay) == 27:
        break
while True:
    # ret : 프레임을 정상적으로 읽었는지 여부
    # frame : 읽어온 한 장의 영상 프레임(numpy 배열)
    ret, frame = sea.read()
    if not ret:
        break
    cv2.imshow("frame", frame)
    if cv2.waitKey(delay) == 27:
        break

green_mask.release()
cv2.destroyAllWindows()