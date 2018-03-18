"""
Game Of Life 
Author : Saifeddine ALOUI
Description : Simple Conway's Game Of life

Features :
    Two modes :
        Randomly initialized world
        Hand initialized world 
"""

import time
import pygame
import random
import sys
import numpy as np
import copy

from tkinter import filedialog
from tkinter import *
 

# Define some colors
black           = (0,0,0)
white           = (255,255,255)

red             = (200,0,0)
gray           = (100,100,100)

bright_red      = (255,0,0)
bright_gray    = (200,200,200)
 
block_color     = (53,115,255)

display_width   = 800
display_height  = 600
 
 
# This sets the margin between each cell
MARGIN      = 0

speed       = 0.01
grid        = []
#length     = 0

# Set the HEIGHT and WIDTH of the screen
WINDOW_SIZE = [800, 600]

NB_COLS     = 100
NB_ROWS     = 100

# This sets the WIDTH and HEIGHT of each grid location
WIDTH       = WINDOW_SIZE[0]/NB_COLS
HEIGHT      = WINDOW_SIZE[1]/NB_ROWS

# Initialize pygame
pygame.init()
clock       = pygame.time.Clock()
screen      = pygame.display.set_mode(WINDOW_SIZE)

# Useful for special initialization
from_scratch = True

# Set title of screen
pygame.display.set_caption("Conway's Game of Life")
# ==================================================================
# GUI 
# ==================================================================
def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

def button(msg,x,y,w,h,ic,ac,action=None, action_param=None):

    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
            
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(screen, ac,(x,y,w,h))

        if click[0] == 1 and action != None:
            action() 
            clock.tick(15)
    else:
        pygame.draw.rect(screen, ic,(x,y,w,h))

    smallText = pygame.font.SysFont("comicsansms",20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    screen.blit(textSurf, textRect)

# ==================================================================
# PAGES
# ==================================================================
def game_intro():

    intro = True

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
        screen.fill(white)
        titleFont = pygame.font.SysFont("Times New Roaman",80)
        normalFont = pygame.font.SysFont("comicsansms",20)
        Game_title, Game_title_rect = text_objects("Conway's Game of Life", titleFont)
        Game_author, Game_author_rect = text_objects("Author : Saifeddine ALOUI", normalFont)
        Game_title_rect.center = ((display_width/2),(display_height/2)-150)
        Game_author_rect.center = ((display_width/2),(display_height/2+50)-1560)
        screen.blit(Game_title, Game_title_rect)
        screen.blit(Game_author, Game_author_rect)

        
        button("Reset",250,275,300,50,gray,bright_gray,reset_game)
        button("Start Game With random Init",250,325,300,50,gray,bright_gray,random_game)
        button("Start Game with spec Init",250,375,300,50,gray,bright_gray,grid_make)
        button("Load init from file",250,425,300,50,gray,bright_gray,load_grid)
        button("Save current init",250,475,300,50,gray,bright_gray,save_grid)
        button("Quit",250,525,300,50,red,bright_red,quitgame)

        pygame.display.update()
        clock.tick(15)    

def quitgame():
    pygame.quit()
    quit()

def unpause():
    global pause
    pause = False
    

def paused():

    largeText = pygame.font.SysFont("comicsansms",115)
    TextSurf, TextRect = text_objects("Paused", largeText)
    TextRect.center = ((display_width/2),(display_height/2))
    screen.blit(TextSurf, TextRect)
    

    while pause:
        for event in pygame.event.get():
            #print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
        screen.fill(white)
        pauseFont = pygame.font.SysFont("Times New Roaman",80)
        pause_text, pause_rect = text_objects("PAUSE", pauseFont)
        pause_rect.center = ((display_width/2),(display_height/2))
        screen.blit(pause_text, pause_rect)

        button("Continue",150,450,100,50,gray,bright_gray,unpause)
        button("Quit",550,450,100,50,red,bright_red,quitgame)

        pygame.display.update()
        clock.tick(15)   

def reset_game():
    global from_scratch
    from_scratch = True
def random_game():        
    init_grid = [[random.randrange(0,2) for x in range(NB_COLS)] for y in range(NB_ROWS)]
    game_loop(init_grid)
    
def game_loop(init_grid):
    global pause

    grid = init_grid
    # Loop until the user clicks the close button.
    done = False

    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()
    # Loop until the user clicks the close button.
    done = False

    FriendList = []
    for i in range(0, len(grid)):
        FriendList.append([])

    while not done:
        for event in pygame.event.get():  # User did something
            if event.type == pygame.QUIT:  # If user clicked close
                done = True  # Flag that we are done so we exit this loop
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    done = True                
                if event.key == pygame.K_p:
                    pause = True
                    paused()
                if event.key == pygame.K_ESCAPE:
                    done = True
                
        # Set the screen background
        screen.fill(black)
    
        # Draw the grid
        for row in range(NB_ROWS):
            for column in range(NB_COLS):
                color = black
                if grid[row][column] == 1:
                    color = white
                pygame.draw.rect(screen,
                                color,
                                [(MARGIN + WIDTH) * column + MARGIN,
                                (MARGIN + HEIGHT) * row + MARGIN,
                                WIDTH,
                                HEIGHT],0)            

        # evolution
        for y in range(0,len(grid)):
            for x in range(0,len(grid)):
                ymin = y - 1
                xmin = x - 1
                yplus = y + 1
                xplus = x + 1
                if yplus > len(grid)-1:
                    yplus = 0
                if ymin < 0:
                    ymin = len(grid)-1
                if xplus > len(grid)-1:
                    xplus = 0
                if xmin < 0:
                    xmin = len(grid)-1
                FriendList[y].append(grid[xmin][ymin] + grid[xmin][yplus] + grid[xmin][y] + grid[xplus][ymin] + grid[xplus][yplus] + grid[xplus][y] + grid[x][ymin] + grid[x][yplus])

        for x in range(0,len(grid)):
            for y in range(0,len(grid)):
                if grid[x][y] == 1:
                    if FriendList[y][x] > 3:
                        grid[x][y] = 0
                    if FriendList[y][x] < 2:
                        grid[x][y] = 0
                else:
                    if FriendList[y][x] == 3:
                        grid[x][y] = 1

        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()
        FriendList = []
        for i in range(0, len(grid)):
            FriendList.append([])

def save_grid():
    global pause, init_grid, from_scratch
    root = Tk()
    root.filename =  filedialog.asksaveasfile(initialdir = "/",title = "Select file",filetypes = (("Grid files","*.grd"),("all files","*.*")))
    root.quit()
    file = open(root.filename.name,'w')
    for row in range(NB_ROWS):
        for column in range(NB_COLS):
            file.write("{}".format(init_grid[row][column]))
        file.write("\n".format(init_grid[row][column]))

def load_grid():
    global pause, init_grid, from_scratch

    init_grid = []
   
    Tk().withdraw()
    fileName =  filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("Grid files","*.grd"),("all files","*.*")))

    try:
        file = open("{}".format(fileName),'r')
        code = file.readlines()
        for i in code:
            templist = list(i)
            while '\n' in templist:
                templist.remove('\n')
            templist2 = []
            for u in templist:
                templist2.append(int(u))
            init_grid.append(templist2)
        from_scratch = False
    except:
        print("")
    
