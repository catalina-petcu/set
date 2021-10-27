#the ttk module offers widgets that are specialized according to the operating system.
# So buttons created using ttk will look different on Mac then on Windows
from tkinter import *
from tkinter import ttk  
from random import randint
import time
from datetime import datetime
from tkinter import simpledialog
import csv

def main():
    #indices of the attributes of cards
    COLOR = 0 #colors are ["red", "green", "purple"]
    SHAPE = 1 #shapes are ["oval", "squiggle", "diamond"]
    SHADING = 2 #shaddings are ["solid", "striped", "outlined"]
    NUMBER = 3 #numbers are ["1", "2", "3"]

    #global variables that are used throughtout the program
    global root, deck, score, cards_showing, cards_remained, selected_cards, cards_matched, canvas, score_variable, time_variable, message_variable, start_time, hinted_cards, time_identifier, hint_button
   
    #initializing information about the cards
    card_width = 90
    card_height = 140
    canvas_width = 4 * card_width + 40 + 30
    canvas_height = 3 * card_height + 40 + 20
    shape_width = 70
    shape_height = 30
    hinted_cards = []

    #initializing the root of the tkinter frame, the canvas for drawing the cards and the StringVars used to set the labels
    root = Tk()
    root.resizable(False, False)
    root.title("Set")
    canvas = Canvas(root, width=canvas_width, height=canvas_height, bg="white")
    score_variable = StringVar()
    time_variable = StringVar()
    message_variable = StringVar()

    create_menu()
    new_game(True)

def create_menu():
    global root
    #avoid the tear off option which makes menu options floatable
    root.option_add("*tearOff", False)

    #create a menu bar with 2 menus
    menu_bar = Menu(root)
    root.config(menu = menu_bar)
    file = Menu(menu_bar)
    help = Menu(menu_bar)
    
    #add the menus to the menu bar
    menu_bar.add_cascade(menu = file, label = "File")
    menu_bar.add_cascade(menu = help, label = "Help")
    
    #add commands for the menu options and a separator to make New Game and High Score stand apart
    file.add_command(label = "New Game", command = new_game)
    file.add_separator()
    file.add_command(label = "High Score", command = show_high_scores)
    help.add_command(label = "How to play", command = show_game_instructions)

#A function to start a new game. The first parameter indicates if it is the first time the game starts
#so it know not to redraw the top frame, just the cards and change all the labels.
def new_game(first = False):
    global cards_showing, cards_remained, cards_matched, selected_cards, score, canvas, score_label, start_time
    
    #initiliza the main global variables of the program
    deck = get_deck()
    cards_remained = deck
    cards_showing = []
    cards_matched = []
    selected_cards = []
    score = 0
    start_time = time.strftime("%H:%M:%S")

    #functions to populate the top frame with its labels and draw the cards
    set_top_frame(first)
    update_time()
    draw_cards_from_deck(12)
    draw_cards()

    #bind the canvas to the left click event to check selection/deselection of card
    canvas.pack()
    canvas.bind('<Button 1>', select_card)
    root.mainloop()

#function that returns all the cards in the set deck.
def get_deck():
    deck = []
    for color in range(0, 3):
        for shape in range(0,3):
            for shading in range(0, 3):
                for number in range(0, 3):
                    deck.append([color, shape, shading, number])
    return deck

