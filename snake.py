import pygame, random, sys, copy
from pygame.locals import *
from collections import deque

# initialize pygame
pygame.init()
gameClock = pygame.time.Clock()

# set up main window
WINDOWWIDTH = 300
WINDOWHEIGHT = 300
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)
pygame.display.set_caption('snake')

# set game area
gameArea = pygame.Rect(17, 17, 266, 266) # game area is set up as a 12x12 grid

# set up colours
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
WHITE = (255, 255, 255)

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

# set font
smallFont = pygame.font.SysFont(None, 12)
medFont = pygame.font.SysFont(None, 18)
largeFont = pygame.font.SysFont(None, 24)

# set initial text
name = smallFont.render('By YS Chua', True, WHITE)
nameRect = name.get_rect()
nameRect.top = gameArea.bottom + 2
nameRect.right = gameArea.right

instr = smallFont.render('Press keys 1-5 to change level', True, WHITE)
instrRect = instr.get_rect()
instrRect.centerx = gameArea.centerx
instrRect.bottom = gameArea.top - 2

score = smallFont.render('Score: 0', True,  WHITE)
scoreRect = score.get_rect()
scoreRect.top = gameArea.bottom + 2
scoreRect.centerx = gameArea.centerx

level = smallFont.render('Level: 1', True, WHITE)
levelRect = level.get_rect()
levelRect.top = gameArea.bottom + 2
levelRect.left = gameArea.left

def cloneList(someList):
	# creates an object clone for each object in the list
	clone = []
	for item in someList:
		clone.append(copy.copy(item))
	return clone

def createFood(x, y):
	# create a food on 12x12 grid position x, y
	gameAreaX = gameArea.left + 7 + 22 * (x - 1)
	gameAreaY = gameArea.top + 7 + 22 * (y - 1)
	return pygame.Rect(gameAreaX, gameAreaY, 10, 10)

def createRandomFood(snakeBody):
	# create a food on random location on game area
	rerollFood = True
	while rerollFood:
		# this is to ensure no food is created under snake
		rerollFood = False
		foodItem = createFood(random.randint(1, 12), random.randint(1, 12))
		for snakePart in snakeBody:
			if snakePart.colliderect(foodItem):
				rerollFood = True
	return foodItem

def reset():
	# initialize snake
	global gameOverStatus, snakeBody, snakeDir, snakeHead, food, consumedFoodQ, nextFood, scoreCounter
	scoreCounter = 0
	gameOverStatus = False
	snakeBody = [] 
	food = [] # list that always contains only one food rect
	consumedFoodQ = deque([]) # queue containing coordinates of consumed foods that have yet to be added to snake's length
	nextFood = () # coordinates of next food to be consumed in queue
	snakeDir = INITDIR
	snakeBody.append(pygame.Rect(STARTINGX, STARTINGY, SNAKESIZE, SNAKESIZE))
	snakeHead = snakeBody[0]
	for i in range(1, INITLENGTH):
		snakeBody.append(pygame.Rect(STARTINGX + i * (SNAKESIZE + 2), STARTINGY, SNAKESIZE, SNAKESIZE))
	food.append(createRandomFood(snakeBody))

reset()
gameSpeed = 2 # initial speed

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
			if event.key == K_1:
				gameSpeed = 2
			elif event.key == K_2:
				gameSpeed = 4
			elif event.key == K_3:
				gameSpeed = 6
			elif event.key == K_4:
				gameSpeed = 8
			elif event.key == K_5:
				gameSpeed = 10
		if event.type == KEYUP:
			if event.key == K_SPACE:
				reset()

	if not gameOverStatus:
		# store current copy of snake
		snakeClone = cloneList(snakeBody)

		# movement
		if snakeDir == UP:
			if snakeHead.left == snakeBody[1].left and snakeHead.top == (snakeBody[1].bottom + 2):
				# prevent going to opposite direction, causing collision		
				snakeHead.top += SNAKEMS # DOWN
			else:
				snakeHead.top -= SNAKEMS # UP
		elif snakeDir == DOWN:
			if snakeHead.left == snakeBody[1].left and snakeHead.bottom == (snakeBody[1].top - 2):
				snakeHead.top -= SNAKEMS # UP
			else:
				snakeHead.top += SNAKEMS # DOWN
		elif snakeDir == RIGHT:
			if snakeHead.right == (snakeBody[1].left - 2) and snakeHead.top == snakeBody[1].top:
				snakeHead.right -= SNAKEMS # LEFT
			else:
				snakeHead.right += SNAKEMS # RIGHT
		elif snakeDir == LEFT:
			if snakeHead.left == (snakeBody[1].right + 2) and snakeHead.top == snakeBody[1].top:
				snakeHead.right += SNAKEMS # RIGHT
			else:
				snakeHead.right -= SNAKEMS # LEFT
		for i in range(len(snakeBody) - 1):
			# this is the snake body following the head
			snakeBody[i + 1].x = snakeClone[i].x
			snakeBody[i + 1].y = snakeClone[i].y

		# collision detection
		for i in range(len(snakeBody) - 1):
			# collision with snake body
			if snakeHead.colliderect(snakeBody[i + 1]):
				gameOverStatus = True
				break
		if not gameArea.collidepoint(snakeHead.center):
			# collision with border
			gameOverStatus = True
		if snakeHead.colliderect(food[0]):
			# collision with food
			consumedFoodQ.append((food[0].centerx, food[0].centery))
			food.remove(food[0])
			scoreCounter += 1

		# create new food if previous was consumed
		if not food:
			food.append(createRandomFood(snakeBody))

		# check to add length to snake		
		if len(consumedFoodQ) != 0 or nextFood != ():
			if nextFood == ():
				nextFood = consumedFoodQ.popleft()
			if snakeClone[-1].centerx == nextFood[0] and snakeClone[-1].centery == nextFood[1]:
				snakeBody.append(pygame.Rect(snakeClone[-1].x, snakeClone[-1].y, SNAKESIZE, SNAKESIZE))
				nextFood = ()

		# update text
		score = smallFont.render('Score: %s ' % scoreCounter, True,  WHITE)
		level = smallFont.render('Level: %d ' % (gameSpeed / 2), True, WHITE)

	if not gameOverStatus:
		# draw background
		windowSurface.fill(BLACK)
		windowSurface.blit(name, nameRect)
		windowSurface.blit(instr, instrRect)
		windowSurface.blit(score, scoreRect)
		windowSurface.blit(level, levelRect)
		pygame.draw.rect(windowSurface, WHITE, gameArea, 1)

		# draw food
		pygame.draw.rect(windowSurface, WHITE, food[0])

		# draw snake
		for snakePart in snakeBody:
			pygame.draw.rect(windowSurface, WHITE, snakePart)
		pygame.draw.rect(windowSurface, GRAY, snakeHead)
	
		# draw window
		pygame.display.update()

		# game speed
		gameClock.tick(gameSpeed)

	if gameOverStatus:
		# display game over text
		gameOver = largeFont.render(' Game Over! ', True, WHITE, BLACK)
		startNewGame = medFont.render(' Press space to start a new game ', True, WHITE, BLACK)
		gameOverRect = gameOver.get_rect()
		startNewGameRect = startNewGame.get_rect()
		gameOverRect.centerx = gameArea.centerx
		gameOverRect.bottom = gameArea.centery
		startNewGameRect.centerx = gameArea.centerx
		startNewGameRect.top = gameArea.centery
		windowSurface.blit(gameOver, gameOverRect)
		windowSurface.blit(startNewGame, startNewGameRect)
		pygame.display.update()
		gameClock.tick(2)