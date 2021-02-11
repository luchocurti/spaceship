#! python

#import pygame
from random import randint
import contextlib
with contextlib.redirect_stdout(None):
    import pygame


# General definitions:
GAME_NAME = "Spaceship"
VERSION = "V1.0.0"
DEBUGGING = False

# Display
DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = DISPLAY_WIDTH * 2 // 3
FRAME_REFRESH_RATE = 30  # Frames per second

# Text
TEXT_SIZE_LEVEL = DISPLAY_WIDTH // 30
TEXT_SIZE_LARGE = TEXT_SIZE_LEVEL * 2
TEXT_SIZE_CONTROLS = TEXT_SIZE_LEVEL * 2 // 3
TEXT_ANTIALIAS = True
TEXT_FONT = "freesansbold.ttf"
TEXT_COLOR = pygame.Color("blue")

# Messages
MESSAGE_CENTER_X = DISPLAY_WIDTH // 2
MESSAGE_CENTER_Y = DISPLAY_HEIGHT // 2
MESSAGE_LEVEL_RIGHT = DISPLAY_WIDTH - DISPLAY_WIDTH // 30
MESSAGE_LEVEL_TOP = DISPLAY_HEIGHT // 20

# Starship
STARSHIP_SPEED = 15
STARSHIP_POS_INIT_X = DISPLAY_WIDTH // 2
STARSHIP_POS_INIT_Y = DISPLAY_HEIGHT * 3 // 4
STARSHIP_IMAGE = "starship.png"
LEVEL_INIT = 1

# Meteors
METEOR_NUMBER_INIT = 1
METEOR_SPEED_MIN = 2
METEOR_SPEED_MAX = 10
METEOR_TIME_NEW = 1000  # ms
METEOR_PER_LEVEL = 10
METEOR_IMAGE = "meteor.png"

# Enemy
ENEMY_POS_X = DISPLAY_WIDTH // 2
ENEMY_POS_Y = DISPLAY_HEIGHT // 5
ENEMY_SPEED = STARSHIP_SPEED // 5
ENEMY_TIME_MIN = 5
ENEMY_TIME_MAX = 30
ENEMY_MOVE = ["stop", "right", "left"]
ENEMY_IMAGE = "enemy.png"

# Bullets
BULLET_NUMBER_INIT = 0
BULLET_SPEED = 10
BULLET_POS_X = ENEMY_POS_X
BULLET_POS_Y = ENEMY_POS_Y
BULLET_IMAGE = "bullet.png"

# Controls
CONTROL_KEY_PAUSE = pygame.K_p
CONTROL_KEY_QUIT = pygame.K_q
CONTROL_KEY_RESTART = pygame.K_r
CONTROL_KEY_POS_X = DISPLAY_WIDTH // 16
CONTROL_KEY_POS_Y = DISPLAY_HEIGHT // 2
CONTROL_KEY_MOVE_DISTANCE = 5
CONTROL_KEY_SPEED = 1
CONTROL_KEY_P_IMAGE = "p_key.png"
CONTROL_KEY_Q_IMAGE = "q_key.png"
CONTROL_KEY_R_IMAGE = "r_key.png"

# Arrows
RIGHT_ARROW_KEY_IMAGE = "right_arrow_key.png"
DOWN_ARROW_KEY_IMAGE = "down_arrow_key.png"
LEFT_ARROW_KEY_IMAGE = "left_arrow_key.png"
UP_ARROW_KEY_IMAGE = "up_arrow_key.png"

# Background
BACKGROUND_IMAGE = "background.jpg"

# Images
IMAGES_FOLDER = "./images/"


class GameObject:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.image = None
        self.width = 0
        self.height = 0

    def load_image(self, filename):
        self.image = pygame.image.load(filename).convert_alpha()
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def rect(self):
        """ Generates a rectangle representing the objects location and dimensions """
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self):
        """ Draw the game object at the current x, y coordinates """
        self.game.display_surface.blit(self.image, (self.x, self.y))


