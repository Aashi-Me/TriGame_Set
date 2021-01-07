#################################
############ Imports ############
#################################
from graphics import *
import time
import random

#################################
########### Functions ###########
#################################
def TIR(rect, text):
    return Text(rect.getCenter(), text)


def slowDraw(p, t, canvas):
    text = title(Text(p, "")).draw(canvas)
    text.setSize(100)
    for element in range(len(t) + 1):
        text.setText(t[0:element])
        time.sleep(0.075)
    return Text(p, t)
        

def title(text):
    text.setTextColor(colours[0])
    text.setFace(heading_font)
    text.setSize(40)
    return text


def heading(text):
    text.setTextColor(colours[0])
    text.setFace(heading_font)
    text.setSize(36)
    return text


def body(text):
    text.setTextColor(colours[0])
    text.setFace(body_font)
    return text


def makeGrid(fontsize, size, p1, p2, win, icons=["X", "O", "!"]):
    rectangles = []
    objects = []
    x1 = p1.getX()
    y1 = p1.getY()
    x2 = p2.getX()
    y2 = p2.getY()

    space_x = (x2 - x1)/(size)
    space_y = (y2 - y1)/(size)

    for i in range(size):
        for a in range(size):
            rect = Rectangle(Point(x1 + i*space_x, y1 + a*space_y), Point(x1 + (i + 1)*space_x, y1 + (a + 1)*space_y)).draw(win)
            rect.setFill(colours[0])
            rectangles.append(rect)
            
            lis = []
            for fgh in icons:
                textfgh = title(TIR(rect, fgh))
                textfgh.setSize(fontsize)
                textfgh.setFill(colours[2])
                lis.append(textfgh)
            objects.append(lis)
            
    return [rectangles, objects]


def choose_icon(icons, fontsiz, siz, p_1, p_2, canvas, tex="Your", colour="black"):
    Image(Point(x/2, y/2), "background3.png").draw(win)
    gri = makeGrid(fontsiz, siz, p_1, p_2, canvas, icons)
    text = heading(Text(Point(x/2, y/8), "Choose {} Icon".format(tex))).draw(win)
    back_rect.draw(win)
    back_text.draw(win)
    close_rect.draw(win)
    close_text.draw(win)
    for ghi in range(len(gri[1])):
        gri[1][ghi][ghi].draw(canvas)

    while True:
        cl = win.getMouse()
        x_coord = cl.getX()
        y_coord = cl.getY()
        
        for i in range(len(gri[0])):
            if gri[0][i].ClickedOn(x_coord, y_coord, win):
                return i
            
        if back_rect.ClickedOn(x_coord, y_coord, win):
            return Difficulty_Level(win)
        
        if close_rect.ClickedOn(x_coord, y_coord, win):
            return win.close()


def is_victory(icons):
    for z in [[0,1,2], [3,4,5], [6,7,8], [0,3,6], [1,4,7], [2,5,8], [0,4,8], [2,4,6]]:
        if set(z).issubset(set(icons)):
            return True
    return False


def is_draw(icons1, icons2):
    if (set(icons1) | set(icons2)) == set({1,2,3,4,5,6,7,8,0}):
        return True
    else:
        return False

    
