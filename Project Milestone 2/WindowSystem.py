#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Window System - Submission
by  Student Name 1 (#999999)
and Student Name 2 (#999999)
"""

from GraphicsEventSystem import *
from Window import *

class WindowSystem(GraphicsEventSystem):
    def start(self):
        pass
    
    
    """
    WINDOW MANAGEMENT
    """
        
    def createWindowOnScreen(self, x, y, width, height, identifier):
        return None
    
    def bringWindowToFront(self, window):
        pass

    
    
    """
    DRAWING
    """
    
    def handlePaint(self):
        pass
    
    
    """
    INPUT EVENTS
    """
    
    def handleMousePressed(self, x, y):
        pass
        
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