import cv2
import numpy as np

# 실행2) 이미지와 꼭짓점 전달받아 그림
def draw_roi(image, corners):
    preview = image.copy()
    point_color = (192, 192, 255)
    line_color = (128, 128, 255)

    # 눈에 보이는 꼭짓점 4개 만들 for문
    for pt in corners:
        # 12: 반지름
        # -1: 안에 색상 채움
        cv2.circle(preview, tuple(pt.astype(int)), 12, point_color, -1)

    # 꼭짓점 연결할 선
    for i in range(4):
        # 현재 꼭짓점
        pt1 = tuple(corners[i].astype(int))
        # 다음 꼭짓점: 마지막 꼭짓점(i=3) 다음에는 첫 번째 꼭짓점(i=0)으로 돌아감
        pt2 = tuple(corners[(i+1) % 4].astype(int))
        cv2.line(preview, pt1, pt2, line_color, 2)

    # preview에 그렸으니 그 자체를 return 시켜 줌
    return preview

# 실행3) 마우스 이벤트 걸어줄거임
def on_mouse(event, x, y, flags, param):

    # 4. 로컬말고 글로벌 사용위해 등록(외부에꺼 가져다 쓰고 이 함수안에서 수정한것도 외부에 적용)
    global src_quad, drag_src

    # 1. 왼쪽버튼이 눌렸을 때: 꼭짓점에서 눌렀을때만 실행되도록
    if event == cv2.EVENT_LBUTTONDOWN:
        # 4개 꼭짓점 체크
        for i in range(4):
            # 거리구함: why? 꼭짓점 근처를 클릭했는지 확인하기 위함
            # norm(): 꼭짓점과 마우스 좌표 사이의 유클리드 거리(직선거리) 계산
            distance = cv2.norm(src_quad[i] - np.array([x, y], dtype=np.float32))
            # 마우스와 꼭짓점 사이 거리 확인 (20은 정하기 나름)
            if distance < 20:
                # 현재 i번째 꼭짓점을 드래그 중이라고 표시
                drag_src[i] = True
                # 선택할 꼭짓점을 찾음 / 더 이상 나머지 꼭짓점 확인X 반복문 종료
                break

    # 2. 버튼 누르고 움직이는 중
    elif event == cv2.EVENT_MOUSEMOVE:
        # 4개 꼭짓점 중 현재 잡고 있는 꼭짓점 찾기
        for i in range(4):
            # drag_src[i]가 True면 지금 꼭짓점 드래그 중이라는 뜻
            if drag_src[i]:

                # 마우스가 이미지 밖으로 나가더라도 꼭짓점 좌표는 이미지 안쪽 범위를 벗어나지 않도록 제한
                new_x = np.clip(x, 0, w-1)
                new_y = np.clip(y, 0, h-1)

                # 바뀐 꼭짓점 좌표 넣어줌
                src_quad[i] = (new_x, new_y)
                # 선도 다시 그림
                preview = draw_roi(img, src_quad)

                cv2.imshow('img', preview)
                break

    # 3. 마우스 드래그 종료
    elif event == cv2.EVENT_LBUTTONUP:
        # 모든 꼭짓점 '드래그 중이 아님(False)' 상태로 변경
        drag_src = [False, False, False, False]


# 실행1)
img = cv2.imread("./images/namecard.jpg")

# 높이, 너비 가져옴
h, w = img.shape[:2]

# 잘라서 보여줄 이미지 크기
dst_h = 500
dst_w = round(dst_h * 297 / 210) # 500의 비율대로 A4비율로 해달라

# 꼭짓점 4개 저장(왼쪽 위, 아래, 오른쪽 아래, 위)
src_quad = np.array([
    [30, 30],
    [30, h-30],
    [w-30, h-30],
    [w-30, 30]
], dtype=np.float32)

# 새로운 창에 대한 꼭짓점(순서 위랑 동일해야 함)
dst_quad = np.array([
    [0, 0],
    [0, dst_h-1],
    [dst_w-1, dst_h-1],
    [dst_w-1, 0]
], dtype=np.float32)

# 현재 내 꼭짓점이 드래그중인지 확인할 리스트
drag_src = [False, False, False, False]



# 실행2 위한 코드
display = draw_roi(img, src_quad)
cv2.imshow("img", display)

# 실행3 위한 코드
cv2.setMouseCallback("img", on_mouse)

print('네개의 꼭짓점을 드래그하여 영역을 맞추세요.')
print('Enter: 투시 변환')
print('ESC: 종료')

# 실행4) 키 입력 기다림
while True:
    key = cv2.waitKey(0)

    # ESC(27)를 누르면 프로그램 종료
    if key == 27:
        cv2.destroyAllWindows()
        raise SystemExit

    # Enter를 누르면 꼭짓점 선택을 끝내고 다음 단계로 이동
    elif key in (10, 13):
        break

# 행렬 얻음
# 내가 선택한 4개 꼭짓점을
# 새 이미지의 4개 꼭짓점으로 옮기기 위한 변환 행렬 계산
prespective_matrix = cv2.getPerspectiveTransform(src_quad, dst_quad)

# 위에서 계산한 변환 행렬을 실제 이미지에 적용
dst = cv2.warpPerspective(img, prespective_matrix, (dst_w, dst_h), flags=cv2.INTER_CUBIC)


cv2.imshow("perspective result", dst)


cv2.waitKey(0)
cv2.destroyAllWindows()