def computer_move(diff, plmo, como):
    possmoves = list(set([i for i in range(9)]) - (set(plmo) | set(como)))
    takenmoves = list(set(plmo) | set(como))
    plmoCopy = plmo[:]
    comoCopy = como[:]
    
    for i in [comoCopy, plmoCopy]:
        for y in possmoves:
            i.append(y)
            if is_victory(i):
                move = y
                return move
            i.remove(y)

    if diff == 3:
        EdgesOpen = []
        if (0 in plmoCopy and 8 in plmoCopy and 4 in comoCopy) or \
           (2 in plmoCopy and 6 in plmoCopy and 4 in comoCopy):
            for z in possmoves:
                if z in [1,3,5,7]:
                    EdgesOpen.append(z)
            if len(EdgesOpen) > 0:
                move = random.choice(EdgesOpen)
                return move

        if len(plmoCopy) == 1:
            if 1 in plmoCopy or 3 in plmoCopy or 5 in plmoCopy or 7 in plmoCopy:
                if 1 in plmoCopy:
                    tempChoices = [0, 2]
                elif 3 in plmoCopy:
                    tempChoices = [0, 6]
                elif 5 in plmoCopy:
                    tempChoices = [2, 8]
                elif 7 in plmoCopy:
                    tempChoices = [6, 8]
                tempChoices.sort(reverse=random.choice([True, False]))
                
                for element in tempChoices:
                    if element in possmoves:
                        return element

        if 4 in possmoves:
            return 4

    elif diff == 2:
        for element in [0,2,6,8]:
            if element in plmoCopy and 4 in possmoves:
                return 4

    cornersOpen = []
    for x in possmoves:
        if x in [0,2,6,8]:
            cornersOpen.append(x)
    if len(cornersOpen) > 0:
        move = random.choice(cornersOpen)
        return move

    elif 4 in possmoves:
        move = 4
        return move

    else:
        move = random.choice(possmoves)
        return move

    move = random.choice(possmoves)
    return move


def Num_Players(win):
    global num_players
    win.undrawAll()
    Image(Point(x/2, y/2), "background.png").draw(win)
    rect1 = Rectangle(Point(x/9, 3*y/7), Point(4*x/9, 4*y/7)).draw(win)
    rect1_text = body(TIR(rect1, "Computer")).draw(win)
    rect2 = Rectangle(Point(5*x/9, 3*y/7), Point(8*x/9, 4*y/7)).draw(win)
    rect2_text = body(TIR(rect2, "2 Players")).draw(win)
    
    back_rect.draw(win)
    back_text.draw(win)
    close_rect.draw(win)
    close_text.draw(win)

    while True:
        click = win.getMouse()
        click_x = click.getX()
        click_y = click.getY()
        
        if rect1.ClickedOn(click_x, click_y, win):
            num_players = 1
            return Difficulty_Level(win)
        elif rect2.ClickedOn(click_x, click_y, win):
            num_players = 2
            return TTT(win)
        elif back_rect.ClickedOn(click_x, click_y, win):
            return PickGame(win)
        elif close_rect.ClickedOn(click_x, click_y, win):
            return win.close()
    


def Make_Person(r):
    ax = x/4
    ay = 2*y/3 + 25
    
    pol1 = Image(Point(ax, ay), "1.png")
    pol2 = Image(Point(ax, ay), "2.png")
    strn = Image(Point(ax, ay), "3.png")
    face = Image(Point(ax, ay), "4.png")
    bodi = Image(Point(ax, ay), "5.png")
    hand = Image(Point(ax, ay), "6.png")
    leg1 = Image(Point(ax, ay), "7.png")
    leg2 = Image(Point(ax, ay), "8.png")

    if diff_level == 1:
        person = [[pol1], [pol2], [strn], [face], [bodi], [hand], [leg1], [leg2]]
    elif diff_level == 2:
        person = [[pol1, pol2], [strn], [face], [bodi], [hand], [leg1, leg2]]
    elif diff_level == 3:
        person = [[pol1, pol2, strn], [face, bodi], [hand], [leg1, leg2]]
    
    return person


################################
######### Introduction #########
################################
def Introduction(win):
    game_name = "Storm "
    win.undrawAll()
    win.setTitle(game_name)

    win.undrawAll()
    Image(Point(x/2, y/2), "storm_background.png").draw(win)
    text = Text(Point(x/2, 2*y/5 + 30), game_name)
    text.setFace(heading_font)
    text.setStyle('bold italic')
    text.setSize(80)
    text.setTextColor(colours[0])
    text.draw(win)

    body(Text(Point(x/2, 3*y/5 + 20), "This game contains a package of 3: \nTic Tac Toe, Hangman and Battleship! \nClick to get Started!")).draw(win)

    win.getMouse()


