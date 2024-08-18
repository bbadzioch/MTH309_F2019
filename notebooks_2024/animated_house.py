import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation, ImageMagickWriter
from math import sin, cos, pi


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
    plt.style.use('seaborn-v0_8')

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
    return ani