#Function to set the top frame. The variable first indicates if this is the first game and if so to 
#create all labels. If it is not the first game, then it only resets the labels.
def set_top_frame(first):
    global score_variable, time_variable, message_variable, hint_button
    if first:
        #create the frame that contains all the labels from the top
        frame = ttk.Frame(root)
        frame.pack()
        frame.config(height = 100, width = 430)
        frame.config(relief = RIDGE)

        #create the score label
        score_label = ttk.Label(frame)
        score_label.config(textvariable = score_variable)
        score_label.grid(row = 0, column = 1, ipadx = 20, stick = "nsw", )

        #create the message label and set its style to be shown in orange    
        label_style = ttk.Style()
        label_style.configure("Set.TLabel", foreground="orange")
        message_label = ttk.Label(frame, text = "", textvariable=message_variable, style="Set.TLabel")
        message_label.grid(row= 0, column = 2, stick = "nsw")

        #create the time label 
        time_label = ttk.Label(frame)
        time_label.config(textvariable=time_variable)
        time_label.grid(row = 0, column = 3, stick ="nsew", ipadx = 10)

        #create the Hint button with a different style to be shown in blue
        button_style = ttk.Style()
        button_style.configure("Set.TButton", foreground = "blue")
        hint_button = ttk.Button(frame, text = "Hint", command = hint, style = "Set.TButton")
        hint_button.grid(row = 0, column = 4, stick ="esn")
    #set the variables attached to the labels and make sure the hint_button is set to normal again
    hint_button.config(state="normal")
    message_variable.set("                                       ")
    time_variable.set("0:00:00")
    score_variable.set("Score: 0")

#a function that update the time label counter on the top frame
def update_time():
    global time_variable, root, time_identifier

    #calculate the difference between the start_time of the game and the time
    #the current function is called and then set the variable for the time label
    now = time.strftime("%H:%M:%S")
    d1 = datetime.strptime(now, "%H:%M:%S")
    d2 = datetime.strptime(start_time, "%H:%M:%S")
    time_variable.set(d1-d2)

    #set a timer to start after 1 second and call this function again
    #the information for this timer is stored in a variable so it can be stoped when the game ends
    time_identifier = root.after(1000, update_time)
    #root.after(50000, something)

#get number_of_cards random cards from the rest of the cards that have not been used
# making sure there are still cards to be drawn from.
# It also updates the cards that are shown on the screen and the ones that remain unused.
def draw_cards_from_deck(number_of_cards):
    global cards_showing, cards_remained
    if len(cards_remained) != 0:
        for _ in range(0,number_of_cards):
            card_index = randint(0, len(cards_remained)-1)
            cards_showing.append(cards_remained[card_index])
            cards_remained.pop(card_index)

#arranges the cards to be shown in a matrix and calls the draw_card_on_canvas function with data
#about where to place the card and which card to show.
def draw_cards():
    index_in_cards_showing = 0
    for row in range(1, 4):
        for column in range(1, 5):
            if index_in_cards_showing < len(cards_showing):
                draw_card_on_canvas(row, column, cards_showing[index_in_cards_showing])
                index_in_cards_showing +=1
            else:
                #in case there are less then 12 cards to be shown on screen, the place of the previous cards
                #is modified by drawing a white rectangle and cover that area
                x0, y0 = get_card_canvas_area(row, column)
                canvas.create_rectangle(x0, y0, x0+90, y0+140, outline = "white", fill="white")
    #after each redrawing of cards, the hint function is called to make sure there are available options
    hint(False)

#a function that receives a card's attibuted and the information about where it should be drawn
#and wheather is selected or not and draws the card border and calls the apropiate function to draw
#the interior of the card
def draw_card_on_canvas(row_at, column_at, card_attributes, selected = False):
    global canvas
    attributes = get_attributes(card_attributes)
    x0, y0 = get_card_canvas_area(row_at, column_at)

    #the card background is by default white, unless is selected and it should be pink
    fill = "white"
    if selected:
        fill="pink"
    
    #the card border is drawn
    canvas.create_rectangle(x0, y0, x0+90, y0+140, outline = "white", fill="white", width = 3)
    canvas.create_rectangle(x0, y0, x0+90, y0+140, outline = "black", fill=fill)

    #get all the positions at which to draw shapes in the card
    points = get_position_for_shapes(x0, y0, attributes["number"])

    #get all the attributes of the cards
    color = attributes["color"]
    shape = attributes["shape"]
    stripes = False
    filled = False
    if attributes["shadding"] == "striped":
        stripes = True
    elif attributes["shadding"] == "solid":
        filled = True
    
    #call functions to draw all the shapes in the card according to their attributes
    if shape == "oval":
        for (x, y) in points:
            draw_round_rectangle(canvas, stripes, filled, color, x, y, x+60, y+30, selected, radius=20)
    elif shape == "squiggle":
        for (x, y) in points:
            draw_squiggle(canvas, stripes, filled, color, x, y, x+ 60, y+ 30, selected)
    else:
        for (x, y) in points:
            draw_diamond(canvas, stripes, filled, color, x, y, x+ 60, y+ 30, selected)