#################################
###### Screen 1: Find name ######
#################################
def EnterName(win):
    win.undrawAll()
    win.setTitle("Name")
    Image(Point(x/2, y/2), "dark_background.png").draw(win)
    Image(Point(3*x/4, y/2), "small_storm_looking_left.png").draw(win)
    name_text = Text(Point(2*x/5, y/3), "What is your Name?")
    title(name_text).draw(win)
    name_entry = Entry(Point(2*x/5, y/2), int(x/40)).draw(win)
    name_entry.setFace(body_font)
    
    key = win.getKey()
    
    while name_entry.getText() == "" or key != "Return" or len(name_entry.getText()) > 8:
        key = win.getKey()

    name = name_entry.getText()
    name = name.title().strip()
    return name


#################################
###### Screen 2: Find Game ######
#################################
def PickGame(win):
    global game
    ghi = 75
    win.undrawAll()
    win.setTitle("Pick a Game!")
    Image(Point(x/2, y/2), "background_image.png").draw(win)
    text = heading(Text(Point(x/2, y/3 + ghi), "Pick a Game, {}".format(name))).draw(win)
    rect1 = Rectangle(Point(x/16, y/2 + ghi), Point(5*x/16, 2*y/3 + ghi)).draw(win)
    rect2 = Rectangle(Point(3*x/8, y/2 + ghi), Point(5*x/8, 2*y/3 + ghi)).draw(win)
    rect3 = Rectangle(Point(11*x/16, y/2 + ghi), Point(15*x/16, 2*y/3 + ghi)).draw(win)
    rec1t = body(TIR(rect1, "Tic Tac Toe")).draw(win)
    rec2t = body(TIR(rect2, "Hangman")).draw(win)
    rec3t = body(TIR(rect3, "Battleship")).draw(win)

    while True:
        click = win.getMouse()
        click_x = click.getX()
        click_y = click.getY()
        if rect1.ClickedOn(click_x, click_y, win):
            game = 1
            return Num_Players(win)
        elif rect2.ClickedOn(click_x, click_y, win):
            game = 2
            break
        elif rect3.ClickedOn(click_x, click_y, win):
            game = 3
            break
    return Difficulty_Level(win)


#################################
### Screen 3: Find Difficulty ###
#################################
def Difficulty_Level(win):
    global diff_level
    win.undrawAll()
    win.setTitle("Start")
    
    Image(Point(x/2, y/2), "background2.png").draw(win)
    
    back_rect.draw(win)
    back_text.draw(win)
    close_rect.draw(win)
    close_text.draw(win)
    
    inst_rect = Rectangle(Point(x/4, y/6), Point(3*x/4, y/3)).draw(win)
    inst_text = heading(TIR(inst_rect, "Instructions")).draw(win)
    
    diff_level = heading(Text(Point(x/2, y/2), "Difficulty Level")).draw(win)
    
    diff_level_easy_rect = Rectangle(Point(x/16, 2*y/3), Point(5*x/16, 5*y/6)).draw(win)
    diff_level_mid_rect = Rectangle(Point(3*x/8, 2*y/3), Point(5*x/8, 5*y/6)).draw(win)
    diff_level_imp_rect = Rectangle(Point(11*x/16, 2*y/3), Point(15*x/16, 5*y/6)).draw(win)

    if game == 1:
        diff_levels = ["Easy", "Medium", "Hard"]

    elif game == 2:
        diff_levels = ["8 Turns", "6 Turns", "4 Turns"]
        
    elif game == 3:
        diff_levels = ["5 by 5", "7 by 7", "10 by 10"]
    
    diff_level_easy_text = body(TIR(diff_level_easy_rect, diff_levels[0])).draw(win)
    diff_level_mid_text = body(TIR(diff_level_mid_rect, diff_levels[1])).draw(win)
    diff_level_imp_text = body(TIR(diff_level_imp_rect, diff_levels[2])).draw(win)

    while True:
        click = win.getMouse()
        click_x = click.getX()
        click_y = click.getY()
        
        if back_rect.ClickedOn(click_x, click_y, win):
            return PickGame(win)

        elif close_rect.ClickedOn(click_x, click_y, win):
            return win.close()
        
        elif inst_rect.ClickedOn(click_x, click_y, win) and instOpen == False:
            inst = GraphWin("Instructions", x, y)
            Instructions(inst)
        elif diff_level_easy_rect.ClickedOn(click_x, click_y, win):
            diff_level = 1
            break
        elif diff_level_mid_rect.ClickedOn(click_x, click_y, win):
            diff_level = 2
            break
        elif diff_level_imp_rect.ClickedOn(click_x, click_y, win):
            diff_level = 3
            break
        
    if game == 1:
        return TTT(win)
    elif game == 2:
        return HM(win)
    elif game == 3:
        return BS(win)


