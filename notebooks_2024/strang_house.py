import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.transforms as mtrans
from matplotlib import style
import numpy as np
# remove the next two imports for use outside a Jupyter notebook
from ipywidgets import widgets
from IPython.display import display


class PlotData():
    """
    Class which provides data for the determinant sign plot
    """

    scale = 0.9
    center = np.array([0, 0])
    v1 = np.array([1, 0])
    v2 = np.array([0, 1])


    def __init__(self, v1 = None, v2 = None):
        if v1 is not None:
            self.v1 = np.array(v1)
        if v2 is not None:
            self.v2 = np.array(v2)
        self.new_v1 = self.v1.copy()
        self.new_v2 = self.v2.copy()


    def get_trans_matrix(self):
        T = np.zeros((3, 3))
        T[:2,0] = self.new_v1
        T[:2,1] = self.new_v2
        T[2,2] = 1
        return T

    @staticmethod
    def angle(v):
        theta = 180*np.arctan2(*v[::-1])/np.pi
        return theta

    def get_r(self):
        return self.scale*min(np.linalg.norm(self.new_v1), np.linalg.norm(self.new_v2))

    def get_theta1(self):
        return self.angle(self.new_v1)

    def get_theta2(self):
        return self.angle(self.new_v2)


    def get_det(self):
        return np.linalg.det(np.vstack((self.new_v1, self.new_v2)))

    def get_orientation(self):
        det = self.get_det()
        if det == 0:
            return 0
        elif  det > 0:
            return 1
        else:
            return -1

    def set_new_v1(self, v1):
        self.new_v1 = np.array(v1)

    def set_new_v2(self, v2):
        self.new_v2 = np.array(v2)


