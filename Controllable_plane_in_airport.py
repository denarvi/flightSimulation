import tkinter as tk
import numpy as np
from numpy import pi

# Set up some constants
WIDTH, HEIGHT = 800, 600
SPEED = 5
SCALE = 5  # scaling factor for airplane size

# Set up the camera
camera_position = [WIDTH // 2, HEIGHT // 2, -5]

# Load the 3D points from the file
with open("airport.pts", "r") as f:
    points = [list(map(float, line.split())) for line in f]

# Define the airplane's vertices
vertices = [
    (0 * SCALE, 0 * SCALE, 2 * SCALE),  # Nose
    (-1 * SCALE, 1 * SCALE, -2 * SCALE), (1 * SCALE, 1 * SCALE, -2 * SCALE),  # Wings
    (0 * SCALE, -1 * SCALE, -2 * SCALE),  # Tail
    (-0.5 * SCALE, 0.5 * SCALE, -2 * SCALE), (0.5 * SCALE, 0.5 * SCALE, -2 * SCALE),  # Inner wings
    (0 * SCALE, 0 * SCALE, -2 * SCALE)  # Inner tail
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

# Initialize rotation angles
(alpha, beta, gamma) = (pi, 2*pi, 0)

def draw_points():
    # Clear the canvas
    canvas.delete("all")

    # Create rotation matrices
    alp = np.array([
        [1, 0, 0],
        [0, np.cos(alpha), -np.sin(alpha)],
        [0, np.sin(alpha), np.cos(alpha)]
    ])
    bet = np.array([
        [np.cos(beta), 0, np.sin(beta)],
        [0, 1, 0],
        [-np.sin(beta), 0, np.cos(beta)]
    ])
    gam = np.array([
        [np.cos(gamma), -np.sin(gamma), 0],
        [np.sin(gamma), np.cos(gamma), 0],
        [0, 0, 1]
    ])
    rotation_matrix = alp @ bet @ gam

    # Draw airport scene
    for x, y, z in points:
        # Apply rotation
        point = rotation_matrix @ np.array([x, y, z])
        x, y, z = point[0], point[1], point[2]
        x -= camera_position[0]
        y -= camera_position[1]
        z -= camera_position[2]
        x2d = x / (4 - y / 200)
        z2d = z / (4 - y / 200)
        canvas.create_oval(WIDTH / 2 + int(x2d) - 1, HEIGHT / 2 + int(z2d) - 1, WIDTH / 2 + int(x2d) + 1, HEIGHT / 2 + int(z2d) + 1, fill="white")

    # Draw airplane
    for edge in edges:
        point1 = np.array(vertices[edge[0]])
        point2 = np.array(vertices[edge[1]])
        # Apply rotation
        rotated_point1 = rotation_matrix @ point1
        rotated_point2 = rotation_matrix @ point2
        # Translate
        x1, y1, z1 = rotated_point1[0], rotated_point1[1], rotated_point1[2]
        x2, y2, z2 = rotated_point2[0], rotated_point2[1], rotated_point2[2]
        # Project to 2D
        x1_2d = x1 / (4 - y1 / 200)
        z1_2d = z1 / (4 - y1 / 200)
        x2_2d = x2 / (4 - y2 / 200)
        z2_2d = z2 / (4 - y2 / 200)
        # Draw line
        canvas.create_line(WIDTH / 2 + int(x1_2d), HEIGHT / 2 + int(z1_2d), WIDTH / 2 + int(x2_2d), HEIGHT / 2 + int(z2_2d), fill="red")

    # Schedule the next update
    root.after(1000 // 60, draw_points)  # 60 FPS

def move_airplane(event):
    if event.keysym == "Left":
        for i, vertex in enumerate(vertices):
            vertices[i] = (vertex[0] - SPEED, vertex[1], vertex[2])  # move left
    if event.keysym == "Right":
        for i, vertex in enumerate(vertices):
            vertices[i] = (vertex[0] + SPEED, vertex[1], vertex[2])  # move right
    if event.keysym == "Up":
        for i, vertex in enumerate(vertices):
            vertices[i] = (vertex[0], vertex[1] - SPEED, vertex[2])  # move up
    if event.keysym == "Down":
        for i, vertex in enumerate(vertices):
            vertices[i] = (vertex[0], vertex[1] + SPEED, vertex[2])  # move down
    if event.char == "a":
        for i, vertex in enumerate(vertices):
            vertices[i] = (vertex[0], vertex[1], vertex[2] - SPEED)  # move forwards
    if event.char == "d":
        for i, vertex in enumerate(vertices):
            vertices[i] = (vertex[0], vertex[1], vertex[2] + SPEED)  # move backwards

# Bind the keyboard events
root.bind("<Key>", move_airplane)

# Start the game loop
draw_points()

root.mainloop()
