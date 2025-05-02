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

global dealer, dealerHide, player1, player2

rank = ["A",2,3,4,5,6,7,8,9,10,"J","Q","K"]
suit = ["diamond","heart","club","spade"]


def giveCard():
    global dealer, dealerHide
    dealer = card(rank[random.randint(0,12)],suit[random.randint(0,3)])
    dealerHide = card(rank[random.randint(0,12)],suit[random.randint(0,3)])



def drawDiamond(x,y):
    color = (203, 56, 74)
    shape1 = [(x+40, y+60), (x+40, y+100), (x+40+20, y+80)]
    shape2 = [(x+40, y+60), (x+40, y+100), (x+40-20, y+80)]

    pygame.gfxdraw.filled_polygon(screen, shape1, color)
    pygame.gfxdraw.filled_polygon(screen, shape2, color)

def drawHeart(x,y):
    color = (203, 56, 74)
    shape1 = [(x+40, y+80), (x+40, y+100), (x+40+20, y+80), (x+40+10,y+70)]
    shape2 = [(x+40, y+80), (x+40, y+100), (x+40-20, y+80), (x+40-10,y+70)]

    pygame.gfxdraw.filled_polygon(screen, shape1, color)
    pygame.gfxdraw.filled_polygon(screen, shape2, color)

def drawClub(x,y):
    color = (27, 42, 57)
    shape1 = [(x+40, y+55), (x+40, y+75), (x+40+10, y+65)]
    shape2 = [(x+40, y+55), (x+40, y+75), (x+40-10, y+65)]

    shape3 = [(x+40-10-1, y+65.5+1), (x+40-10-1, y+65.5+20+1), (x+40-1, y+65.5+10+1)]
    shape4 = [(x+40-10-1, y+65.5+1), (x+40-10-1, y+65.5+20+1), (x+40-20-1, y+65.5+10+1)]

    shape5 = [(x+40+10+1, y+65.5+1), (x+40+10+1, y+65.5+20+1), (x+40+1, y+65.5+10+1)]
    shape6 = [(x+40+10+1, y+65.5+1), (x+40+10+1, y+65.5+20+1), (x+40+20+1, y+65.5+10+1)]

    shape7 = [(x+40, y+65.5+10+7.5), (x+40-10, y+65.5+10+10+7.5), (x+40+10, y+65.5+10+10+7.5)]

    pygame.gfxdraw.filled_polygon(screen, shape1, color)
    pygame.gfxdraw.filled_polygon(screen, shape2, color)
    pygame.gfxdraw.filled_polygon(screen, shape3, color)
    pygame.gfxdraw.filled_polygon(screen, shape4, color)
    pygame.gfxdraw.filled_polygon(screen, shape5, color)
    pygame.gfxdraw.filled_polygon(screen, shape6, color)
    pygame.gfxdraw.filled_polygon(screen, shape7, color)

def drawSpade(x,y):
    color = (27, 42, 57)
    shape1 = [(x+40, y+60), (x+40+20, y+80), (x+40+10,y+80+10), (x+40, y+80)]
    shape2 = [(x+40, y+60), (x+40-20, y+80), (x+40-10,y+80+10), (x+40, y+80)]

    shape3 = [(x+40, y+65.5+10+7.5+5), (x+40-10, y+65.5+10+10+5+7.5), (x+40+10, y+65.5+10+10+7.5+5)]

    pygame.gfxdraw.filled_polygon(screen, shape1, color)
    pygame.gfxdraw.filled_polygon(screen, shape2, color)
    pygame.gfxdraw.filled_polygon(screen, shape3, color)



def drawCard(rank, suit, x, y):
    temp_surf = pygame.Surface((int(2.7 * 50), int(3.7 * 50)), pygame.SRCALPHA)
    pygame.draw.rect(
        temp_surf,
        (7, 13, 18, 179), 
        temp_surf.get_rect(),
        border_radius=10
    )
    screen.blit(temp_surf, (x-5, y-5))
    pygame.draw.rect(screen,
                     color=(225, 225, 225),
                     rect=(x, y, 2.5 * 50, 3.5 * 50),
                     border_radius=10)


    
    color = (0, 0, 0)
    if suit == "diamond":
        color = (203, 56, 74)
        drawDiamond(x,y)
    elif suit == "heart":
        color = (203, 65, 74)
        drawHeart(x,y)
    elif suit == "club":
        color = (27, 42, 57)
        drawClub(x,y)
    elif suit == "spade":
        color = (27, 42, 57)
        drawSpade(x,y)
    
    text = rankFont.render(rank, True, color)
    text_rect = text.get_rect()
    
    text_rect.centerx = x + 40  
    text_rect.bottom = y + 55
    
    screen.blit(text, text_rect.topleft)
    
def drawHideCard(x,y):
    temp_surf = pygame.Surface((int(2.5 * 50), int(3.5 * 50)), pygame.SRCALPHA)
    pygame.draw.rect(
        temp_surf,
        (7, 13, 18, 179), 
        temp_surf.get_rect(),
        border_radius=10
    )
    screen.blit(temp_surf, (x-5, y-5))


    pygame.draw.rect(screen,
                     color=(70, 70, 170),
                     rect=(x, y, 2.5 * 50, 3.5 * 50),
                     border_radius=10)
    pygame.draw.rect(screen,
                     color=(50, 50, 150),
                     rect=(x+5, y+5, 2.5 * 50-10, 3.5 * 50-10),
                     border_radius=10)
    pygame.draw.rect(screen,
                     color=(70, 70, 170),
                     rect=(x+10, y+10, 2.5 * 50-20, 3.5 * 50-20),
                     border_radius=10)
giveCard()

dealerCardCount = 0
playerCardCount = 0

while running: 
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                running = False
    
    
    drawCard(str(dealer.getRank()), dealer.getSuit(), width//2-125, 230)
    drawHideCard(width//2-50, 260)

    

    pygame.display.flip()