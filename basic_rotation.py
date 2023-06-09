import tkinter as tk
import numpy as np
from math import pi

# Set up some constants
WIDTH, HEIGHT = 800, 600
SPEED = 5
ROT_SPEED = 0.02

# Set up the airplane
airplane_position = [WIDTH // 2, HEIGHT // 2, 0]
airplane_size = 100
airplane_rotation = [0, 0, 0]  # Pitch, yaw, roll

# Define the airplane's vertices
vertices = [
    (0, 0, 2),  # Nose
    (-1, 1, -2), (1, 1, -2),  # Wings
    (0, -1, -2),  # Tail
    (-0.5, 0.5, -2), (0.5, 0.5, -2),  # Inner wings
    (0, 0, -2)  # Inner tail
]

# Define the airplane's edges
edges = [
    (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6),  # Nose to everything
    (1, 2), (1, 3), (1, 4), (2, 3), (2, 5),  # Wings to everything
    (3, 6), (4, 5), (4, 6), (5, 6)  # Tail and inner wings
]

# Create the window
root = tk.Tk()

# Create the canvas
canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="black")
canvas.pack()

def rotate(point, angles):
    x, y, z = point
    pitch, yaw, roll = angles

    # Rotate around x-axis (pitch)
    y, z = y * np.cos(pitch) - z * np.sin(pitch), y * np.sin(pitch) + z * np.cos(pitch)

    # Rotate around y-axis (yaw)
    x, z = x * np.cos(yaw) + z * np.sin(yaw), -x * np.sin(yaw) + z * np.cos(yaw)

    # Rotate around z-axis (roll)
    x, y = x * np.cos(roll) - y * np.sin(roll), x * np.sin(roll) + y * np.cos(roll)

    return x, y, z

def draw_airplane():
    # Clear the canvas
    canvas.delete("all")

    rotated_vertices = [rotate(vertex, airplane_rotation) for vertex in vertices]

    projected_points = []
    for x, y, z in rotated_vertices:
        # Project the 3D point to 2D
        x3d = airplane_size * x
        y3d = airplane_size * (y + airplane_position[2] / airplane_size)
        z3d = airplane_size* z
        x2d = x3d / (4 - z3d / 200)
        y2d = y3d / (4 - z3d / 200)

        projected_points.append((airplane_position[0] + int(x2d), airplane_position[1] + int(y2d)))

    for edge in edges:
        canvas.create_line(projected_points[edge[0]], projected_points[edge[1]], fill="white")

    # Schedule the next update
    root.after(1000 // 60, draw_airplane)  # 60 FPS

def move_airplane(event):
    if event.keysym == "Left":
        airplane_position[0] -= SPEED
    if event.keysym == "Right":
        airplane_position[0] += SPEED
    if event.keysym == "Up":
        airplane_position[1] -= SPEED
    if event.keysym == "Down":
        airplane_position[1] += SPEED
    if event.char == "a":
        airplane_position[2] -= SPEED
    if event.char == "d":
        airplane_position[2] += SPEED
    if event.char == "q":
        airplane_rotation[0] += ROT_SPEED  # Pitch
    if event.char == "w":
        airplane_rotation[0] -= ROT_SPEED  # Pitch
    if event.char == "e":
        airplane_rotation[1] += ROT_SPEED  # Yaw
    if event.char == "r":
        airplane_rotation[1] -= ROT_SPEED  # Yaw
    if event.char == "t":
        airplane_rotation[2] += ROT_SPEED  # Roll
    if event.char == "y":
        airplane_rotation[2] -= ROT_SPEED  # Roll

# Bind the keyboard events
root.bind("<Key>", move_airplane)

# Start the game loop
draw_airplane()

root.mainloop()
