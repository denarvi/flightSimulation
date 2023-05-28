import numpy as np
from math import *
import os
import pygame
from pygame.locals import *
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import sys
from OpenGL.GL import *
from OpenGL.GLU import *

# Initialize Pygame
pygame.init()
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height), DOUBLEBUF | OPENGL)

# Set up the perspective
glViewport(0, 0, screen_width, screen_height)
glMatrixMode(GL_PROJECTION)
gluPerspective(45, (screen_width / screen_height), 0.1, 50.0)
glMatrixMode(GL_MODELVIEW)
gluLookAt(0, 0, 5, 0, 0, 0, 0, 1, 0)

# Set up the cube vertices
vertices = (
    (-1, -1, -1),
    (1, -1, -1),
    (1, 1, -1),
    (-1, 1, -1),
    (-1, -1, 1),
    (1, -1, 1),
    (1, 1, 1),
    (-1, 1, 1)
)

# Set up the cube edges
edges = (
    (0, 1),
    (1, 2),
    (2, 3),
    (3, 0),
    (4, 5),
    (5, 6),
    (6, 7),
    (7, 4),
    (0, 4),
    (1, 5),
    (2, 6),
    (3, 7)
)

# Main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    # Clear the screen
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # Rotate the cube
    glRotatef(1, 3, 1, 1)

    # Draw the cube edges
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()

    # Update the display
    pygame.display.flip()
    pygame.time.wait(10)
