import cv2

"""
모폴로지(Morphology)
- 이미지의 모양을 다듬는 연산(줄이거나 늘리며)
- 주로 이진화된 이미지에서 흰색 영역 기준으로 처리함
    - 두껍게 만들거나, 얇게 만들거나, 작은 점 없애거나, 구멍 매우는 작업에 사용
- 작은 커널을 이미지 위에서 움직이며 흰색 영역의 모양 바꿈


1. 침식(Erosion)
- 흰색 영역을 깍아냄(흰색 ↓)
- 언제 사용? 작은 흰색 노이즈 제거
cv.erode()


2. 팽창(Dilation)
- 흰색 영역을 늘림(흰색 ↑)
- 언제 사용? 끊어진 부분 연결할 때(얇은거 두껍게 한다거나)


커널의 크기가 커지면 강한 효과를 낼 수 있음 (너무 크면 물체 사라지거나 서로 붙을수도 있음~)
"""

img = cv2.imread("./images/circuit.bmp", cv2.IMREAD_GRAYSCALE)

# getStructuringElement(): 모폴리지 연산에서 주변 픽셀을 어떤 모양으로 확인할지 결정
# MORPH_RECT(사각형-주로 사용) | MORPH_ELLIPSE(타원) | MORPH_CROSS(십자가)
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

# 침식
# iterations=1: 해당 연산을 1번 적용
eroded = cv2.erode(img, kernel, iterations=1)

# 팽창
dilated = cv2.dilate(img, kernel, iterations=1)

"""
3. 열림(Opening)
- 침식 → 팽창 순서
- 먼저 침식해서 작은 흰색 노이즈를 없앰
- 그 다음 팽창해서 남아있는 물체 크기를 어느 정도 복구(이미 제거된 노이즈는 살아나기 어려움)

- 언제 사용? 작은 흰색 노이즈를 제거하고 주요 객체 크기 복원


4. 닫힘(Closing)
- 팽창 → 침식 순서
- 먼저 팽창해서 작은 검은 구멍이나 끊어진 부분을 메움
- 그 다음 침식해서 커진 물체 크기를 어느 정도 복구(이미 메워진 작은 구멍은 다시 생기기 어려움)

- 언제 사용? 작은 검은 구멍제거, 끊어진 선 연결 후 주요 객체 크기 복원
"""

# 열림: 침식 → 팽창 / 작은 흰색 노이즈 제거
opened = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)

# 닫힘: 팽창 → 침식
closed = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)



cv2.imshow("Original", img)
cv2.imshow("Erosion", eroded)
cv2.imshow("Dilation", dilated)
cv2.imshow("Opened", opened)
cv2.imshow("Closed", closed)

cv2.waitKey(0)
cv2.destroyAllWindows()

