import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.lines as mlines
import matplotlib.text as mtext
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
    Class which generates the determinant sign plot
    """

    # figure properties
    figsize = (5, 5)
    style = "seaborn-v0_8"
    xlim = 2
    ylim = 2

    # properties of the angle patch, markers, and lines
    wedge_color_plus = 'coral'
    wedge_color_minus = 'cornflowerblue'
    wedge_alpha = 0.5
    edge_alpha = 1
    v1_color= "tomato"
    v2_color = "steelblue"
    center_color = "k"
    mfc = "w"
    mew = 2
    ms = 9
    marker = 'o'
    linestyle = '-'
    lw= 4

    # text properties
    # text coordinates are in axes coords
    text_coords = {"text_det":(0.04, 0.96),
                   "text_str_v1":(0.13, 0.96),
                   "text_str_v2":(0.192, 0.96),
                   "text_v1":(0.04, 0.90),
                   "text_v2":(0.04, 0.85)
                   }
    ha = "left"
    va = "top"
    usetex = False #True
    fontsize = 10

    fontfamily = 'monospace'
    fontweight = "bold"

    # rectangle properties
    # rectangle coordinates are in axes coords
    rectangle_xy = (0.01, 0.79)
    rectangle_width = 0.49
    rectangle_height = 0.2
    rectangle_fc = 'w'
    rectangle_ec = 'k'

    # zorders
    zorder_rectangle = 10
    zorder_text = 20
    zorder_wedge = 30
    zorder2 = 40
    zorder1 = 50
    zorder0 = 60




    def get_wedge_params(self):
        center  = self.data.center
        theta1 = self.data.get_theta1()
        theta2 = self.data.get_theta2()
        r = self.data.get_r()
        orientation = self.data.get_orientation()
        if orientation == 0:
            r=0
            color = "w"
        elif orientation == -1:
            theta1, theta2 = theta2, theta1
            color = self.wedge_color_minus
        elif orientation == 1:
            color = self.wedge_color_plus
        return dict(center = center,
                    r = r,
                    theta1 = theta1,
                    theta2 = theta2,
                    color = color,
                    alpha = self.wedge_alpha,
                    zorder = self.zorder_wedge
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
                    marker = self.marker,
                    ms = self.ms,
                    mfc = self.mfc,
                    mec = mec,
                    mew = self.mew,
                    alpha = self.edge_alpha,
                    zorder = zorder
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
                    linestyle = self.linestyle,
                    lw = self.lw,
                    color = color,
                    alpha = self.edge_alpha,
                    zorder = zorder
                   )


    def format_text(self):
        det = round(self.data.get_det(),2)
        v11, v12 = [round(n, 1) for n in self.data.new_v1]
        v21, v22 = [round(n, 1) for n in self.data.new_v2]
        text_det = f"det[     ] = $\\bf{det}$"
        text_str_v1 = r"$\bf{v_1}$"
        text_str_v2 = r"$\bf{v_2}$"
        text_v1 = f"$\\bf{{v_1}}$ = [{v11:>4}, {v12:>4}]"
        text_v2 = f"$\\bf{{v_2}}$ = [{v21:>4}, {v22:>4}]"
        return {"text_det":text_det,
                "text_str_v1":text_str_v1,
                "text_str_v2":text_str_v2,
                "text_v1":text_v1,
                "text_v2":text_v2}


    def get_text_params(self, k):

        text_d = self.format_text()
        text = text_d[k]
        x,y  = self.text_coords[k]
        if k in ["text_str_v1", "text_v1"]:
            color = self.v1_color
        elif k in ["text_str_v2", "text_v2"]:
            color = self.v2_color
        else:
            color = "k"

        return dict(x = x,
                    y = y,
                    text = text,
                    ha = self.ha,
                    va = self.va,
                    fontsize = self.fontsize,
                    usetex = self.usetex,
                    fontfamily = self.fontfamily,
                    color = color,
                    fontweight = self.fontweight,
                    transform =  self.ax.transAxes,
                    zorder = self.zorder_text
                   )


    def get_rectangle_params(self):

        return dict(xy = self.rectangle_xy,
                    width = self.rectangle_width,
                    height = self.rectangle_height,
                    ec = self.rectangle_ec,
                    fc = self.rectangle_fc,
                    transform =  self.ax.transAxes,
                    zorder = self.zorder_rectangle
                   )


    def __init__(self, v1 = None, v2 = None, show_angle = True):

        self.data = PlotData(v1, v2)
        self.show_angle = show_angle


        style.use(self.style)
        self.fig = plt.figure(figsize = self.figsize)
        self.ax = plt.subplot(111, aspect="equal")

        self.text_det = mtext.Text(**self.get_text_params("text_det"))
        self.text_str_v1 = mtext.Text(**self.get_text_params("text_str_v1"))
        self.text_str_v2 = mtext.Text(**self.get_text_params("text_str_v2"))
        self.text_v1 = mtext.Text(**self.get_text_params("text_v1"))
        self.text_v2 = mtext.Text(**self.get_text_params("text_v2"))
        self.wedge = patches.Wedge(**self.get_wedge_params())
        self.rectangle = patches.Rectangle(**self.get_rectangle_params())
        self.m0 = mlines.Line2D(**self.get_marker_params(0))
        self.m1 = mlines.Line2D(**self.get_marker_params(1))
        self.m2 = mlines.Line2D(**self.get_marker_params(2))
        self.edge1 = mlines.Line2D(**self.get_line_params(1))
        self.edge2 = mlines.Line2D(**self.get_line_params(2))


        self.ax.set_xlim(-self.xlim, self.xlim)
        self.ax.set_ylim(-self.ylim, self.ylim)

        self.ax.add_patch(self.rectangle)
        self.ax.add_artist(self.text_det)
        self.ax.add_artist(self.text_str_v1)
        self.ax.add_artist(self.text_str_v2)
        self.ax.add_artist(self.text_v1)
        self.ax.add_artist(self.text_v2)
        self.ax.add_line(self.edge1)
        self.ax.add_line(self.m1)
        self.ax.add_line(self.edge2)
        self.ax.add_line(self.m2)
        self.ax.add_line(self.m0)
        if self.show_angle:
            self.ax.add_patch(self.wedge)


    def move_edge(self):

        T = mtrans.Affine2D(matrix = self.data.get_trans_matrix()) + self.ax.transData

        self.m1.set_transform(T)
        self.m2.set_transform(T)
        self.edge1.set_transform(T)
        self.edge2.set_transform(T)

        wedge_d = self.get_wedge_params()
        self.wedge.set_radius(wedge_d["r"])
        self.wedge.set_theta1(wedge_d["theta1"])
        self.wedge.set_theta2(wedge_d["theta2"])
        self.wedge.set_color(wedge_d["color"])

        self.text_det.set_text(self.format_text()["text_det"])
        self.text_v1.set_text(self.format_text()["text_v1"])
        self.text_v2.set_text(self.format_text()["text_v2"])


def det_sign(show_angle = True):
    """
    Displays an interactive plot of two vectors illustrating
    how the sign of the determinant changes depending on position
    of the vectors.

    :show_angle:
        Boolean. It True, shows the angle between the two vectors.
    """

    p = Plot(show_angle = show_angle)
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







def colored_points():
    """
    Plots points coloring them depending on each side of a straigh line
    they are located. The first two clicks define the line. Color of
    subsequent points is determined using a determinant computation.
    The value of the determinant for each newly selected point is displayed
    in the upper left corner.
    """
    # plot limits
    xlim = 200
    ylim = 100
    lim = xlim + ylim
    line_color = "steelblue"
    fill_line = "w"
    fill_up = "tomato"
    fill_down = "lawngreen"
    # dictionary with properties of markers
    marker_style = dict(marker='o',
                        mec =line_color,
                        mfc= fill_line ,
                        mew = 2,
                        ms=8)

    style.use("seaborn-v0_8")
    fig = plt.figure(figsize = (8, 4))
    ax = plt.subplot(111)
    ax.set_xlim(0, xlim)
    ax.set_ylim(0, ylim)

    # absolute positioning of text, so it is in the same spot after zooming in/out
    init_text = dict(x = 0.03,
                  y = 0.9,
                  s=r"",
                  bbox=dict(facecolor='w', edgecolor='k', pad=5),
                  transform=ax.transAxes,
                  zorder = 30)

    txt = ax.text(**init_text)

    #point counter
    count = 0

    A = np.zeros(2)
    B = np.zeros(2)
    AB = np.zeros(2)

    click_x, click_y = 0, 0

    def onclick(event):
        #Point are plotted on release. Here we just record click
        #coordinates to detect dragging.
        nonlocal click_x, click_y

        click_x, click_y = event.x, event.y


    def onrelease(event):

        nonlocal ax, count, A, B, AB, txt, click_x, click_y

        # if click coordinates are some distance from release coordinates
        # then mouse is being dragged - no plotting in such case.
        if abs(click_x - event.x) + abs(click_y - event.y) > 10:
            return

        X = np.array(ax.transData.inverted().transform((event.x,event.y)))
        text = plt.text
        if count == 0:
            # plot point A
            A = X
            plt.plot(*A, **marker_style, zorder = 10)
            count += 1
        elif count == 1:
            B = X
            AB = B - A
            # check that points A and B not equal
            if not np.array_equal(AB, np.zeros(2)):
                # plot point B and the line through A and B
                plt.plot(*B, 'o', **marker_style, zorder = 10)
                Ainf = A - 2*lim*AB
                Binf = A + 2*lim*AB
                plt.plot(*zip(Ainf, Binf), "-", color = line_color, lw = 3, zorder = 1)
                count += 1
        else:
            #plot subsequent points
            AX = X - A
            d = round(np.linalg.det(np.vstack((AB, AX))), 12)
            if d ==0:
                marker_style["mfc"] = fill_line
            elif d > 0:
                marker_style["mfc"] = fill_up
            else:
                marker_style["mfc"] = fill_down
            plt.plot(*X, **marker_style, zorder = 10)
            if abs(d) > 1:
                dd = int(d)
            elif abs(d) > 0.001:
                dd = format(d, ".4f")
            else:
                dd = format(d, ".12f")
            txt.set_text(r"$\det\ M_X = {}$".format(dd))
            plt.draw()

    cid_click = fig.canvas.mpl_connect('button_press_event', onclick)
    cid_release = fig.canvas.mpl_connect('button_release_event', onrelease)
    plt.show()


    # The rest of the code defines a Jupyer notebook widget with a button resetting the plot.
    # It will not work outside a notebook.
    def reset_values(b):
        """Reset the plots to inital values."""
        nonlocal ax, A, B, AB, count, txt, marker_style
        count = 0
        A = np.zeros(2)
        B = np.zeros(2)
        AB = np.zeros(2)
        marker_style["mfc"] = fill_line
        ax.clear()
        ax.set_xlim(0, xlim)
        ax.set_ylim(0, ylim)
        txt = ax.text(**init_text)


    reset_button = widgets.Button(description = "Reset")
    reset_button.on_click(reset_values)
    display(reset_button)
