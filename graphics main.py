import json
import graphics
import random
import time
from graphics import *
from wonderwords import RandomWord
from appdirs import user_data_dir

# win = graphics.GraphWin("Tetris Game",700,700)

APPNAME = "Tetris"
leaderboard_file = os.path.join(user_data_dir(APPNAME, appauthor=APPNAME), 'leaderboard.json')


def clicked_start(u: Point) -> bool:
    if 200 <= u.getX() <= 400 and 200 <= u.getY() <= 360:
        return True
    else:
        return False
    
def inside(point, rectangle):
    """ Is point inside rectangle? """
    # assume p1 is ll (lower left)
    ll = rectangle.getP1()  
    # assume p2 is ur (upper right)
    ur = rectangle.getP2() 
    return ll.getX() < point.getX() < ur.getX() and ll.getY() < point.getY() < ur.getY()

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
            rotated_grid.append(new_row) # add the new row to the new grid
        # change the rows from 0 and 1 to the x and y coordinates
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
        # put the lists of coordinates into a new shape to draw on the screen
        random_shape = []
        random_shape.append(new_X)
        random_shape.append(new_Y)
        new_shape = []
        for i in range(4):
            pnt1 = graphics.Point(random_shape[0][i],random_shape[1][i])
            pnt2 = graphics.Point(random_shape[0][i] + 30,random_shape[1][i] + 30)
            block = graphics.Rectangle(pnt1,pnt2)
            new_shape.append(block)
        # check of the rotated shape would be outside of the playing grid
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
    '''check if the shape can move left:
    1. it's minimum x coordinates are not outside of the playing grid
    2. there's no block to the left of the shape'''
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
    '''check if the shape can move right:
    1. it's maximum x coordinates are not outside of the playing grid
    2. there's no block to the right of the shape'''
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
    '''check if the shape can move down:
    1. it's minimum y coordinates are not outside of the playing grid
    2. there's no block under the shape'''
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
    

def draw_score(score,win):
    '''draw score from the provided score in the argument and return the graphwin text objects'''
    draw_label = graphics.Text(graphics.Point(180,650), "Score")
    draw_label.setFace("courier")
    draw_label.setSize(24)
    draw_label.setTextColor(graphics.color_rgb(210, 100, 110))
    draw_label.setStyle("bold")
    draw_label.draw(win)

    draw_score = graphics.Text(graphics.Point(180,600), "{}".format(score))
    draw_score.setFace("courier")
    draw_score.setSize(24)
    draw_score.setTextColor(graphics.color_rgb(210, 100, 110))
    draw_score.setStyle("bold")
    draw_score.draw(win)
    return draw_score , draw_label

def draw_next_shape(win):
    '''draw the text "Next Shape" on the screen'''
    draw_score = graphics.Text(graphics.Point(180,210), "Next Shape")
    draw_score.setFace("courier")
    draw_score.setSize(24)
    draw_score.setTextColor(graphics.color_rgb(210, 100, 110))
    draw_score.setStyle("bold")
    draw_score.draw(win)

def freeze_shape(shape,grid,win):
    '''for each of the shape that has reach the bottom and can't move anymore,
    add that shape to the list grid and undraw that shape from win'''
    for i in shape:
        j = i.clone()
        grid.append(j)
        i.undraw()
    for j in range(len(grid) -1, len(grid)-5, -1):
        grid[j].draw(win) 

def get_center(grid):
    '''get the center x and y coordinates of the shape'''
    center = []      
    for j in grid:
        x_y = j.getCenter()
        center.append([x_y.getX(),x_y.getY()])
    return center

def choose_shape(x,y,win):
    '''Randomly choose and draw a shape from the given coordinates. The possible shapes are given in coordinates variation from the given x and y.
    Assign a certain color to the shape chosen and return both the shape and the color'''
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
        color = graphics.color_rgb(252, 157, 160)
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
    '''move the shape from the "Next Shape" area to the beginning of the playing grid'''
    shape = []
    for i in predicted_shape:
        i.move(350,510)
        shape.append(i)
    return shape
    

def check_full_rows(grid):
    '''Check if the row is full, if it's full, collect the row's y coordinates.
    Erase every block with the same y coordinates and move the rows with larger coordinates down to fill in the missing row.
    Return the list of full rows' y coordinates.'''
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
    full_rows.sort(reverse=True)
    for row in full_rows:  
        for block in grid:
            if block.getP1().getY() > row:
                block.move(0, -30)
    return full_rows

