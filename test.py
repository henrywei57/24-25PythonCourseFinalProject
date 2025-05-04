import pygame
import sys

pygame.init()
screen = pygame.display.set_mode((600, 400))
font = pygame.font.SysFont(None, 40)

# Define button
button_rect = pygame.Rect(250, 150, 100, 50)

# Main loop
running = True
while running:
    screen.fill((0, 0, 0))  # Clear screen

    # Draw button
    pygame.draw.rect(screen, (0, 128, 255), button_rect)
    text = font.render("Click", True, (255, 255, 255))
    screen.blit(text, text.get_rect(center=button_rect.center))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if button_rect.collidepoint(event.pos):
                print("Button clicked!")

    pygame.display.flip()

pygame.quit()
sys.exit()
