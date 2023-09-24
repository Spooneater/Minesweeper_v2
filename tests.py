import pytest
from classes import *
import pygame as pg
from constants import *
import time
pg.init()
def test_highlight_closed():
    cell = Cell(4,2,True,4)
    assert cell.highlight(1) == 1
    assert cell.highlight(-1) == -1
def test_highlight_closed_marked():
    cell = Cell(4,2,True,4)
    cell.changemark()
    assert cell.highlight(1) == 0
def test_highlight_opened():
    cell = Cell(4,2,False,4)
    cell.open()
    assert cell.highlight(1) == 0
def test_open_closed_mined():
    cell = Cell(1,1,True,4)
    assert cell.open() == -1
def test_open_closed_not_mined():
    cell = Cell(1,1,False,4)
    assert cell.open() == 1
def test_open_opend_cell():
    cell = Cell(1,1,False,4)
    cell.open()
    assert cell.open() == -2
def test_open_marked():
    cell = Cell(1,1,False,4)
    cell.changemark()
    assert cell.open() == -3
    cell.changemark()
    assert cell.open() == -3
    cell.changemark()
    assert cell.open() == 1
#8
def test_mark_cycle_change():
    cell = Cell(1,1,True,4)
    assert cell.mark == 'space'
    cell.changemark()
    assert cell.mark == 'flag'
    cell.changemark()
    assert cell.mark == 'question'
    cell.changemark()
    assert cell.mark == 'space'
#9
def test_opened_marking():
    cell = Cell(1,1,False,4)
    cell.open()
    assert cell.changemark() == -1 
#10
def test_generated_enough_cells():
    screen = pg.display.set_mode(EASYRES)
    field = Field(screen)
    field.generate(9,9,20)
    assert sum(len(i) for i in field.cell_storage) == 9 * 9
#11
def test_generated_enough_mines():
    screen = pg.display.set_mode(EASYRES)
    field = Field(screen)
    field.generate(9,9,20)
    n=0
    for i in field.cell_storage:
        for cell in i:
            if cell.mined == True:
                n+=1
    assert n == 20
#12
def test_open_cell():
    screen = pg.display.set_mode(EASYRES)
    field = Field(screen)
    field.generate(9,9,20)    
    pg.mouse.set_pos((1,1+UPINDENT))
    field.open()
    assert field.cell_storage[0][0].opened == True
#13
def test_open_all():
    screen = pg.display.set_mode(EASYRES)
    field = Field(screen)
    field.generate(9,9,0)    
    pg.mouse.set_pos((1,1+UPINDENT))
    field.open()
    flag = True
    for i in field.cell_storage:
        for cell in i:
            if not cell.opened:
                flag=False
                break
    assert flag == True
#14
def test_open_mine():
    screen = pg.display.set_mode(EASYRES)
    field = Field(screen)
    field.generate(9,9,81)    
    pg.mouse.set_pos((1,1+UPINDENT))
    assert field.open() == -1
#15
def test_open_cell_out_of_bounds():
    screen = pg.display.set_mode(EASYRES)
    field = Field(screen)
    field.generate(9,9,0)    
    pg.mouse.set_pos((1,1))
    assert field.open() == -2
#16
def test_highlight_closed_cell():
    screen = pg.display.set_mode(EASYRES)
    field = Field(screen)
    field.generate(9,9,20)
    assert field.highlight_cells(1,1,1) == 1
#17
def test_highlight_opened_cell():
    screen = pg.display.set_mode(EASYRES)
    field = Field(screen)
    field.generate(9,9,0)
    pg.mouse.set_pos((1,1 + UPINDENT))
    field.open()

    assert field.highlight_cells(0,0,1) == 2
#18
def test_mark_cell():
    screen = pg.display.set_mode(EASYRES)
    field = Field(screen)
    field.generate(9,9,0)
    pg.mouse.set_pos((1,1 + UPINDENT))
    field.mark()
    assert field.cell_storage[0][0].mark == 'flag'
    field.mark()
    assert field.cell_storage[0][0].mark == 'question'
    field.mark()
    assert field.cell_storage[0][0].mark == 'space'
#19
def test_time_flows_correctly():
    screen = pg.display.set_mode(EASYRES)
    clock = Clock(screen,3)
    clock.windup()
    time.sleep(3)
    assert clock.update() == 3
#20 
def test_counter_can_count():
    screen = pg.display.set_mode(EASYRES)
    counter = Counter(screen,10,3)
    assert counter.number == 10
    assert counter.dec(4) == 6
    assert counter.add(4) == 10