################################
#### Screen 4- Instructions ####
################################
def Instructions(win):
    global instOpen
    instOpen = True
    win.setTitle("Instructions")
    win.setBackground(colours[2])
    win.undrawAll()
    Image(Point(x/2, y/2), "dark_background.png").draw(win)
    close_rect = Rectangle(Point(x - 5*x/32, y/32), Point(x - x/32, 3*y/32)).draw(win)
    close_text = body(TIR(close_rect, "Close")).draw(win)
    if game == 1:
        inst_text = heading(Text(Point(x/2, y/8), "Tic Tac Toe")).draw(win)
        body_text = body(Text(Point(x/2, 4.5*y/8), "This version of Tic Tac Toe allows you to choose your own icon form a selection of 16. \nThe second player will also be able to select their own icon from the remaining icons. \nSelect your icon by simply clicking on it. After that, the game screen will appear. \nOn this screen, the first player's nametag at the bottom will be highlighted. \nClick on a square on your turn. Remember to pick one that hasn't already been chosen! \nThe gameplay will continue until one of 2 things happen: \n1- A Player has their icons appear 3 times in a row; diagonally, horizontally or vertically. \n2- All of the boxes on the grid are filled. \nIf one of the 2 happen, the gameplay stops and a screen will appear which describes \nthe outcome. \n\nGood Luck!")).draw(win)
    elif game == 2:
        inst_text = heading(Text(Point(x/2, y/8), "Hangman")).draw(win)
        body_text = body(Text(Point(x/2, y/2), "In this version of hangman, you can click on the letter that you want to guess. \nIf the letter is in the word, it will be displayed by replacing one of the dashes \nwith the letter. All of the As in the word are already displayed. \nIf you get the letter wrong, a figurine will pop up to which we will add \nlines if you continue getting the letters wrong. \nYou will have a certain number of turns to guess the word. \nIf you guess it wrong, Batman dies. Otherwise, he lives ;) \n\nGood Luck!")).draw(win)
    elif game == 3:
        inst_text = heading(Text(Point(x/2, y/8), "Battleship")).draw(win)
        body_text = body(Text(Point(x/2, y/2), "In this version of the game, you will play with the computer. You will pick the space that \nyour ship is placed in. In the next screen, the gameplay starts. In order for you to win, \nyou must continue guessing until you hit the computer's ship. \nIf the computer gets your one first, it wins! If you get the computer's one first, you win! \nThere is no strategy required, you can place you ship anywhere you like and the \ncomputer will do the same. \nThis is just a guessing game. \n\nGood Luck!")).draw(win)

    while True:
        if close_rect.getClickedOn(win):
            win.close()
            instOpen = False
            return


