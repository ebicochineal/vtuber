## エビでもわかるプログラミング PythonとTkinterでライフゲームを作る  
- 今回の内容は少しでもプログラミングをかじったことがある人はなんとなく理解できるんじゃないかなと思います
- Pythonは実行速度は遅いですが非常に書きやすい言語でプログラミングを始めたばかりの人にもオススメです  
- Pythonは2系と3系がありますが今回はPython3を使います  
- Tkinter(ティーキンター)はPythonに標準で付いてくるGUIプログラムを作成できるライブラリです  

---
#### やっておいた方が良い事
- python3のインストール
- if文やfor文や2次元リストの理解
- ライフゲームのルールの確認
---
#### 今から作るライフゲームの機能
- 左クリックでセルの追加と削除（編集モード）
- 右クリックで時間を進める(再生モード)
- 左クリックで再生を停止し編集モードに戻る
- 外側のループ
---
#### これからやる事
- 1 ウィンドウの表示
- 2 ウィンドウにキャンバスの配置
- 3 キャンバスのクリックイベントの登録
- 4 クリック位置の取得とグリッド上での位置確認
- 5 セルの描画の実装
- 6 一定時間ごとにupdate関数の呼び出し
- 7 次の世代の計算と画面の更新
---
## 1 ウィンドウの表示
```py
#! /usr/bin/env python3
import tkinter
root = tkinter.Tk()
root.mainloop()
```
- この４行のプログラムをメモ帳などにコピペして保存し拡張子をpyに変えてダブルクリックして実行するとタイトルにtkと書かれたウィンドウが表示されます
- １行目はシバン文と言ってwindowsだと意味が無いものですがこれを書いているとwindowsでも2系と3系の２つのPythonをインストールしている環境下でPythonランチャーであるpy.exeがどっちで実行するかを判断してくれます  


---

## 2 ウィンドウにキャンバスの配置
```py
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
```
- ウィンドウはそのままだとリサイズできてしまうのでresizableにFalseを渡しリサイズできないようにします  
- 縦と横に８ピクセルの大きさのセルを６４つ置ける大きさのキャンバスを作りpackで配置します  
---
## 3 キャンバスのクリックイベントの登録
```py
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
```
- これを実行しキャンバスで左クリックすると黒い画面にLと表示され右クリックすると黒い画面にRと表示されます
- `'<Button-1>'`は左クリックのイベントの事で`'<Button-3>'`は右クリックのイベントの事です
- bindでイベントが起こったら何の関数を呼ぶかを登録します
---
## 4 クリック位置の取得とグリッド座標確認
```py
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
```
- leftdown関数もrightdown関数も引数eで何かを受け取っています(引数の名前は何でもいいですaでもbでもeventでも構いません)
- e.xにはX座標が入っていてe.yにはY座標が入っています
- 実はキャンバスは指定したサイズよりも２ピクセルずつ大きく座標も２ピクセルずれています
- 座標を０から６３マスのグリッド座標に変換したいので座標から２ピクセル分の座標を引いて//cellsizeで整数除算します
- キャンバスの隅をクリックすると画面外の座標になってしまうことがあるのでkxが0より小さいなら0にkxがgw-1より大きいならgw-1に修正します  
  次のように書くこともできます
  ```py
  if kx < 0:
      kx = 0
  if kx > gw-1:
      kx = gw-1
  ```
  ↓
  ```py
  if kx < 0 : kx = 0
  if kx > gw-1 : kx = gw-1
  ```
  ↓
  ```py
  kx = min(gw-1, max(kx, 0))
  ```

#### 追記
- 座標のずれを無くす、キャンバスの境界線を消す
tkinter.Canvasのオプション highlightthickness = 0で境界線を消すことができます  


---
## 5 セルの描画の実装
```py
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
```
- `cells`はセルの状態が入った2次元リストです０が死で１が生です  
  次のように書くこともできます
  ```py
  cells = []
  for y in range(gh):
      cells.append([0] * gw)
  ```
  ↓
  ```py
  cells = [[0] * gw for i in range(gh)]
  ```
- `cells_draw`  
  - `cv.delete`  
    最初にすべてのセルをキャンバスから削除  
    消さないと状態が変わって死になっても残ったままになってしまうので
  - `cv.create_rectangle`  
    開始位置X、Y、終了位置X、Y、塗りつぶす色、タグを指定して描画します(色やタグは指定しなくても構いません)  
    タグを指定するのは消す時のためです
    `create_rectangle`を`create_oval`にするとセルを円で描くことができます



---
## 6 一定時間ごとにupdate関数の呼び出し
```py
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
```
- 実行し右クリックするとupdate関数が１００ミリ秒ごとに呼ばれているのが分かります


---
## 7 次の世代の計算と画面の更新
```py
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
```

- 周囲のセルをカウントする  
  次のように書くこともできます
  ```py
  cnt = 0
  for dx, dy in d:
      px = x+dx
      py = y+dy
      if px < 0 : px = gw-1
      if px > gw-1 : px = 0
      if py < 0 : py = gh-1
      if py > gh-1 : py = 0
      cnt += cells[py][px]
  ```
  ↓
  ```py
  cnt = sum(cells[(y+dy)%gh][(x+dx)%gw] for dx, dy in d)
  ```
- 座標(x, y)の次の世代のセルの状態  
  次のように書くこともできます
  ```py
  if cells[y][x]:
      if cnt == 2 or cnt == 3 : nextcells[y][x] = 1
  else:
      if cnt == 3 : nextcells[y][x] = 1 
  ```
  ↓
  ```py
  if 3 - cells[y][x] <= cnt <= 3 : nextcells[y][x] = 1
  ```
