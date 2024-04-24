import turtle 
import time
import random

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


def draw_shape(x, y, grid, height, width, shape, color):
    for y in range(height):
        for x in range(width):
            if(shape[y][x]==1):
                grid[y + y][x + x] = color

def erase_shape(x, y, grid, height, width, shape):
    for i in range(height):
        for j in range(width):
            if(shape[y][x]==1):
                grid[y + i][x + j] = 0

def can_move(x, y, grid, height, width, shape):
    result = True
    for i in range(width):
        # Check if bottom is a 1
        if(shape[height-1][i] == 1):
            if(grid[y + height][x + i] != 0):
                result = False

    return result
    

def check_grid(grid, pen):
    # Check if each row is full
    y = 23
    while y > 0:
        is_full = True
        for x in range(0, 12):
            if grid[y][x] == 0:
                is_full = False
                y -= 1
                break
        if is_full:
            global score
            score += 10
            draw_score(pen, score)
            for copy_y in range(y, 0, -1):
                for copy_x in range(0, 12):
                    grid[copy_y][copy_x] = grid[copy_y-1][copy_x]

def draw_score(pen, score):
    pen.color("black")
    pen.hideturtle()
    pen.goto(-185, 200)
    pen.write("Score: {}".format(score), move=False, align="left", font=("Cambria", 24, "normal"))

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

    
    # Block Shape
    square = [[1,1],
              [1,1]]

    horizontal_line = [[1,1,1,1]]

    vertical_line = [[1],
                    [1],
                    [1],
                    [1]]

    left_l = [[1,0,0],
              [1,1,1]]
            
    right_l = [[0,0,1],
               [1,1,1]]
            
    z = [[1,1,0],
        [0,1,1]]
            
    s = [[0,1,1],
        [1,1,0]]
            
    t = [[0,1,0],
        [1,1,1]]

    shapes = [square, horizontal_line, vertical_line, left_l, right_l, z, s, t]
    
    # Choose a random shape at the start
    shape = random.choice(shapes)
    height = len(shape)
    width = len(shape[0])
    x = 4
    y = 0
    
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
    grid[y][x] = color

    # Draw the initial grid
    # draw_grid(pen, grid)

    wn.onkeypress(lambda: shape.rotate(grid), "space")
    wn.listen()
    wn.onkeypress(lambda: shape.move_left(grid), "Left")
    wn.onkeypress(lambda: shape.move_right(grid), "Right")

    # Set the score to 0
    score = 0

    draw_score(pen, score)

    # Main game loop
    while True:
        wn.update()
        draw_grid(pen, grid)
        draw_score(pen, score)
        

        # Move the shape
        # Open Row
        # Check for the bottom
        # if y == 23 - height + 1:
        #     shape = random.choice(shapes)
        #     check_grid(grid)
        # # Check for collision with next row
        # elif can_move(x,y,grid, height, width, shape):
        #     # Erase the current shape
        #     erase_shape(x,y,grid, height, width, shape)
            
        #     # Move the shape by 1
        #     y +=1
            
        #     # Draw the shape again
        #     draw_shape(grid, height, width, shape, color)

        # else:
        #     shape = random.choice(shapes)
        #     check_grid(grid, pen)
            
        # Draw the screen
        
        
        time.sleep(delay)
        
    wn.mainloop()

if __name__ == "__main__": 
    main()

