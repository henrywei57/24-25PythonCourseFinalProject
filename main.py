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
balanceFont = pygame.font.SysFont(None, 50)
betFont = pygame.font.SysFont(None, 40)
inputFont = pygame.font.SysFont(None, 60)
bannerColor = (22, 44, 57)
bannerFont = pygame.font.SysFont(None, 40)

# Initialize balance and betting variables
balance = 1000  # Starting balance
current_bet = 0
game_in_progress = False
bet_placed = False
input_active = False
bet_input = ""
error_message = ""
error_timer = 0
dealer_revealing = False
dealer_reveal_index = 0
dealer_reveal_timer = 0

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
        self.finishTurn = False
        self.blackjack = False

    def displayCard(self):
        text = cardCountFont.render("Dealer", True, (255, 255, 255))
        text_rect = text.get_rect()
        text_rect.centerx = width // 2
        text_rect.top = 20
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
                    170 - 30 + (i - 1) * 30 
                )
            drawHideCard(
                start_x + (num_cards - 1) * spacing,
                170 - 30 + (num_cards - 1) * 30  
            )
        else:
            # Only show revealed cards
            for i in range(1, min(num_cards, dealer_reveal_index + 1)):
                drawCard(
                    str(self.cardList[i].getRank()),
                    self.cardList[i].getSuit(),
                    start_x + (i - 1) * spacing,
                    170 - 30 + (i - 1) * 30
                )
            # Show hidden card until it's revealed
            if dealer_reveal_index < num_cards:
                drawHideCard(
                    start_x + (num_cards - 1) * spacing,
                    170 - 30 + (num_cards - 1) * 30
                )
            else:
                drawCard(
                    str(self.cardList[0].getRank()),
                    self.cardList[0].getSuit(),
                    start_x + (num_cards - 1) * spacing,
                    170 - 30 + (num_cards - 1) * 30
                )

        if self.blackjack:
            text = bustFont.render("BLACKJACK", True, (0, 200, 0))
            rotated_text = pygame.transform.rotate(text, -45)
            rotated_rect = rotated_text.get_rect()
            rotated_rect.centerx = width // 2
            rotated_rect.top = 30
            screen.blit(rotated_text, rotated_rect)
        elif self.bust:
            text = bustFont.render("BUST", True, (255, 0, 0))
            rotated_text = pygame.transform.rotate(text, -45)
            rotated_rect = rotated_text.get_rect()
            rotated_rect.centerx = width // 2
            rotated_rect.top = 30
            screen.blit(rotated_text, rotated_rect)

    def addCard(self):
        self.cardList.append(get_unique_card())
        screen.fill(background_color)
        self.total = sum(cardToNum(c) for c in self.cardList)
        self.displayCard()
        print("card added")
    
    def flipCard(self):
        global dealer_revealing, dealer_reveal_index, dealer_reveal_timer
        self.flip = true
        dealer_revealing = True
        dealer_reveal_index = 0
        dealer_reveal_timer = pygame.time.get_ticks()

    def newHand(self):
        self.cardList = []
        self.cardList.append(get_unique_card())
        self.cardList.append(get_unique_card())
        self.hardHand = true
        if any(c.rank == 'A' for c in self.cardList):
            self.hardHand = false
        self.total = sum(cardToNum(c) for c in self.cardList)
        self.bust = false
        self.flip = false
        self.finishTurn = false
        self.blackjack = False
        # Check for dealer blackjack
        if (self.total == 11 and not self.hardHand) or self.total == 21:
            self.blackjack = True

    def bustDealer(self):
        self.bust = true
    
    def getTotal(self):
        return self.total

    def isItHard(self):
        return self.hardHand

    def endTurn(self):
        self.finishTurn = true

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
        self.blackjack = False
        # Check for player blackjack
        if (self.total == 11 and not self.hardHand) or self.total == 21:
            self.blackjack = True

    def displayCard(self):
        text = cardCountFont.render("Player", True, (255, 255, 255))
        text_rect = text.get_rect()
        text_rect.centerx = width // 2
        text_rect.top = height - 370
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
                height - 225 - 20 + (i - 1) * 30
            )
        drawCard(
            str(self.cardList[0].getRank()),
            self.cardList[0].getSuit(),
            start_x + (num_cards - 1) * spacing,
            height - 225 - 20 + (num_cards - 1) * 30
        )

        if self.blackjack:
            text = bustFont.render("BLACKJACK", True, (0, 200, 0))
            rotated_text = pygame.transform.rotate(text, -45)
            rotated_rect = rotated_text.get_rect()
            rotated_rect.centerx = width // 2
            rotated_rect.top = height // 2 + 20
            screen.blit(rotated_text, rotated_rect)
        elif self.bust:
            text = bustFont.render("BUST", True, (255, 0, 0))
            rotated_text = pygame.transform.rotate(text, -45)
            rotated_rect = rotated_text.get_rect()
            rotated_rect.centerx = width // 2
            rotated_rect.top = height // 2 + 20
            screen.blit(rotated_text, rotated_rect)

    def addCard(self):
        self.cardList.append(get_unique_card())
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
        # Player can't have blackjack after hitting
        self.blackjack = False

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
        self.playerTurn = True
        self.blackjack = False
        # Check for player blackjack
        if (self.total == 11 and not self.hardHand) or self.total == 21:
            self.blackjack = True

    def endTurn(self):
        self.playerTurn = false
    def isItPlayerTurn(self):
        return self.playerTurn
    
    def isPlayerBust(self):
        return self.bust

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
    centerX, centerY = width//2, height//2+20
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

