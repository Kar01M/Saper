import pygame
import random

class Button:
    n_flag = 0
    def __init__(self, x, y, size_x, size_y, def_color, sel_color, max_n_flag):
        self.button = pygame.Rect(x, y, size_x, size_y)
        self.def_color = def_color #domyślny kolor
        self.sel_color = sel_color #kolor gdy najechano myszą
        self.bFlaged = False
        self.max_n_flag = max_n_flag
        self.flag_txt_surf = pygame.font.SysFont(None, 20).render('Flag', True, (0xFF,0,0))
        self.flag_txt_rect = self.flag_txt_surf.get_rect(center=self.button.center)
        self.bClicked = False
        self.set_indicator('')
    def set_indicator(self, text):
        self.indicator_txt_surf = pygame.font.SysFont(None, 30).render(text, True, (0xFF,0,0))
        self.indicator_txt_rect = self.indicator_txt_surf.get_rect(center=self.button.center)
    def place_on_screen(self, screen):
        # umieszcza przycisk na ekranie
        mouse_pos = pygame.mouse.get_pos()
        color = self.sel_color if self.button.collidepoint(mouse_pos) else self.def_color
        pygame.draw.rect(screen, color, self.button)
        if self.bFlaged: self.place_flag(screen)    # flaguje przycisk
        if self.bClicked: screen.blit(self.indicator_txt_surf, self.indicator_txt_rect) # zmienia przycisk na kliknięty
    def place_flag(self, screen):
        # obsługuje charakter flagowania przycisku
        screen.blit(self.flag_txt_surf, self.flag_txt_rect)
    def handle_event(self, event, index):
        # wykonywane gdy kliknięto przycisk
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.button.collidepoint(event.pos):
                if not self.bClicked and not self.bFlaged:
                    print('Kliknięto', index)
                    self.bClicked = True # odsłonięcie odbywa się tylko raz
                    self.def_color = (0xE3,0xCD,0xA2)
                    self.sel_color = (0xF5,0xE8,0xC0)
            if event.button == 3 and self.button.collidepoint(event.pos) and not self.bClicked:
                if not self.bFlaged:
                    if Button.n_flag < self.max_n_flag:
                        Button.n_flag += 1
                        print('Oflagowano', index, Button.n_flag)
                        self.bFlaged = True
                else:
                    Button.n_flag -= 1
                    print('Odflagowano', index, Button.n_flag)
                    self.bFlaged = False
        return False

class Bomb(Button):
    n_find = 0
    def __init__(self, x, y, size_x, size_y, def_color, sel_color, max_n_flag, font=None):
        Button.__init__(self, x, y, size_x, size_y, def_color, sel_color, max_n_flag)
        self.font = font or pygame.font.SysFont(None, 20)
        self.indicator_txt_surf = self.font.render('Bomb', True, (0,0,0))
        self.indicator_txt_rect = self.indicator_txt_surf.get_rect(center=self.button.center)
    def place_on_screen(self, screen):
        # umieszcza bombę na ekranie
        Button.place_on_screen(self, screen)
        #if self.bClicked: screen.blit(self.txt_surf, self.txt_rect)
    def handle_event(self, event, index):
        # wykonywane gdy kliknięto bombę
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.button.collidepoint(event.pos):
                if not self.bClicked and not self.bFlaged:
                    print('Buuummm !!!', index) # wybuch
                    self.bClicked = True # bomba wybucha tylko raz
                    self.def_color = (100, 10, 10)
                    self.sel_color = (80, 10, 10)
            if event.button == 3 and self.button.collidepoint(event.pos):
                if not self.bFlaged:
                    if Button.n_flag < self.max_n_flag:
                        Button.n_flag += 1
                        Bomb.n_find += 1
                        print('Oflagowano bombę', index, Button.n_flag)
                        self.bFlaged = True
                else:
                    Button.n_flag -= 1
                    Bomb.n_find -= 1
                    print('Odflagowano bombę', index, Button.n_flag)
                    self.bFlaged = False
        return self.bClicked    # zwraca informacje o tym czy bomba wybuchla