def check_full_screen(shape):
    '''Check if the shape's maximum y coordinates is larger than the playing screen'''
    result = False
    Y_coord = []
    for i in shape:
        Y1 = i.getP1().getY()
        Y_coord.append(Y1)
    if max(Y_coord) == 650:
        result = True
    return result

def update_score(score_text, old_score, full_rows, label_text, win):
    '''Take the old score, and the number of full rows. 
    Count the number of full rows to update the score accordingly'''
    new_score = old_score + len(full_rows) * 100
    score_text.undraw()  # Remove previous score
    label_text.undraw()
    score_text , label_text = draw_score(new_score,win)  # Draw updated score
    return score_text, new_score, label_text

def leaderboard(scores,names,win):
    '''take the list of all the players and all the scores collected, 
    sort the 10 highest scores from high to low and draw the leaderboard on the screen'''
    score_list = scores.copy()
    name_score = []
    name_score = list(zip(names,score_list)) + load_leaderboard()
    name_score = sorted(name_score, key = lambda x: x[1], reverse = True)
    for i in range(min(10, len(name_score))):
        leader_score = graphics.Text(graphics.Point(350,450 - (30*i) ), "{}\t.....\t{}".format(name_score[i][0],name_score[i][1]))
        leader_score.setFace("courier")
        leader_score.setSize(16)
        leader_score.setTextColor("white")
        leader_score.setStyle("bold")
        leader_score.draw(win)
    
    save_leaderboard(name_score)

def save_leaderboard(leaderboard):
    leader_score_json = dict()
    for _ in range(10):
        try:
            leader_score_json[leaderboard[_][0]] = leaderboard[_][1]
        except IndexError:
            break
    os.makedirs(os.path.dirname(leaderboard_file), exist_ok=True)
    with open(leaderboard_file, 'w') as f:
        json.dump(leader_score_json, f)

def load_leaderboard():
    try:
        with open(leaderboard_file, 'r') as f:
            data = json.load(f)
            print(data)
            return sorted(data.items(), key=lambda x: x[1], reverse=True)
    except (FileNotFoundError, json.JSONDecodeError):
        # create the file
        # Ensure the directory exists before opening the file
        os.makedirs(os.path.dirname(leaderboard_file), exist_ok=True)
        with open(leaderboard_file, 'w') as f:
            json.dump({}, f)
        return []
    
def generate_random_name():
    r = RandomWord()

    return r.word(include_parts_of_speech=["adjectives"]).capitalize() + r.word(include_parts_of_speech=["nouns"]).capitalize()


