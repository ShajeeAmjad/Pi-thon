# Game Resolution: 1280 x 720
# Laptop screen resolution: 2560 x 1600
# Game doesn't scale properly on my own machine,
# but it should scale fine on a 16:9 display.

from tkinter import Tk, Canvas, PhotoImage, Label, Button, Frame, Entry
import random
import ast

cheat_1 = False
cheat_2 = False
cheat_3 = False
is_boss = False
is_paused = False
speed_inc = 0
width = 1280 
height = 720 
level = 1
score = 0
new_score = 0
snake_size = 48
name_list = []
score_list = []
wall_coords = []
positions_loaded = False
file_loaded = False

Vars = {"the_score": 0, "the_snake": [0],  "the_speed": 0, "the_walls": False, "the_positions": []}

def game_screen(Vars):

    global file_loaded, positions_loaded, name_list, high_score, score_list, wall_coords, boss_image, is_boss, cheat_1, cheat_2, cheat_3, level, score, new_score, snake_size, is_paused, width, height, speed_inc, direction

    snake = Vars["the_snake"]

    score = Vars["the_score"]

    speed_inc = Vars["the_speed"]

    def place_food():
        
        global food, food_x, food_y

        food = canvas.create_oval(0, 0, snake_size, snake_size, fill = "steel blue")
        food_x = random.randint(0, int(height / 3))
        food_y = random.randint(0, int(width / 3))
        canvas.move(food, food_x, food_y)

    def place_walls():

        global wall_coords

        Vars["the_walls"] = True

        wall_list = []

        wall_1 = canvas.create_rectangle(0, 0, 1280, 50, fill = "orange")
        wall_2 = canvas.create_rectangle(0, 0, 50, 720, fill = "orange")
        wall_3 = canvas.create_rectangle(0, 720, 1280, 670, fill = "orange")
        wall_4 = canvas.create_rectangle(1280, 0, 1230, 720, fill = "orange")

        wall_list = [wall_1, wall_2, wall_3, wall_4]

        for item in wall_list:
            wall_coords.append(canvas.coords(item))

    def left_key(event):
        
        new_direction = "left"

        global direction

        if new_direction == "left":
            if direction != "right":
                direction = new_direction

    def right_key(event):
        
        new_direction = "right"

        global direction

        if new_direction == "right":
            if direction != "left":
                direction = new_direction

    def up_key(event):

        new_direction = "up"
        
        global direction

        if new_direction == "up":
            if direction != "down":
                direction = new_direction

    def down_key(event):

        new_direction = "down"
        
        global direction

        if new_direction == "down":
            if direction != "up":
                direction = new_direction

    def pause_key(event):

        global save_game
        
        pause(event)

    def boss_key(event):

        global is_boss, boss_image, boss_screen

        pause(event)

        # Screenshot taken from Lab 09 video on Tkinter 2, Graphics and Animation (Tkinter) - Collision Detection
        boss_image = PhotoImage(master = canvas, file = "lecture_screen_r.png")
        boss_screen = canvas.create_image(0, 0, image = boss_image, anchor = "nw")

        if is_boss:
            is_boss = False
            canvas.delete(boss_screen)
        elif not is_boss:
            is_boss = True

    def cheat_key_1(event):

        global cheat_1

        if not cheat_1:
            cheat_1 = True
            shame_text = canvas.create_text(width / 2, 50)
            canvas.itemconfig(shame_text, text = "HOW DARE YOU CHEAT, YOUR SCORE IS LOCKED.")
            canvas.itemconfig(shame_text, font = ("consolas", 30))
        elif cheat_1:
            cheat_1 = False

    def cheat_key_2(event):

        global cheat_2

        if not cheat_2:
            cheat_2 = True
        elif cheat_2:
            cheat_2 = False

    def cheat_key_3(event):

        global cheat_3

        if not cheat_3:
            cheat_3 = True
        elif cheat_3:
            cheat_3 = False

    def replay():

        child_window.destroy()

        global Vars, score_list, wall_coords, boss_image, is_boss, cheat_1, cheat_2, cheat_3, level, score, new_score, snake_size, is_paused, width, height, speed_inc, direction

        Vars = {"the_score": 0, "the_snake": [0],  "the_speed": 0, "the_walls": False, "the_positions": []}

        cheat_1 = False
        cheat_2 = False
        cheat_3 = False
        is_boss = False
        is_paused = False
        speed_inc = 0
        width = 1280
        height = 720 
        level = 1
        score = 0
        new_score = 0
        snake_size = 48
        score_list = []
        name_list = []
        wall_coords = []

        game_screen(Vars)

    def set_child_window_dimensions(w, h):
        
        child_window = Tk()
        child_window.title("Snake")
        ws = child_window.winfo_screenwidth()
        hs = child_window.winfo_screenheight()
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)
        child_window.geometry("%dx%d+%d+%d" % (w, h, x, y))
        return child_window

    def grow_snake():
        
        last_element = len(snake) - 1
        last_element_pos = canvas.coords(snake[last_element])
        snake.append(canvas.create_rectangle(0, 0, snake_size, snake_size, fill = "green"))
        
        if direction == "left" and not is_paused:
            canvas.coords(snake[last_element + 1], last_element_pos[0] + snake_size, last_element_pos[1], last_element_pos[2] + snake_size, last_element_pos[3])
        
        elif direction == "right" and not is_paused:
            canvas.coords(snake[last_element + 1], last_element_pos[0] - snake_size, last_element_pos[1], last_element_pos[2] - snake_size, last_element_pos[3])
        
        elif direction == "up" and not is_paused:
            canvas.coords(snake[last_element + 1], last_element_pos[0], last_element_pos[1] + snake_size, last_element_pos[2], last_element_pos[3] + snake_size)
        
        elif direction == "down" and not is_paused:
            canvas.coords(snake[last_element + 1], last_element_pos[0], last_element_pos[1] - snake_size, last_element_pos[2], last_element_pos[3] - snake_size)
        
        global score, new_score, cheat_1, Vars

        if score >= 0 and score < 100 and not cheat_1:
            score += 10
            new_score = score
            Vars["the_score"] = score
        elif score >= 100:
            score += 20
            new_score = score
            Vars["the_score"] = score

        txt_s = "Score: " + str(new_score)
        score_label.config(text = txt_s)

        if (score == 80 or score == 90) and not cheat_2:
            message = canvas.create_text(width / 2, 40)
            canvas.itemconfig(message, text = "Get ready, walls about to spawn!")
            canvas.itemconfig(message, font = ("consolas", 15))

        if score >= 100:
            level = 2
            txt_l = "Level: " + str(level)
            level_label.config(text = txt_l)
            if not cheat_2 and not Vars["the_walls"]:
                place_walls()

    def move_food():
        
        global food, food_x, food_y
        
        canvas.move(food, (food_x * (-1)), (food_y * (-1)))
        if score < 90:
            food_x = random.randrange(0, int(width / 1.75))
            food_y = random.randrange(0, int(height / 1.75))
        elif score >= 90:
            food_x = random.randrange(65, 1050)
            food_y = random.randrange(65, 600)
        canvas.move(food, food_x, food_y)

    def overlapping(a, b):

        return a[0] < b[2] and a[2] > b[0] and a[1] < b[3] and a[3] > b[1]

    def name_input():

        global enter_name, name, name_list, score_list, pop_up

        name = enter_name.get()

        name_list.append(name)

        leader_file = open("leaderboard.txt", "a")

        for x in range(len(name_list)):
        
            leader_file.write(name_list[x] + " : " + str(score_list[x]) + "\n")
        
        leader_file.close()

        pop_up.destroy()

    def game_over():

        global score, name_list, enter_name, score_list, pop_up

        score_list.append(score)
        
        new_text = canvas.create_text(width / 2, height / 2)
        canvas.itemconfig(new_text, text="Game Over")
        canvas.itemconfig(new_text, font=("consolas", 45))

        replay_button = Button(child_window, text = "Play Again", highlightbackground = "blue", fg = "black", font = ("consolas", 20), command = replay)
        replay_button.config(height = 3, width = 15)
        replay_button.place(relx = 0.5, y = height - 100, anchor = "center")

        pop_up = Tk()
        pop_up.title("Name entry")
        ws = pop_up.winfo_screenwidth()
        hs = pop_up.winfo_screenheight()
        x = (ws/2) - (width/2)
        y = (hs/2) - (height/2)
        pop_up.geometry("%dx%d+%d+%d" % (width, height, x, y))

        b_g = PhotoImage(master = pop_up, file = "game_over.png")
        go_background = Label(pop_up, image = b_g)
        go_background.place(x = 0, y = 0)

        enter_name = Entry(pop_up, width = 40, justify = "center")
        enter_name.grid(row = 0, column = 0, padx = width / 2 - 160, pady = height / 2 - 100, ipady = 20)

        name_button = Button(pop_up, text = "Enter Name", command = name_input)
        name_button.config(height = 3, width = 15)
        name_button.place(x = width / 2, y = height / 2, anchor = "center")

    def save_file():

        global Vars

        save = open("save_file.txt", "w")

        save.write(str(Vars))

        save.close()

    def pause(event):

        global is_paused, pause_screen

        if is_paused:
            is_paused = False
            canvas.move(pause_screen, 1000000000000, 1000000000000)
        elif not is_paused:
            is_paused = True
            pause_screen = canvas.create_text(width / 2, height / 2)
            canvas.itemconfig(pause_screen, text="Paused")
            canvas.itemconfig(pause_screen, font = ("consolas", 45))

    def moveSnake():

        global speed_inc, wall_coords, positions_loaded, Vars, file_loaded
        
        canvas.pack()

        positions = []

        if not positions_loaded:
            positions = Vars["the_positions"]
            positions_loaded = True
        positions.append(canvas.coords(snake[0]))

        if score >= 0 and score < 100:
            
            if positions[0][0] < 0:
                canvas.coords(snake[0], width, positions[0][1], width - snake_size, positions[0][3])
            elif positions[0][1] < 0:
                canvas.coords(snake[0], positions[0][0], height, positions[0][2], height - snake_size)
            elif positions[0][2] > width:
                canvas.coords(snake[0], 0 - snake_size, positions[0][1], 0, positions[0][3])
            elif positions[0][3] > height:
                canvas.coords(snake[0], positions[0][0], 0 - snake_size, positions[0][2], 0)

        if score >= 100:

            if cheat_3:

                if positions[0][0] < 0:
                    canvas.coords(snake[0], width, positions[0][1], width - snake_size, positions[0][3])
                elif positions[0][1] < 0:
                    canvas.coords(snake[0], positions[0][0], height, positions[0][2], height - snake_size)
                elif positions[0][2] > width:
                    canvas.coords(snake[0], 0 - snake_size, positions[0][1], 0, positions[0][3])
                elif positions[0][3] > height:
                    canvas.coords(snake[0], positions[0][0], 0 - snake_size, positions[0][2], 0)

            s_head_pos = canvas.coords(snake[0])
            for item in wall_coords:
                if overlapping(s_head_pos, item) and not cheat_3:
                    gameOver = True
                    game_over()
        
        positions.clear()
        positions.append(canvas.coords(snake[0]))
        
        if not is_paused and direction == "left":
                canvas.move(snake[0], - snake_size, 0)
            
        elif not is_paused and direction == "right":
                canvas.move(snake[0], snake_size, 0)
        
        elif not is_paused and direction == "up":
                canvas.move(snake[0], 0, - snake_size)

        elif not is_paused and direction == "down":
                canvas.move(snake[0], 0, snake_size)
        
        s_head_pos = canvas.coords(snake[0])
        food_pos = canvas.coords(food)
        
        if overlapping(s_head_pos, food_pos):
            move_food()
            grow_snake()

        for i in range(1, len(snake)):
            if overlapping(s_head_pos, canvas.coords(snake[i])) and not cheat_3:
                gameOver = True
                game_over()
        
        for i in range(1, len(snake)):
            
            positions.append(canvas.coords(snake[i]))
        
        for i in range(len(snake) - 1):
            
            if not is_paused:
                canvas.coords(snake[i + 1], positions[i][0], positions[i][1], positions[i][2], positions[i][3])
        
        if "gameOver" not in locals():
            if score == 0:
                child_window.after(90, moveSnake)
            if score % 10 == 0 and score != 0:
                child_window.after(max(40, int(90 - speed_inc)), moveSnake)
                speed_inc += 0.07
                temp = Vars["the_speed"] 
                Vars["the_speed"] = speed_inc
                speed_inc = temp

    child_window = set_child_window_dimensions(width, height)

    txt_s = "Score: " + str(score)
    score_label = Label(child_window, text = txt_s, font = ("consolas", 20), anchor = "w")
    score_label.pack()

    txt_l = "Level: " + str(level)
    level_label = Label(child_window, text = txt_l, font = ("consolas", 20), anchor = "e")
    level_label.pack()

    save_game = Button(child_window, text = "Save Game", highlightbackground = "blue", fg = "black", font = ("consolas", 20), command = save_file)
    save_game.config(height = 1, width = 10)
    save_game.place(x = 50, y = 5)

    canvas = Canvas(child_window, bg = "black", width = width, height = height)
    canvas.create_rectangle(0, 0, width, height, fill = "grey")
    canvas.pack()

    if Vars["the_walls"] == True:
        place_walls()

    place_food()

    if not file_loaded:
        snake[0] = canvas.create_rectangle(snake_size * 2, snake_size * 2, snake_size * 3, snake_size * 3, fill = "red")

    canvas.bind("<Left>", left_key)
    canvas.bind("<Right>", right_key)
    canvas.bind("<Up>", up_key)
    canvas.bind("<Down>", down_key)
    canvas.bind("<p>", pause_key)
    canvas.bind("<b>", boss_key)
    canvas.bind("<q>", cheat_key_1)
    canvas.bind("<w>", cheat_key_2)
    canvas.bind("<e>", cheat_key_3)
    canvas.focus_set()

    direction = "right"

    moveSnake()

    child_window.mainloop()

