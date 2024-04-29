import graphics
import random
import time

win = graphics.GraphWin("Tetris Game",700,700)

def move_left(shape,center):
    '''move each of the square in the shape 30 pixel to the left'''
    if can_move_left(shape,center):
        for i in shape:
            i.move(-30,0)

def move_right(shape,center):
    '''move each of the square in the shape 30 pixel to the right'''
    if can_move_right(shape,center):
        for i in shape:
            i.move(30,0)

def move_down(shape,center):
    '''move each of the square in the shape 30 pixel down'''
    if can_move_down(shape,center):
        for i in shape:
            i.move(0,-30)

def rotate(shape,color):
    '''Take a shape and rotate it to the right. 
    If the shape is at the edge of the playing screen, it won't rotate.
    Rotation is done by:
    1. Project the shape's shape onto a grid of 0 and 1 demonstrating rows and columns
    2. Turn the rows into columns and columns into rows
    3. Project the grid of 1 and 0 into the new shape by using the old X and Y'''
    old_X = [] #create a list to store old x coordinates
    old_Y = [] #create a list to store old y coordinates
    coord = [] #create a list to store corresponding coordinate
    for i in shape: #iterate over each square in the old shape
        X1 = (i.getP1()).getX() # get the x coordinate
        Y1 = (i.getP1()).getY() # get the y coordinate
        old_X.append(X1) # append the x coordinate to the list
        old_Y.append(Y1) # append the y coordinate to the list
        coord.append([X1,Y1]) # append the 2 coordinates to the list
    n_col = len(set(old_X)) # get the number of columns in the old shape by counting the number of unique x values
    n_row = len(set(old_Y)) # get the number of row in the old shape by counting the number of unique y values
    # check if the shape is on the edge
    if (not (n_col == 1 and max(old_X) == 650)) and (not(n_col == 2 and max(old_X)==650)) and (not(n_col == 1 and min(old_X)==350)) and (not(n_col == 4 and min(old_Y)>=590)):
        grid = [] #create a list for the number of columns
        new_grid = [] #create a list for the number of rows
        for i in range(n_col): #iterate over the number of columns
            grid.append(0) # add one placeholder to the list
        for i in range(n_row): #iterate over the number of rows
            new_grid.append(grid.copy()) #add a list for each row in the shape
        max_Y = max(old_Y) 
        for i in range(n_row): # iterate over the number of rows
            min_X = min(old_X) # change min_X back to min(old_X) for the next row
            for j in range(n_col): # iterate over the number of columns
                if [min_X,max_Y] in coord: #check if there is a block with the coordinate (min_X,max_Y) in the old shape
                    new_grid[i][j] = 1 # if there's a block, the place in the new_grid become 1
                else: 
                    new_grid[i][j] = 0 # if not, it's 0
                min_X += 30 # change min_X 30 pixels to the right to check the next column in the row
            max_Y -= 30 # change min_Y 30 pixels down to check the next row
        rotated_grid = [] # create a list for the new shape projection
        for x in range(len(new_grid[0])): # for each of the column in the old shape
            new_row = [] # create a new row
            for y in range(len(new_grid)-1, -1, -1): # for each of the row in the old shape from bottom to top
                new_row.append(new_grid[y][x]) # add the value in the 
            rotated_grid.append(new_row)
        new_X = []
        new_Y = []
        min_Y = min(old_Y)
        for i in range(n_col):
            min_X = min(old_X)
            for j in range(n_row):
                if rotated_grid[i][j] == 1:
                    new_X.append(min_X)
                    new_Y.append(min_Y + (30*(n_col-i-1)))
                min_X += 30
        random_shape = []
        random_shape.append(new_X)
        random_shape.append(new_Y)
        new_shape = []
        for i in range(4):
            pnt1 = graphics.Point(random_shape[0][i],random_shape[1][i])
            pnt2 = graphics.Point(random_shape[0][i] + 30,random_shape[1][i] + 30)
            block = graphics.Rectangle(pnt1,pnt2)
            new_shape.append(block)
        if n_row == 1:
            for i in new_shape:
                i.move(30,0)
        if n_col == 1:
            for i in new_shape:
                i.move(-30,0)
    else:
        new_shape = shape
    return new_shape, color


