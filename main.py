import pkg_resources

needed = ['pynput', 'matplotlib', 'pyautogui', 'numpy']
package_list = [dist.project_name for dist in pkg_resources.working_set]

def is_package_installed(package_name):
    global package_list
    return package_name in package_list

def check_packages():
    for pkg in needed:
        if not is_package_installed(pkg):
            os.system(f'pip install {pkg}')
    


from pyautogui import size 
from pynput import mouse 
import os
import time
from dataclasses import dataclass
from pynput.mouse import Button
import matplotlib.pyplot as plt
import numpy as np 


@dataclass(slots=True)
class File:
    data = f"{os.getcwd()}\\data.txt"
    clicks = f'{os.getcwd()}\\fortnite_clicks.txt'
    append = 'a'
    write = 'w'


@dataclass(slots=True)
class Position(object):
    x: int
    y: int 
    

@dataclass(slots=True)
class TimePosition(Position):
    ctime = time.ctime()


@dataclass(slots=True)
class TimePositionButton(TimePosition):
    pressed: bool
    button: Button


@dataclass(slots=True)
class Data:
    time_position = 'TPX'
    time_position_button = 'TPBX'
    

class DataGraph:
    pass 


class GraphedTimePosition:
    def __init__(self, parent: DataGraph) -> None:
        self.parent = parent 
        self.xlabel='(X) Pixel Distances from left side of Monitor'
        self.ylabel='(Y) Pixel Distances from top side of monitor'
        self.clabel = "Times of recorded clicks"
        self.title = "Position X and Position Y of Mouse Clicks Over Time"
        self.plt_scatter = None
        self.fig, self.ax = plt.subplots()
        self.scatter = self.ax.scatter([],[])
    
    def update_plot(self):
        self.scatter.set_offsets(list(zip(self.parent.xs, self.parent.ys)))
        plt.draw()
        
    def draw(self):
        self.plt_scatter = plt.scatter(self.parent.xs, self.parent.ys, c=self.parent.times, cmap='cool', alpha=.75)
        self.plt_scatter.set_edgecolor(c='green') 
        plt.title("Position X and Position Y of Mouse Clicks Over Time")
        plt.xlabel(xlabel='Pixel Distances from left side of Monitor')
        plt.ylabel(ylabel='Pixel Distances from top side of monitor')
        plt.clabel("Times of recorded clicks")
        self.plt_scatter.draw()
    
        
class GraphedTimePositionButton:
    def __init__(self, parent: DataGraph) -> None:
        self.screen_width, self.screen_height = size()
        self.parent = parent
        self.title  = 'Mouse Button Click and Position at Clock Time'
        self.xlabel = "X Position of the Mouse When Clicked"
        self.ylabel = 'Y Position of the Mouse When Clicked'
        self.clabel = 'Time of Mouse Clicked'
        self.tlabel = 'Which Mouse Button Was Clicked'
        self.scatter = None
        self.presentation = None 
        self.__x = np.array(self.parent.xs)
        self.__y = np.array(self.parent.ys)
        self.__t = np.array(self.parent.times)
        self.__b = np.array(self.parent.buttons)
        self.list_lists = [self.parent.xs, self.parent.ys, self.parent.times, self.parent.buttons]
        self.list_arrays = [self.__x, self.__y, self.__t, self.__b]
        self.length_xs = len(self.__x)
        self.length_ys = len(self.__y)
        self.length_ts = len(self.__t)
        self.length_bs = len(self.__b)
        self.lengths = [self.length_xs, self.length_ys, self.length_ts, self.length_bs]
        self.maximum_length = 0 
        self.__get_max_length()
        self.__fix_arrays()
        
    def __get_max_length(self):
        for length in self.lengths:
            if length > self.maximum_length:
                self.maximum_length = length
    
    def __make_arrays(self):
        self.__x = np.array(self.list_lists[0])
        self.__y = np.array(self.list_lists[1])
        self.__t = np.array(self.list_lists[2])
        self.__b = np.array(self.list_lists[3])
        self.list_arrays = [self.__x, self.__y, self.__t, self.__b]
        
        
    def __make_lengths(self):
        self.length_xs = len(self.__x)
        self.length_ys = len(self.__y)
        self.length_ts = len(self.__t)
        self.length_bs = len(self.__b)
        self.lengths = [self.length_xs, self.length_ys, self.length_ts, self.length_bs]
    
    def __fix_arrays(self):
        for index, length in enumerate(self.lengths):
            if length != self.maximum_length:
                self.new_length = len(self.list_lists[index])
                while self.new_length != self.maximum_length:
                    self.alist = self.list_lists[index]
                    self.list_lists[index] = self.alist + ['None']
                    self.new_length = len(self.list_lists[index])
        self.__make_arrays()
                    
            
    def draw(self):
        if self.scatter == None:
            self.__make_arrays()
            self.__make_lengths()
            self.__get_max_length()
            self.__fix_arrays()
            self.infos = [f"{x} {self.list_lists[2][index]}" for index, x in enumerate(self.list_lists[3])]
            li = list(zip(self.list_lists[0], self.list_lists[1]))
            self.scatter = plt.scatter(*zip(*li), cmap='cool', alpha=0.75)
            plt.xlabel(self.xlabel)
            plt.ylabel(self.ylabel)
            plt.title(self.title)
            plt.colorbar(self.scatter)
            
            plt.show()


