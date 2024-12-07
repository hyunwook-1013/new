# -*- coding: utf-8 -*-
"""
Created on Sat Dec  7 23:47:51 2024

@author: USER
"""

import cv2
import numpy as np
from tkinter import *
from tkinter.colorchooser import askcolor
from tkinter.simpledialog import askinteger
from PIL import Image, ImageTk

# 함수 선언 부분
def mouseClick(event):
    global x1, y1
    x1, y1 = event.x, event.y

def mouseDrag(event):
    global x1, y1, penWidth, penColor, img, penColor_rgb, eraserMode
    x2, y2 = event.x, event.y
    if eraserMode:
        # 지우개로 선을 삭제
        erase_size = penWidth
        canvas.create_rectangle(x2 - erase_size, y2 - erase_size, x2 + erase_size, y2 + erase_size, fill="white", outline="white")
        cv2.rectangle(img, (x2 - erase_size, y2 - erase_size), (x2 + erase_size, y2 + erase_size), (255, 255, 255), -1)
    else:
        canvas.create_line(x1, y1, x2, y2, width=penWidth, fill=penColor, capstyle=ROUND, smooth=True)
        cv2.line(img, (x1, y1), (x2, y2), penColor_rgb, thickness=penWidth)
    x1, y1 = x2, y2

def mouseDrop(event):
    global x1, y1
    x1, y1 = None, None

def fillColor(event):
    global img
    x, y = event.x, event.y
    # 클릭한 위치의 색상 가져오기
    target_color = img[y, x].tolist()
    # 색상 선택
    fill_color = askcolor()[0]
    if fill_color:
        fill_color_bgr = (int(fill_color[2]), int(fill_color[1]), int(fill_color[0]))
        # floodFill 적용
        mask = np.zeros((img.shape[0] + 2, img.shape[1] + 2), np.uint8)
        cv2.floodFill(img, mask, (x, y), fill_color_bgr, loDiff=(10, 10, 10), upDiff=(10, 10, 10))
        # canvas에 업데이트
        update_canvas()

def update_canvas():
    """OpenCV 이미지를 Tkinter Canvas로 업데이트"""
    global img, canvas_image
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_pil = Image.fromarray(img_rgb)
    img_tk = ImageTk.PhotoImage(img_pil)
    canvas.itemconfig(canvas_image, image=img_tk)
    canvas.img_tk = img_tk  # 참조 유지

def getColor():
    global penColor, penColor_rgb
    color = askcolor()  # 색상 선택
    penColor = color[1]  # tkinter 색상
    # OpenCV용 BGR 색상 변환
    r, g, b = color[0]
    penColor_rgb = (int(b), int(g), int(r))

def getWidth():
    global penWidth
    penWidth = askinteger("선 두께", "선 두께(1~10)를 입력하세요.", minvalue=1, maxvalue=10)

def toggle_eraser():
    global eraserMode
    eraserMode = not eraserMode
    if eraserMode:
        eraser_button.config(relief=RAISED, bg="lightgrey")
    else:
        eraser_button.config(relief=FLAT, bg="SystemButtonFace")

def show_magnifier(event):
    global magnifier_active, magnifier_image
    if not magnifier_active:
        return
    
    # 확대할 영역 설정
    x, y = event.x, event.y
    size = 50  # 돋보기 크기
    zoom_factor = 2

    # 확대할 영역 계산
    start_x = max(0, x - size // 2)
    start_y = max(0, y - size // 2)
    end_x = min(img.shape[1], x + size // 2)
    end_y = min(img.shape[0], y + size // 2)
    magnified_area = img[start_y:end_y, start_x:end_x]

    # 확대 후 이미지 표시
    magnified_resized = cv2.resize(magnified_area, (size * zoom_factor, size * zoom_factor), interpolation=cv2.INTER_LINEAR)
    magnified_rgb = cv2.cvtColor(magnified_resized, cv2.COLOR_BGR2RGB)
    magnified_pil = Image.fromarray(magnified_rgb)
    magnified_tk = ImageTk.PhotoImage(magnified_pil)

    if magnifier_image:
        canvas.delete(magnifier_image)
    magnifier_image = canvas.create_image(x + 10, y + 10, image=magnified_tk)
    canvas.magnifier_image = magnified_tk  # 참조 유지

def toggle_magnifier():
    global magnifier_active
    magnifier_active = not magnifier_active
    if magnifier_active:
        magnifier_button.config(relief=RAISED, bg="lightgrey")
    else:
        magnifier_button.config(relief=FLAT, bg="SystemButtonFace")

# 전역 변수 선언 부분
window = None
canvas = None
x1, y1 = None, None
penColor = 'black'
penColor_rgb = (0, 0, 0)
penWidth = 5
img = np.ones((300, 300, 3), dtype=np.uint8) * 255
eraserMode = False
magnifier_active = False
magnifier_image = None

# 메인 코드 부분
if __name__ == "__main__":
    window = Tk()
    window.title("OpenCV 기반 그림판")
    canvas = Canvas(window, height=300, width=300)
    canvas.pack()

    # 초기 OpenCV 이미지를 설정
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_pil = Image.fromarray(img_rgb)
    img_tk = ImageTk.PhotoImage(img_pil)
    canvas_image = canvas.create_image(0, 0, anchor=NW, image=img_tk)
    canvas.img_tk = img_tk

    # 마우스 이벤트 바인딩
    canvas.bind("<Button-1>", mouseClick)
    canvas.bind("<B1-Motion>", mouseDrag)
    canvas.bind("<ButtonRelease-1>", mouseDrop)
    canvas.bind("<Button-3>", fillColor)
    canvas.bind("<Motion>", show_magnifier)

    # 메뉴 설정
    mainMenu = Menu(window)
    window.config(menu=mainMenu)
    fileMenu = Menu(mainMenu)
    mainMenu.add_cascade(label="설정", menu=fileMenu)
    fileMenu.add_command(label="선 색상 선택", command=getColor)
    fileMenu.add_separator()
    fileMenu.add_command(label="선 두께 설정", command=getWidth)

    # 지우개 버튼 추가
    eraser_button = Button(window, text="지우개", command=toggle_eraser)
    eraser_button.pack(side=LEFT, padx=10)

    # 돋보기 버튼 추가
    magnifier_button = Button(window, text="돋보기", command=toggle_magnifier)
    magnifier_button.pack(side=LEFT, padx=10)

    window.mainloop()
