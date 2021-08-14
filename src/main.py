import pygame
import pygame.freetype

import constants
import levels
import pygame.locals

from player import Player

import choose

import time


opt_music = True
opt_sound = True
opt_hard = False


def generate():
    x = choose.create(opt_hard)
    global back
    back = x[1]
    global choices
    choices = x[0]


def main(first = False):
    """ Main Program """
    global opt_music
    global opt_sound
    global opt_hard


    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load('sounds/music.wav')
    pygame.mixer.music.play(-1)

    # Set the height and width of the screen
    size = [constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption(constants.name)
    pygame.display.set_icon(pygame.image.load(constants.icon))

    # Create the player
    player = Player()

    generate()


    def instructions():
        screen.fill(0xffffff)
        font = pygame.font.SysFont("Arial ms", 50)
        para = ["Welcome to Hex Guess!".center(85), "", "Each round, you will be given a color (the circle in the cen-", "ter of the screen), and four hex-codes. One of the hex-", "codes matches the color, and it's your job to figure out", "which one that is. After {0} rounds, you will be given your".format(constants.rounds), "score. Try to get the perfect {0}/{0}!".format(constants.rounds), "", "Good luck!".center(95)]
        i = 140
        for x in para:
            text = font.render(x, False, constants.BLACK)
            screen.blit(text, (20, i))
            i += 40
        pygame.display.flip()
        x = False
        history = ""
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    key = " "
                    if event.key == pygame.K_BACKSPACE:
                        x = True
                    if event.key == pygame.K_c:
                        controls()
                        instructions()
                        return None
                    if event.key == pygame.K_m:
                        global opt_music
                        opt_music = opt_music == False
                        if opt_music:
                            pygame.mixer.music.play(-1)
                        else:
                            pygame.mixer.music.stop()
                    if event.key == pygame.K_n:
                        global opt_sound
                        opt_sound = opt_sound == False
                    if event.key == pygame.K_UP:
                        key = "u"
                    if event.key == pygame.K_DOWN:
                        key = "d"
                    if event.key == pygame.K_LEFT:
                        key = "l"
                    if event.key == pygame.K_RIGHT:
                        key = "r"
                    if event.key == pygame.K_a:
                        key = "a"
                    if event.key == pygame.K_b:
                        key = "b"
                    if event.key == pygame.K_RETURN:
                        key = "s"
                    history += key
                if event.type == pygame.QUIT:
                    exit()
            if x:
                break

            if "uuddlrlrabs" in history:
                global opt_hard
                opt_hard = opt_hard == False
                if opt_sound:
                    play = pygame.mixer.Sound("sounds/secret4.wav")
                    pygame.mixer.Sound.play(play)
                history = ""


    def controls():
        screen.fill(0xffffff)
        font = pygame.font.SysFont("Arial ms", 75)
        para = ["arrow keys or WASD to move", "enter to select", "r to restart", "m to toggle music", "n to toggle sound", "c to see controls", "i to see instructions", "backspace to continue"]
        i = 10
        for x in para:
            text = font.render(x, False, constants.BLACK)
            screen.blit(text, (11, i))
            i += 80
        pygame.display.flip()
        x = False
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        x = True
                    if event.key == pygame.K_i:
                        instructions()
                        controls()
                        return None
                    if event.key == pygame.K_m:
                        global opt_music
                        opt_music = opt_music == False
                        if opt_music:
                            pygame.mixer.music.play(-1)
                        else:
                            pygame.mixer.music.stop()
                    if event.key == pygame.K_n:
                        global opt_sound
                        opt_sound = opt_sound == False
                if event.type == pygame.QUIT:
                    exit()
            if x:
                break


    if first:
        screen.fill(constants.END_BACKGROUND)
        logo = pygame.image.load("images/logo.png")
        screen.blit(logo, (290, 200))
        pygame.display.flip()

        start_time = time.time()
        left_time = time.time() - start_time
        while left_time < 2:
            left_time = time.time() - start_time
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        break
                    if event.key == pygame.K_m:
                        opt_music = opt_music == False
                        if opt_music:
                            pygame.mixer.music.play(-1)
                        else:
                            pygame.mixer.music.stop()
                    if event.key == pygame.K_n:
                        opt_sound = opt_sound == False
            else:
                continue
            break

        controls()
        instructions()


    def check(x, y, fx):
        if x <= 476:
            if y <= 289:
                match = list(choices.values())[0]
            else:
                match = list(choices.values())[2]
        else:
            if y <= 289:
                match = list(choices.values())[1]
            else:
                match = list(choices.values())[3]
        if match:
            play = pygame.mixer.Sound("sounds/secret2.wav")
            score = 1
        else:
            play = pygame.mixer.Sound("sounds/fall3.wav")
            score = 0
        if fx:
            pygame.mixer.Sound.play(play)

        quarters = [
            (0, 0),
            (500, 0),
            (0, 325),
            (500, 325)
        ]
        i = 0
        for x in choices.values():
            if x:
                quarter = quarters[i]
                break
            i += 1

        screen.fill(0xff0000)
        green = pygame.image.load("images/quarter.png")
        screen.blit(green, quarter)
        pygame.display.flip()
        time.sleep(0.5)
        return score


    # Create all the levels
    l = levels.Round(player)
    level_list = []
    for x in range(constants.rounds):
        level_list.append(l)

    # Set the current level
    current_level_no = 0
    current_level = level_list[current_level_no]

    active_sprite_list = pygame.sprite.Group()
    player.level = current_level

    player.rect.x, player.rect.y = 488, 307

    active_sprite_list.add(player)

    # Loop until the user clicks the close button.
    done = False
    gameover = False

    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()
    # -------- Main Program Loop -----------
    while not done:
        for event in pygame.event.get():  # User did something
            if event.type == pygame.QUIT:  # If user clicked close
                done = True  # Flag that we are done so we exit this loop
            if (event.type == pygame.KEYDOWN) and (gameover == False):
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    player.go_left()
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    player.go_right()
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    player.jump()
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    player.down()
                if event.key == pygame.K_RETURN: # or event.key == pygame.K_SPACE:
                    if (player.rect.x >= 506 or player.rect.x <= 476) and (
                            player.rect.y >= 325 or player.rect.y <= 289):
                        player.score += check ( player.rect.x , player.rect.y , opt_sound )
                        player.rect.x = 488
                        player.rect.y = 307

                        if current_level_no < constants.rounds - 1:
                            current_level_no += 1
                            generate ()
                            current_level = level_list[current_level_no]
                            player.level = current_level
                        else:
                            gameover = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    if opt_sound:
                        click = pygame.mixer.Sound("sounds/coin1.wav")
                        pygame.mixer.Sound.play(click)
                    main()
                    exit()
                if event.key == pygame.K_m:
                    opt_music = opt_music == False
                    if opt_music:
                        pygame.mixer.music.play(-1)
                    else:
                        pygame.mixer.music.stop()
                if event.key == pygame.K_n:
                    opt_sound = opt_sound == False
                if event.key == pygame.K_c:
                    controls()
                if event.key == pygame.K_i:
                    instructions()


            if event.type == pygame.KEYUP:
                if (event.key == pygame.K_LEFT or event.key == pygame.K_a) and player.change_x < 0:
                    player.stop()
                if (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and player.change_x > 0:
                    player.stop()
                if (event.key == pygame.K_UP or event.key == pygame.K_w) and player.change_y < 0:
                    player.stopJump()
                if (event.key == pygame.K_DOWN or event.key == pygame.K_s) and player.change_y > 0:
                    player.stopJump()

        # Update the player.
        active_sprite_list.update()

        # Update items in the level
        current_level.update()
        """
        if (player.rect.x >= 506 or player.rect.x <= 476) and (player.rect.y >= 325 or player.rect.y <= 289) and space:
            space = False
            player.score += check(player.rect.x, player.rect.y, opt_sound)
            player.rect.x = 488
            player.rect.y = 307

            if current_level_no < constants.rounds - 1:
                current_level_no += 1
                generate()
                current_level = level_list[current_level_no]
                player.level = current_level
            else:
                gameover = True
        """

        if gameover:
                screen.fill(constants.END_BACKGROUND)
                comicsansmsfontSmall = pygame.font.SysFont('Arial ms', 50)
                textsurface = comicsansmsfontSmall.render(f'Score: {player.score}/{constants.rounds}', False, constants.WHITE)
                screen.blit(textsurface, (400, 100))
                logo = pygame.image.load("images/logo.png")
                screen.blit(logo, (290, 175))
                textsurface = comicsansmsfontSmall.render('Press \'R\' to restart!', False, constants.WHITE)
                screen.blit(textsurface, (340, 450))
                gameover = True
        if not gameover:
            current_level.draw(screen, back, list(choices.keys()))
            active_sprite_list.draw(screen)

        # Limit to 60 frames per second
        clock.tick(60)

        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

    # Be IDLE friendly. If you forget this line, the program will 'hang'
    # on exit.
    pygame.quit()


if __name__ == "__main__":
    main(True)