def set_window_dimensions(w, h):
        
        parent_window = Tk()
        parent_window.title("Snake")
        ws = parent_window.winfo_screenwidth()
        hs = parent_window.winfo_screenheight()
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)
        parent_window.geometry("%dx%d+%d+%d" % (w, h, x, y))
        return parent_window

def start_game():

    global Vars, file_loaded

    game_screen(Vars)

def load_game():

    global file_loaded
    
    load = open("save_file.txt", "r")

    x = load.read()

    new_dict = ast.literal_eval(x)

    Vars = new_dict

    file_loaded = False

    game_screen(Vars)

def scoreboard():

    global score_window
    
    score_window = Tk()
    score_window.title("Leaderboard")
    ws = score_window.winfo_screenwidth()
    hs = score_window.winfo_screenheight()
    x = (ws/2) - (width/2)
    y = (hs/2) - (height/2)
    score_window.geometry("%dx%d+%d+%d" % (width, height, x, y))

    score_text = open("leaderboard.txt", "r")
    temp_string = score_text.read().rstrip()

    name_list = []
    string = ""
    high_score = 0
    high_name = ""

    with open("leaderboard.txt", "r") as f:
        name = [line.rstrip() for line in f]
        for x in range(len(name)):
            string += name[x] + " : "
        f.close()

        only_scores = [int(s) for s in string.split() if s.isdigit()]

        new_list = string.rstrip().replace(" ", "").split(":")

        new_list.pop()

        for i in range(len(new_list)):
            if i < len(new_list):
                new_list.pop(i + 1)
        
        high_score = max(only_scores)
        high_idx = only_scores.index(high_score)
        high_name = new_list[high_idx]

        final_text = "High score: " + high_name + " with " + str(high_score) + "!"

    score_canvas = Canvas(score_window, bg = "black", width = width, height = height)
    score_canvas.create_rectangle(0, 0, width, height, fill = "grey")
    score_canvas.create_rectangle(140, 0, 1140, 720, fill = "light blue")
    page_text = score_canvas.create_text(width / 2, 50)
    score_canvas.itemconfig(page_text, text = "Leaderboard")
    score_canvas.itemconfig(page_text, font = ("consolas", 25))
    score_canvas.create_rectangle(140, 80, 1140, 100, fill = "black")
    text = score_canvas.create_text(width / 2, 330)
    score_canvas.itemconfig(text, text = temp_string)
    score_canvas.itemconfig(text, font = ("consolas", 25))
    hs_text = score_canvas.create_text(width / 2, 135)
    score_canvas.itemconfig(hs_text, text = final_text)
    score_canvas.itemconfig(hs_text, font = ("consolas", 25))
    score_canvas.create_rectangle(140, 170, 1140, 190, fill = "black")
    score_canvas.pack()

    back_b = Button(score_canvas, text = "Back", highlightbackground = "blue", fg = "black", font = ("consolas", 20), command = back_score)
    back_b.config(height = 3, width = 15)
    back_b.place(relx = 0.5, y = 650, anchor = "center")

