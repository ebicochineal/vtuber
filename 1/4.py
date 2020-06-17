#! /usr/bin/env python3
import tkinter
gw = 64
gh = 64
cellsize = 8
def leftdown(e):
    kx = (e.x-2) // cellsize
    ky = (e.y-2) // cellsize
    if kx < 0:
        kx = 0
    if kx > gw-1:
        kx = gw-1
    if ky < 0:
        ky = 0
    if ky > gh-1:
        ky = gh-1
    print((e.x, e.y), (kx, ky)) # キャンバス上の座標とグリッド上の座標の出力
def rightdown(e):
    print('R')
root = tkinter.Tk()
root.resizable(width = False, height = False)
cv = tkinter.Canvas(root, width = cellsize * gw, height = cellsize * gh)
cv.pack()
cv.bind('<Button-1>', leftdown)
cv.bind('<Button-3>', rightdown)
root.mainloop()
