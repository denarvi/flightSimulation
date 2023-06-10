import tkinter as tk
import numpy as np
from numpy import pi

# Set up some constants
WIDTH, HEIGHT = 800, 600
SPEED = 5

# Set up the camera
camera_position = [WIDTH // 2, HEIGHT // 2, -5]

# Load the 3D points from the file
with open("airport.pts", "r") as f:
    points = [list(map(float, line.split())) for line in f]

# Create the window
root = tk.Tk()

# Create the canvas
canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="black")
canvas.pack()

# Initialize rotation angles
alpha, beta, gamma = 0, 0, 0

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

    # Project the 3D points to 2D
    projected_points = []
    for x, y, z in points:
        # Apply rotation
        point = rotation_matrix @ np.array([x, y, z])
        x, y, z = point[0], point[1], point[2]
        x -= camera_position[0]
        y -= camera_position[1]
        z -= camera_position[2]
        x2d = x / (4 - y / 200)
        z2d = z / (4 - y / 200)
        projected_points.append((WIDTH / 2 + int(x2d), HEIGHT / 2 + int(z2d)))

    # Draw the points
    for x, z in projected_points:
        canvas.create_oval(x - 1, z - 1, x + 1, z + 1, fill="white")

    # Schedule the next update
    root.after(1000 // 60, draw_points)  # 60 FPS

def move_camera(event):
    global alpha, beta, gamma  # make sure these are defined globally
    if event.keysym == "Left":
        camera_position[0] -= SPEED
        gamma -= SPEED / 100.0  # roll
    if event.keysym == "Right":
        camera_position[0] += SPEED
        gamma += SPEED / 100.0  # roll
    if event.keysym == "Up":
        camera_position[1] += SPEED
        beta -= SPEED / 100.0  # pitch
    if event.keysym == "Down":
        camera_position[1] -= SPEED
        beta += SPEED / 100.0  # pitch
    if event.char == "a":
        camera_position[2] += SPEED
        alpha -= SPEED / 100.0  # yaw
    if event.char == "d":
        camera_position[2] -= SPEED
        alpha += SPEED / 100.0  # yaw

# Bind the keyboard


# Bind the keyboard events
root.bind("<Key>", move_camera)

# Start the game loop
draw_points()

root.mainloop()
