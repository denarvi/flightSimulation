import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

# Initialize Pygame
pygame.init()
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height), DOUBLEBUF | OPENGL)
pygame.display.set_caption("Move Cube in 3D Space")

# Set up OpenGL perspective
glViewport(0, 0, screen_width, screen_height)
glMatrixMode(GL_PROJECTION)
gluPerspective(45, (screen_width / screen_height), 0.1, 50.0)
glMatrixMode(GL_MODELVIEW)
glLoadIdentity()
gluLookAt(0, 0, -5, 0, 0, 0, 0, 1, 0)

# Cube vertices and edges
vertices = (
    (-0.5, -0.5, -0.5),
    (-0.5, 0.5, -0.5),
    (0.5, 0.5, -0.5),
    (0.5, -0.5, -0.5),
    (-0.5, -0.5, 0.5),
    (-0.5, 0.5, 0.5),
    (0.5, -0.5, 0.5),
    (0.5, 0.5, 0.5)
)

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

# Initial cube position and rotation
cube_pos = [0, 0, 0]
angle_x = 0
angle_y = 0
angle_z = 0

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # Handle keyboard input
    keys = pygame.key.get_pressed()
    if keys[K_w]:
        cube_pos[1] += 0.1
    if keys[K_s]:
        cube_pos[1] -= 0.1
    if keys[K_a]:
        cube_pos[0] -= 0.1
    if keys[K_d]:
        cube_pos[0] += 0.1
    if keys[K_e]:
        angle_z += 1
    if keys[K_q]:
        angle_z -= 1

    # Set cube position and rotation
    glLoadIdentity()
    glTranslatef(cube_pos[0], cube_pos[1], cube_pos[2])
    glRotatef(angle_x, 1, 0, 0)
    glRotatef(angle_y, 0, 1, 0)
    glRotatef(angle_z, 0, 0, 1)

    # Draw the cube
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()

    # Update the display
    pygame.display.flip()
    pygame.time.wait(10)

# Quit the game
pygame.quit()
