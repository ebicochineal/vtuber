#! /usr/bin/env python3
import tkinter
gw = 64
gh = 64
cellsize = 8
cellcolor = '#c82c55'
cells = [[0] * gw for i in range(gh)]
after_id = None
d = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
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
    global after_id, cells
    nextcells = [[0] * gw for i in range(gh)]
    for y in range(gh):
        for x in range(gw):
            cnt = sum(cells[(y+dy)%gh][(x+dx)%gw] for dx, dy in d)
            if 3 - cells[y][x] <= cnt <= 3 : nextcells[y][x] = 1
    cells = nextcells
    cells_draw()
    after_id = root.after(100, update)
root = tkinter.Tk()
root.resizable(width = False, height = False)
cv = tkinter.Canvas(root, width = cellsize * gw, height = cellsize * gh)
cv.pack()
cv.bind('<Button-1>', leftdown)
cv.bind('<Button-3>', rightdown)
root.mainloop()