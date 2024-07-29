# DIS2
This project is part of the course "Designing Interactive Systems".
There were 4 milestones in total, and you can find the last version in the folder Project Milestone 4.


# Window System Project

## Project Overview

This project has evolved from a simple multilingual greeting application to a sophisticated window system. Developed as part of a course assignment, it consists of multiple milestones, each building upon the previous one to create a more complex and feature-rich application.

## Milestone 3: Advanced Window Management

The third milestone introduces advanced window management features, significantly enhancing the functionality and user interaction of the window system.

### New Features:

1. **Window Manager**
   - Manages window decorations (title bar, minimize, maximize, and close buttons)
   - Handles window dragging and positioning
   - Implements a taskbar for easy window management

2. **Enhanced Window Functionality**
   - Window minimizing and hiding
   - Window closing
   - Bringing windows to the front
   - Proper z-order management

3. **Desktop Environment**
   - Implementation of a desktop background
   - Taskbar displaying all open windows

4. **Improved Event Handling**
   - More sophisticated mouse event handling (pressed, released, dragged)
   - Window-specific event handling

### Key Components:

1. **WindowSystem Class**
   - Main class managing the overall system
   - Handles painting and input events
   - Manages window hierarchy and z-order

2. **WindowManager Class**
   - Manages window decorations and taskbar
   - Handles window positioning and dragging logic
   - Implements desktop drawing

3. **Window Class**
   - Represents individual windows
   - Enhanced with visibility toggle (isHidden property)
   - Improved drawing method

4. **Screen Class**
   - Represents the main screen
   - Implements desktop and taskbar drawing

### Functionality:
- Window Decoration: Title bars with minimize, maximize, and close buttons
- Window Dragging: Users can drag windows by their title bars
- Window State Management: Windows can be minimized, closed, or brought to the front
- Taskbar: Shows all open windows and allows quick access
- Desktop: Implements a desktop background

### How it works:
1. The WindowSystem initializes with a screen, WindowManager, and sample windows.
2. Windows are drawn with decorations (title bar, buttons) managed by the WindowManager.
3. User interactions (clicking, dragging) are handled to manage window states and positions.
4. The taskbar shows all open windows and allows for easy window management.
5. Windows respect z-order, with the ability to bring windows to the front.

## How to Run

To run the Window System:
1. Ensure you have Python 3.x installed on your system.
2. Make sure you have the required dependencies (GraphicsEventSystem).
3. Save the provided code in separate files (`WindowSystem.py`, `Window.py`, and `WindowManager.py`).
4. Run the script using Python: `python WindowSystem.py`

## Dependencies
- Python 3.x
- GraphicsEventSystem (custom module, ensure it's in the same directory or in the Python path)

## Authors
- Filiz Günal (#431174)
- Samuel Kwong (#430273)

## Next Steps
Future developments could include:
- Window resizing functionality
- More advanced desktop features (icons, right-click menus)
- Custom window content and applications

This project now represents a basic but functional window management system, demonstrating key concepts in GUI programming and event handling.