def can_move_left(shape,center):
    result = True
    pointX1 = []
    for i in shape:
        X1 = (i.getP1()).getX()
        pointX1.append(X1)
    if min(pointX1) <= 350:
        result = False
    center_shape = []
    for i in shape:
        y = i.getCenter()
        center_shape.append([y.getX() -30 ,y.getY()])
    for j in range(len(center_shape)):
        if center_shape[j] in center:
            result = False
            break
    return result

def can_move_right(shape,center):
    result = True
    pointX2 = []
    for i in shape:
        X2 = (i.getP2()).getX()
        pointX2.append(X2)
    if max(pointX2) >= 680:
        result = False
    center_shape = []
    for i in shape:
        y = i.getCenter()
        center_shape.append([y.getX() + 30 ,y.getY()])
    for j in range(len(center_shape)):
        if center_shape[j] in center:
            result = False
            break
    return result

def can_move_down(shape,center):
    result = True
    pointY = []
    for i in shape:
        Y = (i.getP1()).getY()
        pointY.append(Y)
    if min(pointY) <= 20:
        result = False
    center_shape = []
    for i in shape:
        y = i.getCenter()
        center_shape.append([y.getX(),y.getY() - 30])
    for j in range(len(center_shape)):
        if center_shape[j] in center:
            result = False
            break
    return result
    

def draw_score(score):
    draw_score = graphics.Text(graphics.Point(180,650), "Score: {}".format(score))
    draw_score.setFace("courier")
    draw_score.setSize(24)
    draw_score.setTextColor(graphics.color_rgb(210, 100, 110))
    draw_score.setStyle("bold")
    draw_score.draw(win)

def draw_next_shape():
    draw_score = graphics.Text(graphics.Point(180,210), "Next Shape")
    draw_score.setFace("courier")
    draw_score.setSize(24)
    draw_score.setTextColor(graphics.color_rgb(210, 100, 110))
    draw_score.setStyle("bold")
    draw_score.draw(win)

def freeze_shape(shape,grid):
    for i in shape:
        j = i.clone()
        grid.append(j)
        i.undraw()
    for j in range(len(grid) -1, len(grid)-5, -1):
        grid[j].draw(win) 

def get_center(grid):
    center = []      
    for j in grid:
        x_y = j.getCenter()
        center.append([x_y.getX(),x_y.getY()])
    return center

def choose_shape(x,y):
    square = [[x,x+30,x,x+30],
              [y,y,y-30,y-30]]
    line = [[x-30,x,x+30,x+60],
            [y,y,y,y]]
    right_l = [[x+30,x-30,x,x+30],
               [y,y-30,y-30,y-30]]
    left_l = [[x-30,x-30,x,x+30],
               [y,y-30,y-30,y-30]]
    r = [[x,x+30,x-30,x],
         [y,y,y-30,y-30]]
    l = [[x-30,x,x,x+30],
         [y,y,y-30,y-30]]
    t = [[x,x-30,x,x+30],
         [y,y-30,y-30,y-30]]
    
    shapes = [square,line,right_l,left_l,r,l,t]
    random_shape = random.choice(shapes)
    if random_shape == square:
        color = graphics.color_rgb(245, 169, 174)
    elif random_shape == line:
        color = graphics.color_rgb(212, 131, 137)
    elif random_shape == left_l or random_shape == right_l:
        color = graphics.color_rgb(227, 109, 118)
    elif random_shape == r or random_shape == l:
        color = graphics.color_rgb(237, 130, 139)
    elif random_shape == t:
        color = graphics.color_rgb(240, 103, 115)
    shape = []
    for i in range(4):
        pnt1 = graphics.Point(random_shape[0][i],random_shape[1][i])
        pnt2 = graphics.Point(random_shape[0][i] + 30,random_shape[1][i] + 30)
        block = graphics.Rectangle(pnt1,pnt2)
        shape.append(block)
    for i in shape:
        i.setFill(color)
        i.setOutline("ivory")
        i.draw(win)
    return shape, color

