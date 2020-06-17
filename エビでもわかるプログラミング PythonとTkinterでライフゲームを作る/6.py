#! /usr/bin/env python3
import tkinter
gw = 64
gh = 64
cellsize = 8
cellcolor = '#c82c55'
cells = [[0] * gw for i in range(gh)]
after_id = None # afterをキャンセルする時に使うid
def cells_draw():
    cv.delete('cellstag')
    for y in range(gh):
        for x in range(gw):
            if cells[y][x] == 0 : continue
            sx, sy = x*cellsize+2, y*cellsize+2
            ex, ey = sx+cellsize-1, sy+cellsize-1
            cv.create_rectangle(sx, sy, ex, ey, fill = cellcolor, tag = 'cellstag')
def leftdown(e):
    if after_id : root.after_cancel(after_id) # updateを止める
    kx = (e.x-2) // cellsize
    ky = (e.y-2) // cellsize
    kx = min(gw-1, max(kx, 0))
    ky = min(gh-1, max(ky, 0))
    if cells[ky][kx]:
        cells[ky][kx] = 0
    else:
        cells[ky][kx] = 1
    cells_draw()
def rightdown(e):
    if after_id : root.after_cancel(after_id) # updateを止める
    update() # update関数を呼ぶ
def update():
    global after_id # 関数の外の変数（グローバル変数）を関数内で変更するときはglobal 変数名と書く
    print(after_id)
    after_id = root.after(100, update) # afterで100ミリ秒後にupdate関数を呼ぶ
root = tkinter.Tk()
root.resizable(width = False, height = False)
cv = tkinter.Canvas(root, width = cellsize * gw, height = cellsize * gh)
cv.pack()
cv.bind('<Button-1>', leftdown)
cv.bind('<Button-3>', rightdown)
root.mainloop()