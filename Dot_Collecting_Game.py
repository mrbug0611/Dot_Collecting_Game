# importing modules
from pygame import *
import random as rd

# Setting screen size variables and number of smaller dots
screen_width = 1400
screen_height = 800
dot_number = 250

# Setting movement variables
P1_X_Change = 1
P1_Y_Change = 1
P2_X_Change = 1
P2_Y_Change = 1

entered = False

seconds = 0

# Setting up screen size, caption, and the icon
init()
screen = display.set_mode((screen_width, screen_height))
display.set_caption('Fake Agar.io')
icon = image.load('blue circle.png')
display.set_icon(icon)

# setting random color value for the PDot class
red_1 = rd.randint(100, 220)
blue_1 = rd.randint(100, 220)
green_1 = rd.randint(100, 220)

# Setting up the fonts
game_font = font.Font('freesansbold.ttf', 30)
title_font = font.Font('Freshman.ttf', 70)
name_font = font.Font('freesansbold.ttf', 30)
big_info_font = font.Font('Konkretika-Black-WIP.ttf', 30)
winner_font = font.Font('Konkretika-Black-WIP.ttf', 70)

# Setting the score count
score_count = 0
score_count_2 = 0

# Setting how fast the pieces move per dot collected
slow_x = 0
slow_xx = 0
slow_y = 0
slow_yy = 0

timer = time.get_ticks()


# big controllable dots
class PDot:

    # Setting size and location
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size

    # Drawing the circle
    def draw(self):
        draw.circle(screen, (red_1, blue_1, green_1), (int(self.x), int(self.y)), self.size)

    # Moving Function
    def move(self, vx, vy):
        self.x += vx
        self.y += vy
        return [self.x, self.y]

    # Make sure the big dot can't move off screen
    def borders(self, w, h):
        if self.x >= w:
            self.x = w
        if self.x <= w - w:
            self.x = w - w
        if self.y <= h - h:
            self.y = h - h
        if self.y >= h:
            self.y = h


# Small collectable dot class
class SmallDot:
    SIZE = 5

    # Setting small dot size and colors
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = random_color()

    # Drawing the smaller dots
    def draw(self):
        draw.circle(screen, self.color, (self.x, self.y), SmallDot.SIZE)


# Class for the text boxes
class Rectangle:

    # Setting text box variables
    def __init__(self, x, y, player):
        self.active = False
        self.player = player
        self.x = x
        self.y = y

        self.text_surface = name_font.render(player, True, (255, 255, 255))
        self.rect_width = max(140, 10 + self.text_surface.get_width())
        self.input_rect = Rect(x, y, self.rect_width, 32)
        self.input_rect.w = self.text_surface.get_width() + 10
        self.click_value = 10

    # Typing text into the boxes
    def naming(self, events):

        for e in events:
            # For activating the text boxes
            if e.type == MOUSEBUTTONDOWN:
                if self.input_rect.x + self.click_value >= mx >= self.input_rect.x - 10 and self.input_rect.y + 26 >= my >= self.input_rect.y - 10:
                    self.active = True
                else:
                    self.active = False

            # For typing letters when they are activated
            if e.type == KEYDOWN:
                if self.active:
                    if e.key == K_BACKSPACE:
                        self.player = self.player[:-1]
                        screen.fill((0, 0, 0))
                        
                    else:
                        self.player += e.unicode
                        self.click_value += 7

                    self.text_surface = name_font.render(self.player, True, (255, 255, 255))

        return self.player

    # Drawing the text boxes
    def draw(self, screen):
        draw.rect(screen, (0, 0, 0), self.input_rect, 0)
        draw.rect(screen, (255, 255, 255), self.input_rect, 2)
        self.input_rect.w = self.text_surface.get_width() + 10
        screen.blit(self.text_surface, (self.input_rect.x + 5, self.input_rect.y + 5))


# Assigning random colors values to the smaller dots
def random_color():
    r = rd.randint(0, 255)
    g = rd.randint(0, 255)
    b = rd.randint(0, 255)
    return r, g, b


