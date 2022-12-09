# hashmap for storing image address
IMAGE = {"credits": "Resources/credits.gif",
         'file_error': "Resources/file_error.gif",
         'file_warning': "Resources/file_warning.gif",
         'leaderboard_error': 'Resources/leaderboard_error.gif',
         'lose': 'Resources/Lose.gif',
         'quitmsg': 'Resources/quitmsg.gif',
         'splash_screen': 'Resources/splash_screen.gif',
         'winner': 'Resources/winner.gif'}

# hashmap for storing frame location
FRAME = {'main': [(-350, 300), (450, 450), 'black', '6'],
         'leaderboard': [(150, 300), (200, 450), 'blue', '6'],
         'option': [(-350, -200), (700, 100), 'black', '6']}

# hashmap for storing button location and render the gif
BUTTON = {'reset_button': [(100, -250), 'Resources/resetbutton.gif'],
          'load_button': [(200, -250), 'Resources/loadbutton.gif'],
          'quit_button': [(300, -250), 'Resources/quitbutton.gif']}

# hashmap for processing leader frame
LEADER = {'leaders_text': (160, 270),
          'step_text': (-320, -260),
          'step_counter': (-180, -260),
          'thumbnail': (310, 280)}

LEGAL_KEYS = {'number', 'size', 'thumbnail'}
