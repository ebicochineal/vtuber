#! /usr/bin/env python3
import tkinter
gw = 64 # 横に64マス
gh = 64 # 縦に64マス
cellsize = 8 # 1セルの大きさ
root = tkinter.Tk()
root.resizable(width = False, height = False) # リサイズ禁止
cv = tkinter.Canvas(root, width = cellsize * gw, height = cellsize * gh) # キャンバスの作成
cv.pack() # キャンバスの配置
root.mainloop()
