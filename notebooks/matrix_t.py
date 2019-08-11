import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation, ImageMagickWriter
from math import sin, cos, pi
import bokeh.plotting as bk
from bokeh.layouts import gridplot
from bokeh.models import Arrow, OpenHead, NormalHead, VeeHead, Range1d, LinearAxis


class house_transform():

    original_house = {
                       "wall" : np.array([[0,0], [1,0], [1,1], [0,1]]).T,
                       "roof" : np.array([[-0.1,1], [0.1, 1.2], [0.1, 1.5], [0.3, 1.5], [0.3, 1.4], [0.5,1.6], [1.1,1]]).T,
                       "door" :  np.array([[0.1,0], [0.4,0], [0.4,0.6], [0.1,0.6]]).T,
                       "window" : np.array([[0.6,0.3], [0.9,0.3], [0.9,0.6], [0.6,0.6]]).T
                      }
    house_colors = {
                      "wall" : "cornflowerblue",
                      "roof" : "orangered",
                      "door" : "orange",
                      "window" : 'white'
                    }

    xlims =  (-1.5, 1.5)
    ylims =  (-1.5, 1.5)


    def __init__(self, MR, ML = None, left_shift = None, right_shift = None):

        self.MR = np.array(MR).astype(np.float64)

        if ML == None:
            self.ML = np.eye(2)
        else:
            self.ML = np.array(ML).astype(np.float64)

        self.det_MR = np.linalg.det(self.MR)
        self.det_ML = np.linalg.det(self.ML)

        if left_shift == None:
            self.left_shift = np.array([0,0]).reshape((2,1))
        else:
            self.left_shift = np.array(left_shift).astype(np.float64).reshape((2,1))

        if right_shift == None:
            self.right_shift = np.array([0,0]).reshape((2,1))
        else:
            self.right_shift = np.array(right_shift).astype(np.float64).reshape((2,1))

        self.house_left, left_xlim, left_ylim = self.h_transform(self.original_house, self.ML, self.left_shift)
        self.house_right, right_xlim, right_ylim = self.h_transform(self.house_left, self.MR, self.right_shift)

        self.xlim = (min(left_xlim[0], right_xlim[0]), max(left_xlim[1], right_xlim[1]))
        self.ylim = (min(left_ylim[0], right_ylim[0]), max(left_ylim[1], right_ylim[1]))


    def h_transform(self, house, A, b):
        new_house = {}
        xmax, xmin, ymax, ymin = 0, 0, 0, 0
        for k in house:
            s = house[k]
            ns = A@s + b
            new_house[k] = ns
            xmax = max(np.max(ns[0]), np.max(s[0]), xmax)
            xmin = min(np.min(ns[0]), np.min(s[0]), xmin)
            ymax = max(np.max(ns[1]), np.max(s[1]), ymax)
            ymin = min(np.min(ns[1]), np.min(s[1]), ymin)
        xlim = (xmin, xmax)
        ylim = (ymin, ymax)

        return (new_house, xlim, ylim)


    def show_house(self, save = False):

        fig = plt.figure(figsize = (12,4))
        fig.patch.set_alpha(0)
        plt.tight_layout()
        plt.style.use('seaborn')

        ax_left = plt.axes([0.05, 0.05, 0.35, 0.9])
        ax_left.axis('equal')
        ax_right = plt.axes([0.6, 0.05, 0.35, 0.9])
        ax_right.axis('equal')
        ax_right.yaxis.tick_right()
        ax_arrow = plt.axes([0.45, 0.05, 0.1, 0.9])
        ax_arrow.arrow(0,0, 0.75,0, width = 0.02, head_width = 0.06, head_length = 0.2, fc = 'k')
        ax_arrow.set_ylim(-1, 1)
        ax_arrow.axis('off')

        xlim_diff = self.xlim[1] - self.xlim[0]
        ylim_diff = self.ylim[1] - self.ylim[0]
        rxy = xlim_diff/ylim_diff
        p = 0.05
        xlim_padded  = np.array((self.xlim[0] - p*xlim_diff, self.xlim[1] + p*xlim_diff))*max(1, 1/rxy)
        ylim_padded  = np.array((self.ylim[0] - p*ylim_diff, self.ylim[1] + p*ylim_diff))*max(1, rxy)


        for k in  self.house_left:
            s = self.house_left[k]
            c = self.house_colors[k]
            if np.array_equal(self.ML, np.zeros((2,2))):
                ax_left.plot(*list(s), 'o', color='orangered', ms = 10)
            elif self.det_ML == 0:
                ax_left.plot(*list(s), c, lw = 4)
            else:
                ax_left.fill(*list(s), c)
            ax_left.plot([0, 0], ylim_padded, 'k')
            ax_left.plot(xlim_padded, [0, 0], 'k')

        for k in  self.house_right:
            s = self.house_right[k]
            c = self.house_colors[k]
            if np.array_equal(self.MR, np.zeros((2,2))):
                ax_right.plot(*list(s), 'o', color='orangered', ms = 10)
            elif self.det_MR == 0:
                ax_right.plot(*list(s), c, lw = 4)
            else:
                ax_right.fill(*list(s), c)
            ax_right.plot([0, 0], ylim_padded, 'k')
            ax_right.plot(xlim_padded, [0, 0], 'k')

        if save:
            plt.savefig(save, pad_inches = 0.5)
        plt.show()



