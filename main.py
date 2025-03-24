import curses
import time
import random
import winsound

# Constantes du jeu
JUMP_HEIGHT = 4
FLOOR_Y = 10
GRAVITY = 0.5

# Initialisation du jeu
def game(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(1)
    stdscr.timeout(100)

    dino_y = FLOOR_Y
    dino_jump = 0
    dino_crouch = False
    dino_falling = False
    obstacles = []
    score = 0
    last_time = time.time()
    is_day = True
    
    while True:
        stdscr.clear()
        key = stdscr.getch()

        # Gestion des touches
        if key == curses.KEY_UP and dino_y == FLOOR_Y:
            dino_jump = JUMP_HEIGHT
            winsound.Beep(800, 100)
        elif key == curses.KEY_DOWN:
            if dino_jump > 0:
                dino_jump = 0
                dino_falling = True
            else:
                dino_crouch = True
        else:
            dino_crouch = False
        
        # Mise à jour de la position du dino
        if dino_jump > 0:
            dino_y -= 1
            dino_jump -= 1
        elif dino_y < FLOOR_Y:
            dino_y += 1

        # Ajout des obstacles
        if random.randint(1, 20) == 1:
            obstacles.append([50, FLOOR_Y])
        
        # Déplacement des obstacles
        for obs in obstacles:
            obs[0] -= 1
        obstacles = [obs for obs in obstacles if obs[0] > 0]

        # Collision
        for obs in obstacles:
            if obs[0] == 5 and dino_y == FLOOR_Y:
                stdscr.addstr(10, 20, "Game Over! Score: {}".format(score))
                stdscr.refresh()
                time.sleep(2)
                return
        
        # Score et changement de cycle
        score += 1
        if score % 800 == 0:
            is_day = not is_day
            if is_day:
                curses.start_color()
                curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
                stdscr.attron(curses.color_pair(1))
            else:
                curses.start_color()
                curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)
                stdscr.attron(curses.color_pair(2))
        
        # Affichage du dino
        stdscr.addstr(dino_y, 5, "D" if not dino_crouch else "_D_")
        
        # Affichage des obstacles
        for obs in obstacles:
            stdscr.addstr(obs[1], obs[0], "|")

        # Affichage du score
        stdscr.addstr(0, 0, "Score: {}".format(score))
        
        stdscr.refresh()
        time.sleep(0.05)

# Lancer le jeu
curses.wrapper(game)