#################################
######### Screen 5- TTT #########
#################################
def TTT(win):
    global diff_level, tttwins, tttlose
    
    win.undrawAll()
    win.setTitle("Tic Tac Toe")
    width = y/2

    if num_players == 1:
        player2 = "Computer"
    else:
        player2 = "Player 2"
        
    icon = choose_icon(emojis, 30, 4, Point(x/2 - width/2, y/2 - width/2), Point(x/2 + width/2, y/2 + width/2), win)
    win.undrawAll()
    player2_icon = choose_icon(emojis, 30, 4, Point(x/2 - width/2, y/2 - width/2), Point(x/2 + width/2, y/2 + width/2), win, player2)
    win.undrawAll()
    while player2_icon == icon:
        player2_icon = choose_icon(emojis, 30, 4, Point(x/2 - width/2, y/2 - width/2), Point(x/2 + width/2, y/2 + width/2), win, player2)
        win.undrawAll()
        
    Image(Point(x/2, y/2), "background3.png").draw(win)
    grid = makeGrid(40, 3, Point(x/2 - width/2, y/2 - width/2), Point(x/2 + width/2, y/2 + width/2), win, emojis)
    
    back_rect.draw(win)
    back_text.draw(win)
    close_rect.draw(win)
    close_text.draw(win)
    ttt_text = heading(Text(Point(x/2, y/2 - 3*width/4), "Tic Tac Toe")).draw(win)
    play_but = Rectangle(Point(x/2 - x/6, y - y/6), Point(x/2, y - y/12)).draw(win)
    play_but.setFill(colours[2])
    comp_but = Rectangle(Point(x/2, y - y/6), Point(x/2 + x/6, y - y/12)).draw(win)
    comp_but.setFill(colours[2])
    play_tex = body(Text(play_but.getCenter(), name)).draw(win)
    comp_tex = body(Text(comp_but.getCenter(), player2)).draw(win)
    play_score = body(Text(Point((x/2 - width/2)/2 - 10, 4*y/5), "{} = {}".format(str(grid[1][0][icon].getText()), tttwins))).draw(win)
    comp_score = body(Text(Point(3*x/4 + width/4 + 10, 4*y/5), "{} = {}".format(str(grid[1][0][player2_icon].getText()), tttlose))).draw(win)
    player = []
    comput = []
    player_moves = []
    comput_moves = []

    while True:
        #Check if Computer Won or Draw
        if is_victory(comput_moves):
            tttlose += 1
            time.sleep(1.5)
            if num_players == 1:
                return Lost(win)
            elif num_players == 2:
                return Won(win, "2 WON!", "Player 2 Won!!!")
        elif is_draw(comput_moves, player_moves):
            time.sleep(1.5)
            return Draw(win)
        
        #Player Move
        for jk in range(num_players):
            if jk == 0:
                play_but.setFill(colours[1])
            elif jk == 1:
                comp_but.setFill(colours[1])
                
            while True:
                click = win.getMouse()
                click_x = click.getX()
                click_y = click.getY()
                
                if back_rect.ClickedOn(click_x, click_y, win):
                    if num_players == 1:
                        return TTT(win)
                    else:
                        return PickGame(win)

                elif close_rect.ClickedOn(click_x, click_y, win):
                    return win.close()
                
                for i in range(len(grid[0])):
                    if grid[0][i].ClickedOn(click_x, click_y, win):
                        try:
                            if jk == 0 and i not in player_moves and i not in comput_moves:
                                grid[1][i][icon].draw(win)
                                player_moves.append(i)
                            elif jk == 1 and i not in player_moves and i not in comput_moves:
                                grid[1][i][player2_icon].draw(win).setFill(colours[1])
                                comput_moves.append(i)
                            else:
                                close_rect.draw(win)
                            break
                        except:
                            GraphicsError
                else:
                    continue
                break
            if jk == 0:
                play_but.setFill(colours[2])
                if is_victory(player_moves):
                    tttwins += 1
                    time.sleep(1.5)
                    return Won(win)
                elif is_draw(comput_moves, player_moves):
                    time.sleep(1.5)
                    return Draw(win)
                
            elif jk == 1:
                comp_but.setFill(colours[2])

        #Check if Player Won
        if is_victory(player_moves):
            tttwins += 1
            time.sleep(1.5)
            return Won(win)
        elif is_draw(comput_moves, player_moves):
            time.sleep(1.5)
            return Draw(win)

        if num_players == 1:
            #Computer's Move
            comp_but.setFill(colours[1])
            compmove = computer_move(diff_level, player_moves, comput_moves)
            time.sleep(0.5)
            grid[1][compmove][player2_icon].draw(win).setFill(colours[1])
            comput_moves.append(compmove)
            comp_but.setFill(colours[2])


