"""
cv2.imread()
이미지 파일을 Numpy 배열 형태로 읽어오는 함수

cv2.IMREAD_GRAYSCALE
- 이미지를 그레이스케일로 읽어옴
- 배열의 형태는 (높이, 너비 : 기존이랑 다름) 순서로 읽어옴

cv2.IMREAD_COLOR
- 이미지를 컬러로 읽어옴(기본값)
- 배열의 형태는 (높이, 너비, 3(채널))가 됨
- openCV의 컬러 채널 순서는 BGR(RGB 역순)임



"""

import cv2
# 사진크기 548 * 364 * 3
img_gray = cv2.imread("./images/dog.bmp", cv2.IMREAD_GRAYSCALE)
img_color = cv2.imread("./images/dog.bmp", cv2.IMREAD_COLOR) # cv2.IMREAD.COLOR 생략가능

print('그레이스케일 이미지 배열: ')
print(img_gray)

print('컬러 이미지 배열: ')
print(img_color)

cv2.imshow('gray', img_gray)
cv2.imshow('color', img_color)

cv2.waitKey(0)
cv2.destroyAllWindows()