#a function to get the attributes of the card. The attributes are stored as numbers to make it easier
#to store and check; it returned a dictionary with all the attributes of the card
def get_attributes(card_attributes):
    attributes = {}
    attributes["color"] = "red"
    if card_attributes[0] == 1:
        attributes["color"] = "green"
    elif card_attributes[0] == 2:
        attributes["color"] = "purple"

    attributes["number"] = 1
    if card_attributes[3] == 1:
        attributes["number"] = 2
    elif card_attributes[3] == 2:
        attributes["number"] = 3
    
    attributes["shadding"] = "solid"
    if card_attributes[2] == 1:
        attributes["shadding"] = "striped"
    elif card_attributes[2] == 2:
        attributes["shadding"] = "outlined"
    
    attributes["shape"] = "oval"
    if card_attributes[1] == 1:
        attributes["shape"] = "squiggle"
    elif card_attributes[1] == 2:
        attributes["shape"] = "diamond"
    return attributes

#a function that receives the row and column the card should be at and returns
# the starting x and y positions of the card
def get_card_canvas_area(row_at, column_at):
    x0, y0 = (20, 20)
    if row_at == 2:
        y0 = 170
    elif row_at == 3:
        y0 = 320
    
    if column_at == 2:
        x0 = 120
    elif column_at == 3:
        x0 = 220
    elif column_at == 4:
        x0 = 320
    return x0, y0

#gets the starting x and y of a card and returns the staring x and y of all the shapes that are inside the card
def get_position_for_shapes(x0, y0, number_of_shapes):
    #add padding of 15 from the card border
    x = x0+ 15
    points = []
    if number_of_shapes == 1:
        points.append([x, y0 + 55])
    elif number_of_shapes == 2:
        points.append([x, y0 + 35])
        points.append([x, y0 + 75])
    else:
        points.append([x, y0+15])
        points.append([x, y0+55])
        points.append([x, y0+95])
    return points

#A function that I found on https://stackoverflow.com/questions/44099594/how-to-make-a-tkinter-canvas-rectangle-with-rounded-corners
# that draws a rounded rectangle by drawing a polygon
def draw_round_rectangle(canvas,stripes, filling, color, x1, y1, x2, y2, selected = False, radius=25):
    points = [x1+radius, y1, x1+radius, y1, x2-radius, y1, x2-radius, y1, x2, y1,
              x2, y1+radius, x2, y1+radius, x2, y2-radius, x2, y2-radius, x2, y2,
              x2-radius, y2, x2-radius, y2, x1+radius, y2, x1+radius, y2, x1, y2,
              x1, y2-radius, x1, y2-radius, x1, y1+radius, x1, y1+radius, x1, y1]

    #select the color to fill the shape in case it outlined and to draw the lines if it is stripped
    fill = "white"
    if selected:
        fill = "pink"

    #draw the rounded rectangle
    if not filling:
        canvas.create_polygon(points, fill= fill, outline=color, smooth=True)
    else:
        canvas.create_polygon(points, fill = color, smooth=True)
    
    #draw the stripes in case the shape is striped
    if stripes:
        for x in range(x1 + 5, x2-2, 5):
            canvas.create_line(x, y1, x, y2, fill=color)

