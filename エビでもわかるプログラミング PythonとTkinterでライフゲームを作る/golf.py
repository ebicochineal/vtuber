#! /usr/bin/env python3

from tkinter import *;q=range(64);s=[[0]*64for i in q];d='<Button-%d>'
def p():v.delete('t');[s[y][x]and v.create_rectangle(x*8+2,y*8+2,x*8+9,y*8+9,fill='#c82c55',tag='t')for x in q for y in q]
def l(e):z(d);t=lambda x:min(63,max((x-2)//8,0));x,y=t(e.x),t(e.y);s[y][x]=s[y][x]<1;p()
def u(_=0):global d,s;s=[[2-s[y][x]<sum(s[(y+j)%64][(x+i)%64]for i,j in[(a,b)for a in[-1,0,1]for b in[-1,0,1]if a or b])<4for x in q]for y in q];p();d=o.after(100,u)
o=Tk();o.resizable(0,0);z=o.after_cancel;v=Canvas(o,width=512,height=512);v.pack();v.bind(d%1,l);v.bind(d%3,lambda e:u(z(d)));o.mainloop()