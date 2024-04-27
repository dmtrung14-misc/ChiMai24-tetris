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

def freeze_shape(shape,grid,center):
    for i in shape:
        grid.append(i)
        i.undraw()
    for j in range(len(grid) -1, len(grid)-5, -1):
        grid[j].draw(win)
        x_y = grid[j].getCenter()
        center.append([x_y.getX(),x_y.getY()])


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
    
    # draw a piece
    # piece = graphics.Rectangle(graphics.Point(450,550),graphics.Point(480,580))
    # piece.setFill("yellow")
    # piece.setOutline("black")

    #draw the shapes
    square = [graphics.Rectangle(graphics.Point(500,650),graphics.Point(530,680)),
              graphics.Rectangle(graphics.Point(530,650),graphics.Point(560,680)),
              graphics.Rectangle(graphics.Point(500,620),graphics.Point(530,650)),
              graphics.Rectangle(graphics.Point(530,620),graphics.Point(560,650))]
    
    line = [graphics.Rectangle(graphics.Point(470,650),graphics.Point(500,680)),
            graphics.Rectangle(graphics.Point(500,650),graphics.Point(530,680)),
            graphics.Rectangle(graphics.Point(530,650),graphics.Point(560,680)),
            graphics.Rectangle(graphics.Point(560,650),graphics.Point(590,680))]
    
    right_l = [graphics.Rectangle(graphics.Point(470,620),graphics.Point(500,650)),
            graphics.Rectangle(graphics.Point(500,620),graphics.Point(530,650)),
            graphics.Rectangle(graphics.Point(530,620),graphics.Point(560,650)),
            graphics.Rectangle(graphics.Point(530,650),graphics.Point(560,680))]
    
    left_l = [graphics.Rectangle(graphics.Point(470,620),graphics.Point(500,650)),
            graphics.Rectangle(graphics.Point(500,620),graphics.Point(530,650)),
            graphics.Rectangle(graphics.Point(530,620),graphics.Point(560,650)),
            graphics.Rectangle(graphics.Point(470,650),graphics.Point(500,680))]
    
    r = [graphics.Rectangle(graphics.Point(500,650),graphics.Point(530,680)),
        graphics.Rectangle(graphics.Point(500,620),graphics.Point(530,650)),
        graphics.Rectangle(graphics.Point(530,620),graphics.Point(560,650)),
        graphics.Rectangle(graphics.Point(470,650),graphics.Point(500,680))]
    
    l = [graphics.Rectangle(graphics.Point(500,650),graphics.Point(530,680)),
        graphics.Rectangle(graphics.Point(500,620),graphics.Point(530,650)),
        graphics.Rectangle(graphics.Point(530,650),graphics.Point(560,680)),
        graphics.Rectangle(graphics.Point(470,620),graphics.Point(500,650))]
    
    t = [graphics.Rectangle(graphics.Point(470,620),graphics.Point(500,650)),
        graphics.Rectangle(graphics.Point(500,620),graphics.Point(530,650)),
        graphics.Rectangle(graphics.Point(530,620),graphics.Point(560,650)),
        graphics.Rectangle(graphics.Point(500,650),graphics.Point(530,680))]
    
    shapes = [square,line,right_l,left_l,r,l,t]
    shape = random.choice(shapes)
    for i in shape:
        if shape == square:
            i.setFill("yellow2")
        elif shape == line:
            i.setFill("red2")
        elif shape == left_l or shape == right_l:
            i.setFill("orange2")
        elif shape == r or shape == l:
            i.setFill("blue2")
        elif shape == t:
            i.setFill("green2")
        i.setOutline("black")
        i.draw(win)
    

    score = 0
    draw_score(score)
    
    delay = 0.3
    grid = []
    center = []

    while True:   
        if can_move_down(shape,center):
            keystrings = win.checkKey()  
            if keystrings == "Left":
                move_left(shape,center)
            elif keystrings == "Right":
                move_right(shape,center)
            elif keystrings == "Down":
                move_down(shape,center) 
            for i in shape:
                i.move(0,-30)
        else:
            freeze_shape(shape,grid,center)
            shape = random.choice(shapes)
            for i in shape:
                if shape == square:
                    i.setFill("yellow2")
                elif shape == line:
                    i.setFill("red2")
                elif shape == left_l or shape == right_l:
                    i.setFill("orange2")
                elif shape == r or shape == l:
                    i.setFill("blue2")
                elif shape == t:
                    i.setFill("green2")
                i.setOutline("black")
                i.undraw()
                i.draw(win)
        # if can_move_down(shape):
        #     for i in shape:
        #         i.move(0,-30)
        #         keystrings = win.checkKey()  
        #         if keystrings == "Left":
        #             move_left(shape)
        #         elif keystrings == "Right":
        #             move_right(shape)
        #         elif keystrings == "Down":
        #             move_down(shape)  
        # else:
        #     shape = random.choice(shapes)
        #     for i in shape:
        #         i.draw(win)
        time.sleep(delay)
        
        
if __name__ == "__main__":
    main()
