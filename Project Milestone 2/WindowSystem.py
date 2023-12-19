#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Window System - Submission
by  Samuel Kwong (#430273)
and Filiz Günal (#431174)
"""
from collections import deque

from GraphicsEventSystem import *
from Window import *

class WindowSystem(GraphicsEventSystem):
    def start(self):
        #self.rootId = 0
        #self.rootWindow = Window(0,0,800,600,id)
        self.screen = Screen(self)
        window4 = Window(100, 100, 600, 400, "WINDOW_4")
        window4.backgroundColor = COLOR_GREEN
        self.screen.addChildWindow(window4)

        window1 = Window(20, 20, 400, 400, "WINDOW_1")
        window1.backgroundColor = COLOR_BLACK
        window2 = Window(20, 20, 200, 200, "WINDOW_2")
        window2.backgroundColor = COLOR_RED
        window1.addChildWindow(window2)
        window3 = Window(20, 240, 200, 140, "WINDOW_3")
        window3.backgroundColor = COLOR_BLUE
        window1.addChildWindow(window3)
        self.screen.addChildWindow(window1)

    
    
    """
    WINDOW MANAGEMENT
    """
        
    def createWindowOnScreen(self, x, y, width, height, identifier):
        window = Window(x, y, width, height, identifier)
        self.screen.childWindows.append(window)
        return window
    
    def bringWindowToFront(self, window):
        currentWindow = window

        # Check if the current window is a top level window
        is_top_level_window = False
        if currentWindow.parentWindow.identifier == "SCREEN_1":
            is_top_level_window = True

        # While the window is not a top level window, go to parent window and get its x and y
        while not is_top_level_window:
            # Update the current window to the parent window
            currentWindow = currentWindow.parentWindow
            # Check if the new current window is a top level window or not, if it is then we do not go back into loop next iteration
            if currentWindow.parentWindow.identifier == "SCREEN_1":
                is_top_level_window = True

        self.screen.childWindows.append(self.screen.childWindows.pop(self.screen.childWindows.index(currentWindow)))
        self.requestRepaint()



    
    
    """
    DRAWING
    """

    def handlePaint(self):
        self.graphicsContext.setOrigin(self.screen.x, self.screen.y)
        self.graphicsContext.setFillColor(self.screen.backgroundColor)
        self.graphicsContext.fillRect(self.screen.x, self.screen.y,
                                       self.screen.width, self.screen.height)

        windowStack = deque([])
        preordered_windows = []
        preordered_windows.append(self.screen.identifier)
        windowStack.append(self.screen)
        while len(windowStack) > 0:
            visited = False
            # Window at the top of the stack has no children
            if len((windowStack[len(windowStack) - 1]).childWindows) == 0:
                windowStack.pop()
            # Window at the top of the stack has children
            else:
                parentWindow = windowStack[len(windowStack) - 1]
            # If child window has not been visited, then push to stack and to the preordered windows list
            # Paint it on the screen, relative to the parent window, break out of loop and
            for i in range(0, len(parentWindow.childWindows)):
                if parentWindow.childWindows[i].identifier not in preordered_windows:
                    visited = True
                    windowStack.append(parentWindow.childWindows[i])
                    preordered_windows.append(parentWindow.childWindows[i].identifier)
                    self.graphicsContext.setOrigin(parentWindow.x, parentWindow.y)
                    self.graphicsContext.setFillColor(parentWindow.childWindows[i].backgroundColor)
                    self.graphicsContext.fillRect(parentWindow.childWindows[i].x, parentWindow.childWindows[i].y,
                                                       parentWindow.childWindows[i].x + parentWindow.childWindows[i].width, parentWindow.childWindows[i].y + parentWindow.childWindows[i].height)
                    break
            if not visited:
                windowStack.pop()

    
    """
    INPUT EVENTS
    """
    
    def handleMousePressed(self, x, y):
        deepestVisibleWindow = self.screen.childWindowAtLocation(x,y)
        if deepestVisibleWindow:
            self.bringWindowToFront(deepestVisibleWindow)

        
    def handleMouseReleased(self, x, y):
        pass
        
    def handleMouseMoved(self, x, y):
        pass
        
    def handleMouseDragged(self, x, y):
        pass
        
    def handleKeyPressed(self, char):
        pass
        
    
    
        
    
# Let's start your window system!
w = WindowSystem(800,600)