#a function to draw the squiggle form
def draw_squiggle(canvas, stripes, filled, color, x1, y1, x2, y2, selected = False):
    #set the colors for the background and the fill color for the shapes that make up the squiggle
    fill = "white"
    if selected:
        fill = "pink"
    if not filled:
        fill_color = fill
    else:
        fill_color = color
        canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="")
    
    #in case the shape is stripped, the stripes are drawn over the entire card and then they are erased
    #by drawing white rectangles or white archs over it.
    striples=False
    if stripes:
        for x in range(x1+5, x2, 5):
            canvas.create_line(x, y1+2, x, y2-2, fill=color)
    arc_height = int((y2-y1)/4)
    arc_width = int((x2-x1)/2)

    #The squiggle is made up of 4 arches with different fillings
    canvas.create_arc(x1, y1, x1+arc_width,y1+arc_height+11, start=0, extent=180, outline = color, style="arc")
    canvas.create_arc(x1+arc_width,y1+arc_height-5, x2,y1+arc_height*2, start=0, extent=-180, outline = color, style="arc")
    if  not stripes and not filled:
        canvas.create_arc(x1+arc_width,y1+arc_height-5, x2,y1+arc_height*2, start=0, extent=-180, outline = color, style="arc")
        canvas.create_arc(x1, y1 +arc_height * 2-1, x1+arc_width,y2-arc_height+11, start=0, extent=180, outline = color, style="arc")
    else:
        canvas.create_arc(x1+arc_width,y1+arc_height-5, x2,y1+arc_height*2, start=0, extent=-180, outline = color, style="chord", fill=fill)
        canvas.create_arc(x1, y1 +arc_height * 2-1, x1+arc_width,y2-arc_height+11, start=0, extent=180, outline = color, style="chord", fill=fill)
   
    canvas.create_arc(x1+arc_width,y2-arc_height-5, x2,y2, start=0, extent=-180, outline = color, style="arc")
    
    #if case the shape has stripes or it needs to be filled, there are some parts of the card that need to be redrawn
    if stripes or filled:
        canvas.create_polygon(x1, y2-arc_height-2, x1+arc_width, y2-arc_height-2, x1+arc_width, y2, x1, y2, fill=fill)
        canvas.create_polygon(x1+arc_width, y1, x2, y1, x2, y1+arc_height+2, x1+arc_width, y1+arc_height+1, fill=fill)
    if filled:
        canvas.create_polygon(x1, y1, x1+ arc_width/2, y1, x1, y1+arc_height, fill=fill)
        canvas.create_polygon(x1+ int(arc_width/2), y1, x1+arc_width, y1, x1+arc_width, y1+arc_height, fill=fill)
        canvas.create_polygon(x1+arc_width, y2-arc_height, x1+arc_width, y2, x2-int(arc_width/2), y2, fill=fill)
        canvas.create_polygon(x2-arc_width/2, y2, x2, y2, x2, y2-arc_height/2, fill=fill)
        canvas.create_line(x1, y2, x2, y2, fill=fill)
        canvas.create_line(x1, y1, x1, y2, fill=fill)
        canvas.create_line(x2, y1, x2, y2, fill=fill)
    else:
        canvas.create_line(x1, y1+arc_height-1, x1, y2-arc_height-2, fill=color)
        canvas.create_line(x2, y1+arc_height+3, x2, y2-arc_height+5, fill=color)

#function to draw a diamond
def draw_diamond(canvas, stripes, filled, color, x1, y1, x2, y2, selected = False):
    #selec the color for the background of the card
    fill = "white"
    if selected:
        fill = "pink"
    
    #if the shape is striped, there are lines drawn for the entire space
    #and then covered by white/pink polygons
    if stripes:
        for x in range(x1+5, x2-2, 5):
            canvas.create_line(x, y1, x, y2, fill=color)
        canvas.create_polygon(x1, y1+ 15, x1, y1, x1 + 30, y1, fill=fill)
        canvas.create_polygon(x1+30, y1, x2, y1, x2, y1+ 15, fill=fill)
        canvas.create_polygon(x2, y1+15, x2, y2, x1+30, y2, fill=fill)
        canvas.create_polygon(x1+ 30, y2, x1, y2, x1, y1+15, fill=fill)
    
    #the cornors of the diamond are calculated and the shape is drawn
    top_x = int((x2-x1)/2) + x1
    left_y = int((y2-y1)/2) + y1
    bottom_x = int()
    points = [top_x, y1, x2, left_y,top_x, y2,x1, left_y]
    if filled:
        canvas.create_polygon(points, fill=color)
    else:
        canvas.create_polygon(points, outline=color, fill="")

