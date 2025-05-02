import pygame 
import random
import pygame.gfxdraw

# Initialize pygame
pygame.init()

# Screen setup
background_colour = (18, 31, 45) 
screen = pygame.display.set_mode((800, 600)) 
pygame.display.set_caption('Blackjack') 
screen.fill(background_colour) 
pygame.display.flip() 

# Game variables
running = True
width, height = screen.get_size()
pygame.font.init()
rankFont = pygame.font.SysFont(None, 55)

class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
    def getRank(self) -> str:
        return self.rank
    def getSuit(self) -> str:
        return self.suit
    def getCard(self) -> str:
        return f"{self.rank} of {self.suit}"

# Card drawing functions
def drawDiamond(x, y):
    color = (203, 56, 74)
    shape1 = [(x+40, y+60), (x+40, y+100), (x+40+20, y+80)]
    shape2 = [(x+40, y+60), (x+40, y+100), (x+40-20, y+80)]

    pygame.gfxdraw.filled_polygon(screen, shape1, color)
    pygame.gfxdraw.filled_polygon(screen, shape2, color)

def drawHeart(x, y):
    color = (203, 56, 74)
    shape1 = [(x+40, y+80), (x+40, y+100), (x+40+20, y+80), (x+40+10, y+70)]
    shape2 = [(x+40, y+80), (x+40, y+100), (x+40-20, y+80), (x+40-10, y+70)]

    pygame.gfxdraw.filled_polygon(screen, shape1, color)
    pygame.gfxdraw.filled_polygon(screen, shape2, color)

def drawClub(x, y):
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

def drawSpade(x, y):
    color = (27, 42, 57)
    shape1 = [(x+40, y+60), (x+40+20, y+80), (x+40+10, y+80+10), (x+40, y+80)]
    shape2 = [(x+40, y+60), (x+40-20, y+80), (x+40-10, y+80+10), (x+40, y+80)]

    shape3 = [(x+40, y+65.5+10+7.5+5), (x+40-10, y+65.5+10+10+5+7.5), (x+40+10, y+65.5+10+10+7.5+5)]

    pygame.gfxdraw.filled_polygon(screen, shape1, color)
    pygame.gfxdraw.filled_polygon(screen, shape2, color)
    pygame.gfxdraw.filled_polygon(screen, shape3, color)

def draw_card_with_shadow(rank, suit, x, y, hidden=False):
    # Shadow settings
    shadow_offset = 8
    shadow_blur_radius = 15
    shadow_color = (0, 0, 0, 150)  # Semi-transparent black
    
    # Create a surface for the shadow with per-pixel alpha
    shadow_surf = pygame.Surface((2.5 * 50 + shadow_blur_radius*2, 
                                3.5 * 50 + shadow_blur_radius*2), pygame.SRCALPHA)
    
    # Draw the shadow (larger and blurred)
    shadow_rect = pygame.Rect(shadow_blur_radius, shadow_blur_radius, 
                            2.5 * 50, 3.5 * 50)
    pygame.draw.rect(shadow_surf, shadow_color, shadow_rect, border_radius=10)
    
    # Blur the shadow by scaling down and up
    shadow_surf = pygame.transform.smoothscale(shadow_surf, 
                                            (shadow_surf.get_width()//2, shadow_surf.get_height()//2))
    shadow_surf = pygame.transform.smoothscale(shadow_surf, 
                                            (shadow_surf.get_width()*2, shadow_surf.get_height()*2))
    
    # Draw the shadow surface
    screen.blit(shadow_surf, (x + shadow_offset - shadow_blur_radius, 
                            y + shadow_offset - shadow_blur_radius))
    
    # Draw the card
    card_color = (240, 240, 240)  # Brighter white for better contrast
    pygame.draw.rect(screen, card_color, (x, y, 2.5 * 50, 3.5 * 50), border_radius=10)
    
    if not hidden:
        color = (0, 0, 0)
        if suit == "diamond":
            color = (203, 56, 74)
            drawDiamond(x, y)
        elif suit == "heart":
            color = (203, 65, 74)
            drawHeart(x, y)
        elif suit == "club":
            color = (27, 42, 57)
            drawClub(x, y)
        elif suit == "spade":
            color = (27, 42, 57)
            drawSpade(x, y)
        
        text = rankFont.render(str(rank), True, color)
        text_rect = text.get_rect()
        text_rect.centerx = x + 40  
        text_rect.bottom = y + 55
        screen.blit(text, text_rect.topleft)
    else:
        # Draw card back pattern
        back_color = (50, 50, 150)
        pygame.draw.rect(screen, back_color, (x, y, 2.5 * 50, 3.5 * 50), border_radius=10)
        # Add some pattern to the back
        pygame.draw.rect(screen, (70, 70, 170), (x+5, y+5, 2.5*50-10, 3.5*50-10), border_radius=5)

# Initialize game
rank = ["A", 2, 3, 4, 5, 6, 7, 8, 9, 10, "J", "Q", "K"]
suit = ["diamond", "heart", "club", "spade"]

dealer = Card(rank[random.randint(0, 12)], suit[random.randint(0, 3)])
dealerHide = Card(rank[random.randint(0, 12)], suit[random.randint(0, 3)])

# Main game loop
while running: 
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                running = False
    
    screen.fill(background_colour)
    
    # Draw dealer cards with obvious shadows
    draw_card_with_shadow(dealer.getRank(), dealer.getSuit(), width//2-125, 230)
    draw_card_with_shadow(None, None, width//2, 270, hidden=True)
    
    # Add some text labels
    font = pygame.font.SysFont(None, 36)
    dealer_text = font.render("Dealer's Cards", True, (255, 255, 255))
    screen.blit(dealer_text, (width//2 - dealer_text.get_width()//2, 180))
    
    pygame.display.flip()

pygame.quit()