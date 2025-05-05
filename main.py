import pygame 
import random
import pygame.gfxdraw
import time
import threading

true = True
false = False


background_color = (18, 31, 45) 
screen = pygame.display.set_mode((0, 0)) 
pygame.display.set_caption('Bur Bur Patapim') 
screen.fill(background_color) 
pygame.display.flip() 
running = true
width,height = screen.get_size()
pygame.font.init()
rankFont = pygame.font.SysFont(None, 55)
cardCountFont = pygame.font.SysFont(None, 55)
bustFont = pygame.font.SysFont(None, 250)
bustFont.set_bold(true)
buttonFont = pygame.font.SysFont(None, 40)
bannerColor = (22, 44, 57)
bannerFont = pygame.font.SysFont(None, 40)

balance = 0

def cardToNum(card):
    if card.getRank() == "A":
        return 1
    if card.getRank() == "J" or card.getRank() == "Q" or card.getRank() == "K":
        return 10
    return eval(str(card.getRank()))

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


rank = ["A",2,3,4,5,6,7,8,9,10,"J","Q","K"]
suit = ["diamond","heart","club","spade"]

used_cards = set()

def get_unique_card():
    while True:
        r = rank[random.randint(0, 12)]
        s = suit[random.randint(0, 3)]
        if (r, s) not in used_cards:
            used_cards.add((r, s))
            return card(r, s)

def reset_used_cards():
    global used_cards
    used_cards = set()



