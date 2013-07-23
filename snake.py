import pygame, random, sys, copy
from pygame.locals import *

# initialize pygame
pygame.init()
gameClock = pygame.time.Clock()

# set up main window
WINDOWWIDTH = 300
WINDOWHEIGHT = 300
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)
pygame.display.set_caption('Snake')

# set up colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

# set game area
gameArea = pygame.Rect(17, 17, 266, 266)

# set up directions
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# set up snake
SNAKESIZE = 20
STARTINGX = gameArea.left + 178
STARTINGY = gameArea.top + 134
INITLENGTH = 3
INITDIR = LEFT
SNAKEMS = SNAKESIZE + 2

# initialize snake
def reset():
	global gameOver, snakeBody, snakeDir, snakeHead
	gameOver = False
	snakeBody = []
	snakeDir = INITDIR
	snakeBody.append(pygame.Rect(STARTINGX, STARTINGY, SNAKESIZE, SNAKESIZE))
	snakeHead = snakeBody[0]
	for i in range(1, INITLENGTH):
		snakeBody.append(pygame.Rect(STARTINGX + i * (SNAKESIZE + 2), STARTINGY, SNAKESIZE, SNAKESIZE))

reset()

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
		if event.type == KEYUP:
			if event.key == K_ESCAPE:
				reset()

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
			# collision with snake body
			if snakeHead.colliderect(snakeBody[i + 1]):
				gameOver = True
				print('Game over') # debug code
				break

		if not gameArea.collidepoint(snakeHead.center):
			# collision with border
			gameOver = True
			print('Game over') # debug code

	if not gameOver:
		# fill background
		windowSurface.fill(BLACK)
		pygame.draw.rect(windowSurface, WHITE, gameArea, 1)

		# draw snake
		for snakePart in snakeBody:
			pygame.draw.rect(windowSurface, WHITE, snakePart)
		pygame.draw.rect(windowSurface, GREEN, snakeHead)
	
		# draw window
		pygame.display.update()

	gameClock.tick(2)