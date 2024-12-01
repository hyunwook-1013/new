from tkinter import *
from tkinter.colorchooser import *
from tkinter.simpledialog import *

# 함수 선언 부분
def mouseClick(event):
    global x1, y1
    x1 = event.x
    y1 = event.y

def mouseDrop(event):
    global x1, y1, x2, y2, penWidth, penColor
    x2 = event.x
    y2 = event.y
    canvas.create_line(x1, y1, x2, y2, width=penWidth, fill=penColor)

def getColor():
    global penColor
    color = askcolor()[1]  # askcolor() returns a tuple, second element is the hex code of the color
    penColor = color

def getWidth():
    global penWidth
    penWidth = askinteger("선 두꼐", "선 두께(1~10)를 입력하세요.", minvalue=1, maxvalue=10)

# 전역 변수 선언 부분
window = None
canvas = None
x1, x2, y1, y2 = None, None, None, None  # 선의 시작점과 끝점
penColor = 'black'
penWidth = 5

# 메인 코드 부분
if __name__ == "__main__":
    window = Tk()
    window.title("그림판 비슷한 프로그램")
    
    # Canvas 생성
    canvas = Canvas(window, height=300, width=300)
    canvas.bind("<Button-1>", mouseClick)  # Fixed the event binding
    canvas.bind("<ButtonRelease-1>", mouseDrop)
    canvas.pack()

    # 메뉴 생성
    mainMenu = Menu(window)
    window.config(menu=mainMenu)
    fileMenu = Menu(mainMenu)
    
    # '설정' 메뉴 항목 추가
    mainMenu.add_cascade(label="설정", menu=fileMenu)
    fileMenu.add_command(label="선 색상 선택", command=getColor)
    fileMenu.add_separator()
    fileMenu.add_command(label="선 두께 설정", command=getWidth)
    
    # '보기' 메뉴 항목 추가 (설정 옆에 위치)
    mainMenu.add_cascade(label="보기")  # 보기 메뉴 추가

    window.mainloop()