################################
######### Screen 5- HM #########
################################
def HM(win):
    win.undrawAll()
    win.setTitle("Hangman")
    Image(Point(x/2, y/2), "background3.png").draw(win)
    back_rect.draw(win)
    back_text.draw(win)
    close_rect.draw(win)
    close_text.draw(win)
    titl = title(Text(Point(x/2, y/8), "Hangman")).draw(win)

    r = y/30
    person = Make_Person(r)

    if diff_level == 1:
        Turns = 8
    elif diff_level == 2:
        Turns = 6
    elif diff_level == 3:
        Turns = 4
    Turns_done = Turns

    Word_List = ["Awkward", "Bagpipes", "Banjo", "Bungler", "Croquet", "Crypt","Dwarves", "Fervid", "Fishhook", "Fjord", "Gazebo", "Gypsy","Haiku", "Haphazard", "Hyphen", "Icicle", "Ivory", "Jazzy", "Jiffy","Jinx", "Jukebox", "Kayak", "Kiosk", "Klutz", "Memento","Mystify", "Numbskull", "Ostracize", "Oxygen", "Pajama","Phlegm", "Pixel", "Polka", "Quad", "Quip", "Rhythmic", "Rogue","Sphinx", "Squawk", "Swivel", "Toady", "Twelfth", "Unzip", "Waxy","Wildebeest", "Yacht", "Zealous", "Zigzag", "Zombie", "Ample", "Ambiguity", "Artist", "Ace", "Apple", "Burnt", "Banana", "Beautiful", "Basement", "Broken", "Boulder", "Cat", "Crevasses", "Cranberry", "Crater", "Carnival", "Doctor", "Doorbell", "Drastic", "Denmark", "Dreadful", "Elephant", "Enormous", "Exercise", "Excel", "Ebbing", "Flattery", "Fantasy", "Flask", "Flabbergast", "Five", "Giraffe", "Gravel", "Grasp", "Grammar", "Glacier", "Hyperbole", "Handicapped", "Harvest", "Hastily", "Heroine", "Inkwell", "Indian", "Immigrant", "Inside", "Impossible", "Jabber", "Joke", "Jail", "Jack", "January", "Kimono", "King", "Kick", "Landscape", "Leftovers", "Kid", "Lamborghini", "Lamb", "Late", "Meat", "May", "Mate", "Mood", "Mint", "nUEROSURGEON", "NERD", "Near", "Nice", "Never", "Open", "Old", "Occasion", "Okay", "Oats", "Prank", "Pillars", "Probable", "Pray", "Pane", "Queen", "Quality", "Quantity", "Quake", "Quiz", "Robber", "Read", "Realistic", "Realise", "Remember", "Snake", "Story", "Sold", "Soldier", "Shaken", "Trek", "Trouble", "Tranquility", "Trait", "Table", "Umbrella", "Ute", "Underestimate", "Understand", "Useful", "Van", "Vain", "Voice", "Vocal", "Vanish", "Wall", "Wake", "Warden", "Waste", "Well", "Youth", "Yatch", "Yellow", "Yen", "Yes", "Zebra", "zoo", "Zodiac", "Zealous", "zest"]
    Word = random.choice(Word_List).upper()
    Word_Guess = ["_" for i in Word]
    Word_Temp = []
    guessed = []
    print_dash = body(Text(Point(x/2, y/3), " ".join(Word_Guess)).draw(win))
    print_dash.setSize(40)
    
    xshift = -200
    yshift = -50
    p1 = Point(3*x/4 + xshift, y/2 + yshift)
    p2 = Point(3*x/4 + y/2 + xshift, y + yshift)
    keyboard = makeGrid(20, 5, p1, p2, win, "b c d e f g h i j k l m n o p q r s t u v w x y z".upper().split(" "))
    
    for abc in range(25):
        keyboard[1][abc][abc].draw(win)

    for i in range(len(Word)):
        Word_Temp.append(Word[i])
        
    if "A" in Word_Temp:
        for f in range(len(Word)):
            if Word_Temp[f] == "A":
                Word_Guess[f] = "A"

    while Turns != 0 and Word_Guess != Word:
        click = win.checkMouse()
        if click != None:
            click_x = click.getX()
            click_y = click.getY()
            
            for element in range(len(keyboard[0])):
                if keyboard[0][element].ClickedOn(click_x, click_y, win) and element not in guessed:
                    keyboard[0][element].setFill(colours[1])
                    guessed.append(element)
                    letter = keyboard[1][element][element].getText()
                    
                    if letter not in Word:
                        Turns -= 1
                        for vz in person[Turns_done - 1 - Turns]:
                            vz.draw(win)
            
                    elif letter in Word_Temp:
                        for f in range(len(Word)):
                            if Word_Temp[f] == letter:
                                Word_Guess[f] = letter
            
                    if Word_Guess == Word_Temp:
                        print_dash.setText(Word)
                        time.sleep(2)
                        Won(win)
                        return
            
                    elif Turns == 0:
                        print_dash.setText(Word)
                        time.sleep(2)
                        Lost(win)
                        return
            
            if back_rect.ClickedOn(click_x, click_y, win):
                Difficulty_Level(win)
                return

            elif close_rect.ClickedOn(click_x, click_y, win):
                win.close()
                return

        print_dash.setText(" ".join(Word_Guess))

    