def grid_make():
    global pause, init_grid, from_scratch
    if from_scratch == True :
        init_grid = [[0 for x in range(NB_COLS)] for y in range(NB_ROWS)]
        from_scratch = False

    # Loop until the user clicks the close button.
    done = False

    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()
    # Loop until the user clicks the close button.
    done = False

    FriendList = []
    for i in range(0, len(init_grid)):
        FriendList.append([])

    while not done:
        for event in pygame.event.get():  # User did something
            if event.type == pygame.QUIT:  # If user clicked close
                done = True  # Flag that we are done so we exit this loop
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # User clicks the mouse. Get the position
                pos = pygame.mouse.get_pos()
                # Change the x/y screen coordinates to grid coordinates
                column = np.int(pos[0] // (WIDTH + MARGIN))
                row = np.int(pos[1] // (HEIGHT + MARGIN))
                # Set that location to one
                if init_grid[row][column]==1:
                    init_grid[row][column] = 0
                else:
                    init_grid[row][column] = 1

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    done = True
                if event.key == pygame.K_ESCAPE:
                    done = True
                    return
        # Set the screen background
        screen.fill(black)
    
        # Draw the grid
        for row in range(NB_ROWS):
            for column in range(NB_COLS):
                color = black
                if init_grid[row][column] == 1:
                    color = white
                pygame.draw.rect(screen,
                                color,
                                [(MARGIN + WIDTH) * column + MARGIN,
                                (MARGIN + HEIGHT) * row + MARGIN,
                                WIDTH,
                                HEIGHT],0)            


        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()
        FriendList = []
        for i in range(0, len(init_grid)):
            FriendList.append([])
    game_loop(copy.deepcopy(init_grid))


game_intro()
pygame.quit()
quit()