#function called when left click. It 
def select_card(event):
    global cards_showing, score, score_variable, message_variable, selected_card
    x, y = event.x, event.y
    x0, y0 = search_coordinate(x, y)

    #if any of the coordinates it's zero, it means the click was not made inside one of the cards
    #so the function can return
    if x0 == 0 or y0 == 0:
        return

    #finding the index of the card that was clicked on
    index_of_card = (y0-1) * 4 + x0 - 1
    card = cards_showing[index_of_card]

    if card in selected_cards:
        #if the card was selected before, it needs to be removed from the selected cards and redrawn
        selected_cards.remove(card)
        score -= 1
        draw_card_on_canvas(y0, x0, card)
    else:
        #if it was not previously selected, it it added to the selected cards array and redrawn
        selected_cards.append(card)
        draw_card_on_canvas(y0, x0, card, True)

        #if there are 3 cards selected by now, they need to be checked to see if they are a match
        if len(selected_cards) == 3:
            if check_selected_cards():
                #if the 3 selected cards are a match, they are removed from the cards_showing array,
                #3 more cards are drawn from the deck and drawn on the screen and the message label is set
                for card in selected_cards:
                    cards_showing.remove(card)
                draw_cards_from_deck (3)
                draw_cards()
                selected_cards.clear()
                message_variable.set("That was a match!!!    ")
                root.after(3000, clear_message_label)
            else:
                #if the cards are not a match, they are being deselected and a message is shown
                deselect_selected_cards()
                message_variable.set("That was not a match!!!")
                root.after(3000, clear_message_label)
    score_variable.set(f"Score: {score}")

#a function to clear the meesage label
def clear_message_label():
    global message_variable
    message_variable.set("                                       ")

#Return the row and the column in the cards table for the x and y coordinates.
#90 width of card; 140-height of card; 10-space between cards; 20 padding
def search_coordinate(x, y):
    column = 0
    row = 0
    if x >=20 and x <= 110:
        column = 1
    if x >= 120 and x<=210:
        column = 2
    if x >= 220 and x <=310:
        column = 3
    if x>= 320 and x <=410:
        column = 4

    if y>= 20 and y<=160:
        row = 1
    if y>= 170 and y <= 310:
        row = 2
    if y>=320 and y<=460:
        row = 3
    print(f"x: {x} y: {y} column: {column} row: {row}")
    return column, row


#a function that looks for a match in the cards on the screen. It it called both by clicking on the Hint button
#and when any changes are made to the cards of the screen to make sure there is a match.
def hint(was_hint_pressed = True):
    global score, score_variable, cards_showing, hinted_cards

    #score decreases by 2 every time the Hint button is pressed
    if was_hint_pressed:
        score -= 2
        score_variable.set(f"Score: {score}")
    #find out if there are 3 cards from card_showing that are a match
    found_match = False
    for first_index in range(0, len(cards_showing)-2):
        card1 = cards_showing[first_index]
        for second_index in range(first_index + 1, len(cards_showing)-1):
            card2 = cards_showing[second_index]
            for third_index in range(second_index + 1, len(cards_showing)):
                card3 = cards_showing[third_index]
                #all the values of the cards are checked. If one of them is not fulfilled, the cards are not a match
                if check_values_of_card(card1[0], card2[0], card3[0]) and check_values_of_card(card1[1], card2[1], card3[1]) and check_values_of_card(card1[2], card2[2], card3[2]) and check_values_of_card(card1[3], card2[3], card3[3]):
                    if was_hint_pressed:
                        #if there is a match and the hint button was pressed, the hinted cards are drawn
                        #differently so the user can see the match and the function returns True
                        set_hinted_cards(first_index, second_index, third_index)
                    return True
    #If the function reaches this point, it means there are no more matches on the screen.
    if len(cards_remained) !=0:
        #if there are still cards that have not been shown, the redraw function is called,
        #which changes all cards on the screen
        redraw()
    else:
        #if there are no more cards left, it means the game has ended
        end_game()
    return False

