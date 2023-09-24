import pygame as pg
import random
from constants import *
import time
#Cell class represents a cell on the field.
#Object of this class contains statuses of cell and it's graphic representation on the field.
class Cell:
    def __init__(self, x, y, mined, adj_mines):
        self.x = x
        self.y = y
        self.mined = mined
        self.adj_mines = adj_mines
        self.clickable = True
        self.opened = False
        self.mark = 'space'
        self.freezed = False
        self.image = pg.image.load('sprites/closed.png')
    def highlight(self,mode):
        #If mode == 1 means we highlight. -1 means stop highlighting
        if (self.opened == False)and(self.mark == 'space'):
            if mode == 1: 
                self.image = pg.image.load('sprites/n0.png')
                return 1
            elif mode == -1:
                self.image = pg.image.load('sprites/closed.png')
                return -1
        return 0
    # 1 - successully opened not mined cell
    # 0 - after loss tried to open cell marked as flag while cell isn't mined 
    # -1 - opened mined cell
    # -2 - tried to open opend cell
    # -3 tried to open marked cell
    def open(self, loss = False):
        if loss == True:
            if self.mark == 'flag':
                if self.mined == False:
                    self.image = pg.image.load('sprites/not_mine.png')
                    return 0
            elif self.mined:
                self.image = pg.image.load('sprites/mine.png')
                return -1
            return -3
        if self.opened:
            return -2
        if self.mark != 'space':
            return -3
        else:
            self.opened = True
            if self.mined:
                self.image = pg.image.load('sprites/mine.png')
                return -1
            self.image = pg.image.load(CELLSPRITES[self.adj_mines])
            return 1

    def changemark(self):
        if self.opened:
            return -1
        if self.mark == 'space':
            self.mark = 'flag'
            self.image = pg.image.load('sprites/fl.png')
            return 1
        elif self.mark == 'flag':
            self.mark = 'question'
            self.image = pg.image.load('sprites/q.png')
            return 2
        else:
            self.mark = 'space'
            self.image = pg.image.load('sprites/closed.png')
            return 0
#Field class stores information about the field and manages it's contents
class Field:

    def __init__(self, screen):
        self.screen = screen
        self.highlighwt_mode = False
        self.res = screen.get_size()
        self.last_highlited_cell = [-1,-1] #x,y for a cell. Everytime highlighting stops it changes to [-1,-1]. It's used to check if cursor is still hovering over the same cell.
        self.freezed = False
    def generate(self, w, h, nmines):
        self.w = w
        self.h = h
        self.highlight_mode = False
        self.freezed = False
        self.last_highlited_cell = [-1,-1]
        self.cell_storage = [[] for i in range(h)]
        self.cell_neihbours = [[] for i in range(h)]
        mines = [ False for i in range(w*h)]
        #Here we decide which cells are mined
        for i in range(nmines):
            j = random.randint(0,w*h-1)
            while mines[j]:
                j = random.randint(0,w*h-1)
            mines[j] = True
        
        #Here we create cells and remember neihbours for each cell
        for y in range(h):
            for x in range(w):
                n = 0 #The amount of adjacent mines 
                neihbours = []
                if x-1>=0:
                    n += mines[(x-1)+(y)*w]
                    neihbours+=[[x-1,y]]
                    if y-1>=0:
                        n += mines[(x-1)+(y-1)*w] 
                        neihbours+=[[x-1,y-1]]
                    if y+1<h:
                        n += mines[(x-1)+(y+1)*w]    
                        neihbours+=[[x-1,y+1]]  
                if x+1 < w:
                    n += mines[(x+1)+(y)*w]
                    neihbours+=[[x+1,y]]
                    if y-1>=0:
                        n += mines[(x+1)+(y-1)*w]
                        neihbours+=[[x+1,y-1]] 
                    if y+1<h:
                        n += mines[(x+1)+(y+1)*w]
                        neihbours+=[[x+1,y+1]]
                if (y + 1 < h):
                    n += mines[(x)+(y+1)*w]
                    neihbours+=[[x,y+1]]
                if (y - 1 >= 0):
                    n += mines[(x)+(y-1)*w]
                    neihbours+=[[x,y-1]]
                self.cell_neihbours[y].append(neihbours)
                self.cell_storage[y].append(Cell(x, y, mines[y*w+x], n))
    #Updating graphic of the field
    def draw(self):
        for y in range(self.h):
            for cell in self.cell_storage[y]:
                self.screen.blit(cell.image, (cell.x * SIDE, cell.y * SIDE + UPINDENT))
    #Higlighting cell when one is pressed.
    def highlight_cells(self, x, y, mode):
        hcell = self.cell_storage[y][x]
        if hcell.opened :
            for xy in self.cell_neihbours[y][x]:
                self.cell_storage[xy[1]][xy[0]].highlight(mode)
            return 2
        else:
            hcell.highlight(mode)
            return 1
    #Here we check which cell we highlight
    def highlight_update(self):
        if self.freezed == True:
            return -4
        if self.highlight_mode == True:
            x,y = pg.mouse.get_pos()
            if (x >=0) and (x < self.res[0]) and (y < self.res[1]) and (y >=UPINDENT):
                x = x // SIDE            
                y = (y - UPINDENT) // SIDE
            else:
                x,y = -1,-1
            if (x == self.last_highlited_cell[0]) and (y == self.last_highlited_cell[1]):
                return [x,y]
            self.highlight_cells(self.last_highlited_cell[0],self.last_highlited_cell[1],-1)
            if (x != -1):
                self.last_highlited_cell = [x,y]
                self.highlight_cells(x,y,1)
                return [x,y]
        self.last_highlited_cell = [-1,-1]
        return [-1,-1]
    def open(self):

        if self.freezed:
            return -4
        self.highlight_mode = False
        x,y = pg.mouse.get_pos()
        if (x >=0) and (x < self.res[0]) and (y < self.res[1]) and (y >=UPINDENT):
            x = x // SIDE            
            y = (y - UPINDENT) // SIDE
        else:
            x,y = -1,-1
            return -2
        if self.last_highlited_cell[0] != -1: #Which means that there WAS a highlighted cell.
            self.highlight_cells(self.last_highlited_cell[0],self.last_highlited_cell[1],-1)
        opened_mine = False
        opened_cells = 0
        stack = [] #Here we store coordinates of empty cells that need to be opened
        cell = self.cell_storage[y][x]
        if cell.opened == False:
            if cell.mark != 'space':
                return 0 
            cell.open()

            if cell.mined == True:
                opened_mine = True
            elif cell.adj_mines == 0:
                stack += [[x,y]]
            opened_cells = 1
        else:
            flags = 0
            for xy in self.cell_neihbours[y][x]:
                if self.cell_storage[xy[1]][xy[0]].mark == 'flag':
                    flags+=1
            #print(flags)
            if flags == 0:
                return 0
            if flags == cell.adj_mines:
                for xy in self.cell_neihbours[y][x]:
                    neighbour_cell = self.cell_storage[xy[1]][xy[0]]
                    if neighbour_cell.open() == 1:
                        opened_cells += 1
                    if (neighbour_cell.mined == True)and(neighbour_cell.mark == 'space' ):
                        opened_mine = True
                    elif (neighbour_cell.adj_mines == 0)and(neighbour_cell.mined == False):
                        stack += [[xy[0],xy[1]]]
        #Here we open empty cells, if there were any
        while len(stack) != 0:
            xy = stack.pop()
            for i in self.cell_neihbours[xy[1]][xy[0]]:
                if (self.cell_storage[i[1]][i[0]].adj_mines == 0) and (self.cell_storage[i[1]][i[0]].opened == False):
                    stack += [[i[0],i[1]]]
                if self.cell_storage[i[1]][i[0]].open() == 1:
                    opened_cells += 1
        if opened_mine == True :
            return -1
        return opened_cells
    def mark(self):
        if self.freezed == True:
            return -4
        x,y = pg.mouse.get_pos()   
        if (x >=0) and (x < self.res[0]) and (y < self.res[1]) and (y >=UPINDENT):
            x = x // SIDE            
            y = (y - UPINDENT) // SIDE
            return self.cell_storage[y][x].changemark()
        else:
            return -1 #It only happens when we click in the clock zone(supposedly at least)
    def reveal_mines(self):
        for x in range(self.w):
            for y in range(self.h):
                self.cell_storage[y][x].open(True)
    def freeze_cells(self):
        self.freezed = True     


