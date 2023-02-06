import pygame
from datetime import datetime
from datetime import timedelta
import random

pygame.init()

#Global value
BLACK = (0,0,0)
WHITE = (255,255,255)
GREEN = (0,255,0)
RED = (255,0,0)
WIDTH = 600
HIGHT = 600
FPS = 10
SCORE = 0
Block_Size = 20

my_font = pygame.font.SysFont(None, 30)
last_moved_time = datetime.now()

#Move direction
KEY_DIRECTION = {
    pygame.K_UP: 'N',
    pygame.K_DOWN: 'S',
    pygame.K_LEFT: 'W',
    pygame.K_RIGHT: 'E',
}


#Setting background
background = pygame.display.set_mode((WIDTH, HIGHT))
pygame.display.set_caption("Snake")
clock = pygame.time.Clock()
play = True

#Update score
def update_score():
    global SCORE
    SCORE += 1

#Display score
def score_display():
    print_message(f"Current Score: {SCORE:,}", BLACK, 10, 10)

#Print message
def print_message(msg, color, width, height):
    my_text = my_font.render(msg, 1, color)
    background.blit(my_text, [width, height])

#Draw block
def draw_block(background, color, position):
    pygame.draw.rect(background, color, [position[0] * Block_Size, position[1] * Block_Size, Block_Size, Block_Size])


#Snake class
class Snake:
    #Initiate value
    def __init__(self):
        self.positions = [(1,0)]
        self.direction = ''

    def draw(self):
        for position in self.positions:
            draw_block(background, GREEN, position)

    #Move the snake
    def move(self):
        head_position = self.positions[0]
        x, y = head_position
        if self.direction == 'N':
            self.positions = [(x, y-1)] + self.positions[:-1]
        elif self.direction == 'S':
            self.positions = [(x, y+1)] + self.positions[:-1]
        elif self.direction == 'W':
            self.positions = [(x-1, y)] + self.positions[:-1]
        elif self.direction == 'E':
            self.positions = [(x+1, y)] + self.positions[:-1]

    #Append the snake tail
    def grow(self):
        tail_position = self.positions[-1] 
        x, y = tail_position
        if self.direction == 'N':
            self.positions.append((x-1, y)) 
        elif self.direction == 'S':
            self.positions.append((x+1, y))
        elif self.direction == 'W':
            self.positions.append((x, y-1))
        elif self.direction == 'E':
            self.positions.append((x, y+1))    

#Apple class
class Apple:
    def __init__(self):
        self.position = (random.randint(0, WIDTH/Block_Size - Block_Size), random.randint(0, HIGHT/Block_Size - Block_Size))
    def draw(self):
        draw_block(background, RED, self.position)

#Display menu
def menu():
    start = True
    while start:
        background.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    start = False
                    runGame()
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()  
        print_message("Snake Game", WHITE, WIDTH/2-60, 100)
        print_message("Press S to start or Q to quit", WHITE, WIDTH/2-140, HIGHT/2)
        pygame.display.update()
        clock.tick(FPS)

#Pause game
def pause():
    paused = True
    while paused:
        background.fill(WHITE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    paused = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()          
            print_message("Paused", BLACK, WIDTH/2-30, 100)
            print_message("Press C to contine or Q to quit", BLACK, WIDTH/2-130, HIGHT/2)
            
            pygame.display.update()
            clock.tick(FPS)

#Game end
def game_end():
    end = True
    global play
    global SCORE
    while end:
        background.fill(WHITE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    end = False
                    play = True
                    SCORE = 0
                    runGame()
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()          
            print_message("Game End", BLACK, WIDTH/2 - 40, 100)
            print_message("Press A to play again or Q to quit", BLACK, WIDTH/2- WIDTH/4, HIGHT/2)
            
            score_display()
            pygame.display.update()
            clock.tick(FPS)

#Run game
def runGame():
    global play
    snake = Snake()
    apple = Apple()
    while play:
        background.fill(WHITE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                play = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    play = False
                elif event.key == pygame.K_p:
                    pause()
                elif event.key in KEY_DIRECTION:
                    snake.direction = KEY_DIRECTION[event.key]
        if timedelta(seconds=0.5) <= datetime.now() - last_moved_time:
            snake.move()            
        snake.draw()
        apple.draw()
        x, y = snake.positions[0]
        if x >= WIDTH/Block_Size or x < 0 or y>= HIGHT/Block_Size or y < 0:
            play = False
            game_end()
        if snake.positions[0] in snake.positions[1:]:
            play = False
            game_end()
        if snake.positions[0] == apple.position:
            snake.grow()    
            update_score()
            apple.position = (random.randint(0, WIDTH/Block_Size - Block_Size), random.randint(0, HIGHT/Block_Size - Block_Size))
        score_display()
        pygame.display.update()
        clock.tick(FPS)

menu()
pygame.quit()
quit()