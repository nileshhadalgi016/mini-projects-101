import pygame
import random

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 800, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hangman Game")

# ASCII art for hangman stages
hangman_pics = [
    """
       +---+
       |   |
           |
           |
           |
           |
    =========
    """,
    """
       +---+
       |   |
       O   |
           |
           |
           |
    =========
    """,
    """
       +---+
       |   |
       O   |
       |   |
           |
           |
    =========
    """,
    """
       +---+
       |   |
       O   |
      /|   |
           |
           |
    =========
    """,
    """
       +---+
       |   |
       O   |
      /|\\  |
           |
           |
    =========
    """,
    """
       +---+
       |   |
       O   |
      /|\\  |
      /    |
           |
    =========
    """,
    """
       +---+
       |   |
       O   |
      /|\\  |
      / \\  |
           |
    =========
    """
]

# Game variables
hangman_status = 0
words = ["PYTHON", "DEVELOPER", "HANGMAN", "PYGAME", "PROGRAMMING"]
word = random.choice(words)
guessed = []

# Fonts
LETTER_FONT = pygame.font.SysFont('comicsans', 20)
WORD_FONT = pygame.font.SysFont('comicsans', 40)
TITLE_FONT = pygame.font.SysFont('comicsans', 60)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Setup game loop
FPS = 60
clock = pygame.time.Clock()
run = True

def draw():
    win.fill(WHITE)
    
    # Draw title
    text = TITLE_FONT.render("HANGMAN GAME", 1, BLACK)
    win.blit(text, (WIDTH/2 - text.get_width()/2, 20))
    
    # Draw word
    display_word = ""
    for letter in word:
        if letter in guessed:
            display_word += letter + " "
        else:
            display_word += "_ "
    text = WORD_FONT.render(display_word, 1, BLACK)
    win.blit(text, (400, 200))
    
    # Draw hangman ASCII art
    hangman_text = hangman_pics[hangman_status]
    y_offset = 300
    for line in hangman_text.split('\n'):
        text = LETTER_FONT.render(line, 1, BLACK)
        win.blit(text, (150, y_offset))
        y_offset += 20
    
    pygame.display.update()

while run:
    clock.tick(FPS)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.unicode.isalpha():
                letter = event.unicode.upper()
                if letter not in guessed:
                    guessed.append(letter)
                    if letter not in word:
                        hangman_status += 1

    draw()

    won = True
    for letter in word:
        if letter not in guessed:
            won = False
            break

    if won:
        print("You WON!")
        break

    if hangman_status == 6:
        print("You LOST!")
        break

pygame.quit()
