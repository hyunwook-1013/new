# -*- coding: utf-8 -*-
"""
Created on Wed Dec  4 12:54:51 2024

@author: cic
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

def mouseDrop(event):
    global x1, y1, x2, y2, penWidth, penColor, img, eraserMode, drawn_lines
    x2, y2 = event.x, event.y
    if eraserMode:
        erase_area(x1, y1, x2, y2)  # 지우개 모드일 경우
    else:
        # 선을 그리고 Canvas에 그린 선의 ID를 리스트에 추가
        line_id = canvas.create_line(x1, y1, x2, y2, width=penWidth, fill=penColor)
        drawn_lines.append(line_id)  # 그린 선의 ID 저장

        cv2.line(img, (x1, y1), (x2, y2), penColor_rgb, thickness=penWidth)
    x1, y1 = x2, y2  # 다음 선을 위한 시작점으로 업데이트

def erase_area(x1, y1, x2, y2):
    global img, drawn_lines
    # 지우개 크기 설정
    eraser_size = penWidth  # 지우개 크기 (선 두께에 맞추기)
    # OpenCV 이미지에서 해당 영역을 흰색으로 덮어 씁니다.
    cv2.rectangle(img, (x1 - eraser_size // 2, y1 - eraser_size // 2), 
                  (x2 + eraser_size // 2, y2 + eraser_size // 2), (255, 255, 255), -1)
    
    # Canvas에서 선 삭제: drawn_lines에 저장된 선의 ID를 이용
    for line_id in drawn_lines[:]:
        bbox = canvas.bbox(line_id)  # 선의 bounding box를 구함
        if is_in_bbox(bbox, x1, y1, x2, y2):
            canvas.delete(line_id)  # 지우개 영역에 포함되면 해당 선을 삭제
            drawn_lines.remove(line_id)  # 삭제된 선의 ID를 리스트에서 제거

    update_canvas()

def is_in_bbox(bbox, x1, y1, x2, y2):
    """지우개 영역과 선의 bounding box가 겹치는지 확인"""
    bx1, by1, bx2, by2 = bbox
    return not (bx2 < x1 or bx1 > x2 or by2 < y1 or by1 > y2)

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
    # OpenCV 이미지를 RGB로 변환
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_pil = Image.fromarray(img_rgb)
    img_tk = ImageTk.PhotoImage(img_pil)
    canvas.itemconfig(canvas_image, image=img_tk)
    canvas.img_tk = img_tk  # 참조 유지

def toggle_eraser():
    global eraserMode
    eraserMode = not eraserMode
    if eraserMode:
        eraser_button.config(relief=RAISED, bg="lightgrey")  # 버튼이 눌려졌음을 나타냄
    else:
        eraser_button.config(relief=FLAT, bg="SystemButtonFace")  # 버튼이 눌리지 않음

# 전역 변수 선언 부분
window = None
canvas = None
x1, y1, x2, y2 = None, None, None, None  # 선의 시작점과 끝점
penColor = 'black'
penColor_rgb = (0, 0, 0)  # OpenCV용 BGR 색상
penWidth = 5
img = np.ones((300, 300, 3), dtype=np.uint8) * 255  # OpenCV 이미지 초기화 (흰색 배경)
eraserMode = False  # 지우개 모드
drawn_lines = []  # 그린 선들의 ID 저장

# 메인 코드 부분
if __name__ == "__main__":
    # Tkinter 윈도우 설정
    window = Tk()
    window.title("OpenCV 기반 그림판")
    canvas = Canvas(window, height=300, width=300)
    canvas.pack()

    # Canvas에 초기 OpenCV 이미지를 설정
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_pil = Image.fromarray(img_rgb)
    img_tk = ImageTk.PhotoImage(img_pil)
    canvas_image = canvas.create_image(0, 0, anchor=NW, image=img_tk)
    canvas.img_tk = img_tk  # 참조 유지

    # 마우스 이벤트 바인딩
    canvas.bind("<Button-1>", mouseClick)
    canvas.bind("<ButtonRelease-1>", mouseDrop)
    canvas.bind("<Button-3>", fillColor)

    # 메뉴 설정
    mainMenu = Menu(window)
    window.config(menu=mainMenu)
    fileMenu = Menu(mainMenu)
    mainMenu.add_cascade(label="설정", menu=fileMenu)
    fileMenu.add_command(label="선 색상 선택", command=getColor)
    fileMenu.add_separator()
    fileMenu.add_command(label="선 두께 설정", command=getWidth)
    mainMenu.add_cascade(label="보기")

    # 지우개 버튼 추가
    eraser_button = Button(window, text="지우개", command=toggle_eraser)
    eraser_button.pack(side=LEFT, padx=10)

    window.mainloop()
