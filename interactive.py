import numpy as np
from math import *
import os
import pygame
from pygame.locals import *
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import sys

# Initialize Pygame
pygame.init()
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Interactive Takeoff Animation")
clock = pygame.time.Clock()


# this function gets called every time a new frame should be generated.
def animate_takeoff(frame_number):
    global tx, ty, tz, beta, alpha, gamma

    # Handle Pygame events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # increasing Alpha makes it go up in a circle - |
    # Increasing beta makes the body turn upside down
    # Increasing gamma makes it take a turn

    # The following 3 blocks are meant to showcase the plane accelerating on the runway.
    if frame_number < 100:
        x = 0
        y = 2.5
        z = 0
    elif 100 < frame_number <= 120:
        x = 0
        y = 2.5
        z = -0.1
    elif 120 < frame_number <= 140:
        x = 0
        y = 2.5
        z = -0.2

    # Move camera along runway
    tx += x
    ty += y

    # Increase altitude
    tz -= z
    bet = np.array(
        [[np.cos(beta), 0, np.sin(beta)],
         [0, 1, 0],
         [-np.sin(beta), 0, np.cos(beta)]])
    alp = np.array([
        [1, 0, 0],
        [0, np.cos(alpha), -np.sin(alpha)],
        [0, np.sin(alpha), np.cos(alpha)]
    ])
    gam = np.array([
        [np.cos(gamma), -np.sin(gamma), 0],
        [np.sin(gamma), np.cos(gamma), 0],
        [0, 0, 1]
    ])

    # apply rotation matrix to 3D points
    rotation_matrix = alp @ bet @ gam

    # apply projection matrix to rotated 3D points
    f = 0.002
    focus = np.array([
        [f, 0, 0],
        [0, f, 0],
        [0, 0, 1]
    ])
    camera = np.array([
        [1, 0, 0, tx],
        [0, 1, 0, ty],
        [0, 0, 1, tz]
    ])
    projection_matrix = focus @ rotation_matrix @ camera

    pr = []
    pc = []
    for pts in pts3:
        point = pts.copy()
        point.append(1)
        point = np.array(point)
        point = point[:, np.newaxis]
        point = projection_matrix @ point
        point[2] = point[2] if point[2][0] > 0 else 0.0001
        pr += [(point[0]) / (point[2])]
        pc += [(point[1]) / (point[2])]

    # Clear the screen
    screen.fill((255, 255, 255))

    # Draw the points
    for i in range(len(pr)):
        pygame.draw.circle(screen, (0, 0, 0), (int(pr[i] * screen_width), int(pc[i] * screen_height)), 2)

    pygame.display.flip()
    clock.tick(60)  # Limit the frame rate to 60 FPS


# load in 3d point cloud
with open("airport.pts", "r") as f:
    pts3 = [[float(x) for x in l.split(" ")] for l in f.readlines()]

# initialize intrinsic and extrinsic parameters
f = 0.002  # focal length
(tx, ty, tz) = (0, 0, -5)
(alpha, beta, gamma) = (-pi / 2, 0, 0)

# create animation!
frame_count = 325
ani = animation.FuncAnimation(plt.figure(), animate_takeoff, frames=range(frame_count), blit=False)

# Start the Pygame main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Update the animation
    ani._func(frame_number=pygame.time.get_ticks() // 10)  # Assumes 100 FPS animation speed
    plt.pause(0.001)

    pygame.display.update()
    clock.tick(60)  # Limit the frame rate to 60 FPS
