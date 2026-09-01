import cv2
import numpy as np


img = cv2.imread("./images/namecard.jpg")
start_x = 0
start_y = 0
is_dragging = False
color = (255, 0, 0) 

dst_w = 600
dst_h = 400

# 네 점의 순서는 왼쪽 위 > 오른쪽 위 > 오른쪽 아래 > 왼쪽 아래
src_quad = np.array([
    [26, 18],
    [718, 15],
    [720, 827],
    [25, 829]
], dtype=np.float32)

dst_quad = np.array([
    [0, 0],
    [dst_w -1, 0],
    [dst_w -1, dst_h -1],
    [0, dst_h-1]
], dtype=np.float32)

perspective_matrix = cv2.getPerspectiveTransform(src_quad, dst_quad)
print(perspective_matrix)

dst = cv2.warpPerspective(img, perspective_matrix, (dst_w, dst_h))



def on_mouse(event, x, y, flags, param):

    global start_x, start_y, is_dragging
    preview = img.copy()
    dst_w = 600
    dst_h = 400
    src_quad = np.array([
        [26, 18],
        [718, 15],
        [720, 827],
        [25, 829]
    ], dtype=np.float32)

    dst_quad = np.array([
        [0, 0],
        [dst_w -1, 0],
        [dst_w -1, dst_h -1],
        [0, dst_h-1]
    ], dtype=np.float32)
    
    for pt in src_quad.astype(int):
        cv2.circle(preview, tuple(pt), 8, (0,0,255), -1)
    cv2.polylines(preview, [src_quad.astype(np.int32)], True, (0, 255, 0), 3)
    cv2.imshow("img", preview)

    if event == cv2.EVENT_LBUTTONDOWN:
        is_dragging = True
        start_x = x
        start_y = y

    elif event == cv2.EVENT_MOUSEMOVE and is_dragging:
    
        cv2.imshow("img", preview)

    elif event == cv2.EVENT_LBUTTONUP and is_dragging:
        is_dragging = False
        x1 = min(start_x, x)
        y1 = min(start_y, y)
        x2 = max(start_x, x)
        y2 = max(start_y, y)
        w = x2 - x1
        h = y2 - y1

        if w<= 0 or h<= 0:
            cv2.imshow("img", img)
            print("영역이 설정되지 않았습니다.")
            return
        roi = img[y1:y2, x1:x2]
        selected = img.copy()
        cv2.rectangle(selected, (x1,y1), (x2,y2), color, 2)
        cv2.imshow("img", selected)
        cv2.imshow("roi", roi)
        print(f"ROI 위치: x={x1}, y={y1}, w={w}, h={h}")






cv2.imshow("img", img)

cv2.setMouseCallback("img", on_mouse)

cv2.waitKey(0)
cv2.destroyAllWindows()