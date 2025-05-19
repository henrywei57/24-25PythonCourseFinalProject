import pygame 
import random
import pygame.gfxdraw
import cv2  # For video playback
from money_manager import save_money, load_money
import math

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
balance = load_money()  # Load balance from file
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
pending_message = ""

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
    pygame.draw.rect(screen, (30, 50, 70), (width//5 - 300, 20, 200, 60), border_radius=10)
    pygame.draw.rect(screen, (20, 40, 60), (width//5 - 295, 25, 190, 50), border_radius=8)
    
    # Draw balance text
    balance_text = balanceFont.render(f"${balance}", True, (255, 255, 255))
    screen.blit(balance_text, (width//5 - 280, 35))
    
    # Draw current bet
    if current_bet > 0:
        pygame.draw.rect(screen, (70, 30, 50), (width//5 + 100, 20, 200, 60), border_radius=10)
        pygame.draw.rect(screen, (60, 20, 40), (width//5 + 105, 25, 190, 50), border_radius=8)
        bet_text = balanceFont.render(f"Bet: ${current_bet}", True, (255, 255, 255))
        screen.blit(bet_text, (width//5 + 120, 35))
    save_money(balance)  # Save balance after updating display

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
    hitButton = pygame.Rect(width//2 - 200 + width//4, height - 175, 200, 100)
    if (bet_placed and game_in_progress and playerGame.isItPlayerTurn() 
        and not playerGame.isPlayerBust() and not playerGame.blackjack and not dealer_revealing):
        mousepos = pygame.mouse.get_pos()
        if hitButton.collidepoint(mousepos):
            color = (0, 100, 255-28) 
        else:
            color = (0, 128, 255)
    else:
        color = (100, 100, 100)  # Grayed out when not active
    pygame.draw.rect(screen, color, hitButton, border_radius=15)
    text = buttonFont.render("Hit", True, (255, 255, 255))
    screen.blit(text, text.get_rect(center=hitButton.center)) 

def standButtonDraw():
    global standButton
    standButton = pygame.Rect(width//2 + 150 + width//4, height - 175, 200, 100)
    if (bet_placed and game_in_progress and playerGame.isItPlayerTurn() 
        and not playerGame.isPlayerBust() and not playerGame.blackjack and not dealer_revealing):
        mousepos = pygame.mouse.get_pos()
        if standButton.collidepoint(mousepos):
            color = (0, 100, 255-28) 
        else:
            color = (0, 128, 255)
    else:
        color = (100, 100, 100)  # Grayed out when not active
    pygame.draw.rect(screen, color, standButton, border_radius=15)
    text = buttonFont.render("Stand", True, (255, 255, 255))
    screen.blit(text, text.get_rect(center=standButton.center))

def newGame():
    global game_in_progress, bet_placed, dealer_revealing, dealer_reveal_index, allDone
    reset_used_cards()
    playerGame.newHand()
    dealerGame.newHand()
    game_in_progress = True
    bet_placed = True
    dealer_revealing = False
    dealer_reveal_index = 0
    allDone = False  # Reset allDone for new round
    
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
    global game_in_progress, bet_placed, current_bet, dealer_revealing, balance, input_active, allDone, pending_message
    
    # Flip dealer's card
    dealerGame.flipCard()
    dealer_revealing = True
    
    # If player busts, just show bust message after reveal
    if playerGame.bust:
        pending_message = "Bust! You lose"
    # If player didn't bust and doesn't have blackjack, compare totals
    elif not playerGame.blackjack:
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
            pending_message = f"Dealer busts! You win ${current_bet}"
        else:
            player_total = playerGame.total if playerGame.hardHand else max(playerGame.total, playerGame.total + 10)
            dealer_total = dealerGame.total if dealerGame.hardHand else max(dealerGame.total, dealerGame.total + 10)
            
            if player_total > 21:
                player_total = playerGame.total  # Use soft total if over 21
            
            if player_total > dealer_total:
                balance += current_bet * 2
                pending_message = f"You win ${current_bet}!"
            elif player_total == dealer_total:
                balance += current_bet  # Push
                pending_message = "Push! Bet returned"
            else:
                pending_message = "You lose!"
    
    # Reset current bet
    current_bet = 0
    
    # End the game
    game_in_progress = False
    bet_placed = False
    input_active = True  # Allow new bet
    allDone = False      # Reset for next round

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
    global dealer_reveal_index, dealer_reveal_timer, dealer_revealing, allDone
    
    if dealer_revealing:
        current_time = pygame.time.get_ticks()
        if current_time - dealer_reveal_timer > 500:  # 0.5 seconds between reveals
            dealer_reveal_index += 1
            dealer_reveal_timer = current_time
            
            # If all cards revealed, stop revealing
            if dealer_reveal_index > len(dealerGame.cardList):
                dealer_revealing = False
                allDone = True

def drawVideoButton():
    global video_button_rect
    btn_size = 60
    margin = 20
    video_button_rect = pygame.Rect(width - btn_size - margin, margin, btn_size, btn_size)
    color = (80, 80, 200)
    pygame.draw.rect(screen, color, video_button_rect, border_radius=15)
    # Draw play icon (triangle)
    points = [
        (width - btn_size - margin + 18, margin + 15),
        (width - btn_size - margin + 18, margin + btn_size - 15),
        (width - margin - 15, margin + btn_size // 2)
    ]
    pygame.draw.polygon(screen, (255, 255, 255), points)
    
    # Draw reward text
    reward_text = buttonFont.render("+$150", True, (255, 255, 255))
    screen.blit(reward_text, (width - btn_size - margin - reward_text.get_width() - 10, margin + btn_size//2 - reward_text.get_height()//2))

def play_video(video_path):
    global balance
    # Add reward before playing video
    balance += 150
    save_money(balance)  # Save the new balance
    
    # Create a fullscreen window
    cv2.namedWindow('Video', cv2.WINDOW_NORMAL)
    cv2.setWindowProperty('Video', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error: Cannot open video {video_path}")
        return
    
    # Get video properties
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_delay = int(1000/fps)  # Delay between frames in milliseconds
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
            
        # Display the frame
        cv2.imshow('Video', frame)
        
        # Wait for the frame duration
        cv2.waitKey(frame_delay)
    
    cap.release()
    cv2.destroyAllWindows()

def drawQuitButton():
    global quit_button_rect, quit_button_velocity, quit_button_size
    
    # Initialize velocity and size if not exists
    if 'quit_button_velocity' not in globals():
        quit_button_velocity = [0, 0]
    if 'quit_button_size' not in globals():
        quit_button_size = 80  # Start with medium size
    
    # Get mouse position
    mouse_pos = pygame.mouse.get_pos()
    
    # Button size and initial position
    btn_width = quit_button_size
    btn_height = quit_button_size // 2
    
    # If button doesn't exist, create it
    if 'quit_button_rect' not in globals():
        quit_button_rect = pygame.Rect(20, 20, btn_width, btn_height)
    
    # Calculate distance from mouse to button center
    button_center = (quit_button_rect.centerx, quit_button_rect.centery)
    distance = math.sqrt((mouse_pos[0] - button_center[0])**2 + (mouse_pos[1] - button_center[1])**2)
    
    # If mouse is close to button, move it away faster
    if distance < 100:  # Same detection radius
        # Calculate direction away from mouse
        dx = button_center[0] - mouse_pos[0]
        dy = button_center[1] - mouse_pos[1]
        # Normalize and scale with increased speed
        length = math.sqrt(dx*dx + dy*dy)
        if length > 0:
            dx = dx/length * 12  # Increased speed from 4 to 12
            dy = dy/length * 12
        # Update velocity
        quit_button_velocity[0] = dx
        quit_button_velocity[1] = dy
        
        # Shrink button when mouse is close, but not as much
        quit_button_size = max(50, quit_button_size - 0.3)  # Same minimum size
    else:
        # Gradually grow back when mouse is far
        quit_button_size = min(80, quit_button_size + 0.2)  # Same maximum size
    
    # Apply velocity with less damping for faster movement
    quit_button_rect.x += quit_button_velocity[0]
    quit_button_rect.y += quit_button_velocity[1]
    quit_button_velocity[0] *= 0.98  # Less damping for faster movement
    quit_button_velocity[1] *= 0.98
    
    # Add more random movement for unpredictability
    if random.random() < 0.08:  # Increased chance from 5% to 8%
        quit_button_velocity[0] += random.uniform(-2, 2)  # Increased random movement
        quit_button_velocity[1] += random.uniform(-2, 2)
    
    # Keep button within screen bounds with bounce
    if quit_button_rect.left < 0:
        quit_button_rect.left = 0
        quit_button_velocity[0] *= -0.95  # More bounce
    if quit_button_rect.right > width:
        quit_button_rect.right = width
        quit_button_velocity[0] *= -0.95
    if quit_button_rect.top < 0:
        quit_button_rect.top = 0
        quit_button_velocity[1] *= -0.95
    if quit_button_rect.bottom > height:
        quit_button_rect.bottom = height
        quit_button_velocity[1] *= -0.95
    
    # Update button size
    quit_button_rect.width = btn_width
    quit_button_rect.height = btn_height
    
    # Draw button with pulsing effect
    pulse = (math.sin(pygame.time.get_ticks() * 0.005) + 1) * 15
    button_color = (min(255, max(0, 200 + int(pulse))), 50, 50)
    pygame.draw.rect(screen, button_color, quit_button_rect, border_radius=10)
    
    # Draw "Quit" text
    quit_text = buttonFont.render("Quit", True, (255, 255, 255))
    text_rect = quit_text.get_rect(center=quit_button_rect.center)
    screen.blit(quit_text, text_rect)

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
allDone = False
dealer_reveal_index = 0
dealer_reveal_timer = 0

def main():
    global WIDTH, HEIGHT, balance, current_bet, game_in_progress, bet_placed
    global input_active, bet_input, error_message, error_timer, pending_message
    
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
                elif event.key == pygame.K_RETURN:
                    try:
                        bet_amount = int(bet_input)
                        if bet_amount <= 0:
                            setError("Bet must be positive")
                        elif bet_amount > balance:
                            setError("Not enough balance")
                        elif game_in_progress:
                            setError("Finish current game first")
                        else:
                            current_bet = bet_amount
                            balance -= bet_amount
                            newGame()
                            bet_input = ""
                    except ValueError:
                        setError("Invalid bet amount")
                elif event.key == pygame.K_BACKSPACE:
                    bet_input = bet_input[:-1]
            elif event.type == pygame.TEXTINPUT:
                # Only allow digits
                if event.text.isdigit():
                    # Limit input length to prevent overflow
                    if len(bet_input) < 10:  # Maximum 10 digits
                        bet_input += event.text
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Video button
                if 'video_button_rect' in globals() and video_button_rect.collidepoint(event.pos):
                    # Play random video
                    video_number = random.randint(1, 5)
                    video_path = f'video{video_number}.mp4'
                    play_video(video_path)
                # Quit button with larger hitbox
                elif 'quit_button_rect' in globals():
                    hitbox = quit_button_rect.inflate(20, 10)  # Larger hitbox
                    if hitbox.collidepoint(event.pos):
                        running = False
                # Bet button
                if bet_button.collidepoint(event.pos):
                    try:
                        bet_amount = int(bet_input) if bet_input else 0
                        if bet_amount <= 0:
                            setError("Bet must be positive")
                        elif bet_amount > balance:
                            setError("Not enough balance")
                        elif game_in_progress:
                            setError("Finish current game first")
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
                            endRound()
                    elif 'standButton' in globals() and standButton.collidepoint(event.pos) and playerGame.isItPlayerTurn() and not playerGame.isPlayerBust():
                        playerGame.endTurn()
                        endRound()

        # Update dealer card reveal animation
        updateDealerReveal()

        # Show pending message after dealer cards are revealed
        if not dealer_revealing and pending_message:
            showMessage(pending_message)
            pending_message = ""

        screen.fill(background_color)
        drawBanner()
        drawBalance()
        drawBetInput()
        drawVideoButton()  # Draw the video button
        drawQuitButton()   # Draw the moving quit button

        if game_in_progress and bet_placed:
            hitButtonDraw()
            standButtonDraw()
            
            # Dealer's turn logic
            if not playerGame.isItPlayerTurn() and not dealer_revealing:
                dealer_total = dealerGame.getTotal()
                dealer_soft = not dealerGame.isItHard()
                
                # Dealer must hit on soft 17 or below
                if (dealer_total < 17) or (dealer_total == 17 and not dealer_soft):
                    dealerGame.addCard()
                    if dealerGame.getTotal() > 21 and dealerGame.isItHard():
                        dealerGame.bustDealer()
                else:
                    dealerGame.endTurn()

        dealerGame.displayCard()
        playerGame.displayCard()
        pygame.display.flip()
        clock.tick(60) 

    pygame.quit()

if __name__ == "__main__":
    main()