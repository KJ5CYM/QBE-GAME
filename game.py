# ; ==========================================================================================;
# ; QBE-GAME                                                                                  ;
# ; ------------------------------------------------------------------------------------------;
# ;     FILENAME : game.py                                                                    ;
# ; ------------------------------------------------------------------------------------------;
# ;       AUTHOR : r0b0h0b0                                                                   ;
# ;        EMAIL : r0b0h0b0@proton.me                                                         ;
# ; DATE CREATED : 12/22/2023                                                                 ;
# ;  DESCRIPTION : A blocky sandbox game made with OpenGL and written in Python! :)           ;
# ; ==========================================================================================;

import pygame as pg
import numpy as np
import random as rand
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from PIL import Image
from math import *

# Define a class for creating 3D meshes
class Mesh:
    # Initialize mesh attributes
    def __init__(self, x, y, z, image):
        self.x = x                                         # X coordinate
        self.y = y                                         # Y coordinate
        self.z = z                                         # Z coordinate
        self.img = image                                   # Texture image
        self.vertices = []                                 # Vertices of the mesh
        self.tex_coords = []                               # Texture coordinates
        self.edges = []                                    # Edges of the mesh
        self.img_data = self.img.convert("RGB").tobytes()  # Image data for OpenGL

    # Move vertices of the mesh
    def move_verts(self, x, y, z):
        for i in range(len(self.vertices)):  # Loop through vertices
            self.vertices[i][0] += float(x)  # Update X coordinate
            self.vertices[i][1] += float(y)  # Update Y coordinate
            self.vertices[i][2] += float(z)  # Update Z coordinate

    # Combine two meshes
    def combine_with_mesh(self, other):
        self.vertices.extend(other.vertices) # Extend current mesh's data with another mesh's data
        self.tex_coords.extend(other.tex_coords)
        self.normals.extend(other.normals)

    # Render the mesh
    def render(self):
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, self.img.width, self.img.height, 0, GL_RGB, GL_UNSIGNED_BYTE, self.img_data)
        glEnable(GL_TEXTURE_2D)  # Enable 2D texturing
        glBegin(GL_QUADS)        # Begin defining quads for rendering
        o = 0
        for i in range(0, len(self.vertices)):
            glNormal3fv(self.normals[i])       # Set normal for lighting
            glTexCoord2fv(self.tex_coords[o])  # Set texture coordinates
            glVertex3fv(self.vertices[i])      # Set vertex coordinates
            o += 1
            if o >= 4:
                o = 0
        glEnd()                   # End rendering quads
        glDisable(GL_TEXTURE_2D)  # Disable 2D texturing after rendering

# Define a Cube class inheriting from Mesh
class Cube(Mesh):
    # Initialize Cube attributes and load texture image
    def __init__(self, x, y, z):
        image = Image.open("grass.jpg")
        image = image.transpose(Image.FLIP_TOP_BOTTOM)                      # Flip image top to bottom
        super().__init__(x, y, z, image)
        self.vertices = []                                                  # Vertices of the cube
        self.normals = []                                                   # Normals of the cube for lighting
        self.tex_coords = [[0.0, 0.0], [1.0, 0.0], [1.0, 1.0], [0.0, 1.0]]  # Texture coordinates
        self.top, self.west, self.east, self.front, self.back, self.bottom = True, True, True, True, True, True

    # Create a cube mesh
    def make_mesh(self):
        if self.front:
            self.vertices.extend([[0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0]])
            self.normals.extend([[0, 0, 1], [0, 0, 1], [0, 0, 1], [0, 0, 1]])
        if self.top:
            self.vertices.extend([[0, 0, 1], [1, 0, 1], [1, 0, 0], [0, 0, 0]])
            self.normals.extend([[0, 1, 0], [0, 1, 0], [0, 1, 0], [0, 1, 0]])
        if self.west:
            self.vertices.extend([[0, 0, 1], [0, 1, 1], [0, 1, 0], [0, 0, 0]])
            self.normals.extend([[1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0]])
        if self.east:
            self.vertices.extend([[1, 0, 1], [1, 1, 1], [1, 1, 0], [1, 0, 0]])
            self.normals.extend([[-1, 0, 0], [-1, 0, 0], [-1, 0, 0], [-1, 0, 0]])
        if self.back:
            self.vertices.extend([[0, 0, 1,], [1, 0, 1], [1, 1, 1], [0, 1, 1]])
            self.normals.extend([[0, 0, -1], [0, 0, -1], [0, 0, -1], [0, 0, -1]])
        if self.bottom:
            self.vertices.extend([[0, 1, 1], [1, 1, 1], [1, 1, 0], [0, 1, 0]])
            self.normals.extend([[0, -1, 0], [0, -1, 0], [0, 1, 0], [0, 1, 0]])

# Define a class for Chunk
class Chunk:
    # Initialize Chunk attributes
    def __init__(self):
        self.base = Cube(0, 0, 0)                                   # Create a base cube
        self.base.make_mesh()                                       # Create mesh for the base cube

        self.blocks = []                                            # Initialize block list

        for z in range(0, 8):                                       # Loop for z-dimension
            y_dimension = []                                        # Initialize y-dimension list
            for y in range(0, 8):                                   # Loop for y-dimension
                x_dimension = []                                    # Initialize x-dimension list
                for x in range(0, 8):                               # Loop for x-dimension
                    x = rand.randint(0, 1)                          # Randomly generate 0 or 1
                    x_dimension.append(x)                           # Append value to x-dimension
                y_dimension.append(x_dimension)                     # Append x-dimension to y-dimension
            self.blocks.append(y_dimension)                         # Append y-dimension to blocks
