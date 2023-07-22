import pygame
import random
import time
import math
import json
import os

pygame.init()

res = width, height = 720, 480
fontsize = 128

root = pygame.display.set_mode((720, 480))
pygame.display.set_caption("Keyboard Game")
screen = pygame.display.get_surface()

running = True

alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
largeFont = pygame.font.Font(None, fontsize)
smallFont = pygame.font.Font(None, int(fontsize/4))

COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = pygame.Color('dodgerblue2')
COLOR_UNFILLED = pygame.Color('red')

keystatePast = pygame.key.get_pressed()

def importJson(dataName):
    with open(os.path.join(os.path.dirname(__file__), f"{dataName}.json"), 'r') as f:
        newData = json.load(f)
        return newData

resultsFile = importJson("results_jeremy")

def randomColour():
    return pygame.color.Color(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

def reverseColour(colour):
    return (255-colour[0], 255-colour[1], 255-colour[2])

current = random.randint(0, 25)
letterColour = randomColour()
backgroundColour = randomColour()
refresh = True
colour = True

beginTime = 0
timer = 30
score = 0

PLAYING = 0
WAITING = 1
COUNTDOWN = 2

mode = PLAYING

letterRender = pygame.surface.Surface((0, 0))
timerRender = letterRender
scoreRender = timerRender

gameData = []

def checkKey(key):
    return key == alphabet[current]

def newKey():
    global current, refresh, letterColour
    gameData.append((alphabet[current], 0 - beginTime + time.time()))
    new = random.randint(0, 24)
    if new >= current:
        new += 1
    current = new
    refresh = True
    letterColour = randomColour()

class InputBox:  # Credit: skrx on https://stackoverflow.com/questions/46390231/how-can-i-create-a-text-input-box-with-pygame, Sep 24, 2017

    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = smallFont.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            if self.active:
                self.color = COLOR_ACTIVE
            else:
                self.color = COLOR_INACTIVE
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = smallFont.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)
    
    def reset(self):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = smallFont.render(text, True, self.color)
        self.active = False

    def get_text(self):
        return self.text

    def deactivate(self):
        self.active = False

    def show_unfilled(self):
        self.color = COLOR_UNFILLED

NameTitle = smallFont.render("Your Name:", True, COLOR_INACTIVE)
AgeTitle = smallFont.render("Your Age:", True, COLOR_INACTIVE)
TouchTyperTitle = smallFont.render("Touch Typer (y/n):", True, COLOR_INACTIVE)
RulerScoreTitle = smallFont.render("Ruler Score:", True, COLOR_INACTIVE)

NameBox = InputBox(20+TouchTyperTitle.get_width(), 20, width-40, smallFont.get_height()+8)
AgeBox = InputBox(20+TouchTyperTitle.get_width(), 20+(smallFont.get_height()+16), width-40, smallFont.get_height()+8)
TouchTyperBox = InputBox(20+TouchTyperTitle.get_width(), 20+(smallFont.get_height()+16)*2, width-40, smallFont.get_height()+8)
RulerScoreBox = InputBox(20+TouchTyperTitle.get_width(), 20+(smallFont.get_height()+16)*3, width-40, smallFont.get_height()+8)

filled = False

while running:
    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            with open(os.path.join(os.path.dirname(__file__), "results.json"), 'w') as f:
                json.dump(resultsFile, f)
        if event.type == pygame.KEYDOWN:
            if checkKey(pygame.key.name(event.key)) and mode == PLAYING:
                newKey()
                score += 1
            if event.key == pygame.K_RETURN and mode != PLAYING:
                filled = True
                if NameBox.text == '':
                    NameBox.show_unfilled()
                    filled = False
                if AgeBox.text == '':
                    AgeBox.show_unfilled()
                    filled = False
                if TouchTyperBox.text == '':
                    TouchTyperBox.show_unfilled()
                    filled = False
                if RulerScoreBox.text == '':
                    RulerScoreBox.show_unfilled()
                    filled = False

                if filled:
                    beginTime = time.time()
                    colour = not colour
                    mode = PLAYING
                    refresh = True
                    score = 0
                    
                    NameBox.deactivate()
                    AgeBox.deactivate()
                    TouchTyperBox.deactivate()
                    RulerScoreBox.deactivate()


        NameBox.handle_event(event)
        AgeBox.handle_event(event)
        TouchTyperBox.handle_event(event)
        RulerScoreBox.handle_event(event)

    
    # Refresh
    if refresh:
        if colour:
            backgroundColour = randomColour()
        else:
            backgroundColour = pygame.Color("BLACK")
        letterRender = largeFont.render(alphabet[current].upper(), True, reverseColour(backgroundColour))
        refresh = False

    NameBox.update()
    AgeBox.update()
    TouchTyperBox.update()
    RulerScoreBox.update()

    # Display
    screen.fill(backgroundColour)
    if mode == PLAYING:
        if beginTime + timer > time.time():
            timerRender = smallFont.render("Time Left: " + str(round((beginTime + timer - time.time()), 2)), 
                                                                    True, reverseColour(backgroundColour))
            scoreRender = smallFont.render("Score: " + str(score), True, reverseColour(backgroundColour))
        else:
            if len(gameData) > 0:
                newEntry = (
                    NameBox.get_text(),
                    AgeBox.get_text(),
                    TouchTyperBox.get_text(),
                    RulerScoreBox.get_text(),
                    colour,
                    gameData
                )
                resultsFile.append(newEntry)
                gameData = []
            mode = WAITING
    if mode == WAITING:
        screen.fill("BLACK")
        timerRender = pygame.surface.Surface((0, 0))
        letterRender = largeFont.render("Enter to Start", True, "WHITE")

        # Draw all input fields
        screen.blits([
            (NameTitle, (8+TouchTyperTitle.get_width()-NameTitle.get_width(), 24)), 
            (AgeTitle, (8+TouchTyperTitle.get_width()-AgeTitle.get_width(), 24+(smallFont.get_height()+16))), 
            (TouchTyperTitle, (8, 24+(smallFont.get_height()+16)*2)),
            (RulerScoreTitle, (8+TouchTyperTitle.get_width()-RulerScoreTitle.get_width(), 24+(smallFont.get_height()+16)*3))
            ])
        NameBox.draw(screen)
        AgeBox.draw(screen)
        TouchTyperBox.draw(screen)
        RulerScoreBox.draw(screen)

    screen.blit(letterRender, ((width-letterRender.get_width())/2, (height-letterRender.get_height())/2))
    screen.blit(timerRender, (20, 20))
    if mode == PLAYING:
        screen.blit(scoreRender, (20, 40))
    elif mode == WAITING:
        screen.blit(scoreRender, ((width-scoreRender.get_width())/2, (height-scoreRender.get_height())/2+50))

    pygame.display.flip()


pygame.quit()