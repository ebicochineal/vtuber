#! /usr/bin/env python3
import tkinter
gw = 64
gh = 64
cellsize = 8
cellcolor = '#c82c55'
cells = [[0] * gw for i in range(gh)]
after_id = None
d = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)] # 周囲の座標を調べるときに座標に足し合わせて使います
def cells_draw():
    cv.delete('cellstag')
    for y in range(gh):
        for x in range(gw):
            if cells[y][x] == 0 : continue
            sx, sy = x*cellsize+2, y*cellsize+2
            ex, ey = sx+cellsize-1, sy+cellsize-1
            cv.create_rectangle(sx, sy, ex, ey, fill = cellcolor, tag = 'cellstag')
def leftdown(e):
    if after_id : root.after_cancel(after_id)
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
    if after_id : root.after_cancel(after_id)
    update()
def update():
    global after_id, cells # after_idとcellsは関数内で書き換える
    nextcells = [[0] * gw for i in range(gh)]
    for y in range(gh):
        for x in range(gw):
            # 周囲のセルをカウントする
            cnt = 0 # 周囲の生きたセルの個数
            for dx, dy in d:
                px = x+dx
                py = y+dy
                # 右と左は繋がっていて、上と下も繋がっている
                if px < 0 : px = gw-1 # pxが0より小さいならgw-1
                if px > gw-1 : px = 0 # pxがgw-1より大きいなら0
                if py < 0 : py = gh-1 # pyが0より小さいならgh-1
                if py > gh-1 : py = 0 # pyがgh-1より大きいなら0
                cnt += cells[py][px]
            # 座標(x, y)の次の世代のセルの状態
            if cells[y][x]: # 座標(x, y)に生きたセルがある場合
                if cnt == 2 or cnt == 3 : nextcells[y][x] = 1 # 周囲のセルが２か３なら座標(x, y)は生存します
            else: # 座標(x, y)に生きたセルが無い場合
                if cnt == 3 : nextcells[y][x] = 1 # 周囲のセルが３なら座標(x, y)は誕生します
    cells = nextcells # nextcellsをcellsに入れる
    cells_draw() # 次の世代をキャンバスに描画
    after_id = root.after(100, update)
root = tkinter.Tk()
root.resizable(width = False, height = False)
cv = tkinter.Canvas(root, width = cellsize * gw, height = cellsize * gh)
cv.pack()
cv.bind('<Button-1>', leftdown)
cv.bind('<Button-3>', rightdown)
root.mainloop()