class house_transform_bk(house_transform):

    def show_house(self, save = False):

        plot_height = 360
        plot_width = 440
        alpha = 0.85
        grid_alpha = 1
        grid_line_width = 0.3

        background_fill_color = "ivory"
        grid_line_color = "darkslategray"
        axes_color = "darkslategray"

        bk.output_notebook() # show plots in the notebook
        if save:
           bk.output_file(save)

        xlim_diff = self.xlim[1] - self.xlim[0]
        ylim_diff = self.ylim[1] - self.ylim[0]
        rxy = xlim_diff/ylim_diff
        s = 0.2
        xlim_padded  = np.array((self.xlim[0] - s*xlim_diff, self.xlim[1] + s*xlim_diff))*max(1, 1/rxy)
        ylim_padded  = np.array((self.ylim[0] - s*ylim_diff, self.ylim[1] + s*ylim_diff))*max(1, rxy)

        p = bk.figure(plot_width=plot_height,
                      plot_height=plot_height,
                      title = "Before transformation",
                      tools="pan, wheel_zoom, box_zoom,reset"
                      )
        p.add_layout(LinearAxis(), 'right')
        p.add_layout(LinearAxis(), 'above')

        p.background_fill_color = background_fill_color
        p.background_fill_alpha = 0.5
        p.xgrid.grid_line_width =  grid_line_width
        p.xgrid.grid_line_color =  grid_line_color
        p.xgrid.grid_line_alpha =  grid_alpha
        p.ygrid.grid_line_width =  grid_line_width
        p.ygrid.grid_line_color =  grid_line_color
        p.ygrid.grid_line_alpha =  grid_alpha
        p.min_border_left = 40
        p.title.text_font_size = '14pt'

        p.x_range = Range1d(xlim_padded[0] - 0.1*xlim_diff,
                            xlim_padded[1] + 0.1*xlim_diff,
                            max_interval=2*(xlim_padded[1]-xlim_padded[0]),
                            min_interval=0.25
                            )
        p.y_range = Range1d(ylim_padded[0] - 0.1*ylim_diff,
                            ylim_padded[1] + 0.1*ylim_diff,
                            max_interval=2*(ylim_padded[1]-ylim_padded[0]),
                            min_interval=0.25
                            )
        #p.x_range.range_padding = 100
        #Zp.y_range.range_padding = 100
        p.x_range.bounds = list(1.5*xlim_padded) #'auto'
        p.y_range.bounds = list(1.5*ylim_padded) #'auto'


        p.line([0, 0], ylim_padded, line_width=0)
        p.line(xlim_padded,[0, 0],  line_width=0)
        p.add_layout(Arrow(end=NormalHead(size = 10, fill_color= axes_color, line_color = axes_color, line_alpha=0.5, fill_alpha=0.6),
                                          x_start= xlim_padded[0],
                                          y_start=0,
                                          x_end=xlim_padded[1],
                                          y_end=0,
                                          line_width=3,
                                          line_color = axes_color,
                                          line_alpha=0.6)
                                          )

        p.add_layout(Arrow(end=NormalHead(size = 10, fill_color=axes_color, line_color = axes_color,line_alpha=0.5, fill_alpha=0.6),
                                          y_start = ylim_padded[0],
                                          y_end=ylim_padded[1],
                                          x_start=0, x_end=0,
                                          line_width=3,
                                          line_color = axes_color,
                                          line_alpha=0.6)
                                          )

        p.patch(self.house_left["wall"][0], self.house_left["wall"][1], color=self.house_colors["wall"], alpha=alpha, line_width=2)
        p.patch(self.house_left["roof"][0], self.house_left["roof"][1], color=self.house_colors["roof"], alpha=alpha, line_width=2)
        p.patch(self.house_left["door"][0], self.house_left["door"][1], color=self.house_colors["door"], alpha=alpha, line_width=2)
        p.patch(self.house_left["window"][0], self.house_left["window"][1], color=self.house_colors["window"], alpha=alpha, line_width=2)



        q = bk.figure(plot_width=plot_height,
                      plot_height=plot_height,
                      y_axis_location="left",
                      title="After transformation",
                      match_aspect=True,
                      x_range=p.x_range,
                      y_range=p.y_range,
                      tools="pan, wheel_zoom, box_zoom,reset"
                      )
        q.add_layout(LinearAxis(), 'right')
        q.add_layout(LinearAxis(), 'above')


        q.background_fill_color = background_fill_color
        q.background_fill_alpha = 0.5
        q.xgrid.grid_line_width =  grid_line_width
        q.xgrid.grid_line_color =  grid_line_color
        q.xgrid.grid_line_alpha =  grid_alpha
        q.ygrid.grid_line_width =  grid_line_width
        q.ygrid.grid_line_color =  grid_line_color
        q.ygrid.grid_line_alpha =  grid_alpha
        q.min_border_left = 40
        q.title.text_font_size = '14pt'


        q.add_layout(Arrow(end=NormalHead(size = 10, fill_color= axes_color, line_color = axes_color, line_alpha=0.5, fill_alpha=0.6),
                                          x_start= xlim_padded[0],
                                          y_start=0,
                                          x_end=xlim_padded[1],
                                          y_end=0,
                                          line_width=3,
                                          line_color = axes_color,
                                          line_alpha=0.6)
                                          )


        q.add_layout(Arrow(end=NormalHead(size = 10, fill_color=axes_color, line_color = axes_color,line_alpha=0.5, fill_alpha=0.6),
                                          y_start = ylim_padded[0],
                                          y_end=ylim_padded[1],
                                          x_start=0, x_end=0,
                                          line_width=3,
                                          line_color = axes_color,
                                          line_alpha=0.6)
                                          )

        # add a patch renderer with an alpha an line width
        q.patch(self.house_right["wall"][0], self.house_right["wall"][1], color=self.house_colors["wall"], alpha=alpha, line_width=2)
        q.patch(self.house_right["roof"][0], self.house_right["roof"][1], color=self.house_colors["roof"], alpha=alpha, line_width=2)
        q.patch(self.house_right["door"][0], self.house_right["door"][1], color=self.house_colors["door"], alpha=alpha, line_width=2)
        q.patch(self.house_right["window"][0], self.house_right["window"][1], color=self.house_colors["window"], alpha=alpha, line_width=2)

        q.line([0, 0], ylim_padded, line_width=3, alpha=0.6, color = axes_color)
        q.line(xlim_padded,[0, 0],  line_width=3, alpha=0.6, color = axes_color)

        bk.show(gridplot([p, q], ncols =2, toolbar_options={"logo":None}))




