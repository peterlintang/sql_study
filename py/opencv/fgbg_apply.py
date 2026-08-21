import cv2

# 读取视频
cap = cv2.VideoCapture('rtsp://10.130.34.1:8554/live')

# 创建 MOG2 背景减除器
fgbg = cv2.createBackgroundSubtractorMOG2()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # 应用背景减除器
    fgmask = fgbg.apply(frame)

    # 显示结果
    cv2.imshow("MOG2 Background Subtraction", fgmask)

    # 按下 'q' 键退出
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 释放资源
cap.release()
cv2.destroyAllWindows()
