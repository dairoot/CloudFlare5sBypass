import random
from datetime import datetime

import cv2
import pytesseract


def get_click_xy(image_path):
    image = cv2.imread(image_path)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150)

    # 查找轮廓
    contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # 设置轮廓的最小和最大面积
    min_area = 10000
    max_area = 100000

    contour_xy = set()
    scontour_xy = set()
    click_xy = set()

    # 遍历所有轮廓并绘制矩形框
    for contour in contours:
        area = cv2.contourArea(contour)
        if min_area < area < max_area:
            x, y, w, h = cv2.boundingRect(contour)
            roi = gray[y : y + h, x : x + w]  # 提取轮廓区域
            text = pytesseract.image_to_string(roi)  #
            if "verify you are human" in text.lower():  # 检查是否包含目标文本
                # print("text", x, y, w, h , text)
                x, y, w, h = cv2.boundingRect(contour)
                roi = gray[y : y + h, x : x + w]  # 提取大轮廓区域

                # 在大轮廓区域内再次进行边缘检测和小轮廓查找
                roi_edges = cv2.Canny(roi, 50, 150)
                small_contours, _ = cv2.findContours(roi_edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

                # 判断是否存在按钮
                for small_contour in small_contours:
                    small_area = cv2.contourArea(small_contour)
                    if 500 < small_area < 5000:  # 小轮廓的面积范围
                        sx, sy, sw, sh = cv2.boundingRect(small_contour)
                        # print("texts", sx, sy, sw, sh)
                        scontour_xy.add((x + sx, y + sy, sw, sh))  # 小轮廓
                        contour_xy.add((x, y, w, h))  # 大轮廓轮廓

    for x, y, w, h in contour_xy.union(scontour_xy):
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

    for x, y, w, h in contour_xy:
        # 大轮廓中寻找点击位置（点击位置可在小轮廓外层）
        click_x = x + random.randint(int(w * 0.05), int(w * 0.2))
        click_y = y + random.randint(int(h * 0.47), int(h * 0.53))
        cv2.circle(image, (click_x, click_y), 5, (0, 0, 255), -1)
        click_xy.add((click_x, click_y))
        cv2.imwrite(image_path + ".click.png", image)  # 保存图片

    # # 使用Tesseract进行OCR识别
    # text = pytesseract.image_to_string(gray)
    #
    # # 显示图像
    # cv2.imshow('Detected Components', image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    return click_xy