def matrix_t(A):
    x = house_transform_bk(A)
    x.show_house()



def animated_house(delay = 40):
    '''
    animation of matrix tranformations
    delay = frame interval

    Note: the return value must to be assigned to a variable
    so that the animation object persists.
    '''
    wall = np.array([[0,0], [1,0], [1,1], [0,1]]).T
    roof = np.array([[-0.1,1], [0.1, 1.2], [0.1, 1.5], [0.3, 1.5], [0.3, 1.4], [0.5,1.6], [1.1,1]]).T
    door =  np.array([[0.1,0], [0.4,0], [0.4,0.6], [0.1,0.6]]).T
    window =  np.array([[0.6,0.3], [0.9,0.3], [0.9,0.6], [0.6,0.6]]).T
    house = [(wall, 'cadetblue'), (roof, 'orangered'), (door, 'tan'), (window, 'white')]

    fig = plt.figure(figsize = (5,5))
    fig.patch.set_alpha(0)
    plt.tight_layout()
    plt.style.use('seaborn')

    ax1 = plt.gca()
    ax1.axis('equal')
    xmax, ymax = 2.5, 2.5
    xmin, ymin = -2.5, -2.5
    house_fills = []
    for (s, c) in  house:
        shape, = ax1.fill(*list(s), c)
        house_fills.append(shape)
    ax1.plot([0, 0], [ymin, ymax], 'k')
    ax1.plot([xmin, xmax], [0, 0], 'k')

    def update_plot(t):
        A = np.array([[cos(t)**3, (1+t/(2*pi))*sin(t)**3], [(1-2*t/(2*pi))*sin(t)**3, cos(t)**3]])
        for i in range(len(house)):
            nshape = np.dot(A, house[i][0]).T
            house_fills[i].set_xy(nshape)
        return house_fills

    ani = FuncAnimation(fig, func = update_plot, frames=np.linspace(0, 2*pi, 100), interval=delay, blit=True, repeat=True)

    plt.show()
    return ani
