# DIS2
This project is part of the course "Designing Interactive Systems".
There were 4 milestones in total, and you can find the last version in the folder Project Milestone 4.

---
# Window System Project with Applications

## Project Overview

This project has evolved from a simple multilingual greeting application to a sophisticated window system with multiple built-in applications. Developed as part of a course assignment, it consists of multiple milestones, each building upon the previous one to create a more complex and feature-rich application environment.

## Milestone 4: Integrated Applications

The fourth milestone introduces several applications that run within the window system, demonstrating the versatility and functionality of the platform.

### New Features:

1. **User Interface Toolkit (UITK)**
   - Implements a set of reusable UI components
   - Includes Widget, Container, Label, Button, and Slider classes

2. **HelloWorld Application**
   - A multilingual greeting application
   - Allows users to select a language and displays a greeting

3. **Colors Application**
   - An RGB color mixer
   - Uses sliders to adjust red, green, and blue values
   - Displays the resulting color and its hex code

4. **Calculator Application**
   - A fully functional calculator
   - Supports basic arithmetic operations
   - Includes a clear function and sign change option

### Key Components:

1. **UITK (User Interface Toolkit)**
   - `Widget`: Base class for UI elements
   - `Container`: Manages layout of child widgets
   - `Label`: Displays text
   - `Button`: Clickable element with customizable actions
   - `Slider`: Allows value selection within a range

2. **HelloWorld Class**
   - Implements a language selection interface
   - Displays greetings in multiple languages

3. **Colors Class**
   - Implements an RGB color mixer
   - Uses sliders for adjusting color values
   - Displays real-time color preview and hex code

4. **Calculator Class**
   - Implements a full calculator interface
   - Supports basic arithmetic operations
   - Includes error handling for invalid expressions

### Functionality:
- Window Management: Create and manage multiple application windows
- User Interface: Consistent UI elements across applications
- Inter-application Communication: Applications can interact with the window system

### How it works:
1. The WindowSystem initializes with the capability to launch multiple applications.
2. Users can open different applications (HelloWorld, Colors, Calculator) in separate windows.
3. Each application utilizes the UITK components for its user interface.
4. Applications handle their own logic and update their UI accordingly.

## How to Run

To run the Window System with applications:
1. Ensure you have Python 3.x installed on your system.
2. Make sure you have the required dependencies (GraphicsEventSystem and any other custom modules).
3. Save all provided code files in the same directory.
4. Run the main script (likely `WindowSystem.py`) using Python: `python WindowSystem.py`

## Dependencies
- Python 3.x
- GraphicsEventSystem (custom module)
- Any additional custom modules (e.g., UITK.py)

## Authors
- Filiz Günal (#431174)
- Samuel Kwong (#430273)

This project now represents a functional window system with multiple integrated applications, demonstrating advanced concepts in GUI programming, event handling, and application design within a custom windowing environment.

