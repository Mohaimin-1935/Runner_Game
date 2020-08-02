import pygame
import random
from pygame import mixer

pygame.init()

# GAME SCREEN
WIDTH = 600
HEIGHT = 400
ground = 265
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("RUNNER")
bg_image = pygame.image.load('my_bg.jpg')
bg_image = pygame.transform.scale(bg_image, (WIDTH+10, HEIGHT))
bgX1 = 0
bgX2 = WIDTH
score = 0

font = pygame.font.SysFont('Comic Sans MS', 30)
text = font.render('Press "SPACE" to start!', True, (0, 0, 0))
quitText = font.render('GAME OVER!', True, (0, 0, 0))
scoreFont = pygame.font.SysFont('Comic Sans MS', 24)
showFont = pygame.font.SysFont('Comic Sans MS', 18)

mixer.music.load("bgmusic.mp3")
mixer.music.play(-1)

gameOver = False


# CHARECTER
char = pygame.image.load('standing.png')
walkRight = [pygame.image.load('R1.png'), pygame.image.load('R2.png'), pygame.image.load('R3.png'),
             pygame.image.load('R4.png'), pygame.image.load('R5.png'), pygame.image.load('R6.png'),
             pygame.image.load('R7.png'), pygame.image.load('R8.png'), pygame.image.load('R9.png')]


clock = pygame.time.Clock()

class player(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.velocity = 7
        self.jumpCount = 9
        self.walkCount = 0
        self.right = False
        self.left = False
        self.isJump = False
        self.hitbox = (self.x+17, self.y+11, 29, 52)

    def draw(self, screen):
        if self.walkCount+1 >= 27:
            self.walkCount = 10

        if self.right:
            screen.blit(walkRight[self.walkCount // 3], (self.x, self.y))
            self.walkCount += 1
        elif not gameOver:
            screen.blit(char, (self.x, self.y))
            self.walkCount = 0
        self.hitbox = (self.x+17, self.y+11, 29, 52)


class saw(object):
    rotate = [pygame.image.load('SAW0.png'), pygame.image.load('SAW1.png'),
              pygame.image.load('SAW2.png'), pygame.image.load('SAW3.png')]
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rotateCount = 0

    def draw(self, screen):
        self.hitbox = (self.x+4, self.y+5, self.width-8, self.height-5)

        if self.rotateCount >= 8:
            self.rotateCount = 0
        screen.blit(pygame.transform.scale(self.rotate[self.rotateCount//2], (self.width, self.height)), (self.x, self.y))
        self.rotateCount += 1

    def collide(self, rect):
        if rect[0]+rect[2] > self.hitbox[0] and rect[0] < self.hitbox[0]+self.hitbox[2]:
            if rect[1] > self.hitbox[1]:
                return True
        return False


def show_score(x, y):
    showScore = showFont.render("Score : " + str(score), True, (0, 0, 0))
    screen.blit(showScore, (x, y))


def gameScreen():
    global walkCount
    screen.fill((0, 200, 255))
    screen.blit(bg_image, (bgX1, 0))
    screen.blit(bg_image, (bgX2, 0))
    if not man.right and not gameOver:
        screen.blit(text, (137, 100))
    if gameOver:
        screen.blit(quitText, (220, 100))
        screen.blit(scoreText, (250, 150))
    for obstacle in obstacles:
        obstacle.draw(screen)
    if not gameOver:
        show_score(500, 20)
    man.draw(screen)
    pygame.display.update()



speed = 7
obstacles = []
vel = 27
pygame.time.set_timer(pygame.USEREVENT+1, random.randrange(1000, 2000))
pygame.time.set_timer(pygame.USEREVENT+2, 3000)

man = player(150, ground, 64, 64)
cnt = 0


# GAME LOOP
running = True
while running:
    clock.tick(vel)

    if man.right:
        bgX1 -= speed
        bgX2 -= speed
        cnt += 1
        if (cnt % 10 == 0):
            score += 1
            scoreText = scoreFont.render('Score: ' + str(score), True, (0, 0, 0))

    if bgX1 <= WIDTH * -1:
        bgX1 = WIDTH
    if bgX2 <= WIDTH * -1:
        bgX2 = WIDTH

    for obstacle in obstacles:
        if not gameOver and man.right:
            obstacle.x -= speed+1
        if obstacle.x + obstacle.width < 0:
            obstacles.pop(obstacles.index(obstacle))
            score += 3
            scoreText = scoreFont.render('Score: ' + str(score), True, (0, 0, 0))
        if obstacle.collide(man.hitbox):
            man.right = False
            gameOver = True
            deadSound = mixer.Sound("AAAGH1.wav")
            deadSound.play()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.USEREVENT + 1 and man.right:
            r = random.randrange(0, 5)
            if score < 200:
                if (r != 2) and man.right:
                    obstacles.append(saw(650, ground, 60, 60))
                else:
                    obstacles.append(saw(670, ground - 15, 75, 75))
            else :
                if (r == 2) and man.right:
                    obstacles.append(saw(650, ground, 60, 60))
                else:
                    obstacles.append(saw(670, ground - 15, 75, 75))
        if event.type == pygame.USEREVENT + 2 and vel < 30:
            vel += 1

    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE] and not man.isJump and not gameOver:
        jumpSound = mixer.Sound("laser.wav")
        jumpSound.play()
        man.isJump = True
        man.left = False
        man.right = True

    if man.isJump and not gameOver:
        neg = 1
        if man.jumpCount < 0:
            neg = -1

        if man.jumpCount >= -9:
            man.y -= (man.jumpCount ** 2) * 0.5 * neg
            man.jumpCount -= 1
        else:
            man.isJump = False
            man.jumpCount = 9

    gameScreen()



# MOHAIMINUL ISLAM