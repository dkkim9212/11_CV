import cv2
import numpy as np

oldx = 0
oldy = 0

def on_mouse(event, x, y, flags, param):

    """
    event : 발생한 마우스 이벤트 종류 객체
    x, y : 현재 마우스 좌표
    flags : 마우스 버튼/키 상태
    param : setMouseCallback()에서 전달할 추가 데이터
    """

    global oldx, oldy

    if event == cv2.EVENT_LBUTTONDOWN:
        print(f'왼쪽 버튼 DOWN : ({x}, {y})')
        oldx, oldy = x,y
    elif event == cv2.EVENT_LBUTTONUP:
        print(f'왼쪽 버튼 UP: ({x}, {y})')
    elif event == cv2.EVENT_MOUSEMOVE:
        if flags & cv2.EVENT_FLAG_LBUTTON: 
            # flags에는 현재 눌린 마우스 버튼이나 키 상태가 여러 개 들어갈 수 있다.
            # &를 사용해서 그중 '왼쪽 마우스 버튼이 눌려 있는지'만 확인한다.
            # 눌려 있으면 0이 아닌 값(True), 안 눌려 있으면 0(False)이 된다.
            print(f'드래그 중: ({x}, {y})')
            cv2.line(img, (oldx, oldy), (x,y), (255, 51, 255), 3)
            oldx, oldy = x, y
            cv2.imshow("canvas", img)

img = np.full((500, 500, 3), 255, dtype=np.uint8)

cv2.rectangle(img, (50, 200), (200, 300), (0, 255, 0), 3)#(이미지, 좌측 상단 모서리 좌표, 우측 하단 모서리 좌표, 색상좌표, 두께)
cv2.rectangle(img, (300, 200), (400, 300), (0, 255, 0), -1)# 두께 -1 이면 내용이 채워 진다
cv2.circle(img, (150, 400), 50, (255, 0, 0), 3)
cv2.putText(img, "Hello", (50, 100), cv2.FONT_HERSHEY_SCRIPT_COMPLEX, 0.8, (0, 0, 0), 1)

cv2.imshow("canvas", img)
cv2.setMouseCallback("canvas", on_mouse)

cv2.waitKey(0)
cv2.destroyAllWindows()