import pygame as pg
#Cell resolution
CELL = (35,35)
#Resolution of the digits of the counter/clock
NUMBERRES = (29,50)
#Starting Y from which we place cells
UPINDENT = 50
#Resolution of the field for different difficulties
EASYRES = (9*35, 9*35 + UPINDENT)
NORMALRES = (16 * 35, 16*35 + UPINDENT)
HARDRES = (30 * 35, 16 * 35 + UPINDENT)
#Length of the cell side
SIDE = 35
#Sprites of cells
CELLSPRITES = ['sprites/n0.png','sprites/n1.png','sprites/n2.png','sprites/n3.png','sprites/n4.png','sprites/n5.png','sprites/n6.png','sprites/n7.png','sprites/n8.png']
#Sprites of digits of the clock/counter
NUMBRERSPRITES = ['sprites/zero.png','sprites/one.png','sprites/two.png','sprites/three.png','sprites/four.png','sprites/five.png','sprites/six.png','sprites/seven.png','sprites/eight.png','sprites/nine.png']