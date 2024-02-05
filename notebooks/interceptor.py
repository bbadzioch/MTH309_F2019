import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import TextBox
import numpy as np
from sympy import *
init_printing(use_latex='mathjax')


class interceptor():

    sol_range = (1, 15)     # range of possible solutions
    tv_range = (1, 30)      # range of coorinates of the target velocity vector
    mv = np.array([0,4])    # velocity vector of the missile
    mp0 = np.array([0,0])   # initial position of the missile
    font = 'monospace'
    figsize = (6,6)
    color = "lime"

    launched = False        # flag inticating if the missile launch time has been entered by the user
    t0 = 0                  # missile launch time


    def __init__(self, q=None):
        # select the velocity and the initial position of the target
        self.tp0 = np.array([0, 0])    # position of the target
        self.tv0 = np.array([0, 0])    # velocity vector of the target

        # select target velocity and problem solution at random
        # check if these choices are reasonable; if not try again
        while self.tp0[1] <= 0 or self.tv0[0] == 0:
            self.tv0 = self.choose_tv()
            # self.sol is the solution vector
            # self.sol[1] is the correct launch time of the missile
            # self.sol[0] is the duration of the flight is the missile to the inteception point
            self.sol = self.choose_sol()
            self.tp0 = self.sol[0]*self.mv - np.sum(self.sol)*self.tv0 # initial position of the target
           
        self.code = int(self.tp0.sum() + self.tv0.sum()) % 31
        
        
        # limits of plot axes
        self.xmax = abs(self.tp0[0]) + 10
        self.xmin = (-1)*abs(self.tp0[0]) -10
        self.ymax = max(abs(self.tp0[1]), self.sol[0]*self.mv[1]) +15
        self.ymin = -1
        self.start_game(q)
        
   
        
    def start_game(self, q=None):
    
        # reset initial values
        self.tp = self.tp0.copy()
        self.tv = self.tv0.copy()
        self.mp = self.mp0.copy()
        # distance to target
        self.dist = np.linalg.norm(self.tp - self.mp)
        self.launched = False
        self.t0 = 0

        # set up plot
        self.fig = plt.figure(figsize = self.figsize)
        #main axes object
        self.ax = axbox = plt.axes([0.1, 0.15, 0.8, 0.8])
        #textbox axes object
        self.t_ax= plt.axes([0.8, 0.05, 0.1, 0.05])
        self.ax.set_facecolor('k')
        self.ax.set_xlim(self.xmin, self.xmax)
        self.ax.set_ylim(self.ymin, self.ymax)
        self.ax.grid(alpha = 0.2, color=self.color)

        # text box for entering the missile launch time
        istr = ('' if q != 'show' else str(self.sol[1]))
        self.text_box = TextBox(self.t_ax, 'Select missile launch time:  ', initial=istr)
        self.text_box.on_submit(self.missile_launch)


        #text with problem data
        text1 = 'target position         =  [{:4}, {:4}]'.format(self.tp[0], self.tp[1])
        text2 = 'target velocity vector  =  [{:4}, {:4}]'.format(self.tv[0], self.tv[1])
        text3 = '---------------------------------------'
        text4 = 'missile position        =  [{:4}, {:4}]'.format(self.mp[0], self.mp[1])
        text5 = 'missile velocity vector =  [{:4}, {:4}]'.format(self.mv[0], self.mv[1])
        
        # text for the final screen
        summary = []
        summary.append('TARGET INTERCEPTED') 
        summary.append('MISSION SUMMARY:')
        summary.append('----------------------------------------')
        summary.append('initial target position  =  [{:4}, {:4}]'.format(self.tp0[0], self.tp0[1]))
        summary.append('target velocity vector   =  [{:4}, {:4}]'.format(self.tv0[0], self.tv0[1]))
        summary.append('----------------------------------------')
        #summary.append('initial missile position =  [{:4}, {:4}]'.format(self.mp0[0], self.mp0[1]))
        #summary.append('missile velocity vector  =  [{:4}, {:4}]'.format(self.mv[0], self.mv[1]))
        #summary.append('----------------------------------------')
        summary.append('missile launch time      =  {:>2} seconds'.format(self.sol[1]))
        #summary.append('target interception time =  {:>2} seconds'.format(np.sum(self.sol)))
        #summary.append('----------------------------------------')
        summary.append('control code             =  {:>2}'.format(self.code))
        summary.append('----------------------------------------')
        summary.append('THE END') 
        self.summary_text = '\n'.join(summary)
        
        # self.text_all is the string displyed on the plot
        self.text_all = '\n'.join([text1, text2, text3, text4, text5])
        self.data_text = self.ax.text(0.05, 0.95,
                                      self.text_all,
                                      transform=self.ax.transAxes,
                                      color=self.color,
                                      family = self.font,
                                      verticalalignment = 'top',
                                     )
        #target position
        self.tp_plot, = self.ax.plot(*list(self.tp), '+', color = self.color, ms=7)
        #target velocity vector
        self.tv_plot, = self.ax.plot(*zip(list(self.tp), list(self.tp+self.tv)), self.color)
        #missile position
        self.mp_plot, = self.ax.plot(*list(self.mp), '^', color=self.color)
        #missile velocity vector
        self.mv_plot, = self.ax.plot(*zip(list(self.mp), list(self.mp+self.mv)), self.color)


        #animation
        self.ani = FuncAnimation(self.fig,
                                 func = self.update_plot,
                                 init_func= self.init_plot,
                                 cache_frame_data=False,
                                 frames=self.frames,
                                 interval=20,
                                 blit=True,
                                 repeat=False
                                )

        plt.show()
    
    
    def missile_launch(self, t0):
        '''
        function linked to the text box
        for entering missile launch time
        '''
        try:
            # check if a numerical value has been entered
            self.t0 = float(t0)
            self.launched = True
        except:
            self.text_box.set_val("")


    def choose_tv(self):
        '''
        selects a random
        target velocity vector
        '''
        return  np.random.randint(*self.tv_range, 2)

    def choose_sol(self):
        '''
        selects a random
        problem solution
        '''
        return np.random.randint(*self.sol_range, 2)


    def init_plot(self):
        '''
        initialized animation
        '''
        self.tv_plot.set_visible(False)
        self.mv_plot.set_visible(False)
        return self.data_text, self.tp_plot, self.mp_plot, self.tv_plot, self.mv_plot

    def update_plot(self, t):
        '''
        updates plot on each animation frame
        '''
        self.tv_plot.set_visible(True)
        self.mv_plot.set_visible(True)
        self.data_text.set_text(self.text_all)
        if t >= 0:
            self.tv_plot.set_visible(False)
            self.mv_plot.set_visible(False)
            self.tp_plot.set_data(*list(self.tp.T))
            self.mp_plot.set_data(*list(self.mp))

        return self.data_text, self.tp_plot, self.mp_plot, self.tv_plot, self.mv_plot

    def frames(self):
        '''
        generating fuction which
        computes data for each animation frame
        '''
        incr = 0.04    # time increment on each animation frame
        fired = False  # flag indicating if the missile has been fired
        hit = False    # flag indicating if the target has been hit

        N = 50         # number of animated particles after missile-target collision
        spread = np.array([0.02*self.xmax, 0.02*self.ymax], dtype=float) # controls the spread of particles
        fall_rate = np.array([0, -0.003*self.ymax]) # controls the fall rate of particles
        brightness = 0.95  # controls decrease in the brightness of the particles
        alpha = 1      # initial transparency of the target marker
        
        #do not animate until missile launch time has been entered
        while not self.launched:
            yield -1

        # start time count
        t = 0
        while True:
            yield t
            if not fired:
                self.text_all = 'time: {:.2f}\ntarget distance: {:.2f}\nmissile launch in {:.2f}'.format(
                    t, self.dist, self.t0 - t, )
            else:
                self.text_all = 'time: {:.2f}\ntarget distance: {:.2f}\nmissile en route'.format(t, self.dist)
            t += incr


            if not hit:
                # increment target position
                self.tp = self.tp + incr*self.tv
                if t > self.t0:
                    if not fired:
                        # just for aesthetic: a small missile back jump just before it is launched
                        self.mp = self.mp - np.array([0, 0.5])
                        fired = True
                    else:
                        # increment missile position
                        self.mp = self.mp + incr*self.mv

                    # if missile is above target or target crossed the missile axis then the missile will not hit
                    if self.tp[0] > 2 or self.mp[1] > self.tp[1] + 2:
                        self.text_all = 'time: {:.2f}\ntarget lost'.format(t)
                        
                self.dist = np.linalg.norm(self.tp - self.mp)

                # missile hit
                if self.t0 == self.sol[1] and t >= np.sum(self.sol):
                    self.tp = np.zeros((N,2), dtype=float) + self.tp - np.array([0, -0.2])
                    self.mp = self.mp + np.array([0, 0.5])
                    hit = True

            else:
                #after the hit
                # remove the missile plot
                self.mp_plot.set_visible(False)
                # replace the target by a particle cloud
                self.tp = self.tp + (np.random.rand(N, 2)-0.5)*spread + fall_rate
                self.tp_plot.set_markersize(1.5)
                alpha = min(alpha*brightness + 0.05*np.random.rand(1)[0], 1)
                self.tp_plot.set_alpha(alpha)    
                text_end = int((t - np.sum(self.sol))/incr)
                self.text_all = '\n'+ self.summary_text[:text_end]

                
if __name__ == "__main__":
    x = interceptor()