class Plot():
    """
    Class which generates the plot of the house
    """

    # figure properties
    figsize = (6, 6)
    style = "seaborn-v0_8"
    ax_facecolor = "lightblue" #"skyblue" #paleturquoise"
    gridcolor = "w"
    xlim = (-3, 3)
    ylim = (-2, 4)

    # properties of the angle patch, markers, and lines
    edge_alpha = 1
    v1_color= "orangered"
    v2_color = "blue"
    center_color = "k"

    # properties of house patches
    house_lw =  2
    coord_ax_lw = 3
    house_ec = "k"

    # text properties
    # text coordinates are in axes coords
    text_coords_x = {1 : 0.07, 2 : 0.2}
    text_coords_y = {0 : 0.91, 1 : 0.81}

    # rectangle properties
    # rectangle coordinates are in axes coords
    rectangle_width = 0.32
    rectangle_height = 0.22
    rectangle_xy = (0.03, 1 - 0.03 - rectangle_height)
    rectangle_fc = 'w'
    rectangle_ec = 'k'

    small_rectangle_width = rectangle_width - 0.05
    small_rectangle_height = rectangle_height - 0.05
    small_rectangle_xy = (0.03+0.025, rectangle_xy[1] + 0.026)

    mask_rectangle_width = small_rectangle_width - 0.03
    mask_rectangle_height = rectangle_height
    mask_rectangle_xy = (small_rectangle_xy[0] + 0.015, rectangle_xy[1])
    mask_rectangle_fc = rectangle_fc

    # zorders
    zorder_rectangle = 5
    zorder_small_rectangle = 10
    zorder_mask_rectangle = 15
    zorder_coord_ax = 10
    zorder_text = 20
    zorder_roof = 25
    zorder_wall = 30
    zorder_door = 35
    zorder_window = 35
    zorder_sun = 35
    zorder2 = 40
    zorder1 = 50
    zorder0 = 60


    def get_wall_params(self):

        return dict(xy = (0,0),
            width = 1,
            height = 1,
            ec = self.house_ec,
            fc = "w",
            lw = self.house_lw,
            zorder = self.zorder_wall,
            mclass = mpl.patches.Rectangle
            )

    def get_door_params(self):

        return dict(xy = (0.1,0),
            width = 0.35,
            height = 0.7,
            ec = self.house_ec,
            fc = "burlywood",
            lw = self.house_lw,
            zorder = self.zorder_door,
            mclass = mpl.patches.Rectangle
            )

    def get_window_params(self):

        return dict(xy = (0.55,0.35),
            width = 0.35,
            height = 0.35,
            ec = self.house_ec,
            fc = "lightgray",
            lw = self.house_lw,
            zorder = self.zorder_window,
            mclass = mpl.patches.Rectangle
            )

    def get_roof_params(self):

        return dict(xy = np.array([[-0.1,0.5, 1.1],[1, 1.5, 1]]).T,
            ec = self.house_ec,
            fc = "salmon",
            closed = True,
            lw = self.house_lw,
            zorder = self.zorder_roof,
            mclass = mpl.patches.Polygon
            )

    def get_sun_params(self):

        return dict(xy = (1.25, 1.75),
            radius = 0.3,
            ec = self.house_ec,
            fc = "gold",
            lw = self.house_lw,
            zorder = self.zorder_sun,
            mclass = mpl.patches.Circle
            )


    def get_coord_ax_params(self, name):
        x_dist = self.xlim[1] - self.xlim[0]
        y_dist = self.ylim[1] - self.ylim[0]
        if name == "x":
            x = self.xlim[0] + 0.125*x_dist
            y = 0
            dx = 0.75*x_dist
            dy = 0
        if name == "y":
            x = 0
            y = self.ylim[0] + 0.125*y_dist
            dx = 0
            dy = 0.75*y_dist

        return dict(x = x,
                    y = y,
                    dx=dx,
                    dy = dy,
                    length_includes_head = True,
                    lw = self.coord_ax_lw,
                    color = "steelblue",
                    head_width = 0.075,
                    zorder = self.zorder_coord_ax,
                    mclass = mpl.patches.FancyArrow
                    )

    def get_marker_params(self, i):

        if i == 0:
            coords = self.data.center
            mec = self.center_color
            zorder = self.zorder0
        elif i == 1:
            coords = self.data.v1
            mec = self.v1_color
            zorder = self.zorder1
        elif i == 2:
            coords = self.data.v2
            mec = self.v2_color
            zorder = self.zorder2

        xdata = [coords[0]]
        ydata = [coords[1]]

        return dict(xdata = xdata,
                    ydata = ydata,
                    marker = "o",
                    ms = 9,
                    mfc = "w",
                    mec = mec,
                    mew = 2,
                    alpha = self.edge_alpha,
                    zorder = zorder,
                    mclass = mpl.lines.Line2D
                   )


    def get_line_params(self, i):

        if i == 1:
            xdata, ydata = zip(self.data.center, self.data.v1)
            color = self.v1_color
            zorder = self.zorder1
        elif i == 2:
            xdata, ydata = zip(self.data.center, self.data.v2)
            color = self.v2_color
            zorder = self.zorder2

        return dict(xdata = xdata,
                    ydata = ydata,
                    linestyle = "-",
                    lw = 4,
                    color = color,
                    alpha = self.edge_alpha,
                    zorder = zorder,
                    mclass = mpl.lines.Line2D
                   )


    def format_text(self, i, j):
        v = self.data.new_v1 if i==1 else  self.data.new_v2
        n  = v[j]
        s = f"{n:>4.1f}"
        if  "-0.0" in s:
            s = " " + s[1:]
        return s

    def get_text_params(self, i, j):

        text = self.format_text(i, j)
        x  = self.text_coords_x[i]
        y  = self.text_coords_y[j]
        if i == 1:
            color = self.v1_color
        else:
            color = self.v2_color

        return dict(x = x,
                    y = y,
                    text = text,
                    ha = "left",
                    va = "center",
                    fontsize = 14,
                    usetex = False,
                    family = "monospace",
                    color = color,
                    fontweight = "bold",
                    transform =  self.ax.transAxes,
                    zorder = self.zorder_text,
                    mclass = mpl.text.Text
                   )


    def get_rectangle_params(self):

        return dict(xy = self.rectangle_xy,
                    width = self.rectangle_width,
                    height = self.rectangle_height,
                    ec = self.rectangle_ec,
                    fc = self.rectangle_fc,
                    lw = 0,
                    transform =  self.ax.transAxes,
                    zorder = self.zorder_rectangle,
                    mclass = mpl.patches.Rectangle
                   )

    def get_small_rectangle_params(self):

        return dict(xy = self.small_rectangle_xy,
                    width = self.small_rectangle_width,
                    height = self.small_rectangle_height,
                    ec = "k",
                    fc = "None",
                    lw = 2,
                    transform =  self.ax.transAxes,
                    zorder = self.zorder_small_rectangle,
                    mclass = mpl.patches.Rectangle
                    )


    def get_mask_rectangle_params(self):

        return dict(xy = self.mask_rectangle_xy,
                    width = self.mask_rectangle_width,
                    height = self.mask_rectangle_height,
                    ec = "None",
                    fc = self.mask_rectangle_fc,
                    lw = 0,
                    transform =  self.ax.transAxes,
                    zorder = self.zorder_mask_rectangle,
                    mclass = mpl.patches.Rectangle
                    )


    def make_artist(self, d, method):
        a = d.pop("mclass")(**d)
        obj = method(a)
        return obj


    def __init__(self, v1 = None, v2 = None):

        self.data = PlotData(v1, v2)

        style.use(self.style)
        self.fig = plt.figure(figsize = self.figsize)
        self.ax = plt.subplot(111, aspect="equal")
        self.ax.set_xlim(*self.xlim)
        self.ax.set_ylim(*self.ylim)
        self.ax.set_facecolor(self.ax_facecolor)
        self.ax.grid(color = self.gridcolor)

        self.background_params = [self.get_rectangle_params,
                                  self.get_small_rectangle_params,
                                  self.get_mask_rectangle_params,
                                  lambda : self.get_coord_ax_params("x"),
                                  lambda : self.get_coord_ax_params("y")
                                  ]

        self.foreground_params = [self.get_wall_params,
                                  self.get_door_params,
                                  self.get_window_params,
                                  self.get_roof_params,
                                  self.get_sun_params,
                                  lambda : self.get_line_params(1),
                                  lambda : self.get_line_params(2),
                                  lambda : self.get_marker_params(0),
                                  lambda : self.get_marker_params(1),
                                  lambda : self.get_marker_params(2)
                                  ]

        self.textbox_params = [lambda : self.get_text_params(1, 0),
                               lambda : self.get_text_params(1, 1),
                               lambda : self.get_text_params(2, 0),
                               lambda : self.get_text_params(2, 1)
                               ]


        for f in self.background_params:
            self.make_artist(f(), method = self.ax.add_artist)

        self.foreground = []
        for f in self.foreground_params:
            self.foreground.append(self.make_artist(f(), method = self.ax.add_artist))
            # draw shadows
            d = f()
            d["zorder"] = 1
            d["alpha"] = 0.3
            for k in ["color", "fc", "ec", "mfc", "mec"]:
                if k in d:
                    d[k] = "steelblue"

            self.make_artist(d, method = self.ax.add_artist)

        self.textbox = []
        for f in self.textbox_params:
            self.textbox.append(self.make_artist(f(), method = self.ax.add_artist))


    def move_edge(self):

        T = mtrans.Affine2D(matrix = self.data.get_trans_matrix()) + self.ax.transData

        for artist in self.foreground:
            artist.set_transform(T)

        for i in range(len(self.textbox)):
            self.textbox[i].set_text(self.textbox_params[i]()["text"])


