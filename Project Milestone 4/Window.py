#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Window System - Submission
by  Samuel Kwong (#430273)
and Filiz Günal (#431174)
"""

from collections import deque
from GraphicsEventSystem import *
from collections import namedtuple

import Window

AllAnchors = namedtuple('AllAnchors', "top right bottom left")
LayoutAnchor = AllAnchors(1 << 0, 1 << 1, 1 << 2, 1 << 3)
MIN_WINDOW_WIDTH = 304
MIN_WINDOW_HEIGHT = 420

class Window:
    def __init__(self, originX, originY, width, height, identifier):
        self.x = originX
        self.y = originY
        self.width = width
        self.height = height
        self.identifier = identifier
        self.backgroundColor = COLOR_LIGHT_GRAY

        # Indicates whether window is visible
        self.isHidden = False
        # Indicates whether window is being dragged
        self.isDraggable = False
        # Indicates whether the cursor is over the resizing tab
        self.isResizing = False

        self.childWindows = []
        self.parentWindow = None

        # Default layout anchor
        self.layoutAnchors = LayoutAnchor.top | LayoutAnchor.left

        
    def addChildWindow(self, window):
        self.childWindows.append(window)
        window.parentWindow = self
        
    def removeFromParentWindow(self):
        self.parentWindow.childWindows.remove(self)
        self.parentWindow = None

    def childWindowAtLocation(self, x, y):

        windowStack = deque([])
        preordered_windows = []
        preordered_windows.append(self.identifier)
        windowStack.append(self)

        # Will return none if the window has no children
        deepestWindow = None

        # Pre order traversal, saves the window as the deepest window if it is the last element in tree and has no more children
        while (len(windowStack)):
            visited = False
            # Window at the top of the stack has no children
            if len((windowStack[len(windowStack) - 1]).childWindows) == 0:
                windowStack.pop()
            # Window at the top of the stack has children
            else:
                parentWindow = windowStack[len(windowStack) - 1]
            # If child window has not been visited, then push to stack and to the preordered windows list
            # Returns the deepest visible window
            if len(windowStack) > 0:
                for childWindow in parentWindow.childWindows:
                    if childWindow.identifier not in preordered_windows:
                        visited = True
                        windowStack.append(childWindow)
                        preordered_windows.append(childWindow.identifier)
                        localX, localY = childWindow.convertPositionFromScreen(x, y)
                        if childWindow.hitTest(localX, localY) and not childWindow.isHidden:
                            deepestWindow = childWindow
                        break
                if not visited:
                    windowStack.pop()
        return deepestWindow


    # Checks if the window is hit by the cursor
    def hitTest(self, x, y):
        if self.x <= x <= self.x + self.width and self.y <= y <= self.y + self.height:
            return True
        else:
            return False

    def convertPositionToScreen(self, x, y):
        pos_x = x
        pos_y = y
        currentWindow = self

        #Check if the current window is a top level window
        not_top_level_window = True
        if currentWindow.parentWindow.identifier == "SCREEN_1":
            not_top_level_window = False

        # While the window is not a top level window, go to parent window and get its x and y
        while not_top_level_window:
            # Update the current window to the parent window
            currentWindow = currentWindow.parentWindow
            pos_x += currentWindow.x
            pos_y += currentWindow.y
            # Check if the new current window is a top level window or not, if it is then we do not go back into loop next iteration
            if currentWindow.parentWindow.identifier == "SCREEN_1":
                not_top_level_window = False

        return (pos_x,pos_y)
    
    def convertPositionFromScreen(self, x, y):
        pos_x = x
        pos_y = y
        currentWindow = self

        # Check if the current window is a top level window
        not_top_level_window = True
        if currentWindow.parentWindow.identifier == "SCREEN_1":
            not_top_level_window = False

        # While the window is not a top level window, go to parent window and get its x and y
        while not_top_level_window:
            # Update the current window to the parent window
            currentWindow = currentWindow.parentWindow
            pos_x -= currentWindow.x
            pos_y -= currentWindow.y
            # Check if the new current window is a top level window or not, if it is then we do not go back into loop next iteration
            if currentWindow.parentWindow.identifier == "SCREEN_1":
                not_top_level_window = False

        return (pos_x, pos_y)

    def resize(self, x, y, width, height):

        # Top level window width and height changes
        deltaWidth = width - self.width
        deltaHeight = height - self.height

        # Handles case for resizing the top level window
        if self.parentWindow.identifier == "SCREEN_1":
            # the new width has to be greater than the minimum window width and less than the parent window's width
            if MIN_WINDOW_WIDTH <= width <= self.parentWindow.width:
                self.width = width
            # otherwise, we do not change the width
            else:
                deltaWidth = 0
            # the new height has to be greater than the minimum window height and less than the parent window's height
            if MIN_WINDOW_HEIGHT <= height <= self.parentWindow.height:
                self.height = height
            # otherwise, we do not change the height
            else:
                deltaHeight = 0
        else:
            self.x = x
            self.width = width

            self.y = y
            self.height = height

        for childWindow in self.childWindows:
            #Resize the child window's local coordinates by the change in cursor position

            newWindowX = childWindow.x
            newWindowY = childWindow.y
            newWindowWidth = childWindow.width
            newWindowHeight = childWindow.height

            #Left Anchor
            if childWindow.layoutAnchors & LayoutAnchor.left:
                pass
            # Right Anchor, add deltaWidth to the child window's x position
            if childWindow.layoutAnchors & LayoutAnchor.right:
                newWindowX += deltaWidth
            # Top Anchor
            if childWindow.layoutAnchors & LayoutAnchor.top:
                pass
            # Bottom Anchor, add deltaHeight to the child window's y position
            if childWindow.layoutAnchors & LayoutAnchor.bottom:
                newWindowY += deltaHeight
            # Left and Right Anchor set, should stretch horizontally,
            if childWindow.layoutAnchors & LayoutAnchor.left and childWindow.layoutAnchors & LayoutAnchor.right:
                newWindowX -= deltaWidth
                newWindowWidth += deltaWidth
            # Top and bottom anchor set, should stretch vertically
            if childWindow.layoutAnchors & LayoutAnchor.top and childWindow.layoutAnchors & LayoutAnchor.bottom:
                newWindowY -= deltaHeight
                newWindowHeight += deltaHeight
            childWindow.resize(newWindowX, newWindowY, newWindowWidth, newWindowHeight)


    
    def draw(self, ctx):
        ctx.setOrigin(0, 0)
        localX, localY = self.convertPositionToScreen(self.x, self.y)
        ctx.setFillColor(self.backgroundColor)
        ctx.fillRect(localX, localY, localX + self.width, localY + self.height)

    def handleMouseClicked(self, x, y):
        print("Window " + self.identifier + " was clicked.")




class Screen(Window):
    def __init__(self, windowSystem):
        super().__init__(0, 0, windowSystem.width, windowSystem.height, "SCREEN_1")
        self.windowSystem = windowSystem

        
    def draw(self, ctx):
        self.windowSystem.windowManager.drawDesktop(ctx)
        self.windowSystem.windowManager.drawTaskbar(ctx)


