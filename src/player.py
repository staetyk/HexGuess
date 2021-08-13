import pygame
from time import sleep


class Player(pygame.sprite.Sprite):

    # -- Attributes
    # Set speed vector of player
    change_x = 0
    change_y = 1 #This prevents the user from spawning inside of blocks
    sleep(0.001)
    change_y = 0

    level = None

    # -- Methods
    def __init__(self):

        pygame.sprite.Sprite.__init__(self)

        #Set the player sprite
        self.image = pygame.image.load('../images/cursor.png')

        #Set the player's default score
        self.score = 0

        #Set player hit radius
        self.radius = 1

        #Render player
        self.rect = self.image.get_rect()

    def update(self):
        """ Move the player. """

        # Move left/right
        self.rect.x += self.change_x

        # See if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            # If we are moving right,
            # set our right side to the left side of the item we hit
            if self.change_x > 0:
                self.rect.right = block.rect.left
            elif self.change_x < 0:
                # Otherwise if we are moving left, do the opposite.
                self.rect.left = block.rect.right

        # Move up/down
        self.rect.y += self.change_y

        # Check and see if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:

            # Reset our position based on the top/bottom of the object.
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom

            # Stop our vertical movement
            self.change_y = 0

    def jump(self):
        """ Called when user hits the UP button. """
        self.change_y = -6

    def down(self):
        """ Called when the user hits the DOWN button """
        self.change_y = 6

    # Player-controlled movement:
    def go_left(self):
        """ Called when the user hits the left arrow. """
        self.change_x = -6

    def go_right(self):
        """ Called when the user hits the right arrow. """
        self.change_x = 6

    def stop(self):
        """ Called when the user lets off the keyboard. """
        self.change_x = 0

    def stopJump(self):
        """ Called when the user lets off the UP or DOWN keys """
        self.change_y = 0