# The Big dots pick up the small dots
def pick_up(p, dot):
    p_size = int(p.size - (p.size / 8))
    p_rect = Rect(p.x - p_size, p.y - p_size, p_size * 2, p_size * 2)
    dot_rect = Rect(dot.x - dot.SIZE, dot.y - dot.SIZE, dot.SIZE * 2, dot.SIZE * 2)

    # Seeing if the dots are colliding
    if p_rect.colliderect(dot_rect) > 0:
        return True
    if dot_rect.colliderect(p_rect) > 0:
        return True
    return False


# Updating the value of the scores and putting them on the screen
def scoring(x, y):
    score_text = game_font.render(f'Player 1 Score: {score_count}', True, (0, 0, 0))
    score_text_2 = game_font.render(f'Player 2 Score {score_count_2}', True, (0, 0, 0))
    screen.blit(score_text, (x, y))
    screen.blit(score_text_2, (x + 1120, y))


# Updating timer and putting it onto the screen
def clocking(x, y):
    global seconds
    seconds += 0.005
    seconds = round(seconds, 3)
    clock_font = game_font.render(f'Time: {seconds}', True, (0, 0, 0))
    screen.blit(clock_font, (x, y))


# Showing the information on the title screen
def title_screen_info(x, y):
    title_text = title_font.render("Fake Agar.io", True, (255, 255, 255))
    big_name_info_1 = big_info_font.render("Player 1 Nickname: ", True, (255, 255, 255))
    big_name_info_2 = big_info_font.render("Player 2 Nickname: ", True, (255, 255, 255))
    enter_game_info = big_info_font.render("Click of the text box and press Enter to play ", True, (255, 255, 255))

    screen.blit(title_text, (x, y - 50))
    screen.blit(big_name_info_1, (x - 500, y + 70))
    screen.blit(big_name_info_2, (x - 500, y + 250))
    screen.blit(enter_game_info, (x - 150, y + 600))


# Showing who won the match
def declare_winner(x, y):
    # Winner declared when dots are zero
    if dot_number == 0:
        # If player 1 won
        if score_count > score_count_2:
            screen.fill((255, 255, 255))
            winner_text = winner_font.render("Player 1 Wins!!! ", True, (0, 0, 0))

            screen.blit(winner_text, (x, y))
        # If player 2 won
        if score_count_2 > score_count:
            screen.fill((255, 255, 255))
            winner_text = winner_font.render("Player 2 Wins!!! ", True, (0, 0, 0))

            screen.blit(winner_text, (x, y))
        # If it is a tie
        if score_count == score_count_2:
            screen.fill((255, 255, 255))
            winner_text = winner_font.render("It's a Tie", True, (0, 0, 0))

            screen.blit(winner_text, (x, y))
        restart_text = winner_font.render("Press 'r' to restart.", True, (0, 0, 0))
        screen.blit(restart_text, (x - 50, y + 200))


# Making the 2 text boxes
rect_1 = Rectangle(200, 200, "")

rect_2 = Rectangle(200, 400, "")

# Making the 2 controllable dots
dots = []
ball = PDot(90, 90, 15)
ball_2 = PDot(790, 90, 15)

# Print all of the small dots onto the screen
for i in range(dot_number):
    x = rd.randint(100, 1300)
    y = rd.randint(100, 700)
    dots.append(SmallDot(x, y))

