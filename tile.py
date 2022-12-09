import turtle
from turtle_tool import Tool


class Tile(Tool):
    def __init__(self, game, image, index, cur_index, cords):
        super().__init__(cords)
        self.sc = turtle.getscreen()
        self.game = game
        self.index = index
        self.cur_index = cur_index
        if "blank" in image:
            self.game.set_blank_index(cur_index)
        # render image
        self.sc.register_shape(image)
        self.shape(image)
        self.showturtle()
        self.onclick(self.swap)

    def get_index(self):
        return self.index

    def get_cur_index(self):
        return self.cur_index

    def update_cur_index(self, index):
        self.cur_index = index

    def draw_frame(self, size):
        """
        render image
        :param: float
        :return: None
        """
        cords = self.pos()
        # left upper
        self.goto(cords[0] - size / 2.0, cords[1] + size / 2.0)
        self.draw_rectangle((size, size))
        # back to center
        self.goto(cords)

    def swap(self, x, y):
        """
        get the cord of blank tile, only player choose blank tile
        will the swap succeed
        :param: Tile instance
        :return: None
        """
        blank_tile = self.game.get_blank_tile()
        distance = self.distance(blank_tile.pos())
        # check validate or not
        if distance == self.game.get_tile_size() + self.game.get_tile_interval():
            self.exchange(blank_tile)
            self.game.update_steps()

    def exchange(self, other):
        """
        exchange the position and coordinate of two titles
        :param: Tile instance
        :return: None
        """
        cords = other.pos()
        other.goto(self.pos())
        self.goto(cords)
        # exchange
        temp = self.cur_index
        self.cur_index = other.cur_index
        other.cur_index = temp
