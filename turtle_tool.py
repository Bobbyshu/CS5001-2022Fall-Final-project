import turtle


class Tool(turtle.Turtle):
    def __init__(self, directions=(0, 0)):
        """
        New a NewTurtle and set its directions for starting
        Params -- tuple for starting coordinate
        Return -- None
        """
        super().__init__(visible=False)
        self.gs = turtle.getscreen()
        self.pen(pendown=False, speed=0)
        self.goto(directions)

    def draw_rectangle(self, size, color='black', pen_size=1):
        """
        draw a rectangle by input variable, tuple including weight and height
        :param size: tuple
        :param color: str
        :param pen_size: int
        :return: None
        """
        # initialize
        self.pen(pendown=True, pencolor=color, pensize=pen_size)
        # drawing
        self.forward(size[0])
        self.right(90)
        self.forward(size[1])
        self.right(90)
        self.forward(size[0])
        self.right(90)
        self.forward(size[1])
        self.right(90)
        # finish
        self.penup()

    def create_button(self, image, func):
        """
        distribute the button and related them with the event
        :param image: str
        :param func: func
        :return: None
        """
        self.gs.register_shape(image)
        self.shape(image)
        self.showturtle()
        self.onclick(func)