class TimePositionData(DataGraph):
    def __init__(self) -> None:
        self.times = []
        self.ys = []
        self.xs = []
        self.variant = Data.time_position
        self.graph = None
        self.graphed = False
        self.has_data = False
        
    def time_position_data(self, tp: TimePosition) -> None:
        self.has_data = True
        self.times = self.times +  [tp.ctime]
        self.ys = self.ys + [tp.y]
        self.xs = self.xs + [tp.x]
    
    def get_graph(self):
        if self.has_data:
            if self.variant == Data.time_position:
                self.graph = GraphedTimePosition()
                self.graphed = True
            elif self.variant == Data.time_position_button:
                self.graph = GraphedTimePositionButton(parent=self)
                self.graphed = True
            else:
                pass 
        
    def draw_graph(self):
        if self.graphed:
            self.graph.draw()
            
    
class ButtonTimePositionData(TimePositionData):
    def __init__(self) -> None:
        super().__init__()
        self.buttons = []
        self.variant = Data.time_position_button
        
    def time_position_button_data(self, tpb: TimePositionButton) -> None:
        self.has_data = True
        self.times = self.times +  [tpb.ctime]
        self.ys = self.ys + [tpb.y]
        self.xs = self.xs + [tpb.x]
        self.buttons = self.buttons + [tpb.button]


class ClickTracker:
    """ Tracks the Mouse position over time and which button is pressed """
    
    def __init__(self) -> None:
        self.data = ButtonTimePositionData()
        self.amount = 0
        self.running = False
        self.listener = None
        
    def on_click(self, x: int, y: int, button:Button, pressed:bool) -> bool:
        """ When the mouse is clicked this method is called """
        self.new_data = TimePositionButton(x=x, 
                                           y=y, 
                                           pressed=pressed, 
                                           button=button)
        self.data.time_position_button_data(self.new_data)
        self.amount = self.amount - 1
        print(f'--> {self.new_data.button} @ {self.new_data.ctime} # ( X:{self.new_data.x} Y:{self.new_data.y} )')
        print(f'clicks left: {self.amount}')
        if self.amount < 1:
            return False
        else:
            return True

        
    def start(self, amount=10):
        """ 
        starts the tracker with amount of clicks left to track, 
        default is ten, when the amount reaches 0, the plot is 
        graphed and the tracker is stopped 
        """
        self.amount = amount*2
        self.running = True
        with mouse.Listener(on_click=self.on_click) as self.listener:
            self.listener.join()
            self.data.get_graph()
            self.data.draw_graph()

def track100clicks():
    print('[ tracking 100 mouse clicks ]')
    ct = ClickTracker()
    ct.start(amount=100)


def test():
    tracker = ClickTracker()
    tracker.start()



if __name__ == '__main__':
    tracker = ClickTracker()
    tracker.start()