def draw_shape(predicted_shape):
    shape = []
    for i in predicted_shape:
        i.move(350,510)
        shape.append(i)
    return shape
    

def check_full_rows(grid):
    full_rows = []
    row_width = 330  # Width of a row
    block_width = 30  # Width of a block
    for y in range(20, 680, 30):  # Iterate over y-coordinates of rows
        row_blocks = [block for block in grid if block.getP1().getY() == y]
        row_width_filled = sum([block_width for block in row_blocks if block.getP1().getY() == y])  # Calculate total width of blocks in the row
        if row_width_filled == row_width:  # If the row is fully occupied
            full_rows.append(y)
    for row in full_rows:
        row_blocks = [block for block in grid if block.getP1().getY() == row]
        for block in row_blocks:
            block.undraw()  # Remove blocks in the full row
            grid.remove(block)  # Remove the block from the grid
        # Shift down blocks above the removed row
        for block in grid:
            if block.getP1().getY() > row:
                block.move(0, -30)

def check_full_screen(shape):
    result = False
    Y_coord = []
    for i in shape:
        Y1 = i.getP1().getY()
        Y_coord.append(Y1)
    if max(Y_coord) == 650:
        result = True
    return result


def main():
    
    # Sets the coordinate system
    win.setCoords(0,0,700,700)
    
    # changes the background color
    win.setBackground(graphics.color_rgb(222,236,255))
    
    # creates a black rec1 from lower-left pnt_a to upper-right pnt_b
    pnt_a = graphics.Point(350,20)
    pnt_b = graphics.Point(680,680)
    rec1 = graphics.Rectangle(pnt_a, pnt_b)
    rec1.setFill(graphics.color_rgb(250, 217, 219))
    rec1.setOutline("ivory")
    rec1.draw(win)

    pnt_c = graphics.Point(30,50)
    pnt_d = graphics.Point(320,250)
    rec1 = graphics.Rectangle(pnt_c, pnt_d)
    rec1.setFill(graphics.color_rgb(250, 217, 219))
    rec1.setOutline("ivory")
    rec1.draw(win)
    
    predicted_shape, predicted_color = choose_shape(150,140)

    score = 0
    draw_score(score)
    draw_next_shape()
    
    delay = 0.3
    grid = []
    center = []
    shape = draw_shape(predicted_shape) 
    color = predicted_color
    predicted_shape, predicted_color = choose_shape(150,140)
    while True:  
        if can_move_down(shape,center):
            for i in shape:
                i.move(0,-30)
            keystrings = win.checkKey()  
            if keystrings == "Left":
                move_left(shape,center)
            elif keystrings == "Right":
                move_right(shape,center)
            elif keystrings == "Down":
                move_down(shape,center) 
            elif keystrings == "Up":
                for i in shape:
                    i.undraw()
                shape, color = rotate(shape,color)
                for i in shape:
                    i.setFill(color)
                    i.setOutline("ivory")
                    i.draw(win)
        else:
            if check_full_screen(shape):
                break
            freeze_shape(shape,grid)
            check_full_rows(grid)
            center = get_center(grid)
            shape = draw_shape(predicted_shape) 
            color = predicted_color
            predicted_shape, predicted_color = choose_shape(150,140)
        draw_score(score)
        time.sleep(delay)
        
    pnt_1 = graphics.Point(200,250)
    pnt_2 = graphics.Point(500,450)
    rec2 = graphics.Rectangle(pnt_1, pnt_2)
    rec2.setFill("black")
    rec2.draw(win)

    win.getMouse()
        
if __name__ == "__main__":
    main()
