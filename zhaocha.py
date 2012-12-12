import ctypes
fn="llkdll.dll"
dll=ctypes.CDLL(fn)

def move(x,y):
    "move mouse cursor"
    ctypes.windll.user32.SetCursorPos(x,y)
def ld():
    "left down"
    ctypes.windll.user32.mouse_event(2,0,0,0,0)
def lu():
    "left up"
    ctypes.windll.user32.mouse_event(4,0,0,0,0)
def get_wnd_offset(hwn):
    ofs=dll.get_wnd_offset(hwn)
    return ofs>>16,ofs&((1<<16)-1)
    
def wnd():
    return dll.find_wnd("大家来找茬")

 
def get_dif_set(x0,x1,y,w,h):
    ret=set()
    for r in range(y,y+h):
        for c in range(w):
            if dll.get_clr(x0+c,r)!=dll.get_clr(x1+c,r):
                ret.add((x0+c,r))
    return ret

def _get_joint(pt,ds):
    ret=[pt]
    n=0
    L=1
    while n<L:
        x,y=ret[n]
        if (x+1,y) in ds:
            ret.append((x+1,y))
            ds.remove((x+1,y))
            L+=1
        if (x-1,y) in ds:
            ret.append((x-1,y))
            ds.remove((x-1,y))
            L+=1
        if (x,y+1) in ds:
            ret.append((x,y+1))
            ds.remove((x,y+1))
            L+=1
        if (x,y-1) in ds:
            ret.append((x,y-1))
            ds.remove((x,y-1))
            L+=1
        n+=1
    return ret
           

def get_joints(ds):
    ret=[]
    while len(ds)!=0:
        ret.append(_get_joint(ds.pop(),ds))
    return ret

def get_gravity_center(dl):
    x,y=0,0
    for t in dl:
        x+=t[0]
        y+=t[1]
    L=len(dl)
    return x//L,y//L

def get_frame_center1(dl):
    maxx,maxy=dl[0]
    minx,miny=dl[0]
    for x in dl:
        if x[0]<minx:
            minx=x[0]
        if x[0]>maxx:
            maxx=x[0]
        if x[1]<miny:
            miny=x[1]
        if x[1]>maxy:
            maxy=x[1]
    return (maxx+minx)//2,(maxy+miny)//2

def get_dif_pt(para=None):
    if para==None:
        return
    ds=get_dif_set(*para)
    jl=sorted(get_joints(ds),key=lambda x:len(x),reverse=True)
    cents=list(map(get_gravity_center,jl[:5]))
    return cents

para1=(8,517,190,497,450)
para2=(10,403,186,380,285)

_N=10
def manual(para):
    global _N
    dll.snap(wnd())
    dll.save(r"c:\zc%d.png" % _N)
    _N+=1
    global dl,para1,para2
    hwn=wnd()
    dll.show()
    ds=get_dif_set(*para)
    for x in ds:
        a=dll.set_pixel(x[0],x[1],0x0000ff)

def fill100(x,y,clr):
    for r in range(y-10,y+10):
        for c in range(x-10,x+10):
            dll.set_pixel(c,r,clr)

def test(para):
    dll.snap(wnd())
    dl=get_dif_pt(para)
    if len(dl)==0:
        return
    dx,dy=get_wnd_offset(wnd())
    for t in dl:
        move(t[0]+dx,t[1]+dy)
        ld()
        lu()


            
import hotkey

hotkey.reg(2,49,lambda :test(para1))
hotkey.reg(2,50,lambda :test(para2))
hotkey.reg(2,51,lambda :manual(para1))
hotkey.reg(2,52,lambda :manual(para2))

#dif=get_dif_set(10,403,186,380,285)
