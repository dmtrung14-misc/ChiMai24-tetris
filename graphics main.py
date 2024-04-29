import graphics
import random
import time

win = graphics.GraphWin("My Window",700,700)

def move_left(shape,center):
    if can_move_left(shape,center):
        for i in shape:
            i.move(-30,0)

def move_right(shape,center):
    if can_move_right(shape,center):
        for i in shape:
            i.move(30,0)

def move_down(shape,center):
    if can_move_down(shape,center):
        for i in shape:
            i.move(0,-30)

def check_grid(grid):
    for i in grid:
        X1 = (i.getP1()).getX()
        Y1 = (i.getP1()).getY()
    


def rotate(shape,color):
    old_X = []
    old_Y = []
    coord = []
    for i in shape:
        X1 = (i.getP1()).getX()
        Y1 = (i.getP1()).getY()
        old_X.append(X1)
        old_Y.append(Y1)
        coord.append([X1,Y1])
    n_col = len(set(old_X))
    n_row = len(set(old_Y))
    grid = []
    new_grid = []
    for i in range(n_col):
        grid.append(0)
    for i in range(n_row):
        new_grid.append(grid.copy())
    max_Y = max(old_Y)
    for i in range(n_row):
        min_X = min(old_X)
        for j in range(n_col):
            if [min_X,max_Y] in coord:
                new_grid[i][j] = 1
            else:
                new_grid[i][j] = 0
            min_X += 30
        max_Y -= 30
    rotated_grid = []
    for x in range(len(new_grid[0])):
        new_row = []
        for y in range(len(new_grid)-1, -1, -1):
            new_row.append(new_grid[y][x])
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
    draw_score.setTextColor("black")
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

def draw_shape(x,y):
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
        color = "yellow2"
    elif random_shape == line:
        color = "red2"
    elif random_shape == left_l or random_shape == right_l:
        color = "orange2"
    elif random_shape == r or random_shape == l:
        color = "blue2"
    elif random_shape == t:
        color = "green2"
    shape = []
    for i in range(4):
        pnt1 = graphics.Point(random_shape[0][i],random_shape[1][i])
        pnt2 = graphics.Point(random_shape[0][i] + 30,random_shape[1][i] + 30)
        block = graphics.Rectangle(pnt1,pnt2)
        shape.append(block)
    return shape, color

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

def main():
    
    # Sets the coordinate system
    win.setCoords(0,0,700,700)
    
    # changes the background color
    win.setBackground("lightblue") # <-- comment later
    
    # creates a black rec1 from lower-left pnt_a to upper-right pnt_b
    pnt_a = graphics.Point(350,20)
    pnt_b = graphics.Point(680,680)
    rec1 = graphics.Rectangle(pnt_a, pnt_b)
    rec1.setFill(graphics.color_rgb(0, 0, 0))
    
    # indicates where to draw the circle
    rec1.draw(win)
    
    x = 500
    y = 650
    shape, color = draw_shape(x,y)
    for i in shape:
        i.setFill(color)
        i.setOutline("black")
        i.draw(win)

    score = 0
    draw_score(score)
    
    delay = 0.3
    grid = []
    center = []
    

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
                    i.setOutline("black")
                    i.draw(win)
        else:
            freeze_shape(shape,grid)
            check_full_rows(grid)
            center = get_center(grid)
            shape, color = draw_shape(x,y)
            for i in shape:
                i.setFill(color)
                i.setOutline("black")
                i.draw(win)
        draw_score(score)
        time.sleep(delay)
        
        
if __name__ == "__main__":
    main()
