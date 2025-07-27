import saper_classes as sc

# game setop
nx, ny, n_bomb = 10, 8, 10

# pygame setup
sc.pygame.init()
OX, OY = nx*40, ny*40
screen = sc.pygame.display.set_mode((OX, OY))
clock = sc.pygame.time.Clock()
running = True

# board settings
board = sc.Board(OX, OY, nx, ny, screen, n_bomb, (0xB4,0xD7,0x7A), (0xC4,0xE7,0x7A), (0xC4,0xF7,0x7B))
board.create()
board.place_bombs()
board.set_number_indicators()
#board.buttons[0] = sc.Bomb(0, 0, OX/10, OY/10)

# end game text settings
endgame_txt_surf = sc.pygame.font.SysFont(None, 50).render('Koniec Gry', True, (0,0,0))
endgame_txt_rect = endgame_txt_surf.get_rect(center=(OX//2, OY//2))

while running:
    # enables quiting window
    for event in sc.pygame.event.get():
        if event.type == sc.pygame.QUIT:
            running = False
        if not board.endgame: board.handle_events(event)

    if not board.endgame and sc.Bomb.n_find == n_bomb:
        board.endgame = True
        endgame_txt_surf = sc.pygame.font.SysFont(None, 50).render('Wygrałeś!', True, (0,0,0))
        print('Wygrałeś :)')
    
    board.show()
    if board.endgame: screen.blit(endgame_txt_surf, endgame_txt_rect)
    
    # updates window
    sc.pygame.display.flip()
    
sc.pygame.quit()


#(0xE3,0xCD,0xA2)
#(0xF5,0xE8,0xC0)
#łatwy: 10, 8, 10
#średni: 18, 14, 40
#trudny: 24, 20, 99