def main():
    '''The main loop for the game:
    1. Take the user's name and store it
    2. Begin the game and the main loop
    3. If game over, store the score and update the leaderboard
    4. The user can play again or exit the game'''
    # create 2 lists to store the user name and score
    names =[]
    scores = []
    play_game = True
    # if play_game is true(at the start or the user choose to play again), draw the start screen
    curName = None
    while play_game:
        win = GraphWin("Tetris Game",700,700)
        win.setBackground(graphics.color_rgb(222,236,255))

        # Sets the coordinate system
        win.setCoords(0,0,700,700)

        # Menu
        cloud_image = Image(Point(350, 350), "images/star_bg.png")
        cloud_image.draw(win)
        tetris_image = Image(Point(350, 530), "images/Tetris_font.png")
        tetris_image.draw(win)
        start_image = Image(Point(350, 280), "images/start.png")
        start_image.draw(win)
        name_box = Entry(Point(350,370), 20)
        name_box.setSize(18)
        name_box.setText(curName if curName else generate_random_name())
        name_box.setFill(graphics.color_rgb(55, 17, 130))
        name_box.setTextColor("white")
        name_box.draw(win)
        rec5 = graphics.Rectangle(graphics.Point(150,50), graphics.Point(550,200))
        rec5.setFill(graphics.color_rgb(55, 17, 130))
        rec5.setOutline("white")
        rec5.draw(win)
        draw_label = graphics.Text(graphics.Point(350,125), "Instructions \n \n 1. Use arrows to move the blocks \n \n 2. Use 'space' to rotate the blocks ")
        draw_label.setFace("arial")
        draw_label.setSize(16)
        draw_label.setTextColor("white")
        draw_label.draw(win)
        u = win.getMouse()

        # if the game hasn't started, then wait and keep listening for start event
        while clicked_start(u) == False:
            u = win.getMouse()

        # HERE iS THE BEGINNING OF THE GAME
        # erase the old elements of the start screen and set up the new playing screen
        curName = name_box.getText()
        names.append(name_box.getText())
        cloud_image.undraw()
        tetris_image.undraw()
        start_image.undraw()
        name_box.undraw()
        rec5.undraw()
        draw_label.undraw()
        
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
        
        predicted_shape, predicted_color = choose_shape(150,140,win)

        score = 0
        score_text, label_text = draw_score(score,win)
        draw_next_shape(win)
        
        delay = 0.2
        grid = []
        center = []
        shape = draw_shape(predicted_shape) 
        color = predicted_color
        predicted_shape, predicted_color = choose_shape(150,140,win)
        '''The main game loop check if the shape can move down or not.
        If the shape can move down, the user can use the keys to move the shape to the left, right, down or rotate the shape and the shape will move down.
        If the shape can't move down, check if game over, then check for full rows, update the score, draw a new shape, and wait the delay amount of time'''
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
                    # move the shape to the bottom
                    while can_move_down(shape,center):
                        move_down(shape,center)
                elif keystrings == "space":
                    for i in shape:
                        i.undraw()
                    shape, color = rotate(shape,color)
                    for i in shape:
                        i.setFill(color)
                        i.setOutline("ivory")
                        i.draw(win)
            else:
                time.sleep(0.2)
                while True:
                    keystrings = win.checkKey()
                    if keystrings == "Left":
                        move_left(shape,center)
                    elif keystrings == "Right":
                        move_right(shape,center)
                    elif keystrings == "space":
                        for i in shape:
                            i.undraw()
                        shape, color = rotate(shape,color)
                        for i in shape:
                            i.setFill(color)
                            i.setOutline("ivory")
                            i.draw(win)
                    else:
                        break
                    time.sleep(0.5)
                if check_full_screen(shape):
                    break
                freeze_shape(shape,grid,win)
                full_rows = check_full_rows(grid)
                score_text, score, label_text = update_score(score_text, score, full_rows,label_text,win)
                center = get_center(grid)
                shape = draw_shape(predicted_shape) 
                color = predicted_color
                predicted_shape, predicted_color = choose_shape(150,140,win)
            time.sleep(delay)
        
        '''If game over, the main game loop break and start drawing the leaderboard screen'''
        scores.append(score)
        rec2 = graphics.Rectangle(graphics.Point(150,50), graphics.Point(550,550))
        rec2.setFill(graphics.color_rgb(55, 17, 130))
        rec2.setOutline("white")

        rec3 = graphics.Rectangle(graphics.Point(151,49), graphics.Point(350,200))
        rec3.setFill(graphics.color_rgb(55, 17, 130))
        rec3.setOutline(graphics.color_rgb(55, 17, 130))

        rec4 = graphics.Rectangle(graphics.Point(351,49), graphics.Point(549,200))
        rec4.setFill(graphics.color_rgb(55, 17, 130))
        rec4.setOutline(graphics.color_rgb(55, 17, 130))

        cloud_image = Image(Point(350, 350), "images/star_bg.png")
        cloud_image.draw(win)
        game_over_image = Image(Point(350, 625), "images/game_over.png")
        game_over_image.draw(win)
        rec2.draw(win)
        replay_image = Image(Point(250, 100), "images/replay.png")
        replay_image.draw(win)
        exit_image = Image(Point(450, 100), "images/exit.png")
        exit_image.draw(win)


        leader_score = graphics.Text(graphics.Point(350,500), "LEADERBOARD")
        leader_score.setFace("courier")
        leader_score.setSize(20)
        leader_score.setTextColor("white")
        leader_score.setStyle("bold")
        leader_score.draw(win)

        leaderboard(scores,names,win)
        
        # check if the user want to play again or not
        click_point = win.getMouse()
        if inside(click_point,rec3):
            play_game = True
            win.close()
        elif inside(click_point,rec4):
            play_game = False

    win.close()
        
if __name__ == "__main__":
    main()
