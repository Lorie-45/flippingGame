import pygame
import random
import sys
from utils.game_utils import shuffle_cards, check_match
# Initialize Pygame
pygame.init()
# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Memory Card Game")
# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
# Font settings
FONT_SIZE = 64
font = pygame.font.SysFont("Arial", FONT_SIZE)
# Emoji settings
EMOJIS = [":grinning:", ":sunglasses:", ":robot_face:", ":jack_o_lantern:", ":dog:", ":cat:", ":apple:", ":pizza:"]  # 8 unique emojis (4 pairs)
CARD_WIDTH, CARD_HEIGHT = 100, 150
CARD_GAP = 20
ROWS, COLS = 4, 4  # 4x4 grid for 16 cards (8 pairs)
# Create a list of cards
cards = EMOJIS * 2  # Create pairs of emojis
shuffle_cards(cards)  # Shuffle the cards
# Game variables
flipped_cards = []
matched_cards = []
game_over = False
# Game loop
clock = pygame.time.Clock()
running = True
while running:
    screen.fill(WHITE)
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            x, y = pygame.mouse.get_pos()
            for i, card in enumerate(cards):
                card_rect = pygame.Rect(
                    (i % COLS) * (CARD_WIDTH + CARD_GAP) + 50,
                    (i // COLS) * (CARD_HEIGHT + CARD_GAP) + 50,
                    CARD_WIDTH,
                    CARD_HEIGHT,
                )
                if card_rect.collidepoint(x, y) and i not in matched_cards:
                    flipped_cards.append(i)
                    if len(flipped_cards) == 2:
                        if check_match(cards, flipped_cards):
                            matched_cards.extend(flipped_cards)
                        flipped_cards = []
    # Draw cards
    for i, card in enumerate(cards):
        card_rect = pygame.Rect(
            (i % COLS) * (CARD_WIDTH + CARD_GAP) + 50,
            (i // COLS) * (CARD_HEIGHT + CARD_GAP) + 50,
            CARD_WIDTH,
            CARD_HEIGHT,
        )
        if i in matched_cards or i in flipped_cards:
            # Render the emoji
            text = font.render(card, True, BLACK)
            text_rect = text.get_rect(center=card_rect.center)
            screen.blit(text, text_rect)
        else:
            # Draw a blank card (rectangle)
            pygame.draw.rect(screen, BLACK, card_rect, 2)
    # Check for game over
    if len(matched_cards) == len(cards):
        game_over = True
        font_large = pygame.font.SysFont("Arial", 72)
        text = font_large.render("You Win!", True, BLACK)
        screen.blit(text, (WIDTH // 2 - 120, HEIGHT // 2 - 40))
    # Update the display
    pygame.display.flip()
    clock.tick(60)
# Quit Pygame
pygame.quit()
sys.exit()