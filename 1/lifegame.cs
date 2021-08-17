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