################################
######### Screen 5- BS #########
################################
def BS(win):
    win.undrawAll()
    
    win.setTitle("Battleship")
    
    Image(Point(x/2, y/2), "background3.png").draw(win)
    
    back_rect.draw(win)
    back_text.draw(win)
    close_rect.draw(win)
    close_text.draw(win)

    if diff_level == 1:
        siz = 5
    elif diff_level == 2:
        siz = 7
    elif diff_level == 3:
        siz = 10

    width = y/2
    temp_board = makeGrid(15, siz, Point(x/2 - width/2, y/2 - width/2), Point(x/2 + width/2, y/2 + width/2), win, emojis)
    titl = title(Text(Point(x/2, y/8), "Pick Your Ship Space")).draw(win)

    while True:
        click = win.getMouse()
        click_x = click.getX()
        click_y = click.getY()
        
        if back_rect.ClickedOn(click_x, click_y, win):
            return Difficulty_Level(win)

        elif close_rect.ClickedOn(click_x, click_y, win):
            return win.close()

        for element in range(len(temp_board[0])):
            if temp_board[0][element].ClickedOn(click_x, click_y, win):
                player_ship = element
                break

        else:
            continue
        break

    win.undrawAll()
    Image(Point(x/2, y/2), "storm_background.png").draw(win)
    back_rect.draw(win)
    back_text.draw(win)
    close_rect.draw(win)
    close_text.draw(win)

    play_rect = Rectangle(Point(0, y/2 - 80), Point(50, y/2 + 80)).draw(win)
    play_text = body(Text(play_rect.getCenter(), name, 90)).draw(win)
    comp_rect = Rectangle(Point(x - 50, y/2 - 80), Point(x, y/2 + 80)).draw(win)
    comp_text = body(Text(comp_rect.getCenter(), "Computer", -90)).draw(win)
    
    titl = title(Text(Point(x/2, y/8), "Battleship")).draw(win)
    
    board = makeGrid(15, siz, Point(x/2 - width - 20, y/2 - width/2), Point(x/2 - 20, y/2 + width/2), win, emojis)
    board2 = makeGrid(15, siz, Point(x/2 + 20, y/2 - width/2), Point(x/2 + 20 + width, y/2 + width/2), win, emojis)
    line = Line(Point(x/2, y/2 - width/2), Point(x/2, y/2 + width/2)).draw(win)
    ship = random.randint(0, siz**2 - 1)
    guessed = []

    while True:
        while True:
            play_rect.setFill(colours[1])
            click = win.getMouse()
            click_x = click.getX()
            click_y = click.getY()
            
            if back_rect.ClickedOn(click_x, click_y, win):
                return Difficulty_Level(win)

            elif close_rect.ClickedOn(click_x, click_y, win):
                return win.close()

            for i in range(len(board[0])):
                if board[0][i].ClickedOn(click_x, click_y, win):
                    try:
                        if i == ship:
                            board[0][i].setFill(colours[1])
                            board[1][i][-1].draw(win)
                            time.sleep(2)
                            return Won(win)
                            break
                        else:
                            board[0][i].setFill("lightgrey")
                            board[1][i][-2].draw(win)
                            break

                    except:
                        GraphicsError
            else:
                continue
            break
        play_rect.setFill(colours[2])

        comp_rect.setFill(colours[1])
        time.sleep(0.1)
        num = random.randint(0, siz**2 - 1)
        while num in guessed:
            num = random.randint(0, siz**2 - 1)
            
        if num == player_ship:
            guessed.append(num)
            board2[1][num][-1].draw(win)
            board2[0][num].setFill(colours[1])
            time.sleep(2)
            return Lost(win)
        
        elif num != player_ship:
            guessed.append(num)
            board2[0][num].setFill("lightgrey")
            board2[1][num][-2].draw(win)
        comp_rect.setFill(colours[2])


