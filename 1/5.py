#! /usr/bin/env python3
import tkinter
gw = 64
gh = 64
cellsize = 8
cellcolor = '#c82c55' # セルの色ですカラーコードの１６進数文字列を渡します #c82c55はコチニールレッドのカラーコードです
cells = [] # リストを作成します
for y in range(gh): # gh回ループします
    cells.append([0] * gw) # 長さgwのすべて０のリストを作成しcellsに追加します
def cells_draw():
    cv.delete('cellstag') # すべてのセルをキャンバスから削除
    for y in range(gh): # gh回ループしyには0～gh-1が順に入ります
        for x in range(gw): # gw回ループしxには0～gw-1が順に入ります
            if cells[y][x] == 0 : continue # cells[y][x]が死なら何も描かず次のxへ
            sx, sy = x*cellsize+2, y*cellsize+2 # xの開始座標, yの開始座標
            ex, ey = sx+cellsize-1, sy+cellsize-1 # xの終了座標, yの終了座標
            cv.create_rectangle(sx, sy, ex, ey, fill = cellcolor, tag = 'cellstag') # 矩形をキャンバスに描きます
def leftdown(e): # セルの追加と削除
    kx = (e.x-2) // cellsize
    ky = (e.y-2) // cellsize
    kx = min(gw-1, max(kx, 0))
    ky = min(gh-1, max(ky, 0))
    if cells[ky][kx]: # 1なら0に 0なら1に
        cells[ky][kx] = 0
    else:
        cells[ky][kx] = 1
    cells_draw() # 変更内容をキャンバスに反映するためcells_drawを呼びます
def rightdown(e):
    print('R')
root = tkinter.Tk()
cv = tkinter.Canvas(root, width = cellsize * gw, height = cellsize * gh)
cv.pack()
cv.bind('<Button-1>', leftdown)
cv.bind('<Button-3>', rightdown)
root.mainloop()
