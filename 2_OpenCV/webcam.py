import cv2
import sys
import os

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

print(f'녹화시작: {width}x{height}, {fps:.1f}FPS')#문구 바꾸기
print('ESC 키를 누르면 녹화를 종료합니다.')#문구 바꾸기



filter_mode = 0

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
)
register_mode = False
user_name = ""
save_count = 0
frame_count = 0
max_images = 120

while True:
    ret, frame = cap1.read()
    
    if not ret:
        break

    display_frame = frame.copy()

    gray_face = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(
        gray_face,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(50, 50)
    )
    if filter_mode == 1:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        display_frame = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)

    elif filter_mode == 2:
        display_frame = cv2.GaussianBlur(frame, (15, 15), 0)

    elif filter_mode == 3:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        edge = cv2.Canny(gray, 100, 200)
        display_frame = cv2.cvtColor(edge, cv2.COLOR_GRAY2BGR)

    for (x, y, w, h) in faces:

        face_roi = frame[y:y+h, x:x+w]

        cv2.rectangle(
            display_frame,
            (x, y),
            (x + w, y + h),
            (0, 255, 0),
            2
        )    
        face_resized = cv2.resize(face_roi, (224, 224))
        cv2.imshow("face", face_resized)

        if register_mode:

            frame_count += 1

            if frame_count % 5 == 0:
                file_name = f"{save_count:03d}.jpg"
                file_path = os.path.join(save_dir, file_name)
                cv2.imwrite(file_path, face_resized)
                save_count += 1
                if save_count >= max_images:
                    register_mode = False
                    print(f"{user_name} 얼굴 등록 완료: {save_count}장")
    
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

    elif key == ord('r'):
        user_name = input("등록할 이름을 입력하세요: ")
        save_dir = os.path.join("dataset", user_name)
        os.makedirs(save_dir, exist_ok=True)
        register_mode = True
        save_count = 0
        frame_count = 0

    elif key == 27:
        break


cap1.release()
cv2.destroyAllWindows()