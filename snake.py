import pygame, random, sys, copy
from pygame.locals import *

# initialize pygame
pygame.init()
gameClock = pygame.time.Clock()

# set up window
WINDOWWIDTH = 400
WINDOWHEIGHT = 400
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)
pygame.display.set_caption('Snake')

# set up colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

# set up directions
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4
STOP = 0

# set up snake
SNAKESIZE = 20
STARTINGX = 200
STARTINGY = 200
INITLENGTH = 10
INITDIR = LEFT
SNAKEMS = SNAKESIZE + 2

# initialize snake
gameOver = False
snakeBody = []
snakeDir = INITDIR
snakeBody.append(pygame.Rect(STARTINGX, STARTINGY, SNAKESIZE, SNAKESIZE))
snakeHead = snakeBody[0]
for i in range(1, INITLENGTH):
	snakeBody.append(pygame.Rect(STARTINGX + i * (SNAKESIZE + 2), STARTINGY, SNAKESIZE, SNAKESIZE))

# game loop
while True:
	# event handling
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
		if event.type == KEYDOWN:
			if event.key == K_UP:
				snakeDir = UP
			elif event.key == K_DOWN:
				snakeDir = DOWN
			elif event.key == K_RIGHT:
				snakeDir = RIGHT
			elif event.key == K_LEFT:
				snakeDir = LEFT

	if not gameOver:
		# store current copy of snake
		snakeCopy = []
		for snakePart in snakeBody:
			snakeCopy.append(copy.copy(snakePart))

		# movement
		if snakeDir == UP:
			snakeHead.top -= SNAKEMS
		elif snakeDir == DOWN:
			snakeHead.top += SNAKEMS
		elif snakeDir == RIGHT:
			snakeHead.right += SNAKEMS
		elif snakeDir == LEFT:
			snakeHead.right -= SNAKEMS

		for i in range(len(snakeBody) - 1):
			snakeBody[i + 1].x = snakeCopy[i].x
			snakeBody[i + 1].y = snakeCopy[i].y

		# collision detection
		for i in range(len(snakeBody) - 1):
			if snakeHead.colliderect(snakeBody[i + 1]):
				gameOver = True
				print('Game over') # debug
				break

	if not gameOver:
		# fill background
		windowSurface.fill(BLACK)

		# draw snake
		for snakePart in snakeBody:
			pygame.draw.rect(windowSurface, WHITE, snakePart)
		pygame.draw.rect(windowSurface, GREEN, snakeHead)
	
		# draw window
		pygame.display.update()

	gameClock.tick(2)