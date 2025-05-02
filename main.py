import pygame 
import random
import pygame.gfxdraw
import time

background_colour = (18, 31, 45) 
screen = pygame.display.set_mode((0, 0)) 
pygame.display.set_caption('Geeksforgeeks') 
screen.fill(background_colour) 
pygame.display.flip() 
running = True
width,height = screen.get_size()
pygame.font.init()
rankFont = pygame.font.SysFont(None, 55)
# rankFont.set_bold(True)

class card:
    def __init__(self,rank,suit):
        self.rank = rank
        self.suit = suit
    def getRank(self) -> str:
        return self.rank
    def getSuit(self) -> str:
        return self.suit
    def getCard(self) -> str:
        return f"{self.rank} of {self.suit}"

global dealer1, dealer2, player1, player2

rank = ["A",2,3,4,5,6,7,8,9,10,"J","Q","K"]
suit = ["diamond","heart","club","spade"]


def giveCard():
    global dealer1
    dealer1 = card(rank[random.randint(0,12)],suit[random.randint(0,3)])


def drawDiamond(x,y):
    color = (203, 56, 74)
    shape1 = [(x+40, y+60), (x+40, y+100), (x+40+20, y+80)]
    shape2 = [(x+40, y+60), (x+40, y+100), (x+40-20, y+80)]
    pygame.gfxdraw.filled_polygon(screen, shape1, color)
    pygame.gfxdraw.filled_polygon(screen, shape2, color)

def drawHeart(x,y):
    color = (203, 56, 74)
    shape1 = [(x+40, y+60), (x+40, y+100), (x+40+20, y+80)]
    shape2 = [(x+40, y+60), (x+40, y+100), (x+40-20, y+80)]
    pygame.gfxdraw.filled_polygon(screen, shape1, color)
    pygame.gfxdraw.filled_polygon(screen, shape2, color)

def drawCard(rank, suit, x, y):
    pygame.draw.rect(screen,
                     color=(225, 225, 225),
                     rect=(x, y, 2.5 * 50, 3.5 * 50),
                     border_radius=10)
    
    color = (0, 0, 0)
    if suit == "diamond":
        color = (203, 56, 74)
        drawHeart(x,y)
    
    text = rankFont.render(rank, True, color)
    text_rect = text.get_rect()
    
    text_rect.centerx = x + 40  
    text_rect.bottom = y + 55
    
    screen.blit(text, text_rect.topleft)
    

giveCard()

while running: 
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                running = False
    
    drawCard(str(dealer1.getRank()),"diamond",100,100)
    pygame.display.flip()