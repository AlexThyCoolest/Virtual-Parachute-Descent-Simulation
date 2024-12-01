# Virtual Parachute Descent Simulation

This Python script simulates parachute descents with different canopy shapes (circle, square, triangle) to compare virtual air times. It's part of a science fair project investigating the accuracy of virtual simulations in replicating real-life experiments.

## Features

- Interactive GUI using Pygame and Pygame GUI
- Customizable parachute parameters:
  - Shape (Circle, Square, Triangle)
  - Size
  - Payload mass
  - Coin size (as weight)
- Real-time physics simulation
- Stopwatch functionality
- Visual representation of parachute descent

## Requirements

- Python 3.x
- Pygame
- Pygame GUI

## Installation

1. Ensure Python 3.x is installed on your system.
2. Install required libraries:
   ```
   pip install pygame pygame_gui
   ```

## Usage

Run the script:
```
python app.py
```

Use the GUI controls to adjust parachute parameters and control the simulation:
- Sliders: Adjust mass, size, and coin size
- Dropdown: Select parachute shape
- Buttons: Start, Pause, and Reset the simulation

The info box displays real-time data including velocity, position, drag coefficient, elapsed time, and coin mass.

## Physics Model

The simulation uses a simplified physics model considering:
- Gravitational force
- Drag force
- Air density
- Shape-specific drag coefficients

## Limitations

- Simplified 2D representation
- Ideal conditions (no wind, constant air density)
- Limited to three basic shapes

This simulation is designed for educational purposes and may not fully replicate real-world parachute behavior.
