import cv2
import matplotlib.pyplot as plt
import numpy as np

# img = cv2.imread("./images/dog.bmp") # 블러 개념욕 확인
# img = cv2.imread("./images/gaussian_noise.jpg") # 노이즈 제거되는거 확인
img = cv2.imread("./images/noise.bmp") # 너무 심하게 소금후투가 들어간 경우
# 소금 후추: 노이즈 많은거 말함


# matplotlib 찍기위해 변환
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

cv2.imshow("original", img)


"""
블러링
- 픽셀 주변의 픽셀들을 같이 보고 새로운 픽셀 값을 결정하는 것

사용하는 이유:
- 컴퓨터 비전에서 노이즈나 작은 디테일 줄이기 위한 전처리
- 
"""

"""
1. 평균 블러 (주변 픽셀의 평균값 사용)
- 현재 픽셀 주변의 값을 모두 더한 다음 평균을 구함(예 7*7)
- 가장 단순하게 모든걸 흐리게 함

cv2.blur(입력 이미지, 커널 크기, 결과 저장할 배열, 커널의 기준점, 이미지 가장자리 처리 방법)

> 중요한 경계와 노이즈를 구별하지 않아 실무에선 쓰는일이 잘 없음
"""
# 뒤엔 생략 = 기본값
mean_blur = cv2.blur(img, (7,7))

cv2.imshow("mean blur", mean_blur)

"""
2. 가우시안 블러 (가까운 픽셀에 더 큰 가중치)
- 중앙에서 멀어질수록 가중치를 작게 만드는 방식
- 자연스럽게 흐려지고 노이즈 제거에 많이 사용함

> MeanBlur보다 GaussianBlur를 더 많이 사용함

:: 이거 코드는 수업시간에 안씀, 설명만 하셨음
:: Canny전에 잠깐 사용함
"""


"""
3. Bilateral Filter(양방향 필터) - 경계선 유지!
- 공간적으로 가까운지, 픽셀의 색상과 밝기가 비슷한지 확인
- 가까운데 색이 비슷하면 블러링 많이 반영
- 가깝지만 색이 매우 다르면 블러링 적게 반영(덜 뿌옇게 만든다는 뜻)

cv2.bilateralFilter(이미지, 지름, 시그마 컬러, 시그마 스페이스)
- 지름: 주변 영역 크기
- 시그마 컬러: 픽셀값 or 색상 차이를 얼마나 허용할지 결정
    - 값 작으면 비슷한 색만 섞음
    - 값 크면 색 다른 픽셀도 더 많이 섞일 수 있음
- 시그마 스페이스: 공간적으로 얼마나 떨어진 픽셀까지 영향줄지 결정
    - 값 크면 더 멀리있는 픽셀까지 고려


> 노이즈는 줄이고 경계선 살리고 싶을 때 사용
> 일반적인 블러링보다 연산량많아 속도 느림
> 근데 우리가 사용하기 좋다고 강사님이 말씀하심~
"""
bilateral_blur = cv2.bilateralFilter(img, 12, 100, 100)
cv2.imshow("bilateral blur", bilateral_blur)


"""
4. Canny Edge Detection
- Edge : 픽셀값이 급격하게 변하는 위치
- 컬러 이미지를 그레이스케일로 변환 > 밝기가 갑자기 변화하는 위치 찾는 알고리즘
- 이미지 밝기의 중앙값 기준으로 threshold 정하는 휴리스틱(경험적 방법)을 통해 Canny threshold를 조절 or 다른 방법으로 threshold를 결정하는 경우가 많음(lower, upper)

> 최소 임계값보다 작으면 → 경계선 X
> 최대 임계값보다 크면 → 확실한 경계선
> 두 값 사이면 → 주변 경계선과 연결되어 있는지 확인해서 결정

cv2.Canny(이미지, 최소 임계값, 최대 임계값, 커널 크기)
"""

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
median_value = np.median(gray)              # 흑백이미지 전체 픽셀 밝기 중앙값 구함
lower = int(max(0, 0.7 * median_value))     # 중앙감 70%를 최소 임겨값 (조정 가능)
upper = int(min(255, 1.3* median_value))    # 중앙값 130%를 최대 입계값 (조정 가능)

print("Canny lower threshold:", lower)
print("Canny upper threshold:", upper)

# Canny 전 가볍게 가우시안블러 적용해 잡음 영향 줄임
edge_input = cv2.GaussianBlur(gray, (3, 3), 0)
cv2.imshow("Gaussian Blur", edge_input)

canny_edge = cv2.Canny(edge_input, lower, upper, 3)
cv2.imshow("canny edge", canny_edge)



"""
5. 직접 평균 커널 만들기
filter2D()를 사용해 사용자가 직접 만든 커널 적용가능
"""
plt.figure(figsize=(10, 5))
for i, k in enumerate([5, 7, 9]):
    kernel = np.ones((k, k), dtype=np.float32) / (k * k)
    # -1: 출력 영상의 데이터 타입을 입력 영상과 같게 유지
    filtered = cv2.filter2D(img_rgb, -1, kernel)

    plt.subplot(1, 3, i+1)
    plt.imshow(filtered)
    plt.title(f'kernel size: {k} x {k}')
    plt.axis('off')
plt.tight_layout()
plt.show()


cv2.waitKey(0)
cv2.destroyAllWindows()