class Board:
    def __init__(self, OX, OY, nx, ny, screen, n_bombs, color1=(100,100,100), color2=(10,10,10), color3=(100,10,10)):
        self.OX = OX
        self.OY = OY
        self.nx = nx
        self.ny = ny
        self.screen = screen
        self.n_bombs = n_bombs
        self.color1 = color1
        self.color2 = color2
        self.color3 = color3
        self.endgame = False
    def create(self):
        # tworzy listę przycisków które są na mapie
        self.buttons = []
        pos_x, pos_y = 0, 0
        size_x, size_y = self.OX/self.nx, self.OY/self.ny
        color = self.color1
        for i in range(self.ny):
            for j in range(self.nx):
                self.buttons.append(Button(pos_x, pos_y, size_x, size_y, color, self.color3, self.n_bombs))
                pos_x += size_x
                if color==self.color1: color = self.color2 #tak by była ładna kratownica
                else: color = self.color1
            pos_x = 0
            pos_y += size_y
            if color==self.color1: color = self.color2 #tak by była ładna kratownica
            else: color = self.color1
        print('Board was created.')
    def show(self):
        for i in self.buttons:
            i.place_on_screen(self.screen)
    def handle_events(self, event):
        for i in range(len(self.buttons)):
            if self.buttons[i].handle_event(event, i): self.endgame = True
    def place_bombs(self):
        # losuje pozycje dla bomb tak by się nie powtarzały
        indexes = list(range(len(self.buttons)))
        random.shuffle(indexes)
        self.bombs_id = indexes[:self.n_bombs]  #zapisuje indexy bomb

        # umieszcza bomby w liście self.bombs
        for i in self.bombs_id:    #self.buttons[i].def_color, self.buttons[i].sel_color
            self.buttons[i] = Bomb(self.buttons[i].button.x,
                                   self.buttons[i].button.y,
                                   self.buttons[i].button.width,
                                   self.buttons[i].button.height,
                                   self.buttons[i].def_color,
                                   self.buttons[i].sel_color,
                                   self.n_bombs)
    def set_number_indicators(self):
        tmpS = set()

        for i in self.bombs_id:
            x = self.buttons[i].button.x / self.buttons[i].button.width
            y = self.buttons[i].button.y / self.buttons[i].button.height
            index = x + y*self.nx
            tmp2S = {_x+_y*self.nx for (_x,_y) in ((x-1,y-1), (x,y-1), (x+1,y-1), (x-1,y), (x+1,y), (x-1,y+1), (x,y+1), (x+1,y+1))
                     if (_x>=0 and _x<self.nx) and (_y>=0 and _y<self.ny) and _x+_y*self.nx not in self.bombs_id}
            tmpS |= tmp2S

        def ile_bomb(x, y):
            ile = 0
            if (((x-1)>=0 and (x-1)<self.nx) and ((y-1)>=0 and (y-1)<self.ny)) and isinstance(self.buttons[int((x-1)+(y-1)*self.nx)], Bomb): ile+=1
            if ((x>=0 and x<self.nx) and ((y-1)>=0 and (y-1)<self.ny)) and isinstance(self.buttons[int(x+(y-1)*self.nx)], Bomb): ile+=1
            if (((x+1)>=0 and (x+1)<self.nx) and ((y-1)>=0 and (y-1)<self.ny)) and isinstance(self.buttons[int((x+1)+(y-1)*self.nx)], Bomb): ile+=1
            if (((x-1)>=0 and (x-1)<self.nx) and (y>=0 and y<self.ny)) and isinstance(self.buttons[int((x-1)+y*self.nx)], Bomb): ile+=1
            if (((x+1)>=0 and (x+1)<self.nx) and (y>=0 and y<self.ny)) and isinstance(self.buttons[int((x+1)+y*self.nx)], Bomb): ile+=1
            if (((x-1)>=0 and (x-1)<self.nx) and ((y+1)>=0 and (y+1)<self.ny)) and isinstance(self.buttons[int((x-1)+(y+1)*self.nx)], Bomb): ile+=1
            if ((x>=0 and x<self.nx) and ((y+1)>=0 and (y+1)<self.ny)) and isinstance(self.buttons[int(x+(y+1)*self.nx)], Bomb): ile+=1
            if (((x+1)>=0 and (x+1)<self.nx) and ((y+1)>=0 and (y+1)<self.ny)) and isinstance(self.buttons[int((x+1)+(y+1)*self.nx)], Bomb): ile+=1
            return ile
        
        for i in tmpS:
            x = self.buttons[int(i)].button.x / self.buttons[int(i)].button.width
            y  = self.buttons[int(i)].button.y / self.buttons[int(i)].button.height
            self.buttons[int(i)].set_indicator(str(ile_bomb(x, y)))
        #print('Ustalono numery:', tmpS)
        
        
if __name__ == '__main__':
    #tmp = Board(100, 50, 10, 5, None, 1)
    #tmp.create()
    #for i in range(tmp.ny):
    #        for j in range(i*tmp.nx, i*tmp.nx+tmp.nx):
    #           print(j)
    #test = pygame.Rect(0, 1, 2, 3)
    #print(test.x, test.y, test.width, test.height)
    test = set()
    print(test)
    test |= {1, 2, 1}
    print(test)
    
        