class Starship(GameObject):
    """ Represents a starship """

    def __init__(self, game):
        super().__init__()
        self.game = game
        self.x = STARSHIP_POS_INIT_X
        self.y = STARSHIP_POS_INIT_Y
        self.load_image(IMAGES_FOLDER + STARSHIP_IMAGE)

    def move_right(self):
        """ Move the starship right across the screen """
        if self.x + self.width + STARSHIP_SPEED < DISPLAY_WIDTH:
            self.x = self.x + STARSHIP_SPEED
        else:
            self.x = DISPLAY_WIDTH - self.width

    def move_left(self):
        """ Move the starship left across the screen """
        if self.x - STARSHIP_SPEED > 0:
            self.x = self.x - STARSHIP_SPEED
        else:
            self.x = 0

    def move_down(self):
        """ Move the starship down the screen """
        if self.y + self.height + STARSHIP_SPEED < DISPLAY_HEIGHT:
            self.y = self.y + STARSHIP_SPEED
        else:
            self.y = DISPLAY_HEIGHT - self.height

    def move_up(self):
        """ Move the starship up the screen """
        if self.y - STARSHIP_SPEED > 0:
            self.y = self.y - STARSHIP_SPEED
        else:
            self.y = 0

    def __str__(self):
        return 'Starship(' + str(self.x) + ', ' + str(self.y) + ')'


class Meteor(GameObject):
    """ Represents a meteor in the game """

    def __init__(self, game):
        super().__init__()
        self.game = game
        self.load_image(IMAGES_FOLDER + METEOR_IMAGE)
        self.speed = randint(METEOR_SPEED_MIN, METEOR_SPEED_MAX)
        self.x = randint(0, DISPLAY_WIDTH - self.width)
        self.y = -self.height

    def move_down(self):
        """ Move the meteor down the screen """
        self.y = self.y + self.speed
        if self.y > DISPLAY_HEIGHT:
            self.speed = randint(METEOR_SPEED_MIN, METEOR_SPEED_MAX)
            self.x = randint(0, DISPLAY_WIDTH - self.width)
            self.y = -self.height

    def __str__(self):
        return 'Meteor(' + str(self.x) + ', ' + str(self.y) + ')'


class Enemy(GameObject):
    """ Represents the enemy """

    def __init__(self, game):
        super().__init__()
        self.game = game
        self.load_image(IMAGES_FOLDER + ENEMY_IMAGE)
        self.x = ENEMY_POS_X
        self.y = ENEMY_POS_Y
        self.time = randint(ENEMY_TIME_MIN, ENEMY_TIME_MAX)
        self.moving = ENEMY_MOVE[randint(0, len(ENEMY_MOVE) - 1)]

    def move(self):
        """ Move the enemy across the screen """
        if self.time > 0:
            self.time -= 1
            if self.moving == "right":
                """ Move the enemy right across the screen """
                if self.x + self.width + ENEMY_SPEED < DISPLAY_WIDTH:
                    self.x = self.x + ENEMY_SPEED
                else:
                    self.x = DISPLAY_WIDTH - self.width
                    self.moving = "stop"
            if self.moving == "left":
                """ Move the enemy left across the screen """
                if self.x - ENEMY_SPEED > 0:
                    self.x = self.x - ENEMY_SPEED
                else:
                    self.x = 0
                    self.moving = "stop"
        else:
            self.time = randint(ENEMY_TIME_MIN, ENEMY_TIME_MAX)
            self.moving = ENEMY_MOVE[randint(0, len(ENEMY_MOVE) - 1)]

    def __str__(self):
        return 'Enemy(' + str(self.x) + ', ' + str(self.y) + ')'


class Bullet(GameObject):
    """ Represents a bullet in the game """

    def __init__(self, game, pos_x, pos_y):
        super().__init__()
        self.game = game
        self.load_image(IMAGES_FOLDER + BULLET_IMAGE)
        self.x = pos_x
        self.y = pos_y

    def move_down(self):
        """ Move the bullet down the screen """
        self.y = self.y + BULLET_SPEED
        if self.y > DISPLAY_HEIGHT:
            return True
        else:
            return False

    def __str__(self):
        return 'Bullet(' + str(self.x) + ', ' + str(self.y) + ')'


