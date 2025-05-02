import pygame

pygame.init()
screen = pygame.display.set_mode((400, 300))
pygame.display.set_caption("Opacity Overlap Example")

# Font for demonstration
font = pygame.font.SysFont(None, 48)
text = font.render("Underneath!", True, (0, 0, 255))  # Blue text

# Create a transparent black square
square_surface = pygame.Surface((100, 100), pygame.SRCALPHA)
square_surface.fill((0, 0, 0, 179))  # 70% opacity

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255))  # White background

    # Draw the text first (it will be "under" the square)
    screen.blit(text, (160, 120))

    # Draw the semi-transparent black square on top of the text
    screen.blit(square_surface, (150, 100))

    pygame.display.flip()

pygame.quit()
