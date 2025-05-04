import pygame
pygame.init()

screen = pygame.display.set_mode((400, 300))
pygame.display.set_caption("Ellipse Example")

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255))

    # Draw an ellipse (filled)
    pygame.draw.ellipse(screen, (0, 0, 255), (100, 50, 200, 100))

    pygame.display.flip()

pygame.quit()
