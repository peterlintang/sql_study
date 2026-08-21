import cv2

# 创建 MOG 背景减除器
mog = cv2.bgsegm.createBackgroundSubtractorMOG()

# 读取视频
cap = cv2.VideoCapture('rtsp://10.130.34.1:8554/live')

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # 应用背景减除
    fg_mask = mog.apply(frame)

    # 显示结果
    cv2.imshow('Frame', frame)
    cv2.imshow('FG Mask', fg_mask)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
