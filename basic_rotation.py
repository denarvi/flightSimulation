import tkinter as tk
import math

# Set up some constants
WIDTH, HEIGHT = 800, 600
SPEED = 5
ROT_SPEED = 0.02

# Set up the cube
cube_position = [WIDTH // 2, HEIGHT // 2, 0]
cube_size = 100
cube_rotation = [0, 0, 0]  # Pitch, yaw, roll

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
    y, z = y * math.cos(pitch) - z * math.sin(pitch), y * math.sin(pitch) + z * math.cos(pitch)

    # Rotate around y-axis (yaw)
    x, z = x * math.cos(yaw) + z * math.sin(yaw), -x * math.sin(yaw) + z * math.cos(yaw)

    # Rotate around z-axis (roll)
    x, y = x * math.cos(roll) - y * math.sin(roll), x * math.sin(roll) + y * math.cos(roll)

    return x, y, z

def draw_cube():
    # Clear the canvas
    canvas.delete("all")

    rotated_vertices = [rotate(vertex, cube_rotation) for vertex in vertices]

    projected_points = []
    for x, y, z in rotated_vertices:
        # Project the 3D point to 2D
        x3d = cube_size * x
        y3d = cube_size * (y + cube_position[2] / cube_size)
        z3d = cube_size * z
        x2d = x3d / (4 - z3d / 200)
        y2d = y3d / (4 - z3d / 200)

        projected_points.append((cube_position[0] + int(x2d), cube_position[1] + int(y2d)))

    for edge in edges:
        canvas.create_line(projected_points[edge[0]], projected_points[edge[1]], fill="white")

    # Schedule the next update
    root.after(1000 // 60, draw_cube)  # 60 FPS

def move_cube(event):
    if event.keysym == "Left":
        cube_position[0] -= SPEED
    if event.keysym == "Right":
        cube_position[0] += SPEED
    if event.keysym == "Up":
        cube_position[1] -= SPEED
    if event.keysym == "Down":
        cube_position[1] += SPEED
    if event.char == "a":
        cube_position[2] -= SPEED
    if event.char == "d":
        cube_position[2] += SPEED
    if event.char == "w": #s
        cube_rotation[0] += ROT_SPEED  # Pitch
    if event.char == "s": #w
        cube_rotation[0] -= ROT_SPEED  # Pitch
    if event.char == "a": #a
        cube_rotation[1] += ROT_SPEED  # Yaw
    if event.char == "d": #d
        cube_rotation[1] -= ROT_SPEED  # Yaw
    if event.char == "t":
        cube_rotation[2] += ROT_SPEED  # Roll
    if event.char == "y":
        cube_rotation[2] -= ROT_SPEED  # Roll

# Bind the keyboard events
root.bind("<Key>", move_cube)

# Start the game loop
draw_cube()

root.mainloop()
