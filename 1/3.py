#! /usr/bin/env python3
import tkinter
gw = 64
gh = 64
cellsize = 8
def leftdown(e): # マウス左ボタンが押された時に呼ばれる関数
    print('L') # Lと出力します
def rightdown(e): # マウス右ボタンが押された時に呼ばれる関数
    print('R') # Rと出力します
root = tkinter.Tk()
root.resizable(width = False, height = False)
cv = tkinter.Canvas(root, width = cellsize * gw, height = cellsize * gh)
cv.pack()
cv.bind('<Button-1>', leftdown) # キャンバスの左クリックイベント登録
cv.bind('<Button-3>', rightdown) # キャンバスの右クリックイベント登録
root.mainloop()
