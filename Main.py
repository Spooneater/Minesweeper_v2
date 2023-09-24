import pygame as pg
from constants import *
from classes import *
pg.init()
running = True
screen, field, clock, counter, w, h, mines = create_game(1) 
game_started = False
game_ended = False
victory = False
opened_cells_count = 0
bgrd = pg.image.load('sprites/bgrd.png')
wintxt = pg.font.SysFont(None, 30).render('You won', True, 'Black')
losttxt = pg.font.SysFont(None, 30).render('You lost', True, 'Black')
while running:
    screen.blit(bgrd, (0, 0))
    field.draw()
    clock.draw(screen.get_size()[0] - clock.digits * NUMBERRES[0], 0)
    counter.draw(0,0)
    if game_ended == True:
        if victory == True:
            screen.blit(wintxt, ( (w * SIDE - wintxt.get_size()[0])//2, 15))
        else:
            screen.blit(losttxt, ( (w * SIDE - losttxt.get_size()[0])//2, 15))
    pg.display.update()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
            pg.quit()
        #Here we change the difficulty and create components of the game according to difficulty
        if event.type == pg.KEYDOWN:
            key = event.key
            if key == pg.K_1:
                sscreen, field, clock, counter, w, h, mines = create_game(1)                           
            elif key == pg.K_2:
                screen, field, clock, counter, w, h, mines = create_game(2)
            elif key == pg.K_3:
                screen, field, clock, counter, w, h, mines = create_game(3)
            if (key == pg.K_1) or (key == pg.K_2) or (key == pg.K_3):
                opened_cells_count = 0
                game_started = False
                game_ended = False
                victory = False
        #If we press LMB we highlight cells, untill LMB not released
        #If RMB is pressed then we just try to mark the cell
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                field.highlight_mode = True
            if event.button == 3:
                mark = field.mark()
                if (mark != -1) and (game_started == False):
                    game_started = True
                    clock.windup()                   
                if mark == 1:
                    counter.dec(1)
                elif mark == 2:
                    counter.add(1)
        #Here we open cell upon releasing the LMB       
        if event.type == pg.MOUSEBUTTONUP:
            if event.button == 1:
                if field.highlight_mode == False:
                    continue
                n = field.open()
                if n > 0 : #If we opened n cells successfully
                    if (game_started == False):
                        game_started = True
                        clock.windup()
                    opened_cells_count += n
                    if opened_cells_count == w*h - mines: # <---victory condition
                        field.freeze_cells()
                        clock.stop()
                        victory = True 
                        game_ended = True
                elif n == -1:#Which means we opened a mined cell and hence lost
                    game_ended = True
                    field.reveal_mines()
                    field.freeze_cells()
                    clock.stop()
    if running:
        #Here we update the timer and which cells are highlighted
        field.highlight_update()
        if game_started:
            clock.update()
        
    