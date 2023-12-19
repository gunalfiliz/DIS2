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
from WindowManager import *

class WindowSystem(GraphicsEventSystem):
    def start(self):
        self.deepestVisibleWindow = None
        self.isDraggable = False
        #self.rootId = 0
        #self.rootWindow = Window(0,0,800,600,id)
        
        self.screen = Screen(self)
        window4 = Window(100, 100, 600, 400, "4_WINDOW")
        #window4.backgroundColor = COLOR_GREEN
        self.screen.addChildWindow(window4)

        window1 = Window(20, 20, 400, 400, "1_WINDOW")
       # window1.backgroundColor = COLOR_BLACK
        #window2 = Window(20, 40, 200, 180, "WINDOW_2")
        #window2.backgroundColor = COLOR_RED
        #window1.addChildWindow(window2)
        #window3 = Window(20, 240, 200, 140, "WINDOW_3")
        #window3.backgroundColor = COLOR_BLACK
        #window1.addChildWindow(window3)
        self.screen.addChildWindow(window1)

        window5 = Window(150, 150, 500, 500, "5_WINDOW")
        # window4.backgroundColor = COLOR_GREEN
        self.screen.addChildWindow(window5)

        self.windowManager = WindowManager(self)
    
    
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
        self.screen.draw(self.graphicsContext)

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
                    if not parentWindow.childWindows[i].isHidden:
                        parentWindow.childWindows[i].draw(self.graphicsContext)
                        if parentWindow is self.screen:
                            self.windowManager.decorateWindow(parentWindow.childWindows[i], self.graphicsContext)
                    #self.windowManager.decorateWindow(parentWindow.childWindows[i], self.graphicsContext)
                    break
            if not visited:
                windowStack.pop()

    
    """
    INPUT EVENTS
    """



    def handleMousePressed(self, x, y):
        self.initialMousePosX = x
        self.mousePosX = x
        self.initialMousePosY = y
        self.mousePosY = y
        self.deepestVisibleWindow = self.screen.childWindowAtLocation(x,y)
        if self.deepestVisibleWindow:
            #self.deepestVisibleWindow = deepestVisibleWindow
            self.initialDeepestVisibleWindowX = self.deepestVisibleWindow.x
            self.initialDeepestVisibleWindowY = self.deepestVisibleWindow.y
            # Check if the mouse pointer press is on the window decoration
            if self.windowManager.hitDecorationTest(self.deepestVisibleWindow, x, y):
                self.isDraggable = True
            self.bringWindowToFront(self.deepestVisibleWindow)

        
    def handleMouseReleased(self, x, y):
        # Check if a window was clicked
        if self.deepestVisibleWindow:
            # if initial mouse pos and current mouse position is same
            if self.initialMousePosX == self.mousePosX and self.initialMousePosY == self.mousePosY:
                self.deepestVisibleWindow.handleMouseClicked(x, y)
                # if minimize button is pressed
                if self.windowManager.hitMinimizeTest(self.deepestVisibleWindow, x, y):
                    self.deepestVisibleWindow.isHidden = True
                # if close button is pressed
                elif self.windowManager.hitCloseTest(self.deepestVisibleWindow, x, y):
                    self.deepestVisibleWindow.removeFromParentWindow()
            # if the window is being dragged and the ending position of the drag is out of the screen, then set it to the inital window position
            if self.isDraggable and not self.windowManager.checkWindowPosition(self.deepestVisibleWindow, x, y):
                self.deepestVisibleWindow.x = self.initialDeepestVisibleWindowX
                self.deepestVisibleWindow.y = self.initialDeepestVisibleWindowY
        self.requestRepaint()
        self.deepestVisibleWindow = None
        self.isDraggable = False
        
    def handleMouseMoved(self, x, y):
        pass
        
    def handleMouseDragged(self, x, y):
        cursorDiffX = x - self.mousePosX
        cursorDiffY = y - self.mousePosY
        if self.isDraggable and self.windowManager.checkWindowPosition(self.deepestVisibleWindow, x, y):
            self.deepestVisibleWindow.x += cursorDiffX
            self.deepestVisibleWindow.y += cursorDiffY
            self.mousePosX = x
            self.mousePosY = y
            self.requestRepaint()

        
    def handleKeyPressed(self, char):
        pass
        
    
    
        
    
# Let's start your window system!
w = WindowSystem(800,600)