def back_score():

    global score_window

    score_window.destroy()

def instruc():

    global inst_window

    inst_window = Tk()
    inst_window.title("Instructions")
    ws = inst_window.winfo_screenwidth()
    hs = inst_window.winfo_screenheight()
    x = (ws/2) - (width/2)
    y = (hs/2) - (height/2)
    inst_window.geometry("%dx%d+%d+%d" % (width, height, x, y))

    instruc_canvas = Canvas(inst_window, bg = "black", width = width, height = height)
    instruc_canvas.create_rectangle(0, 0, width, height, fill = "grey")
    instruc_canvas.create_rectangle(0, 50, 1280, 590, fill = "light blue")
    instruc_canvas.pack()

    back_button = Button(instruc_canvas, text = "Back", highlightbackground = "blue", fg = "black", font = ("consolas", 20), command = back_inst)
    back_button.config(height = 3, width = 15)
    back_button.place(relx = 0.5, y = 655, anchor = "center")
    
    game_info = instruc_canvas.create_text(width / 2, 320)
    instruc_canvas.itemconfig(game_info, text = "Welcome to Pi-thon: The Game! It's basically like classic Snake. \n The aim is simple, collect food pellets and \n aim for the highest score. \n Try not to crash into your tail! \n Here are the controls: \n Left key: left \n Right key: right \n Up key: up \n Down key: down \n p : pause game \n b : boss key (Can't be too careful at work) \n q : cheat 1 (Dare to try? Go ahead) \n w : cheat 2 (Prevents walls from spawning in level 2) \n e : cheat 3 (Prevents snake from dying) \n You can toggle the cheat keys to activate and deactivate them. \n Have fun!")
    instruc_canvas.itemconfig(game_info, font=("consolas", 20))