#################################
#### Screen 6- Lost/Won/Draw ####
#################################
def Won(win, t1="You WON!!!", t2="You WON!!!"):
    win.undrawAll()
    Image(Point(x/2, y/2), "won_image.png").draw(win)
    won_text = title(slowDraw(Point(x/2, y/2), t1, win))
    back_rect.draw(win)
    back_text.draw(win)
    close_rect.draw(win)
    close_text.draw(win)

    while True:
        click = win.getMouse()
        click_x = click.getX()
        click_y = click.getY()
        
        if back_rect.ClickedOn(click_x, click_y, win):
            PickGame(win)
            return

        if close_rect.ClickedOn(click_x, click_y, win):
            win.close()
            return


def Lost(win, t1="", t2=""):
    win.undrawAll()
    Image(Point(x/2, y/2), "dark_background.png").draw(win)
    if t1 != "":
        lost_text = title(slowDraw(Point(x/2, y/2), t1, win))
        time.sleep(0.5)
        lost_text.setText(t2)
        lost_text.draw(win)
    else:
        lost_text = title(slowDraw(Point(x/2, y/2), "You Lost :(", win))
    back_rect.draw(win)
    back_text.draw(win)
    close_rect.draw(win)
    close_text.draw(win)

    while True:
        click = win.getMouse()
        click_x = click.getX()
        click_y = click.getY()
        
        if back_rect.ClickedOn(click_x, click_y, win):
            PickGame(win)
            return

        if close_rect.ClickedOn(click_x, click_y, win):
            win.close()
            return


def Draw(win):
    win.undrawAll()
    Image(Point(x/2, y/2), "dark_background.png").draw(win)
    draw_text = title(slowDraw(Point(x/2, y/2), "It was a Draw...", win))
    back_rect.draw(win)
    back_text.draw(win)
    close_rect.draw(win)
    close_text.draw(win)

    while True:
        click = win.getMouse()
        click_x = click.getX()
        click_y = click.getY()

        if back_rect.ClickedOn(click_x, click_y, win):
            return PickGame(win)
        if close_rect.ClickedOn(click_x, click_y, win):
            return win.close()


###########################
######## Variables ########
###########################
colours = ["white", "grey", "black"]
heading_font = "playfair display black"
body_font = "poppins"

emojis = [u"\uD83D\uDC08", u"\uD83D\uDC15", u"\uD83D\uDC28", u"\uD83D\uDC18",
          u"\uD83D\uDC3C", u"\uD83D\uDC27", u"\uD83D\uDC35", u"\uD83D\uDC07",
          u"\uD83D\uDC2C", u"\uD83D\uDC01", u"\uD83D\uDC29", u"\uD83D\uDC05",
          u"\uD83D\uDC19", u"\uD83D\uDC1F", u"\uD83D\uDC24", u"\uD83D\uDC20",
          u"\uD83D\uDCA6", u"\uD83D\uDCA3"]


instOpen = False
game = 0
diff_level = 0
tttwins = 0
tttlose = 0
hmwins = 0
bswins = 0
num_players = 0


##########################
######### Window #########
##########################
x = 1200
y = 800
win = GraphWin("", x, y)
win.setBackground(colours[2])

back_rect = Rectangle(Point(x/32, y/32), Point(5*x/32, 3*y/32))
back_text = body(TIR(back_rect, "Back"))
close_rect = Rectangle(Point(x - 5*x/32, y/32), Point(x - x/32, 3*y/32))
close_text = body(TIR(close_rect, "Close"))


################################
######### Run the Game #########
################################
Introduction(win)
name = EnterName(win)
game = PickGame(win)