#a function to check if three values are a match;
# it is used only for the same attributes of a card, not for all
def check_values_of_card(x, y, z):
    #the attributes fulfill the set requirments if they are all equal
    if x == y and y == z:
        return True
    #or if they are all the same
    if x != y and y != z and x != z:
        return True
    return False

#a function to check if the selected cards are a match
def check_selected_cards():
    global score, cards_matched
    card1 = selected_cards[0]
    card2 = selected_cards[1]
    card3 = selected_cards[2]
    if check_values_of_card(card1[0], card2[0], card3[0]) and check_values_of_card(card1[1], card2[1], card3[1]) and check_values_of_card(card1[2], card2[2], card3[2]) and check_values_of_card(card1[3], card2[3], card3[3]):
        #if the cards are a match, they are moved to the cards_matched array and the score is updated
        cards_matched.append(card1)
        cards_matched.append(card2)
        cards_matched.append(card3)
        score += 2

        if selected_cards[0] in hinted_cards and selected_cards[1] in hinted_cards and selected_cards[2] in hinted_cards:
            #if the cards are part of the hint shown, the score should decrease
            score -= 2
        hinted_cards.clear()
        return True
    #if the function reaches this point, it means the selected cards are not a match, so the score is updated
    score -= 1
    return False

#a function to deselect all selected cards
def deselect_selected_cards():
    for card in selected_cards:
        #find out the index of the card in the cards_showing array
        index = cards_showing.index(card)
        #find out the index of the card in the canvas
        x0 = int (index / 4)
        y0 = int (index %4) 
        #redraw the card with a white background
        draw_card_on_canvas(x0+1, y0+1, card, False)
    #clear the selected_cards array
    selected_cards.clear()

#a function that redraws the hinted cards when the Hint button is pressed
def set_hinted_cards(first_index, second_index, third_index):
    card1 = cards_showing[first_index]
    card2 = cards_showing[second_index]
    card3 = cards_showing[third_index]
    set_hint_card(first_index)
    set_hint_card(second_index)
    set_hint_card(third_index)
    hinted_cards.append(card1)
    hinted_cards.append(card2)
    hinted_cards.append(card3)

#a function that highlites a hinted card using its index in the main array of cards_showing
#then creates a blue border around it to mark it as hinted
def set_hint_card(index):
    x = int (index / 4) + 1
    y = int (index %4) + 1
    x0, y0 = get_card_canvas_area(x, y)
    canvas.create_rectangle(x0, y0, x0+90, y0+140, outline = "blue", fill="", width = 3)

#a function to redraw the cards if there are not matches        
def redraw():
    global cards_remained, cards_showing, selected_cards
    #all the unmatched cards are added into the cards_remained array and the cards_showing is cleared
    cards_remained += cards_showing
    cards_showing.clear()
    selected_cards.clear()

    #12 new cards are drawn
    draw_cards_from_deck( 12)
    draw_cards()

    #the hint function is called to make sure there is a match on the screen
    hint(False)

#a function that starts the end of the game
def end_game():
    #the timer is cancelled and the score is calculated accordingly
    root.after_cancel(time_identifier)
    set_score_according_to_time()
    hint_button.config(state="disabled")
    #a log is shown asking the user for this name so it can be included in the high score list
    name = simpledialog.askstring("Game over", "Enter your name for the high score list.",
                                parent=root)
    #If the user provided a name, then it will be aded to the high score if it is in the first 10.
    if name is not None:
        set_high_scores(name)

