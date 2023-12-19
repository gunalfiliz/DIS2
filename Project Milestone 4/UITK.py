#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Window System - Submission
by  Student Name 1 (#999999)
and Student Name 2 (#999999)
"""

from GraphicsEventSystem import *
from Window import *
from enum import Enum

class Widget(Window):
	def __init__(self, originX, originY, width, height, identifier):
		super().__init__(originX, originY, width, height, identifier)
		self.backgroundColor = COLOR_CLEAR


class ContainerAxis(Enum):
	HORIZONTAL = 0
	VERTICAL = 1

class Container(Widget):
	def __init__(self, originX, originY, width, height, identifier):
		super().__init__(originX, originY, width, height, identifier)
		self.spacing = 20
		self.axis = ContainerAxis.VERTICAL
		self.layoutAnchors = LayoutAnchor.left | LayoutAnchor.right | LayoutAnchor.top | LayoutAnchor.bottom

	def resize(self, x, y, width, height):
		deltaWidth = width - self.width
		deltaHeight = height - self.height
		self.x = x
		self.width = width
		self.y = y
		self.height = height

		for idx, childWindow in enumerate(self.childWindows):
			# Resize the child window's local coordinates by the change in cursor position
			newWindowX = childWindow.x
			newWindowY = childWindow.y
			newWindowWidth = childWindow.width
			newWindowHeight = childWindow.height

			# If container axis is vertical
			if self.axis == ContainerAxis.VERTICAL:
				# Left Anchor
				if childWindow.layoutAnchors & LayoutAnchor.left:
					pass
				# Right Anchor, add deltaX to the child window's x position
				if childWindow.layoutAnchors & LayoutAnchor.right:
					newWindowX += deltaWidth
					if type(childWindow) is Slider:
						childWindow.handleX += childWindow.value * deltaWidth
				# Left and Right Anchor set, should stretch horizontally
				if childWindow.layoutAnchors & LayoutAnchor.left and childWindow.layoutAnchors & LayoutAnchor.right:
					newWindowX -= deltaWidth
					newWindowWidth += deltaWidth
					if type(childWindow) is Slider:
						childWindow.handleX -= childWindow.value * deltaWidth / 10
						childWindow.handleWidth += deltaWidth / 10
				# Top and bottom anchor set, should stretch vertically
				if childWindow.layoutAnchors & LayoutAnchor.top and childWindow.layoutAnchors & LayoutAnchor.bottom:
					newWindowY -= deltaHeight / len(self.childWindows)
					newWindowHeight += deltaHeight / len(self.childWindows)
					if type(childWindow) is Slider:
						childWindow.handleHeight += deltaHeight / len(self.childWindows)
				# Top Anchor
				if childWindow.layoutAnchors & LayoutAnchor.top:
					pass
				# Bottom Anchor, add deltaY to the child window's y position
				if childWindow.layoutAnchors & LayoutAnchor.bottom:
					newWindowY += (idx + 1) / len(self.childWindows) * deltaHeight
			# if container access is Horizontal
			elif self.axis == ContainerAxis.HORIZONTAL:
				# Left Anchor
				if childWindow.layoutAnchors & LayoutAnchor.left:
					pass
				# Right Anchor, add deltaX to the child window's x position
				if childWindow.layoutAnchors & LayoutAnchor.right:
					newWindowX += (idx + 1) / len(self.childWindows) * deltaWidth
				# Left and Right Anchor set, should stretch horizontally
				if childWindow.layoutAnchors & LayoutAnchor.left and childWindow.layoutAnchors & LayoutAnchor.right:
					newWindowX -= deltaWidth / len(self.childWindows)
					newWindowWidth += deltaWidth / len(self.childWindows)
					if type(childWindow) is Slider:
						childWindow.handleWidth += deltaWidth / 10
				# Top and bottom anchor set, should stretch vertically
				if childWindow.layoutAnchors & LayoutAnchor.top and childWindow.layoutAnchors & LayoutAnchor.bottom:
					newWindowY -= deltaHeight
					newWindowHeight += deltaHeight
					if type(childWindow) is Slider:
						childWindow.handleHeight += deltaHeight / len(self.childWindows)
				# Top Anchor
				if childWindow.layoutAnchors & LayoutAnchor.top:
					pass
				# Bottom Anchor, add deltaY to the child window's y position
				if childWindow.layoutAnchors & LayoutAnchor.bottom:
					newWindowY += deltaHeight
			childWindow.resize(newWindowX, newWindowY, newWindowWidth, newWindowHeight)

	def draw(self, ctx):
		super().draw(ctx)


class Label(Widget):
	def __init__(self, originX, originY, width, height, identifier):
		super().__init__(originX, originY, width, height, identifier)
		self.backgroundColor = COLOR_LIGHT_BLUE
		self.font_size = 18
		self.font = Font(family="Helvetica", size=self.font_size, weight="normal")
		self.textColor = COLOR_BLACK
		self.text = ""


	def draw(self, ctx):
		super().draw(ctx)
		localX, localY = self.convertPositionToScreen(self.x, self.y)

		# Draw the text on the label
		ctx.setFont(self.font)
		ctx.setStrokeColor(self.textColor)
		ctx.drawString(self.text, localX + self.width / 6, localY + self.height / 4)

class ButtonState(Enum):
	NORMAL = 0
	HOVERING = 1
	PRESSED = 2

class Button(Label):
	def __init__(self, originX, originY, width, height, identifier):
		super().__init__(originX, originY, width, height, identifier)
		self.backgroundColor = COLOR_LIGHT_GRAY
		self.action = None
		self.ButtonState = ButtonState.NORMAL

	def draw(self, ctx):
		# UI for Normal Button State
		if self.ButtonState is ButtonState.NORMAL:
			self.backgroundColor = COLOR_LIGHT_GRAY
			self.textColor = COLOR_BLACK
		# UI for Hovering Button State
		elif self.ButtonState is ButtonState.HOVERING:
			self.backgroundColor = COLOR_GRAY
			self.textColor = COLOR_BLACK
		# UI for Pressed Button State
		elif self.ButtonState is ButtonState.PRESSED:
			self.backgroundColor = "#5A5A5A"
			self.textColor = COLOR_WHITE
		super().draw(ctx)
		localX, localY = self.convertPositionToScreen(self.x, self.y)

		# Draw border around button
		ctx.setStrokeColor(COLOR_GRAY)
		ctx.strokeRect(localX, localY, localX + self.width, localY + self.height)

		# Draw Label Text
		ctx.setFont(self.font)
		ctx.setStrokeColor(self.textColor)
		ctx.drawString(self.text, localX + self.width / 6, localY + self.height / 4)

class SliderState(Enum):
	NORMAL = 0
	PRESSED = 1

class Slider(Widget):
	def __init__(self, originX, originY, width, height, identifier):
		super().__init__(originX, originY, width, height, identifier)
		self.backgroundColor = COLOR_GRAY
		self.value = 0.0
		self.handleOffset = 2
		self.handleHeight = self.height
		self.handleWidth = self.width / 10
		self.handleBackgroundColor = COLOR_LIGHT_GRAY
		self.handleBorderColor = "#5A5A5A"
		self.SliderState = SliderState.NORMAL
		self.handleX = self.x
		self.action = None


	def draw(self, ctx):
		# UI for normal slider handle
		if self.SliderState == SliderState.NORMAL:
			self.handleBackgroundColor = COLOR_LIGHT_GRAY
		# UI for pressed slider handle
		elif self.SliderState == SliderState.PRESSED:
			self.handleBackgroundColor = "#5A5A5A"
		super().draw(ctx)
		ctx.setOrigin(0, 0)
		localX, localY = self.convertPositionToScreen(self.x, self.y)

		# Draw border around slider box
		ctx.setStrokeColor("#5A5A5A")
		ctx.strokeRect(localX, localY, localX + self.width, localY + self.height)

		# Draw Handle
		localHandleX, localHandleY = self.convertPositionToScreen(self.handleX, self.y)
		ctx.setFillColor(self.handleBackgroundColor)
		ctx.fillRect(localHandleX + self.handleOffset,
					 localY + self.handleOffset,
					 localHandleX + self.handleWidth,
					 localY + self.handleHeight - self.handleOffset)
		# Draw border around handle
		ctx.setStrokeColor(self.handleBorderColor)
		ctx.fillRect(localHandleX + self.handleOffset,
					 localY + self.handleOffset,
					 localHandleX + self.handleWidth,
					 localY + self.handleHeight - self.handleOffset)

	# Test if the passed in x and y coordinates hit the handle
	def hitTest(self, x, y):
		if self.handleX + self.handleOffset <= x <= self.handleX + self.handleWidth and self.y + self.handleOffset <= y <= self.y + self.handleHeight - self.handleOffset:
			return True
		else:
			return False

	def handleSliderDragged(self, x, y):
		pass
		#print("Slider " + self.identifier + " has value " + str(self.value))
	
		