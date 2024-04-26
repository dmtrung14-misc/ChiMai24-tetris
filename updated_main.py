import turtle 
import time
import random

#draw the grid
def draw_grid(pen, grid):
    pen.clear()
    top = 230
    left = 20
    
    colors = ["black", "lightblue", "blue", "orange", "yellow", "green", "purple", "red"]
    
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            screen_x = left + (x * 20)
            screen_y = top - (y * 20)
            color_number = grid[y][x]
            color = colors[color_number]
            pen.color(color)
            pen.goto(screen_x, screen_y)
            pen.stamp()

def draw_score(pen, score):
    pen.color("black")
    pen.hideturtle()
    pen.goto(-185, 200)
    pen.write("Score: {}".format(score), move=False, align="left", font=("Cambria", 24, "normal"))

def draw_shape(x, y, grid, height, width, shape, color):
    for i in range(height):
        
        for j in range(width):
            if(shape[i][j]==1):
                grid[y + i][x + j] = color

def main():
    wn = turtle.Screen()
    wn.title("Tetris")
    wn.bgcolor("white")
    wn.setup(width=560, height=540)
    wn.tracer(0)

    # Create the drawing pen
    pen = turtle.Turtle()
    pen.penup()
    pen.speed(0)
    pen.shape("square")
    pen.setundobuffer(None)

    #set the delay time
    delay = 0.2

    #define the grid
    grid = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]

    x = 4
    y = 0
    square = [grid[y][x:x+2],
              grid[y+1][x:x+2]]

    horizontal_line = [grid[y][x:x+4]]

    vertical_line = [grid[y][x],
                    grid[y+1][x],
                    grid[y+2][x],
                    grid[y+3][x]]

    left_l = [grid[y][x],
              grid[y+1][x:x+3]]
            
    right_l = [grid[y][x+2],
               grid[y+1][x:x+3]]
            
    z = [grid[y][x:x+2],
        grid[y+1][x+1:x+3]]
            
    s = [grid[y][x+1:x+3],
        grid[y+1][x:x+2]]
            
    t = [grid[y][x+1],
        grid[y+1][x:x+3]]

    shapes = [square, horizontal_line, vertical_line, left_l, right_l, z, s, t]
    
    # Choose a random shape at the start
    shape = random.choice(shapes)
    height = len(shape)
    # width = 0
    # for i in range(height):
    #     w = len(shape[i])
    #     if w > width:
    #         width = w
    #     else:
    #         width = width

    # width = len(shape[0])
    

    
    # assign color
    if shape == square:
        color = 1
    elif shape == horizontal_line or shape == vertical_line:
        color = 2
    elif shape == left_l or shape == right_l:
        color = 3
    elif shape == s or shape == z:
        color = 4
    elif shape == t:
        color = 5


    # Put the shape in the grid
    shape = color

    # Draw the initial grid
    draw_grid(pen, grid)

    score = 0


    while True:
        wn.update()
        draw_grid(pen, grid)
        draw_score(pen,score)
        

if __name__ == "__main__": 
    main()