# Basically remove cube faces if they're shared.
        for x in range(0, 8):                                       # Loop for x-dimension
            for y in range(0, 8):                                   # Loop for y-dimension
                for z in range(0, 8):                               # Loop for z-dimension
                    if self.blocks[x][y][z] == 1:                   # Check block value
                        b = Cube(0, 0, 0)                           # Create a cube
                        if x >= 1 and self.blocks[x-1][y][z] == 1:
                            b.west = False                          # Disable west face
                        if x < 7 and self.blocks[x+1][y][z] == 1:
                            b.east = False                          # Disable east face
                        if y >= 1 and self.blocks[x][y-1][z] == 1:
                            b.top = False                           # Disable top face
                        if y < 7 and self.blocks[x][y+1][z] == 1:
                            b.bottom = False                        # Disable bottom face
                        if z >= 1 and self.blocks[x][y][z-1] == 1:
                            b.front = False                         # Disable front face
                        if z < 7 and self.blocks[x][y][z+1] == 1:
                            b.back = False                          # Disable back face
                        b.make_mesh()                               # Create mesh for the cube
                        b.move_verts(x, y, z)                       # Move vertices of the cube
                        self.base.combine_with_mesh(b)              # Combine cube mesh with the base cube

    # Render the chunk
    def render(self):
        self.base.render()                            # Render the base cube

# Define a class for Camera
class Camera:
    x, y, z, rot_y, dir_z, dir_x = 0, 0, 5, 0, -1, 0  # Initialize camera attributes

# Define a class for Main
class Main:
    test = Chunk()                                    # Create a Chunk object

    last_mouse_x, last_mouse_y = 0, 0                 # Initialize mouse position variables

    # Start the game
    @staticmethod
    def start():
        pg.init()  # Initialize Pygame
        pg.display.set_mode((1280, 720), DOUBLEBUF|OPENGL)  # Set display mode
        pg.display.set_caption("DAM QBES!!!")               # Set window title

        # Set texture parameters for OpenGL
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        gluPerspective(70, 1280/720, 0.1, 100.0)            # Set perspective projection

        glEnable(GL_DEPTH_TEST)                             # Enable depth testing for 3D rendering

        pg.mouse.set_visible(False)                         # Hide the mouse cursor

        Main.loop()                                         # Start the game loop

    # Game loop
    @staticmethod
    def loop():
        while True:                        # Main game loop
            for event in pg.event.get():   # Event handling loop
                if event.type == pg.QUIT:  # Check for quit event
                    pg.quit()              # Quit Pygame
                    quit()                 # Exit the program

            glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)             # Clear buffers

            keys = pg.key.get_pressed()                                  # Get pressed keys

            mouse_x, mouse_y = pg.mouse.get_pos()                        # Get mouse position

            if Main.last_mouse_x != mouse_x:                             # Check if mouse moved horizontally
                # Update camera rotation based on mouse movement
                Camera.rot_y += (mouse_x - Main.last_mouse_x) / 100
                Camera.dir_x = sin(Camera.rot_y)
                Camera.dir_z = -cos(Camera.rot_y)
                mouse_x, mouse_y = 1280/2, 720/2                         # Reset mouse position to center
                Main.last_mouse_x, Main.last_mouse_y = mouse_x, mouse_y  # Update last mouse position
                pg.mouse.set_pos(1280/2, 720/2)                          # Set mouse position to center

            # Handle key presses for movement and quitting
            if keys[pg.K_w]:
                Camera.x += Camera.dir_x * 0.3
                Camera.z += Camera.dir_z * 0.3
            if keys[pg.K_s]:
                Camera.x -= Camera.dir_x * 0.3
                Camera.z -= Camera.dir_z * 0.3
            if keys[pg.K_q]:
                Camera.y -= 0.1
            if keys[pg.K_e]:
                Camera.y += 0.1
            if keys[pg.K_ESCAPE]:
                pg.quit()   # Quit Pygame
                quit()      # Exit the game

            glPushMatrix()  # Push the current matrix stack

            glClearColor(0.0, 0.0, 0.0, 0.0)           # Set clear color
            pos = [1.0, 3.0, 1.0, 0.0]                 # Light position
            ambient = [0.8, 0.9, 1.0, 1.0]             # Ambient light
            glShadeModel(GL_SMOOTH)                    # Enable smooth shading
            glLightfv(GL_LIGHT0, GL_POSITION, pos)     # Set light position
            glLightfv(GL_LIGHT0, GL_AMBIENT, ambient)  # Set ambient light
            glDisable(GL_LIGHTING)                     # Disable lighting
            glEnable(GL_LIGHT0)                        # Enable light 0
            glClearColor(0.3, 0.5, 1.0, 1.0)           # Set sky color

            gluLookAt(Camera.x, Camera.y+1.0, Camera.z, Camera.x+Camera.dir_x, Camera.y+1.0, Camera.z+Camera.dir_z, 0.0, 1.0, 0.0)  # Set camera view

            Main.test.render()  # Render the chunk
            glPopMatrix()       # Pop the matrix stack
            pg.display.flip()   # Update the display

Main.start()  # Start the game