class dealer:
    def __init__(self):
        self.cardList = []
        self.cardList.append(get_unique_card())
        self.cardList.append(get_unique_card())
        self.hardHand = True
        if any(c.rank == 'A' for c in self.cardList):
            self.hardHand = False
        self.total = sum(cardToNum(c) for c in self.cardList)
        self.flip = False
        self.bust = False



    def displayCard(self):
        text = cardCountFont.render("Dealer", True, (255, 255, 255))
        text_rect = text.get_rect()
        text_rect.centerx = width // 2
        text_rect.top = 50
        screen.blit(text, text_rect)

        ellipse_width = text_rect.width + 20 
        ellipse_height = text_rect.height + 10 
        ellipse_x = text_rect.centerx - ellipse_width // 2
        ellipse_y = text_rect.bottom + 15
        pygame.draw.ellipse(screen, bannerColor, (ellipse_x, ellipse_y, ellipse_width, ellipse_height))

        if self.flip:
            counterString = str(self.total)
            if not self.hardHand:
                counterString += f"/{self.total + 10}"
        else:
            counterString = f"{cardToNum(self.cardList[1])}+?"

        displayCounter = cardCountFont.render(counterString, True, (255, 255, 255))
        counter_rect = displayCounter.get_rect()
        counter_rect.centerx = width // 2
        counter_rect.top = ellipse_y + 6
        screen.blit(displayCounter, counter_rect)

        displayCounter = cardCountFont.render(counterString, True, (255, 255, 255))
        counter_rect = displayCounter.get_rect()
        counter_rect.centerx = width // 2
        counter_rect.top = ellipse_y + 6
        screen.blit(displayCounter, counter_rect)


        num_cards = len(self.cardList)
        card_width = 100
        spacing = 75 
        total_width = (num_cards - 1) * spacing + card_width
        start_x = (width // 2) - (total_width // 2)

        if not self.flip:
            for i in range(1, num_cards):
                drawCard(
                    str(self.cardList[i].getRank()), 
                    self.cardList[i].getSuit(), 
                    start_x + (i - 1) * spacing,
                    170 + (i - 1) * 30 
                )
            drawHideCard(
                start_x + (num_cards - 1) * spacing,
                170 + (num_cards - 1) * 30  
            )
        else:
            for i in range(1, num_cards):
                drawCard(
                    str(self.cardList[i].getRank()),
                    self.cardList[i].getSuit(),
                    start_x + (i - 1) * spacing,
                    170 + (i - 1) * 30
                )
            drawCard(
                str(self.cardList[0].getRank()),
                self.cardList[0].getSuit(),
                start_x + (num_cards - 1) * spacing,
                170 + (num_cards - 1) * 30
            )

        if(self.bust):
            text = bustFont.render("BUST", True, (255, 0, 0))
            rotated_text = pygame.transform.rotate(text, -45)
            rotated_rect = rotated_text.get_rect()
            rotated_rect.centerx = width // 2
            rotated_rect.top = 30
            screen.blit(rotated_text, rotated_rect)


    def addCard(self):
        self.cardList.append(card(rank[random.randint(0, 12)], suit[random.randint(0, 3)]))
        screen.fill(background_color)
        self.total = sum(cardToNum(c) for c in self.cardList)
        self.displayCard()
        print("card added")
    
    def flipCard(self):
        self.flip = true

    def newHand(self):
        self.cardList = []
        self.cardList.append(get_unique_card())
        self.cardList.append(get_unique_card())
        self.hardHand = true
        if any(c.rank == 'A' for c in self.cardList):
            self.hardHand = false
        self.total = sum(cardToNum(c) for c in self.cardList)
        self.bust = false

    def bustDealer(self):
        self.bust = true


class player:
    def __init__(self):
        self.cardList = []
        self.cardList.append(get_unique_card())
        self.cardList.append(get_unique_card())
        self.hardHand = True
        if any(c.rank == 'A' for c in self.cardList):
            self.hardHand = False
        self.total = sum(cardToNum(c) for c in self.cardList)
        self.bust = False
        self.playerTurn = True



    def displayCard(self):
        text = cardCountFont.render("Player", True, (255, 255, 255))
        text_rect = text.get_rect()
        text_rect.centerx = width // 2
        text_rect.top = height // 2 + 100
        screen.blit(text, text_rect)

        ellipse_width = text_rect.width + 20 
        ellipse_height = text_rect.height + 10 
        ellipse_x = text_rect.centerx - ellipse_width // 2
        ellipse_y = text_rect.bottom + 15
        pygame.draw.ellipse(screen, bannerColor, (ellipse_x, ellipse_y, ellipse_width, ellipse_height))

        counterString = str(self.total)

        if not self.hardHand:
            counterString += f"/{self.total + 10}"

        displayCounter = cardCountFont.render(counterString, True, (255, 255, 255))
        counter_rect = displayCounter.get_rect()
        counter_rect.centerx = width // 2
        counter_rect.top = ellipse_y + 6
        screen.blit(displayCounter, counter_rect)

        displayCounter = cardCountFont.render(counterString, True, (255, 255, 255))
        counter_rect = displayCounter.get_rect()
        counter_rect.centerx = width // 2
        counter_rect.top = ellipse_y + 6
        screen.blit(displayCounter, counter_rect)


        num_cards = len(self.cardList)
        card_width = 100
        spacing = 75 
        total_width = (num_cards - 1) * spacing + card_width
        start_x = (width // 2) - (total_width // 2)

        for i in range(1, num_cards):
            drawCard(
                str(self.cardList[i].getRank()),
                self.cardList[i].getSuit(),
                start_x + (i - 1) * spacing,
                height // 2 + 220 + (i - 1) * 30
            )
        drawCard(
            str(self.cardList[0].getRank()),
            self.cardList[0].getSuit(),
            start_x + (num_cards - 1) * spacing,
            height // 2 + 220 + (num_cards - 1) * 30
        )

        if(self.bust):
            text = bustFont.render("BUST", True, (255, 0, 0))
            rotated_text = pygame.transform.rotate(text, -45)
            rotated_rect = rotated_text.get_rect()
            rotated_rect.centerx = width // 2
            rotated_rect.top = height // 2 + 80
            screen.blit(rotated_text, rotated_rect)


    def addCard(self):
        self.cardList.append(card(rank[random.randint(0, 12)], suit[random.randint(0, 3)]))
        screen.fill(background_color)
        if any(c.rank == 'A' for c in self.cardList):
            self.hardHand = false
        self.total = sum(cardToNum(c) for c in self.cardList)
        self.displayCard()
        print("card added")
        if(self.total > 21):
            self.bustPlayer()
        if(self.total + 10 > 21):
            self.hardHand = true

    def bustPlayer(self):
        self.bust = true

    def newHand(self):
        self.cardList = []
        self.cardList.append(get_unique_card())
        self.cardList.append(get_unique_card())
        self.hardHand = true
        if any(c.rank == 'A' for c in self.cardList):
            self.hardHand = false
        self.total = sum(cardToNum(c) for c in self.cardList)
        self.bust = false
        self.playerTurn = true

    def endTurn(self):
        self.playerTurn = false
    def isItPlayerTurn(self):
        return self.playerTurn
    
    def isPlayerBust(self):
        return self.bust
    

# global dealer, dealerHide, player1, player2




# def giveCard():
    # global dealer, dealerHide
    # dealer = card(rank[random.randint(0,12)],suit[random.randint(0,3)])
    # dealerHide = card(rank[random.randint(0,12)],suit[random.randint(0,3)])



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
    temp_surf = pygame.Surface((int(2.5 * 50), int(3.5 * 50)), pygame.SRCALPHA)
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
    
    text = rankFont.render(rank, true, color)
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

def drawBanner():
    centerX, centerY = width//2, height//2
    color = bannerColor
    pygame.draw.rect(screen,
                    color=color,
                    rect=(centerX-200, centerY-60, 400, 80),
                    border_radius=10)
    shape1 = [(centerX-205, centerY-45), 
              (centerX-275, centerY-45),
              (centerX-265, centerY-5), 
              (centerX-275, centerY+35), 
              (centerX-165, centerY+35), 
              (centerX-165, centerY+25), 
              (centerX-205, centerY+25)]
    pygame.draw.rect(screen,
                    color=color,
                    rect=(centerX-170, centerY+25, 10, 10),
                    border_radius=2)

    shape2 = [(centerX+205, centerY-45), 
              (centerX+275, centerY-45),
              (centerX+265, centerY-5), 
              (centerX+275, centerY+35), 
              (centerX+165, centerY+35), 
              (centerX+165, centerY+25), 
              (centerX+205, centerY+25)]
    pygame.draw.rect(screen,
                    color=color,
                    rect=(centerX+170, centerY+25, -10, 10),
                    border_radius=2)
    
    pygame.gfxdraw.filled_polygon(screen, shape1, color)
    pygame.gfxdraw.filled_polygon(screen, shape2, color)

    banner = buttonFont.render("BLACKJACK PAYS 3 TO 2", True, (127, 138, 157))
    screen.blit(banner, banner.get_rect(center=(centerX, centerY-60+40))) 



# def game():
#     x = dealer()
#     x.displayCard()
#     while(1):
#         for event in pygame.event.get(): 
#             if event.type == pygame.KEYDOWN:
#                 if event.key == pygame.K_g:
#                     x.addCard()
#                     print("key pressed")
#             if event.type == pygame.KEYDOWN:
#                 if event.key == pygame.K_q:
#                     running = false


dealerGame = dealer()
playerGame = player()

def hitButtonDraw():
    global hitButton
    hitButton = pygame.Rect(225, height-175, 100, 50)
    mousepos = pygame.mouse.get_pos()
    if (hitButton.collidepoint(mousepos) and 
        playerGame.isItPlayerTurn() and 
        not playerGame.isPlayerBust()):
        color = (0, 100, 255-28) 
    else:
        color = (0, 128, 255)
    pygame.draw.rect(screen, color, hitButton, border_radius=15)
    text = buttonFont.render("Hit", True, (255, 255, 255))
    screen.blit(text, text.get_rect(center=hitButton.center)) 

def standButtonDraw():
    global standButton
    standButton = pygame.Rect(225+150, height-175, 100, 50)
    mousepos = pygame.mouse.get_pos()
    if (standButton.collidepoint(mousepos) and 
        playerGame.isItPlayerTurn() and 
        not playerGame.isPlayerBust()):
        color = (0, 100, 255-28) 
    else:
        color = (0, 128, 255)
    pygame.draw.rect(screen, color, standButton, border_radius=15)
    text = buttonFont.render("Stand", True, (255, 255, 255))
    screen.blit(text, text.get_rect(center=standButton.center))    

def newGame():
    playerGame.newHand()
    dealerGame.newHand()


def main():
    global WIDTH, HEIGHT
    

    clock = pygame.time.Clock()
    running = True
    
    while running:
        if pygame.event.get(pygame.VIDEORESIZE):
            WIDTH, HEIGHT = pygame.display.get_surface().get_size()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_g:
                    dealerGame.addCard()
                elif event.key == pygame.K_q:
                    running = False
                elif event.key == pygame.K_t:
                    playerGame.addCard()
                elif event.key == pygame.K_b:
                    playerGame.bustPlayer()
                    dealerGame.bustDealer()
                elif event.key == pygame.K_n:
                    playerGame.newHand()
                    dealerGame.newHand()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if hitButton.collidepoint(event.pos) and playerGame.isItPlayerTurn() and not playerGame.isPlayerBust():
                    playerGame.addCard()
                elif standButton. collidepoint(event.pos):
                    playerGame.endTurn()




        screen.fill(background_color)
        

        if playerGame.isItPlayerTurn() and not playerGame.isPlayerBust():
            hitButtonDraw()
            standButtonDraw()


        if(playerGame.isPlayerBust() or not playerGame.isItPlayerTurn()):
            newGame()
        


        dealerGame.displayCard()
        playerGame.displayCard()
        drawBanner()
        pygame.display.flip()
        clock.tick(60) 

    pygame.quit()

if __name__ == "__main__":
    main()