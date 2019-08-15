# Attempt to reproduce in Python the "Strang house" demo I made a long time ago in DD.


'''
Usage:
strangehouse()
strangehouse("symmetric")
strangehouse("diagonal")
strangehouse("orthogonal")
Grid fineness can be altered by changing grid_digits
Initial matrix can be chosen at will
'''


from numpy import  *
import matplotlib.pyplot as pl
from time import sleep
import sys

def stranghouse(matrix = 'all'):
    SYMMETRIC  = matrix == 'symmetric'
    DIAGONAL   = matrix == 'diagonal'
    ORTHOGONAL = matrix == 'orthogonal'

    dragging = 0

    grid_digits = 1 # (digits after the decimal point)
    for arg in sys.argv[1:]:
        if arg.isnumeric():  # note this only checks if all characters are digits. ok here.
            grid_digits = int(arg)
            print('Setting grid resolution to', grid_digits, 'digits')

    A = eye(2)   # the initial matrix
    #A[0,0] = -1

    xmin,xmax = -2,2
    ymin,ymax = -1,3

    clip_on = False

    roofoverhang = 0.1
    roof = array([[-roofoverhang,0,1,1+roofoverhang,0.5,0],[1-roofoverhang,1,1,1-roofoverhang,1.5,1]])

    polygons = [array([[0,1,1,0,0],[0,0,1,1.,0]]),
        roof,
        array([[.6,.8,.8,.6,.6],[0,0,.5,.5,0]])]

    t = linspace(0,2*pi,100)
    moon = array([.2+.2*cos(t),1.6+.2*sin(t)])
    polygons.append( moon )
    colors = ['cadetblue','tomato','sienna','gold']

    e1 = array([[0,1.],[0,0]])
    e2 = array([[0,0.],[0,1]])
    lines = array([e1,e2])
    lcolors = ['r','b']

    dots = [ e1[:,1], e2[:,1] ]
    dcolors = lcolors
    dotsize = 10
    dotalpha = 1

    def move(event):
        nonlocal buttonisdown,xyinv,dragging,A1,A2,grid_digits
        if buttonisdown:
            xyinv = ax.transData.inverted()  # function to convert from pixels to user coordinates
            if dragging > 0:
                ux,uy = xyinv.transform( (event.x,event.y) )
                if dragging==1:
                    if DIAGONAL:
                        A1[0] = ux.round(grid_digits)
                    elif ORTHOGONAL:
                        m = array([ux,uy])
                        lm = linalg.norm(m)
                        A1[:] = m/lm
                        newA2 = array([-A1[1],A1[0]])
                        A2[:] = sign(dot(A2,newA2))*newA2
                    else:
                        A1[:] = array([ux,uy]).round(grid_digits)
                    if SYMMETRIC: A2[0] = A1[1]

                else:
                    if DIAGONAL:
                        A2[1] = uy.round(grid_digits)
                    elif ORTHOGONAL:
                        m = array([ux,uy])
                        lm = linalg.norm(m)
                        A2[:] = m/lm
                        newA1 = array([-A2[1],A2[0]])
                        A1[:] = sign(dot(A1,newA1))*newA1
                    else:
                        A2[:] = array([ux,uy]).round(grid_digits)
                    if SYMMETRIC: A1[1] = A2[0]
                redraw()

    def dist(u,v): return linalg.norm(u-v)

    def press(event):
        nonlocal xyinv,A1,A2,buttonisdown,dragging,grid_digits
        selection_tolerance = .1
        xyinv = ax.transData.inverted()  # function to convert from pixels to user coordinates
        ux,uy = xyinv.transform( (event.x,event.y) )
        m = array([ux,uy]).round(grid_digits)
        if dist(m,A1) < selection_tolerance:
            dragging = 1
            if DIAGONAL:
                A1[0] = m[0]
            else:
                A1[:] = m
            if SYMMETRIC: A2[0] = A1[1]
            redraw()
        elif dist(m,A2) < selection_tolerance:
            dragging = 2
            if DIAGONAL:
                A2[1] = m[1]
            else:
                A2[:] = m
            if SYMMETRIC: A1[1] = A2[0]
            redraw()
        else:
            dragging = 0
        buttonisdown = True

    def release(event):
        nonlocal buttonisdown
        buttonisdown = False

    def redraw():
        nonlocal A
        for i,p in enumerate(polygons):
            Ap = dot(A,p)
            strokes[i].set_xdata(Ap[0])
            strokes[i].set_ydata(Ap[1])
            fills[i].set_xy(Ap.T)
        for i,p in enumerate(lines):
            Ap = dot(A,p)
            lstrokes[i].set_xdata(Ap[0])
            lstrokes[i].set_ydata(Ap[1])
        for i,p in enumerate(dots):
            Ap = dot(A,p)
            ldots[i].set_xdata(Ap[0])
            ldots[i].set_ydata(Ap[1])
        text00.set_text(stringify(A[0,0]))
        text10.set_text(stringify(A[1,0]))
        text01.set_text(stringify(A[0,1]))
        text11.set_text(stringify(A[1,1]))
        pl.draw()

    buttonisdown = False

    # make picture

    pl.figure('Strang house',figsize=(5,5),facecolor='w')
    ax = pl.subplot(111,aspect=1)


    pl.connect('motion_notify_event' , move   )
    pl.connect('button_press_event'  , press  )
    pl.connect('button_release_event', release)


    fills = []
    strokes = []
    lstrokes = []
    ldots = []

    A1 = A[:,0]  # first  column reference
    A2 = A[:,1]  # second column reference

    # write matrix as text
    pl.fill([xmin,xmin+1,xmin+1,xmin],[ymax-1,ymax-1,ymax,ymax],'k',alpha=0.05)
    textdelta = 0.5
    textoffsetx = 0.4
    textoffsety = 0.3

    def stringify(x):
        s = str(x.round(grid_digits)).replace('.0','').replace('-','−')
        if s=='−0': s = '0'
        return s

    text00 = ax.text(xmin+textoffsetx          ,ymax-textoffsety          ,stringify(A[0,0]),color=lcolors[0],fontsize=12,ha='right')
    text10 = ax.text(xmin+textoffsetx          ,ymax-textoffsety-textdelta,stringify(A[1,0]),color=lcolors[0],fontsize=12,ha='right')
    text01 = ax.text(xmin+textoffsetx+textdelta,ymax-textoffsety          ,stringify(A[0,1]),color=lcolors[1],fontsize=12,ha='right')
    text11 = ax.text(xmin+textoffsetx+textdelta,ymax-textoffsety-textdelta,stringify(A[1,1]),color=lcolors[1],fontsize=12,ha='right')

    # draw grid
    if True:
        for x in linspace(-1,1,3):
            pl.plot([x,x],[ymin,ymax],'k',lw=2,alpha=0.1)
        for y in linspace( 0,2,3):
            pl.plot([xmin,xmax],[y,y],'k',lw=2,alpha=0.1)


    # draw untransformed picture
    for i,p in enumerate(polygons):
        x = list(p[0])+[p[0,0]]  # close polygon
        y = list(p[1])+[p[1,0]]
        ax.fill(x,y,color=colors[i],alpha=0.1)
        ax.plot(x,y,'k',lw=3,alpha=.2)
    for i,p in enumerate(lines):
        x,y = p
        ax.plot(x,y,color=lcolors[i],lw=3,alpha=.3)
    for i,p in enumerate(dots):
        x,y = p
        ax.plot(x,y,'o',color=dcolors[i],markersize=dotsize,alpha=.3)

    # draw picture to be transformed in untransformed state
    for i,p in enumerate(polygons):
        Ap = dot(A,p)
        x = list(Ap[0])+[Ap[0,0]]  # close polygon
        y = list(Ap[1])+[Ap[1,0]]
        fill,   = ax.fill(x,y,color=colors[i],alpha=0.3,clip_on=clip_on)
        stroke, = ax.plot(x,y,'k',lw=3,alpha=1,clip_on=clip_on)
        fills.append(fill)
        strokes.append(stroke)

    for i,p in enumerate(lines):
        Ap = dot(A,p)
        x,y = Ap
        lstroke, = ax.plot(x,y,color=lcolors[i],lw=3,alpha=1,clip_on=clip_on)
        lstrokes.append(lstroke)

    for i,p in enumerate(dots):
        Ap = dot(A,p)
        x,y = Ap
        ldot, = ax.plot(x,y,'o',color=dcolors[i],markersize=dotsize,alpha=dotalpha,clip_on=clip_on)
        ldots.append(ldot)

    ax.set_xlim(xmin,xmax)
    ax.set_ylim(ymin,ymax)
    ax.tick_params(axis='x', labelsize=12)
    ax.tick_params(axis='y', labelsize=12)
    xyinv = ax.transData.inverted()  # function to convert from pixels to user coordinates

    if   SYMMETRIC : pl.title('matrix constrained to be symmmetric')
    elif DIAGONAL  : pl.title('matrix constrained to be diagonal')
    elif ORTHOGONAL: pl.title('matrix constrained to be orthogonal')
    else           : pl.title('')#general real matrix')
    pl.show()