# Main game loop
while True:
    # Getting mouse position
    mx, my = mouse.get_pos()

    # Making the screen white after enter is pressed
    if entered:
        screen.fill((255, 255, 255))

    events = event.get()

    for e in events:
        if e.type == QUIT:
            quit()
    keys = key.get_pressed()

    # 1st big dot moving right
    if keys[K_RIGHT]:
        P1_X_Change = 1
        P1_Y_Change = 0
        P1_X_Change = P1_X_Change - slow_x
        ball.move(+P1_X_Change, P1_Y_Change)

    # 1st big dot moving left
    if keys[K_LEFT]:
        P1_X_Change = -1
        P1_Y_Change = 0
        P1_X_Change = P1_X_Change + slow_x
        ball.move(+P1_X_Change, P1_Y_Change)
    # 1st big dot moving up
    if keys[K_UP]:
        P1_X_Change = 0
        P1_Y_Change = 1
        P1_Y_Change = P1_Y_Change - slow_y
        ball.move(P1_X_Change, -P1_Y_Change)
    # 1st big dot moving down
    if keys[K_DOWN]:
        P1_X_Change = 0
        P1_Y_Change = 1
        P1_Y_Change = P1_Y_Change - slow_y
        ball.move(P1_X_Change, +P1_Y_Change)
    # Starting the game
    if keys[K_RETURN]:
        entered = True
    # Restarting the game after a winner is declared
    if keys[K_r]:
        screen.fill((255, 255, 255))
        dot_number = 250
        entered = False
        score_count = 0
        score_count_2 = 0

        slow_x = 0
        slow_xx = 0
        slow_y = 0
        slow_yy = 0

        dots = []
        ball = PDot(90, 90, 15)
        ball_2 = PDot(790, 90, 15)

        for i in range(dot_number):
            x = rd.randint(100, 1300)
            y = rd.randint(100, 700)
            dots.append(SmallDot(x, y))

        seconds = 0

    # 2nd big dot moving right
    if keys[K_d]:
        P2_X_Change = 1
        P2_Y_Change = 0
        P2_X_Change = P2_X_Change - slow_xx
        ball_2.move(+P2_X_Change, P2_Y_Change)
    # 2nd big dot moving left
    if keys[K_a]:
        P2_X_Change = -1
        P2_Y_Change = 0
        P2_X_Change = P2_X_Change + slow_xx
        ball_2.move(+P2_X_Change, P2_Y_Change)
    # 2nd big dot moving up
    if keys[K_w]:
        P2_X_Change = 0
        P2_Y_Change = 1
        P2_Y_Change = P2_Y_Change - slow_yy
        ball_2.move(P2_X_Change, -P2_Y_Change)
    # 2nd big dot moving down
    if keys[K_s]:
        P2_X_Change = 0
        P2_Y_Change = 1
        P2_Y_Change = P2_Y_Change - slow_yy
        ball_2.move(P2_X_Change, +P2_Y_Change)


    # Activating what happens when the big dot picks up the smaller dot
    for dot in dots:
        if pick_up(ball, dot):  # if dot in range ball
            dots.remove(dot)
            dot_number -= 1
            ball.size += 1
            score_count += 1
            slow_x += 0.003
            slow_y += 0.003
        if pick_up(ball_2, dot):
            dots.remove(dot)
            dot_number -= 1
            ball_2.size += 1
            score_count_2 += 1
            slow_xx += 0.003
            slow_yy += 0.003

        if entered:
            dot.draw()
    # Setting up everything once the player presses enter and enters their name
    if entered:
        ball.draw()

        ball_2.draw()

        rect_font = name_font.render(rect_1.naming(events), True, (0, 0, 0))
        rect_font_2 = name_font.render(rect_2.naming(events), True, (0, 0, 0))
        move_values = ball.move(0, 0)
        move_values_2 = ball_2.move(0, 0)
        screen.blit(rect_font, (move_values[0] - 10, move_values[1] - 10))
        screen.blit(rect_font_2, (move_values_2[0] - 10, move_values_2[1] - 10))

        scoring(0, 50)

        ball.borders(screen_width, screen_height)
        ball_2.borders(screen_width, screen_height)
        clocking(50, 90)

        declare_winner(420, 350)

    # Setting up everything before the player enters their name
    if not entered:
        screen.fill((0, 0, 0))

        title_screen_info(600, 90)

        rect_1.naming(events)
        rect_1.draw(screen)

        rect_2.naming(events)
        rect_2.draw(screen)

    # making sure the window updates and changes according to these instructions
    display.update()
    time.delay(1)
