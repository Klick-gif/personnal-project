import pyautogui
import cv2
import time
import webbrowser
import sys
import os

def click_image(image_path, confidence = 0.8):
    """
    尝试点击屏幕上显示的指定图像

    :param image_path: 要查找并点击图像文件的路径
    :param confidence: 图像匹配的置信度阈值，默认为0.8. 范围是0-1，值最高匹配越严格

    :return:
        bool: 如果成功找到并点击了图像，则返回True，否则返回False。
    """
    try:
        # 尝试在屏幕定位指定的图像
        image_location = pyautogui.locateOnScreen(image_path, confidence=confidence)
        # 如果找到了图像位置
        if image_location:
            # 点击图像所在位置
            pyautogui.click(image_location)
            return True
        else:
            # 如果没找到图像，则返回False
            return False
    except pyautogui.ImageNotFoundException:
        # 如果图像未找到，则捕获ImageNotFoundException 异常并返回False
        return False
l = input("请输入开始：")

print("程序已经开始,请打开学习通点开劳动教育观视频等待！")

while True:
    if click_image("over.png"):
        print("over")
        if click_image("zjmw2.png"):
            print("视频播放结束")
            # 关机
            # os.system("shutdown -s -t  60 ")
            sys.exit()
        time.sleep(1)
        pyautogui.scroll(-1000)  # 鼠标向下滚1000个单位
        time.sleep(1)
        if click_image("last3.png"):
            click_image("last3.png")
            print("下一节")
            time.sleep(2)
    elif click_image("bf2.png"):
        click_image("bf2.png")
    elif click_image("cbf2.png"):
        click_image("cbf2.png")
    elif click_image("zjcs.png"):
        while True:
            pyautogui.scroll(-2000)  # 鼠标向下滚1000个单位
            time.sleep(1)
            if click_image("last3.png"):
                click_image("last3.png")
                time.sleep(1)
                click_image("last3.png")
                time.sleep(1)
                click_image("last3.png")
                break



    else:
        continue

