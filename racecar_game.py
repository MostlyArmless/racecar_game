# From video tutorial series by sentdex:
# https://www.youtube.com/watch?v=ujOTNg17LjI&index=1&list=PLQVvvaa0QuDdLkP8MrOXLe_rKuf6r80KO
import pygame
import time
import random

pygame.init()

# Define the display size
display_width = 800
display_height = 600
gameDisplay = pygame.display.set_mode((display_width, display_height))
quitimg = pygame.image.load('quitscreen.png')
num_obstacles = 1

# Define colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)


def text_objects(text, font):
    # Render given text onto a pygame surface
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()


def message_display(text, duration=1):
    # Display a message on the screen
    largeText = pygame.font.Font('freesansbold.ttf', 115)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((display_width / 2), (display_height / 2))
    gameDisplay.blit(TextSurf, TextRect)
    pygame.display.update()
    time.sleep(duration)


# Window title
pygame.display.set_caption('A Bit Racey')

# Define the game's clock
clock = pygame.time.Clock()
targetFps = 120


def draw_score(score):
    font = pygame.font.SysFont(None, 25)
    text = font.render(f'Dodged: {score}', True, black)
    gameDisplay.blit(text, (0, 0))


class obstacle:
    def reset(self):
        self.x = random.randrange(0, display_width - 200)
        self.y = -400
        self.w = random.randrange(100, 200)
        self.h = random.randrange(100, 200)
        self.vx = 0  # random.randrange(0, 3)
        self.vy = random.randrange(3, 7)
        r = random.randrange(0, 255)
        g = random.randrange(0, 255)
        b = random.randrange(0, 255)
        a = random.randrange(128, 255)
        self.color = pygame.Color(r, g, b, a)

    def __init__(self):
        self.reset()

    def check_if_offscreen(self):
        # Determine if the obstacle has gone off the left, right, or bottom of the screen
        is_offscreen = False
        if self.x > display_width or (self.x + self.w) < 0 or self.y > display_height:
            is_offscreen = True

        return is_offscreen

    def check_player_collision(self, player):
        x_overlap = self.x < (player.x + player.w) and (self.x + self.w) > player.x
        y_overlap = (self.y + self.h) > player.y and (player.y + player.h) > self.y
        if x_overlap and y_overlap:
            return True
        else:
            return False

    def move(self):
        self.x += self.vx
        self.y += self.vy
        if self.check_if_offscreen() == True:
            self.reset()
            return True
        else:
            return False

    def draw(self):
        pygame.draw.rect(gameDisplay, self.color, [self.x, self.y, self.w, self.h])


class car:
    def __init__(self):
        self.vx = 0
        self.vy = 0
        self.img = pygame.image.load('racecar2.png')
        self.w = self.img.get_rect().size[0]
        self.h = self.img.get_rect().size[1]
        # Initially center in the display
        self.x = display_width / 2 - self.w / 2
        self.y = display_height / 2 - self.h / 2
        self.crashed = False
        self.num_dodged = 0

    def move(self):
        # Move the player's car
        new_x = self.x + self.vx
        new_y = self.y + self.vy

        # Check if off the left or right side of the screen
        if new_x > (display_width - self.w):
            # Hit right edge, so set the x position to line up with the edge
            self.x = display_width - self.w
        elif new_x < 0:
            self.x = 0
        else:
            self.x = new_x

        if new_y < 0:
            self.y = 0
        elif new_y > display_height - self.h:
            self.y = display_height - self.h
        else:
            self.y = new_y

    def draw(self):
        gameDisplay.blit(self.img, (self.x, self.y))


def game_intro():
    # Run once at the game startup to provide a menu and/or instructions
    intro = True

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            # Exit due to any keypress
            if event.type == pygame.KEYDOWN:
                intro = False

        gameDisplay.fill(white)
        message_display('A Bit Racey')


def game_loop():
    # The primary game loop.

    # Instantiate the player and obstacle objects
    car_player = car()
    obstacles = [obstacle() for i in range(0, num_obstacles)]
    # keystates = {"left": pygame.KEYUP,
    #             "right": pygame.KEYUP}
    gameExit = False
    while not gameExit:
        # Reset everything if crashed last loop
        if car_player.crashed:
            car_player.__init__()
            for ob in obstacles:
                ob.reset()

        # Interpret the actions that have occurred this clock tick
        for event in pygame.event.get():
            # KEYUP EVENTS
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a and car_player.vx < 0:
                    car_player.vx = 0
                if event.key == pygame.K_d and car_player.vx > 0:
                    car_player.vx = 0

                if event.key == pygame.K_s and car_player.vy > 0:
                    car_player.vy = 0
                if event.key == pygame.K_w and car_player.vy < 0:
                    car_player.vy = 0

            # KEYDOWN EVENTS
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    # Left
                    car_player.vx = -5
                elif event.key == pygame.K_d:
                    # Right
                    car_player.vx = 5
                elif event.key == pygame.K_w:
                    # Up
                    car_player.vy = -5
                elif event.key == pygame.K_s:
                    # Down
                    car_player.vy = 5
                elif event.key == pygame.K_ESCAPE:
                    gameExit = True

            if event.type == pygame.QUIT:
                gameExit = True

        # Move objects
        car_player.move()
        for idx, ob in enumerate(obstacles):
            # Move obstacle
            obstacle_was_dodged = ob.move()
            if obstacle_was_dodged:
                car_player.num_dodged += 1

            # Check for collisions with player
            if ob.check_player_collision(car_player) == True:
                car_player.crashed = True

        # Draw next frame
        if car_player.crashed:
            gameDisplay.fill(red)
            message_display('You suck.')
        else:
            gameDisplay.fill(white)
            car_player.draw()
            for ob in obstacles:
                ob.draw()
            draw_score(car_player.num_dodged)

        # Update screen contents now that we've redrawn
        pygame.display.update()

        # Advance the game clock
        clock.tick(targetFps)


# Display the intro screen
game_intro()
# Run the game
game_loop()
# Show quit screen
gameDisplay.blit(quitimg, (0, 0))
pygame.display.update()
clock.tick(targetFps)
# Quit pygame
pygame.quit()
# Quit python
quit()
