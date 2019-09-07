import matplotlib.pyplot as plt
import numpy as np
from matplotlib import style
from ipywidgets import widgets
from IPython.display import display


style.use("seaborn")
fig, ax = plt.subplots()
lim = 1000
ax.set_xlim(0, lim)
ax.set_ylim(0, lim)

# absolute positioning of text, so it is in the same spot after zooming in/out
txt = ax.text(0.03,
              0.935,
              r"",
              bbox=dict(facecolor='w', edgecolor='k', pad=5),
              transform=ax.transAxes,
              zorder = 30)

#point counter
count = 0
A = np.zeros(2)
B = np.zeros(2)
AB = np.zeros(2)

def onclick(event):

    global ax, count, A, B, AB, txt

    # dictionary with properties of matkers
    marker_style = dict(marker='o', mec ="steelblue",  mfc="w", mew = 2, ms=8)
    count +=1
    X = np.array(ax.transData.inverted().transform((event.x,event.y)))
    text = plt.text
    if count == 1:
        # plot point A
        A = X
        plt.plot(*A, **marker_style, zorder = 10)
    elif count == 2:
        # plot point B and the line through A and B
        color =  "steelblue"
        B = X
        plt.plot(*B, 'o', **marker_style, zorder = 10)
        AB = B - A
        Ainf = A - 2*lim*AB
        Binf = A + 2*lim*AB
        #plot the line through the points A, B
        plt.plot(*zip(Ainf, Binf), "-", color = color, lw = 3, zorder = 1)
    else:
        #plot subsequent points
        AX = X - A
        d = round(np.linalg.det(np.vstack((AB, AX))), 12)
        if d ==0:
            color = "w"
        elif d > 0:
            color = "lawngreen"
        else:
            color = "tomato"
        marker_style["mfc"] = color
        plt.plot(*X, **marker_style, zorder = 10)
        if abs(d) > 1:
            dd = int(d)
        elif abs(d) > 0.001:
            dd = format(d, ".4f")
        else:
            dd = format(d, ".12f")
        txt.set_text(r"$\det\ M_X = {}$".format(dd))
        plt.draw()

cid = fig.canvas.mpl_connect('button_press_event', onclick)
plt.show()

def reset_values(b):
    """Reset the plots to inital values."""
    global ax, A, B, AB, count, txt
    count = 0
    A = np.zeros(2)
    B = np.zeros(2)
    AB = np.zeros(2)
    ax.clear()
    ax.set_xlim(0, lim)
    ax.set_ylim(0, lim)
    txt = ax.text(0.03,
                  0.935,
                  r"",
                  bbox=dict(facecolor='w', edgecolor='k', pad=5),
                  transform=ax.transAxes,
                  zorder = 30)

reset_button = widgets.Button(description = "Reset")
reset_button.on_click(reset_values)
display(reset_button)