class Key(GameObject):
    """ Represents a keyboard key in the game """

    def __init__(self, game, pos_x, pos_y, key):
        super().__init__()
        self.game = game
        self.load_image(key)
        self.x = pos_x
        self.y = pos_y
        self.moving = "down"
        self.y_orig = pos_y

    def move(self):
        """ Move the key up and down """
        if self.moving == "up":
            if self.y - CONTROL_KEY_SPEED >= self.y_orig:
                self.y = self.y - CONTROL_KEY_SPEED
            else:
                self.moving = "down"
        elif self.moving == "down":
            if self.y + CONTROL_KEY_SPEED <= self.y_orig + CONTROL_KEY_MOVE_DISTANCE:
                self.y = self.y + CONTROL_KEY_SPEED
            else:
                self.moving = "up"

    def reset(self):
        self.y = self.y_orig
        self.moving = "down"

    def __str__(self):
        return 'Key(' + str(self.x) + ', ' + str(self.y) + ')'


class Background(GameObject):

    def __init__(self, game):
        super().__init__()
        self.game = game
        self.x = 0
        self.y = 0
        self.load_image(IMAGES_FOLDER + BACKGROUND_IMAGE)


class Game:
    """ Represents the game itself, holds the main game playing loop """

    def __init__(self):
        # Initialising PyGame
        pygame.init()
        # Set up the display
        self.display_surface = pygame.display.set_mode(
            (DISPLAY_WIDTH, DISPLAY_HEIGHT))
        pygame.display.set_caption(GAME_NAME)
        # Set up the icon
        self.icon = pygame.image.load(IMAGES_FOLDER + STARSHIP_IMAGE)
        pygame.display.set_icon(self.icon)
        # Used for timing within the program
        self.clock = pygame.time.Clock()
        # Set the background
        self.background = Background(self)
        # Set up the starship
        self.starship = Starship(self)
        # Set up meteors
        self.meteors = [Meteor(self) for _ in range(0, METEOR_NUMBER_INIT)]
        # Set up the enemy
        self.enemy = Enemy(self)
        # Set up bullets
        self.bullets = [Bullet(self, BULLET_POS_X, BULLET_POS_Y)
                        for _ in range(0, BULLET_NUMBER_INIT)]
        # Set up the control keys
        self.key_q = Key(self, CONTROL_KEY_POS_X, CONTROL_KEY_POS_Y,
                         IMAGES_FOLDER + CONTROL_KEY_Q_IMAGE)
        self.key_r = Key(self, self.key_q.x + self.key_q.width,
                         CONTROL_KEY_POS_Y, IMAGES_FOLDER + CONTROL_KEY_R_IMAGE)
        self.key_p = Key(self, self.key_r.x + self.key_r.width,
                         CONTROL_KEY_POS_Y, IMAGES_FOLDER + CONTROL_KEY_P_IMAGE)
        # Set up the arrow keys
        self.key_arrow_right = Key(self, DISPLAY_WIDTH - CONTROL_KEY_POS_X -
                                   self.key_p.width, CONTROL_KEY_POS_Y, IMAGES_FOLDER + RIGHT_ARROW_KEY_IMAGE)
        self.key_arrow_down = Key(self, self.key_arrow_right.x - self.key_arrow_right.width,
                                  CONTROL_KEY_POS_Y, IMAGES_FOLDER + DOWN_ARROW_KEY_IMAGE)
        self.key_arrow_left = Key(self, self.key_arrow_down.x - self.key_arrow_down.width,
                                  CONTROL_KEY_POS_Y, IMAGES_FOLDER + LEFT_ARROW_KEY_IMAGE)
        self.key_arrow_up = Key(self, self.key_arrow_down.x, CONTROL_KEY_POS_Y -
                                self.key_arrow_down.height, IMAGES_FOLDER + UP_ARROW_KEY_IMAGE)
        # Timer
        self.last_time = pygame.time.get_ticks()
        # Level
        self.level = LEVEL_INIT

    def _check_for_collision(self):
        """ Checks to see if any of the meteors have collided with the starship """
        for meteor in self.meteors:
            if self.starship.rect().colliderect(meteor.rect()):
                return True
        return False

    def _check_for_enemy_collision(self):
        """ Checks to see if the starship has collided with the enemy """
        if self.starship.rect().colliderect(self.enemy.rect()):
            return True
        else:
            return False

    def _check_for_bullet_collision(self):
        """ Checks to see if any of the bullets have collided with the starship """
        for bullet in self.bullets:
            if self.starship.rect().colliderect(bullet.rect()):
                return True
        return False

    def _display_message(self, message):
        """ Displays a message to the user on the screen """
        text_font = pygame.font.Font(TEXT_FONT, TEXT_SIZE_LARGE)
        text_surface = text_font.render(message, TEXT_ANTIALIAS, TEXT_COLOR)
        text_rectangle = text_surface.get_rect()
        text_rectangle.center = (MESSAGE_CENTER_X, MESSAGE_CENTER_Y)
        self.display_surface.blit(text_surface, text_rectangle)

    def _display_message_level(self, message):
        """ Displays a message to the user on the screen """
        text_font = pygame.font.Font(TEXT_FONT, TEXT_SIZE_LEVEL)
        text_surface = text_font.render(message, TEXT_ANTIALIAS, TEXT_COLOR)
        text_rectangle = text_surface.get_rect()
        text_rectangle.right = MESSAGE_LEVEL_RIGHT
        text_rectangle.top = MESSAGE_LEVEL_TOP
        self.display_surface.blit(text_surface, text_rectangle)

    def _display_message_controls(self):
        """ Displays a message to the user on the screen """
        text_font = pygame.font.Font(TEXT_FONT, TEXT_SIZE_CONTROLS)

        text_surface = text_font.render("Pause", TEXT_ANTIALIAS, TEXT_COLOR)
        text_rectangle = text_surface.get_rect()
        text_rectangle.centerx = self.key_p.x + self.key_p.width // 2
        text_rectangle.top = self.key_p.y + self.key_p.height
        self.display_surface.blit(text_surface, text_rectangle)

        text_surface = text_font.render("Quit", TEXT_ANTIALIAS, TEXT_COLOR)
        text_rectangle = text_surface.get_rect()
        text_rectangle.centerx = self.key_q.x + self.key_q.width // 2
        text_rectangle.top = self.key_q.y + self.key_q.height
        self.display_surface.blit(text_surface, text_rectangle)

        text_surface = text_font.render("Restart", TEXT_ANTIALIAS, TEXT_COLOR)
        text_rectangle = text_surface.get_rect()
        text_rectangle.centerx = self.key_r.x + self.key_r.width // 2
        text_rectangle.top = self.key_r.y + self.key_r.height
        self.display_surface.blit(text_surface, text_rectangle)

        text_surface = text_font.render("Move", TEXT_ANTIALIAS, TEXT_COLOR)
        text_rectangle = text_surface.get_rect()
        text_rectangle.centerx = self.key_arrow_down.x + self.key_arrow_down.width // 2
        text_rectangle.top = self.key_arrow_down.y + self.key_arrow_down.height
        self.display_surface.blit(text_surface, text_rectangle)

    def _display_keys_controls(self):
        """ Displays the keys to the user on the screen """
        self.key_p.draw()
        self.key_q.draw()
        self.key_r.draw()

        self.key_arrow_right.draw()
        self.key_arrow_down.draw()
        self.key_arrow_left.draw()
        self.key_arrow_up.draw()

    def _pause(self):
        while True:
            self._update_screen(pause=True)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.key_p.reset()
                    return (False, True)    # restart, close
                elif event.type == pygame.KEYDOWN:
                    if event.key == CONTROL_KEY_QUIT:
                        self.key_p.reset()
                        return (False, True)    # restart, close
                    if event.key == CONTROL_KEY_RESTART:
                        self.key_p.reset()
                        return (True, True)     # restart, close
                    if event.key == CONTROL_KEY_PAUSE:
                        self.key_p.reset()
                        return (False, False)   # restart, close

            # Defines the frame rate
            self.clock.tick(FRAME_REFRESH_RATE)

    def _update_screen(self, running=False, pause=False, lose=False):
        # Draw the background, the meteors, the starship, the enemy, the bullets and the level
        self.background.draw()
        self.starship.draw()
        for meteor in self.meteors:
            meteor.draw()
        self._display_message_level("Level {0}".format(self.level))
        self.enemy.draw()
        for bullet in self.bullets:
            bullet.draw()

        if running:
            # Move the Meteors
            for meteor in self.meteors:
                meteor.move_down()

            # Move the Enemy
            self.enemy.move()

            # Move the Bullets
            for bullet in self.bullets:
                if bullet.move_down():
                    self.bullets.remove(bullet)

        if pause:
            self.key_p.move()
            self.key_p.draw()

            self._display_keys_controls()
            self._display_message_controls()

        if lose:
            self.key_r.move()
            self.key_r.draw()

            self._display_keys_controls()
            self._display_message_controls()

            self._display_message("Game Over")

        # Update the display
        pygame.display.update()

    def play(self):
        lose = False
        restart = False
        close = False

        # Main game playing Loop
        while not lose and not close:
            # Work out what the user wants to do
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    close = True
                elif event.type == pygame.KEYDOWN:
                    # Check to see which key is pressed
                    if event.key == CONTROL_KEY_PAUSE:
                        (restart, close) = self._pause()
                    elif event.key == CONTROL_KEY_QUIT:
                        close = True

            if not close:
                # Update the screen
                self._update_screen(running=True)

                # Work out what the user wants to do
                # Check to see which key is pressed
                if pygame.key.get_pressed()[pygame.K_RIGHT]:
                    self.starship.move_right()
                if pygame.key.get_pressed()[pygame.K_LEFT]:
                    self.starship.move_left()
                if pygame.key.get_pressed()[pygame.K_UP]:
                    self.starship.move_up()
                if pygame.key.get_pressed()[pygame.K_DOWN]:
                    self.starship.move_down()

                # Check to see if a meteor has hit the ship
                if self._check_for_collision():
                    lose = True
                # Check to see if the ship has hit the enemy
                if self._check_for_enemy_collision():
                    lose = True
                # Check to see if a bullet has hit the ship
                if self._check_for_bullet_collision():
                    lose = True

                # Determine if new meteors or bullets should be added
                if (pygame.time.get_ticks() - self.last_time) >= METEOR_TIME_NEW:
                    self.last_time = pygame.time.get_ticks()
                    self.meteors.append(Meteor(self))
                    self.level = len(
                        self.meteors) // METEOR_PER_LEVEL + LEVEL_INIT

                    if len(self.bullets) == 0:
                        self.bullets.append(Bullet(
                            self, self.enemy.x + self.enemy.width // 2, self.enemy.y + self.enemy.height))

                    if DEBUGGING:
                        print(
                            "Meteors = {0} - Bullets = {1}".format(len(self.meteors), len(self.bullets)))

            # Defines the frame rate
            self.clock.tick(FRAME_REFRESH_RATE)

        if lose and not close:
            is_waiting = True

            while is_waiting:
                self._update_screen(lose=True)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        is_waiting = False
                    if event.type == pygame.KEYDOWN and event.key == CONTROL_KEY_QUIT:
                        # Check to see which key is pressed
                        is_waiting = False
                    if event.type == pygame.KEYDOWN and event.key == CONTROL_KEY_RESTART:
                        is_waiting = False
                        restart = True

                # Defines the frame rate
                self.clock.tick(FRAME_REFRESH_RATE)

        pygame.quit()

        return restart


def main():
    print("{0} - {1}".format(GAME_NAME, VERSION))

    playing = True
    while playing:
        game = Game()
        playing = game.play()


# Starting point
# Check if the file is used as a Script
if __name__ == "__main__":
    main()

# The file is imported as a module
else:
    pass
