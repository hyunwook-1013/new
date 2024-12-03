from tkinter.colorchooser import askcolor
from tkinter.simpledialog import askinteger
from tkinter import Tk, Canvas, Menu, Button

# 함수 선언 부분
def mouseClick(event):
    global x1, y1
    x1 = event.x
    y1 = event.y

def mouseDrop(event):
    global x1, y1, x2, y2, penWidth, penColor, eraserMode
    x2 = event.x
    y2 = event.y
    color = 'white' if eraserMode else penColor  # 지우개 모드일 때는 흰색으로 그리기
    canvas.create_line(x1, y1, x2, y2, width=penWidth, fill=color)

def getColor():
    global penColor, eraserMode
    if eraserMode:
        toggleEraser()  # 지우개 모드 비활성화
    color = askcolor()
    if color[1]:  # 색상이 선택된 경우만 적용
        penColor = color[1]

def getWidth():
    global penWidth
    width = askinteger("선 두께", "선 두께(1~10)를 입력하세요.", minvalue=1, maxvalue=10)
    if width:  # 취소를 누르지 않은 경우만 적용
        penWidth = width

def toggleEraser():
    global eraserMode, eraserButton
    eraserMode = not eraserMode
    if eraserMode:
        eraserButton.config(text="펜")
    else:
        eraserButton.config(text="지우개")

# 전역 변수 선언 부분
window = None
canvas = None
x1, y1, x2, y2 = None, None, None, None  # 선의 시작점과 끝점
penColor = 'black'
penWidth = 5
eraserMode = False  # 지우개 모드 초기 상태

# 메인 코드 부분
if __name__ == "__main__":
    window = Tk()
    window.title("그림판 비슷한 프로그램")

    # 캔버스 생성
    canvas = Canvas(window, height=300, width=300, bg='white')  # 배경색을 흰색으로 설정
    canvas.bind("<Button-1>", mouseClick)
    canvas.bind("<ButtonRelease-1>", mouseDrop)
    canvas.pack()

    # 메뉴 생성
    mainMenu = Menu(window)
    window.config(menu=mainMenu)
    fileMenu = Menu(mainMenu)
    mainMenu.add_cascade(label="설정", menu=fileMenu)
    fileMenu.add_command(label="선 색상 선택", command=getColor)
    fileMenu.add_separator()
    fileMenu.add_command(label="선 두께 설정", command=getWidth)
    
    # '보기' 메뉴 항목 추가 (설정 옆에 위치)
    mainMenu.add_cascade(label="보기")  # 보기 메뉴 추가

     # 지우개 버튼 추가
    eraserButton = Button(window, text="지우개", command=toggleEraser)
    eraserButton.pack(side='left', pady=5)
   

    window.mainloop()