def drawBalance():
    # Draw balance background
    pygame.draw.rect(screen, (30, 50, 70), (width//4 - 300, 20, 200, 60), border_radius=10)
    pygame.draw.rect(screen, (20, 40, 60), (width//4 - 295, 25, 190, 50), border_radius=8)
    
    # Draw balance text
    balance_text = balanceFont.render(f"${balance}", True, (255, 255, 255))
    screen.blit(balance_text, (width//4 - 280, 35))
    
    # Draw current bet
    if current_bet > 0:
        pygame.draw.rect(screen, (70, 30, 50), (width//4 + 100, 20, 200, 60), border_radius=10)
        pygame.draw.rect(screen, (60, 20, 40), (width//4 + 105, 25, 190, 50), border_radius=8)
        bet_text = balanceFont.render(f"Bet: ${current_bet}", True, (255, 255, 255))
        screen.blit(bet_text, (width//4 + 120, 35))

def drawBetInput():
    global bet_input_box, bet_button
    
    # Draw bet input area at the top center
    pygame.draw.rect(screen, (40, 40, 60), (width//5 - 200, height//4+height//2, 400, 80), border_radius=10)
    
    # Draw input box
    input_color = (60, 60, 80) if not input_active else (80, 80, 100)
    bet_input_box = pygame.Rect(width//5 - 180, height//4+height//2+20, 240, 50)
    pygame.draw.rect(screen, input_color, bet_input_box, border_radius=8)
    
    # Draw input text
    input_text = inputFont.render(bet_input if bet_input else "0", True, (255, 255, 255))
    screen.blit(input_text, (bet_input_box.x + 10, bet_input_box.y + 5))
    
    # Draw bet button
    bet_button = pygame.Rect(width//5 + 70, height//4+height//2+20, 110, 50)
    button_color = (0, 150, 0) if bet_button.collidepoint(pygame.mouse.get_pos()) else (0, 180, 0)
    pygame.draw.rect(screen, button_color, bet_button, border_radius=8)
    bet_text = buttonFont.render("BET", True, (255, 255, 255))
    screen.blit(bet_text, (bet_button.centerx - bet_text.get_width()//2, 
                          bet_button.centery - bet_text.get_height()//2))
    
    # Draw error message if any
    if error_message and pygame.time.get_ticks() - error_timer < 3000:  # Show for 3 seconds
        error_text = buttonFont.render(error_message, True, (255, 50, 50))
        screen.blit(error_text, (width//5 - error_text.get_width()//4, height//4+height//2-20))

def hitButtonDraw():
    global hitButton
    hitButton = pygame.Rect(width//2 - 150, height - 175, 100, 50)
    if (bet_placed and game_in_progress and playerGame.isItPlayerTurn() and 
        not playerGame.isPlayerBust() and not playerGame.blackjack):
        mousepos = pygame.mouse.get_pos()
        if hitButton.collidepoint(mousepos):
            color = (0, 100, 255-28) 
        else:
            color = (0, 128, 255)
        pygame.draw.rect(screen, color, hitButton, border_radius=15)
        text = buttonFont.render("Hit", True, (255, 255, 255))
        screen.blit(text, text.get_rect(center=hitButton.center)) 

def standButtonDraw():
    global standButton
    standButton = pygame.Rect(width//2 + 50, height - 175, 100, 50)
    if (bet_placed and game_in_progress and playerGame.isItPlayerTurn() and 
        not playerGame.isPlayerBust() and not playerGame.blackjack):
        mousepos = pygame.mouse.get_pos()
        if standButton.collidepoint(mousepos):
            color = (0, 100, 255-28) 
        else:
            color = (0, 128, 255)
        pygame.draw.rect(screen, color, standButton, border_radius=15)
        text = buttonFont.render("Stand", True, (255, 255, 255))
        screen.blit(text, text.get_rect(center=standButton.center))    

def newGame():
    global game_in_progress, bet_placed, dealer_revealing, dealer_reveal_index
    reset_used_cards()
    playerGame.newHand()
    dealerGame.newHand()
    game_in_progress = True
    bet_placed = True
    dealer_revealing = False
    dealer_reveal_index = 0
    
    # Check for immediate blackjack
    checkBlackjack()

def checkBlackjack():
    global balance, game_in_progress
    
    # Player has blackjack
    if playerGame.blackjack:
        # Dealer also has blackjack - push
        if dealerGame.blackjack:
            balance += current_bet  # Return original bet
            showMessage("Push! Both have Blackjack")
        else:
            # Player wins 3:2
            winnings = current_bet * 2.5
            balance += int(winnings)
            showMessage(f"Blackjack! You win ${int(winnings - current_bet)}")
        endRound()
    # Dealer has blackjack (player doesn't)
    elif dealerGame.blackjack:
        showMessage("Dealer has Blackjack! You lose")
        endRound()

def endRound():
    global game_in_progress, bet_placed, current_bet, dealer_revealing, balance
    
    # Flip dealer's card
    dealerGame.flipCard()
    dealer_revealing = True
    
    # If player didn't bust and doesn't have blackjack, compare totals
    if not playerGame.bust and not playerGame.blackjack:
        # Dealer must hit until 17
        while dealerGame.getTotal() < 17 or (not dealerGame.isItHard() and dealerGame.getTotal() == 17):
            dealerGame.addCard()
            if dealerGame.getTotal() > 21 and dealerGame.isItHard():
                dealerGame.bustDealer()
                break
        
        # Determine winner
        if dealerGame.bust:
            # Player wins
            balance += current_bet * 2
            showMessage(f"Dealer busts! You win ${current_bet}")
        else:
            player_total = playerGame.total if playerGame.hardHand else max(playerGame.total, playerGame.total + 10)
            dealer_total = dealerGame.total if dealerGame.hardHand else max(dealerGame.total, dealerGame.total + 10)
            
            if player_total > 21:
                player_total = playerGame.total  # Use soft total if over 21
            
            if player_total > dealer_total:
                balance += current_bet * 2
                showMessage(f"You win ${current_bet}!")
            elif player_total == dealer_total:
                balance += current_bet  # Push
                showMessage("Push! Bet returned")
            else:
                showMessage("You lose!")
    
    # Reset current bet
    current_bet = 0
    
    # End the game
    game_in_progress = False
    bet_placed = False

def showMessage(msg):
    # Create a semi-transparent overlay
    overlay = pygame.Surface((width, height), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))  # Semi-transparent black
    screen.blit(overlay, (0, 0))
    
    # Draw message box
    msg_box = pygame.Rect(width//2 - 200, height//2 - 75, 400, 150)
    pygame.draw.rect(screen, (30, 50, 80), msg_box, border_radius=15)
    pygame.draw.rect(screen, (50, 80, 120), msg_box.inflate(-10, -10), border_radius=10)
    
    # Draw message text
    msg_text = buttonFont.render(msg, True, (255, 255, 255))
    screen.blit(msg_text, (width//2 - msg_text.get_width()//2, height//2 - 30))
    
    # Draw continue button
    continue_btn = pygame.Rect(width//2 - 50, height//2 + 30, 100, 40)
    pygame.draw.rect(screen, (0, 150, 0), continue_btn, border_radius=10)
    continue_text = buttonFont.render("OK", True, (255, 255, 255))
    screen.blit(continue_text, (continue_btn.centerx - continue_text.get_width()//2, 
                               continue_btn.centery - continue_text.get_height()//2))
    
    pygame.display.flip()
    
    # Wait for user to click OK
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if continue_btn.collidepoint(event.pos):
                    waiting = False
        pygame.time.delay(100)

def setError(message):
    global error_message, error_timer
    error_message = message
    error_timer = pygame.time.get_ticks()

def updateDealerReveal():
    global dealer_reveal_index, dealer_reveal_timer, dealer_revealing
    
    if dealer_revealing:
        current_time = pygame.time.get_ticks()
        if current_time - dealer_reveal_timer > 500:  # 0.5 seconds between reveals
            dealer_reveal_index += 1
            dealer_reveal_timer = current_time
            
            # If all cards revealed, stop revealing
            if dealer_reveal_index >= len(dealerGame.cardList):
                dealer_revealing = False

# Initialize game objects
dealerGame = dealer()
playerGame = player()
game_in_progress = False
bet_placed = False
input_active = False
bet_input = ""
error_message = ""
error_timer = 0
dealer_revealing = False
dealer_reveal_index = 0
dealer_reveal_timer = 0

def main():
    global WIDTH, HEIGHT, balance, current_bet, game_in_progress, bet_placed
    global input_active, bet_input, error_message, error_timer
    
    clock = pygame.time.Clock()
    running = True
    
    while running:
        if pygame.event.get(pygame.VIDEORESIZE):
            WIDTH, HEIGHT = pygame.display.get_surface().get_size()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False
                elif input_active:
                    if event.key == pygame.K_RETURN:
                        try:
                            bet_amount = int(bet_input)
                            if bet_amount <= 0:
                                setError("Bet must be positive")
                            elif bet_amount > balance:
                                setError("Not enough balance")
                            else:
                                current_bet = bet_amount
                                balance -= bet_amount
                                newGame()
                                bet_input = ""
                        except ValueError:
                            setError("Invalid bet amount")
                    elif event.key == pygame.K_BACKSPACE:
                        bet_input = bet_input[:-1]
                    elif event.unicode.isdigit():
                        bet_input += event.unicode
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Bet input box
                if bet_input_box.collidepoint(event.pos):
                    input_active = True
                else:
                    input_active = False
                
                # Bet button
                if bet_button.collidepoint(event.pos) and not game_in_progress:
                    try:
                        bet_amount = int(bet_input) if bet_input else 0
                        if bet_amount <= 0:
                            setError("Bet must be positive")
                        elif bet_amount > balance:
                            setError("Not enough balance")
                        else:
                            current_bet = bet_amount
                            balance -= bet_amount
                            newGame()
                            bet_input = ""
                    except ValueError:
                        setError("Invalid bet amount")
                
                # Game buttons
                if game_in_progress and bet_placed:
                    if 'hitButton' in globals() and hitButton.collidepoint(event.pos) and playerGame.isItPlayerTurn() and not playerGame.isPlayerBust():
                        playerGame.addCard()
                        if playerGame.isPlayerBust():
                            showMessage("Bust! You lose")
                            endRound()
                    elif 'standButton' in globals() and standButton.collidepoint(event.pos) and playerGame.isItPlayerTurn() and not playerGame.isPlayerBust():
                        playerGame.endTurn()
                        endRound()

        # Update dealer card reveal animation
        updateDealerReveal()

        screen.fill(background_color)
        drawBanner()
        drawBalance()
        drawBetInput()

        if game_in_progress and bet_placed:
            hitButtonDraw()
            standButtonDraw()
            
            if not playerGame.isItPlayerTurn() and not dealer_revealing:
                if dealerGame.getTotal() <= 16:
                    dealerGame.addCard()
                if dealerGame.getTotal() > 21 and dealerGame.isItHard():
                    dealerGame.bustDealer()
                if dealerGame.getTotal() < 16 and dealerGame.isItHard():
                    dealerGame.endTurn()

        dealerGame.displayCard()
        playerGame.displayCard()
        pygame.display.flip()
        clock.tick(60) 

    pygame.quit()

if __name__ == "__main__":
    main()