- 黒い画面(コンソール)を非表示にするには拡張子を.pyから.pywにすれば表示されなくなります
---
#### 完成コード
```py
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
```

---
#### 今日の闇Python

```py
from tkinter import *;q=range(64);s=[[0]*64for i in q];d='<Button-%d>'
def p():v.delete('t');[s[y][x]and v.create_rectangle(x*8+2,y*8+2,x*8+9,y*8+9,fill='#c82c55',tag='t')for x in q for y in q]
def l(e):z(d);t=lambda x:min(63,max((x-2)//8,0));x,y=t(e.x),t(e.y);s[y][x]=s[y][x]<1;p()
def u(_=0):global d,s;s=[[2-s[y][x]<sum(s[(y+j)%64][(x+i)%64]for i,j in[(a,b)for a in[-1,0,1]for b in[-1,0,1]if a or b])<4for x in q]for y in q];p();d=o.after(100,u)
o=Tk();o.resizable(0,0);z=o.after_cancel;v=Canvas(o,width=512,height=512);v.pack();v.bind(d%1,l);v.bind(d%3,lambda e:u(z(d)));o.mainloop()
```
- [海老レンジャイ 競技プログラミング部 闇Python入門](https://github.com/ebi-cp/docs/blob/master/dark-pythonista.md)


---
#### おまけ C#で書き直したライフゲームのコード
- csc.exeでコンパイルできます
- csc.exeの場所はたぶんこのへん C:/Windows/Microsoft.NET/Framework64/v4.0.30319
- コンソールを非表示オプション /target:winexe  




```cs
using System;
using System.Drawing;
using System.Windows.Forms;

class LifeGame : Form {
    static private int GW = 64;
    static private int GH = 64;
    static private int CellSize = 8;
    private int[] dx = new int[] {-1, 0, 1, -1, 1, -1, 0, 1};
    private int[] dy = new int[] {-1, -1, -1, 0, 0, 1, 1, 1};
    private int cw = LifeGame.CellSize*LifeGame.GW;
    private int ch = LifeGame.CellSize*LifeGame.GH;
    private SolidBrush cellcolor = new SolidBrush(Color.FromArgb(255, 200, 44, 85));
    private SolidBrush backcolor = new SolidBrush(Color.FromArgb(255, 240, 240, 240));
    private int[,] cells = new int[LifeGame.GH, LifeGame.GW];
    private int[,] nextcells = new int[LifeGame.GH, LifeGame.GW];
    private Graphics graphics;
    private Bitmap bitmap;
    private PictureBox picturebox;
    private Timer timer = new Timer() { Interval = 100 };
    public LifeGame () {
        this.picturebox = new PictureBox() { Height = this.ch, Width = this.cw };
        this.bitmap = new Bitmap(this.cw, this.ch);
        this.graphics = Graphics.FromImage(this.bitmap);
        this.picturebox.MouseDown += new MouseEventHandler(this.MouseDownEvent);
        this.Width = this.cw+6;
        this.Height = this.ch+29;
        this.Controls.Add(this.picturebox);
        this.FormBorderStyle = FormBorderStyle.FixedSingle;
        this.timer.Tick += new EventHandler(this.Update);
    }
    private void MouseDownEvent (object sender, MouseEventArgs e) {
        if (e.Button == MouseButtons.Left) { this.LeftDown(); }
        if (e.Button == MouseButtons.Right) { this.RightDown(); }
    }
    private void LeftDown () {
        this.timer.Stop();
        Point p = this.PointToClient(Cursor.Position);
        int x = Math.Min(LifeGame.GW-1, Math.Max(p.X / LifeGame.CellSize, 0));
        int y = Math.Min(LifeGame.GH-1, Math.Max(p.Y / LifeGame.CellSize, 0));
        this.cells[y, x] = this.cells[y, x] == 0 ? 1 : 0;
        this.CellsDraw();
    }
    private void RightDown () { this.timer.Start(); }
    private void CellsDraw () {
        this.graphics.FillRectangle(this.backcolor, 0, 0, this.cw, this.ch);
        for (int y = 0; y < LifeGame.GH; ++y) {
            for (int x = 0; x < LifeGame.GH; ++x) {
                if (this.cells[y, x] == 0) { continue; }
                int px = LifeGame.CellSize * x;
                int py = LifeGame.CellSize * y;
                this.graphics.FillRectangle(Brushes.Black, px, py, LifeGame.CellSize, LifeGame.CellSize);
                this.graphics.FillRectangle(this.cellcolor, px+1, py+1, LifeGame.CellSize-2, LifeGame.CellSize-2);
            }
        }
        this.picturebox.Image = this.bitmap;
    }
    private void Update (object sender, EventArgs e) {
        for (int y = 0; y < LifeGame.GH; ++y) {
            for (int x = 0; x < LifeGame.GH; ++x) {
                int cnt = 0;
                for (int d = 0; d < 8; ++d) {
                    cnt += this.cells[(LifeGame.GH+y+this.dy[d])%LifeGame.GH, ((LifeGame.GW+x+this.dx[d])%LifeGame.GW)];
                }
                this.nextcells[y, x] = (3-this.cells[y, x] <= cnt && cnt <= 3) ? 1 : 0;
            }
        }
        Array.Copy(this.nextcells, this.cells, this.nextcells.Length);
        this.CellsDraw();
    }
}
class Program {
    static void Main () { Application.Run(new LifeGame()); }
}
```


