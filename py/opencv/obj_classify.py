import cv2
import numpy as np

# 加载目标图像和模板图像
img = cv2.imread('target_image.jpg', 0)
template = cv2.imread('template_image.jpg', 0)

# 获取模板图像的尺寸
w, h = template.shape[::-1]

# 进行模板匹配
res = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)

# 设置匹配阈值
threshold = 0.8

# 找到匹配位置
loc = np.where(res >= threshold)

# 在目标图像中标记匹配位置
for pt in zip(*loc[::-1]):
    cv2.rectangle(img, pt, (pt[0] + w, pt[1] + h), (0, 255, 0), 2)

# 显示结果图像
cv2.imshow('Matched Image', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