#at the end, the score is calculated according to the points earned during the game and the time spent
def set_score_according_to_time():
    global score
    now = time.strftime("%H:%M:%S")
    d1 = datetime.strptime(now, "%H:%M:%S")
    d2 = datetime.strptime(start_time, "%H:%M:%S")
    difference = (d1 - d2).total_seconds()
    if score != 0:
        score = round(score / difference, 3) * 100


#opens the high_scores.csv file and checks to see if the current score can be included
def set_high_scores(name):
    high_score_names = []
    high_scores = []
    high_score_dates = []
    is_modified = False
    today = datetime.today().strftime('%m-%d-%Y')
    index_in_high_scores = 0

    with open("high_scores.csv") as csv_file:
        reader = csv.reader(csv_file)
        next(reader)
        for row in reader:
            if row != "":
                index_in_high_scores += 1
                current_score = float(row[1])
                #if the current score in the file is smaller then
                #the score to be added into the high score and it was not added already
                if score > current_score and not is_modified:
                    is_modified = True
                    index_in_high_scores += 1
                    high_score_names.append(name)
                    high_scores.append(score)
                    high_score_dates.append(today)
                #if there are already 10 scores and the current score in the file is not equal to the last one
                #added to the score list, the for is exited
                if index_in_high_scores > 10 and str(current_score) != high_scores[len(high_scores)-1]:
                    break
                else:
                    high_score_names.append(row[0])
                    high_scores.append(row[1])
                    high_score_dates.append(row[2])
    #if the high score list does not have 10 scores yet ot the last score in the list is equal to the current user's score
    #and the score has not been added yet, the information about it will be added to the corresponding arrays
    if (len(high_score_dates) < 10 or str(score) == str(high_scores[len(high_scores)-1])) and not is_modified:
        is_modified = True
        high_score_names.append(name)
        high_scores.append(score)
        high_score_dates.append(today)
    #if a new score has been added to the array, the file needs to change
    if is_modified:
        modify_high_scores_file(high_score_names, high_scores, high_score_dates)
    show_high_scores()

#a function to show the high scores
#it is shown when the menu option is chosen or after the user enters his name
def show_high_scores():
    #a new window is created
    high_scores_window = Toplevel(root)
    high_scores_window.title("High scores")
    scores_table = []
    index = 0

    #the high_scores.csv file is read and the information is added in the scores_table
    with open("high_scores.csv") as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            if index != 0:
                list = (index, row[0], row[1], row[2])
            else:
                list = ("", row[0], row[1], row[2])
            index += 1
            scores_table.append(list) 
    
    #all the scores in the scores_table are drawn on the new window created
    for i in range(len(scores_table)):
        for j in range(4):
            e = Entry(high_scores_window, width=10, fg='blue')
            e.grid(row=i, column=j)
            e.insert(END, scores_table[i][j])
    high_scores_window.mainloop()

#a function to write inside the high_score.csv file
def modify_high_scores_file(high_score_names, high_scores, high_score_dates):
    with open("high_scores.csv", "w", newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["Name","Score","Date"])
        for index in range(0, len(high_score_names)):
            row = []
            row.append(high_score_names[index])
            row.append(high_scores[index])
            row.append(high_score_dates[index])
            writer.writerow(row)


#a function to show the game instructions when the menu option is chosen
def show_game_instructions():
    instructions_window = Toplevel(root)
    instructions_window.title("How to play")
    instructions = """A set consists of three cards satisfying all of these conditions:

They all have the same number or have three different numbers.
They all have the same shape or have three different shapes.
They all have the same shading or have three different shadings.
They all have the same color or have three different colors.
The rules of Set are summarized by: If you can sort a group of three cards into "two of ____ and one of ____", then it is not a set.

For example, these three cards form a set:

One red striped diamond
Two red solid diamonds
Three red open diamonds
Given any two cards from the deck, there is one and only one other card that forms a set with them.
(source: https://en.wikipedia.org/wiki/Set_(card_game) )"""

    text_label = Label(instructions_window, text= instructions, height=20, width=70, justify = "left", wraplength=480)
    text_label.pack()

    instructions_window.mainloop()


if __name__ == "__main__":
    main()