def strang_house():
    """
    Displays an interactive plot of two vectors illustrating
    how the sign of the determinant changes depending on position
    of the vectors.
    """

    p = Plot()
    button_down = False
    selected = 0
    selection_tolerance = 0.2

    def dist(u, v):

        return np.linalg.norm(np.array(u) - np.array(v))

    def onclick(event):

        nonlocal button_down, selected, selection_tolerance

        button_down = True
        position = [round(event.xdata, 1), round(event.ydata, 1)]

        if dist(p.data.new_v1, position) < selection_tolerance:
            selected = 1
        elif dist(p.data.new_v2, position) < selection_tolerance:
            selected = 2

    def onrelease(event):
        nonlocal button_down, selected
        button_down = False
        selected = 0


    def move(event):
        nonlocal p, button_down, selected

        if not button_down or selected == 0:
            return

        position = [round(event.xdata, 1), round(event.ydata, 1)]
        if selected == 1:
            p.data.set_new_v1(position)
        elif selected == 2:
            p.data.set_new_v2(position)
        p.move_edge()

    p.fig.canvas.mpl_connect('button_press_event', onclick)
    p.fig.canvas.mpl_connect('button_release_event', onrelease)
    p.fig.canvas.mpl_connect('motion_notify_event', move)

    plt.show()