#It's a clock.

class Clock:
    def __init__(self, screen,  digits = 1):
        self.ticking = False
        self.screen = screen     
        self.counter = 0
        self.digits = digits
        self.limit = sum([9*(10**i) for i in range(digits)])
        self.sprites = [pg.image.load(NUMBRERSPRITES[0]) for i in range(digits)]
        self.start = 0
    def windup(self):
        self.ticking = True
        self.start = time.time()
    def stop(self):
        self.ticking = False
    def update(self):
        if (int(time.time()-self.start)!=self.counter) and (self.ticking == True):
            self.counter = int(time.time()-self.start)
            self.sprites = [pg.image.load(NUMBRERSPRITES[ min(self.counter,self.limit) // (10 ** (self.digits - i - 1)) % 10 ])for i in range(self.digits)]
        return self.counter
    def draw(self, x, y):
        i = 0
        for num in self.sprites:
            self.screen.blit(num, (x + i * NUMBERRES[0], y ))
            i+=1
#Counter
#Shows number in range from (-99999999..9 // (digits - 1) ) to number of mines
#Initial value is the amount of mines
#For every flag on the field one is substracted from counter
class Counter:
    def __init__(self, screen, mines, digits):
        self.digits = digits
        self.mines = mines #This one is starting amount
        self.number = mines #This one is used to show actual count
        #self.limit = sum([9*(10**i) for i in range(digits-1)]) * (-1)
        self.sprites = [pg.image.load(NUMBRERSPRITES[0]) for i in range(digits)]
        self.screen = screen
        self.update()
    def dec(self, n):
        self.number -= n
        self.update()
        return self.number
    def add(self, n):
        self.number += n
        self.update()
        return self.number
    def update(self):
        if self.number < 0 :
            self.sprites[0] = pg.image.load('sprites/minus.png')
        for i in range( (self.number < 0), self.digits):
            self.sprites[i] = pg.image.load(NUMBRERSPRITES[abs(self.number) // (10 ** (self.digits - i - 1)) % 10])
    def draw(self, x, y):
        i = 0
        for num in self.sprites:
            self.screen.blit(num, (x + i * NUMBERRES[0], y ))
            i+=1
def create_game(difficulty, clock_digits = 3, mine_counter_digits = 3):
    if difficulty == 1:
        screen = pg.display.set_mode(EASYRES)
        hight,width,mines = 9, 9, 10
    elif difficulty == 2:
        screen = pg.display.set_mode(NORMALRES)
        hight,width,mines = 16, 16, 40
    else:
        screen = pg.display.set_mode(HARDRES)
        hight,width,mines = 16, 30, 99      
    screen.fill('Grey')
    field = Field(screen)
    field.generate(width, hight, mines)
    clock = Clock(screen, clock_digits)
    mine_counter = Counter(screen, mines, mine_counter_digits)
    return screen, field, clock, mine_counter, width, hight, mines
