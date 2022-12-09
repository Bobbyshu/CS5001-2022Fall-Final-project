import math
import random
import time
import os
import turtle

from tile import Tile
from background import *
from turtle_tool import Tool
from datetime import datetime


class Game:
    def __init__(self):
        # initialize the background
        self.sc = turtle.Screen()  # get the screen
        self.sc.title('CS5001 Sliding Puzzle Game')
        self.sc.setup(800, 700)
        self.sc.bgcolor('white')
        turtle.hideturtle()

        # distribute the attribute
        self.username = "Default"
        self.max_step = 5
        # list for storing info of file
        self.leaders_list = []
        # information dictionary of the puzzle
        self.info_dict = {}
        # set the interval between 2 tiles
        self.tile_interval = 2
        # steps counter
        self.player_steps = 0
        # List<Tile> total_tiles = new ArrayList<>()
        self.total_tiles = []
        # the position index of the blank tile
        self.blank_tile_index = 0

        # main pen
        self.pen = Tool()

        # thumbnail turtle pen
        self.thumb_pen = Tool(LEADER.get("thumbnail"))

        # step counter pen
        self.step_pen = Tool(LEADER.get("step_counter"))

        self.play()

    def play(self):
        """
        initialize the SlidingPuzzle
        :return: None
        """
        # get the information
        self.show_image('splash_screen', 3)
        self.username = self.get_username()
        self.max_step = self.get_max_step()
        # generate user interface
        self.draw_frames()
        self.load_button()
        # assess leader from file
        self.leaders_list = self.read_leaderboard_file()
        # print it into frame
        self.show_leaderboard()
        # change puzzle
        self.load_puzzle()
        # draw counter
        self.draw_counter()

        turtle.mainloop()

    def show_image(self, name, seconds=3):
        """
        show the intro image for users
        :param name: str
        :param seconds: int
        :return: None
        """
        image = IMAGE.get(name)
        self.sc.register_shape(image)
        load = turtle.Turtle(shape=image)
        time.sleep(seconds)
        # load to next stage
        load.ht()

    def get_username(self):
        """
        get the username
        :return: str
        """
        username = self.sc.textinput('CS5001 Puzzle Slide', 'Your Name:')
        if username is None or username.strip() == '':
            return "Default"
        return username

    def get_max_step(self):
        """
        get the max step for user, default number is 50(same as video)
        :return: int
        """
        step = self.sc.numinput('Puzzle Slide Game - Moves',
                                'Enter the number of moves (chances) you want (5-200)?',
                                50, minval=5, maxval=200)
        if step is None:
            return 50
        elif type(step) == float:
            return math.floor(step)
        else:
            return step

    def draw_frames(self):
        """
        Draw the frames as user interface
        :return: None
        """
        for each in FRAME.values():
            self.pen.goto(each[0])
            self.pen.draw_rectangle(each[1], each[2], each[3])

    def load_button(self):
        """
        bind the image with function
        :return: None
        """
        # load reset button
        pen = Tool(BUTTON.get("reset_button")[0])
        pen.create_button(BUTTON.get("reset_button")[1], self.reset)
        # load quit button
        pen2 = Tool(BUTTON.get("load_button")[0])
        pen2.create_button(BUTTON.get("load_button")[1], self.load)
        # load load button
        pen1 = Tool(BUTTON.get("quit_button")[0])
        pen1.create_button(BUTTON.get("quit_button")[1], self.quit)

    def reset(self, x, y):
        """
        let tiles return to their original position and update cur index
        x, y are bound with mouse click
        :param: int
        :param: int
        :return: None
        """
        position_list = self.generate_positions()
        # return
        for i in range(int(self.info_dict.get("number"))):
            self.total_tiles[i].goto(position_list[self.total_tiles[i].get_index()])
            self.total_tiles[i].update_cur_index(self.total_tiles[i].get_index())

    def load(self, x, y):
        """
        let user choose a new file to load and process the error
        x, y are bound with mouse click
        :param: int
        :param: int
        :return: None
        """
        puzzles = self.get_puz()
        title = 'Load Puzzle'
        notification = ('Enter the name of the puzzle you wish to load. Choices are:\n'
                        + '\n'.join(puzzles))
        choice = self.sc.textinput(title, notification)

        # if user didn't choose cancel
        if choice is not None:
            choice = choice.strip()
            try:
                self.load_puzzle(choice)
            except IOError:
                # print("Inside 169 line branch")
                self.show_image("file_error")
                self.log_error("File '{}' does not exist.".format(choice), "Game.load()")
            except ValueError:
                self.show_image("file_error")
                self.log_error("Malformed puzzle file: {}".format(choice), "Game.load_puzzle()")

    def get_puz(self):
        """
        scan and get file name end with (.puz) from directory
        :return: list
        """
        files = os.listdir(".")
        puzzles = []
        for file in files:
            if file.endswith(".puz"):
                puzzles.append(file)
        if len(puzzles) > 10:
            self.show_image("file_warning")
        return puzzles[:10]

    def quit(self, x, y):
        """
        finish game with gif of quit and credit
        x, y are bound with mouse click
        :param: int
        :param: int
        :return: None
        """
        self.show_image('quitmsg')
        self.sc.clearscreen()
        self.sc.bye()

    def read_leaderboard_file(self):
        """
        Get game leaders list from leaderboard file.
        If failing to open the file,
        show error image and log the error, return [max_step, username]
        :return: -- list
        """
        leaders = []
        try:
            with open('leaderboard.txt', mode='r') as infile:
                for each in infile:
                    each = each.split(":")
                    leaders.append([int(each[0].strip()), each[1].strip()])
        except IOError:
            self.show_image('leaderboard_error')
            name = "Could not open leaderboard.txt."
            location = 'Game.read_leaderboard_file()'
            self.log_error(name, location)
        return leaders

    def log_error(self, name, location):
        """
        print error log to the '5001_puzzle.err
        :param: name: str
        :param: location: str
        :return: None
        """
        cur_time = datetime.now().strftime('%c') + ':'
        name = 'Error: ' + name
        location = ' LOCATION: ' + location
        with open('5001_puzzle.err', mode='a') as file:
            file.write(cur_time + name + location + '\n')

    def show_leaderboard(self):
        """
        read the content of leaders_list(updated from file) and show
        it in the left upper frame
        :return: None
        """
        self.pen.goto(LEADER.get("leaders_text"))
        self.pen.pencolor("blue")
        self.pen.write("Leaders: ", align='left', font=('Arial', 17, 'normal'))
        self.pen.setheading(270)
        # the gap between title and grade
        self.pen.forward(40)
        for step, username in self.leaders_list:
            # limited the longest length to show
            info = "{} : {}".format(step, username[:16])
            self.pen.write(info, align='left', font=('Arial', 15, 'normal'))
            self.pen.forward(25)

    def load_puzzle(self, choice='mario.puz'):
        """
        load puzzle based on the user choice
        the default puzzle is mario
        each time it will change related attribute
        :param: choice: str
        :return: None
        """
        self.read_puzzle_file(choice)
        # reset the counter and steps
        self.player_steps = 0
        self.step_pen.clear()
        for each in self.total_tiles:
            each.clear()
            each.hideturtle()
        self.total_tiles = []
        # load new tiles
        self.generate_tiles()
        # load thumbnail
        self.load_thumbnail(self.info_dict.get("thumbnail"))

    def read_puzzle_file(self, choice):
        """
        read puzzle based on the user choice
        check whether it exists or not
        :param: choice: str
        :return: None
        """
        updated_info_dict = {}
        with open(choice, mode="r") as file:
            for each in file:
                sentence = each.split(":")
                updated_info_dict[sentence[0].strip()] = sentence[1].strip()
        self.check_file(updated_info_dict)

    def check_file(self, updated_info_dict):
        """
        check the quantity of tile and size is legal or not
        :param: choice: str
        :return: None
        """
        # check keys
        if updated_info_dict.keys() <= LEGAL_KEYS:
            raise ValueError
        size = float(updated_info_dict.get("size"))
        num = int(updated_info_dict.get("number"))
        # illegal circumstance
        if (num != 4 and num != 9 and num != 16) or (size > 110 or size < 50):
            raise ValueError
        # check whether each number in the dict
        for i in range(1, num + 1):
            if str(i) not in updated_info_dict:
                raise ValueError
        # after checked can we update
        self.info_dict = updated_info_dict

    def generate_tiles(self):
        """
        generate the tiles and updated total tiles
        :return: None
        """
        position_list = self.generate_positions()
        index_list = list(range(int(self.info_dict.get("number"))))
        random.shuffle(index_list)

        for i in range(len(index_list)):
            new_tile = Tile(self, self.info_dict[str(index_list[i] + 1)],
                            index_list[i], i, position_list[i])
            self.total_tiles.append(new_tile)

    def generate_positions(self):
        """
        generate the tiles and updated total tiles
        :return: list
        """
        position_list = []
        # rank of the tile = sqrt(number)
        rank = int(math.sqrt(int(self.info_dict.get("number"))))
        size = float(self.info_dict.get("size"))
        gap = size + self.tile_interval  # distance between 2 positions

        # calculate the left top tile coordinates (x_0, y_0)
        # FRAME.get("main")[0]: left top coordinates (x, y) of play area
        # FRAME.get("main")[1]: size of play area, (width, height)

        left_upper_x = FRAME.get("main")[0][0] + (FRAME.get("main")[1][0] - (rank - 1) * gap) / 2.0
        left_upper_y = FRAME.get("main")[0][1] - (FRAME.get("main")[1][1] - (rank - 1) * gap) / 2.0

        # print(left_upper_y)

        # generate and append coordinates row by row
        for i in range(rank):
            x = left_upper_x
            for j in range(rank):
                position_list.append((x, left_upper_y))
                x += gap
            left_upper_y -= gap
        return position_list

    def load_thumbnail(self, image):
        """
        load thumbnail
        :param: str
        :return: None
        """
        # render image
        self.sc.register_shape(image)
        self.thumb_pen.shape(image)
        # only start will the thumbnail visible
        if not self.thumb_pen.isvisible():
            self.thumb_pen.showturtle()

    def update_steps(self):
        """
        step++ and update its recording
        check win or not each time after updating
        :return: None
        """
        self.player_steps += 1
        self.step_pen.clear()
        # counter_pen move a bit of right side
        # counter text (-180,-260)
        self.step_pen.goto(-145, -260)
        self.step_pen.write(str(self.player_steps), font=('Arial', 20, 'bold'))

        self.check_succeed()

    def check_succeed(self):
        """
        if tiles are unscrambled, we can show win and exit game
        elif user reach maximum steps, show lose
        else continue playing
        :return: None
        """
        if self.unscrambled():
            self.update_leaderboard()
            self.show_image("winner")
            self.show_image("credits")
            self.sc.clearscreen()
            self.sc.bye()
        elif self.player_steps == self.max_step:
            self.show_image("lose")
            self.show_image("credits")
            self.sc.clearscreen()
            self.sc.bye()

    def unscrambled(self):
        """
        check the index of original order and return the result
        only all pass can we return True
        :return: bool
        """
        for each in self.total_tiles:
            if each.get_index() != each.get_cur_index():
                return False
        return True

    def update_leaderboard(self):
        """
        cuz original file is in order, so we should find the
        location to insert the name and grade by comparing
        :return: None
        """
        i = 0
        # bubble search to the right location
        while (i < len(self.leaders_list)) and (self.player_steps >= self.leaders_list[i][0]):
            i += 1

        # the greatest move
        if i == len(self.leaders_list):
            self.leaders_list.append([self.player_steps, self.username])
        else:
            self.leaders_list.insert(i, [self.player_steps, self.username])

        # update file
        with open('leaderboard.txt', mode='w') as infile:
            # limited to show at most 10 username
            for i in range(min(len(self.leaders_list), 10)):
                infile.write(str(self.leaders_list[i][0]) + ":" + self.leaders_list[i][1] + "\n")

    def set_blank_index(self, index):
        """
        set blank tile index by input index
        :param: int
        :return: int
        """
        self.blank_tile_index = index

    def get_blank_tile(self):
        """
        assess the index of blank tile
        :return: int
        """
        return self.total_tiles[self.blank_tile_index]

    def get_tile_size(self):
        """
        :return: float
        """
        return float(self.info_dict.get("size"))

    def get_tile_interval(self):
        """
        :return: int
        """
        return self.tile_interval

    def draw_counter(self):
        """
        draw counter to register users moves accordingly
        :return: None
        """
        self.pen.goto(LEADER.get("step_text"))
        self.pen.pencolor("black")
        self.pen.write("Player Move: ", font=('Arial', 20, 'bold'))