def back_inst():

    global inst_window

    inst_window.destroy()

parent_window = set_window_dimensions(width, height)
parent_window.title("Start screen")

# Background image source: https://unsplash.com/@keithmisner, Author: Keith Misner
# The image itself has been taken and converted to pixel art, but the original image is royalty free.
bg = PhotoImage(file = "background.png") 
start_background = Label(parent_window, image = bg)
start_background.place(x = 0, y = 0)

game_title = Label(parent_window, text = "Pi-thon: The Game", font = ("consolas", 40))
game_title.place(relx = 0.5, y = height/2 - 150, anchor = "n")

instructions = Button(parent_window, text = "Instructions", highlightbackground = "blue", fg = "black", font = ("consolas", 20), command = instruc)
instructions.config(height = 3, width = 15)
instructions.place(relx = 0.5, y = height/2 + 115, anchor = "center")

sb_button = Button(parent_window, text = "Leaderboard", highlightbackground = "blue", fg = "black", font = ("consolas", 20), command = scoreboard)
sb_button.config(height = 3, width = 15)
sb_button.place(relx = 0.5, y = height / 2 + 230, anchor = "center")

load_button = Button(parent_window, text = "Load Game", highlightbackground = "blue", fg = "black", font = ("consolas", 20), command = load_game)
load_button.config(height = 3, width = 15)
load_button.place(x = 250, y = height / 2 + 115, anchor = "center")

end_splash_screen = Button(parent_window, text = "Start Game", highlightbackground = "blue", fg = "black", font = ("consolas", 20), command = start_game)
end_splash_screen.config(height = 3, width = 15)
end_splash_screen.place(relx = 0.5, rely = 0.5, anchor = "center")

parent_window.mainloop()
