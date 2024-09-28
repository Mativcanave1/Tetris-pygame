import pygame
import random

# Options
WIDTH, HEIGHT = 300, 600
BLOCK_SIZE = 30
ROWS = HEIGHT // BLOCK_SIZE
COLS = WIDTH // BLOCK_SIZE
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
COLORS = [
    (0, 255, 255),  
    (255, 165, 0),  
    (0, 0, 255),    
    (255, 255, 0),  
    (128, 0, 128), 
    (0, 255, 0),    
    (255, 0, 0),    
]

# Figures
SHAPES = [
    [[1, 1, 1, 1]],  
    [[1, 1], [1, 1]],  
    [[0, 1, 0], [1, 1, 1]],  
    [[1, 1, 0], [0, 1, 1]],  
    [[0, 1, 1], [1, 1, 0]],  
    [[1, 0, 0], [1, 1, 1]],  
    [[0, 0, 1], [1, 1, 1]],  
]

class Tetris:
    def __init__(self):
        self.grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]
        self.current_piece = list(self.new_piece())
        self.next_piece = list(self.new_piece())
        self.position = (COLS // 2 - 1, 0)
        self.score = 0
        self.fall_time = 0

    def new_piece(self):
        shape = random.choice(SHAPES)
        color = random.choice(COLORS)
        return shape, color
    
    def horizontal_flip(self):
        self.current_piece[0] = [row[::-1] for row in self.current_piece[0]]

    def vertical_flip(self):
        self.current_piece[0] = self.current_piece[0][::-1]

    def rotate(self):
        self.current_piece[0] = [list(row) for row in zip(*self.current_piece[0][::-1])]

    def valid_move(self, shape, offset):
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    new_x = x + offset[0]
                    new_y = y + offset[1]
                    if new_x < 0 or new_x >= COLS or new_y >= ROWS or self.grid[new_y][new_x]:
                        return False
        return True

    def merge(self):
        shape, color = self.current_piece
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    self.grid[y + self.position[1]][x + self.position[0]] = color

    def clear_lines(self):
        new_grid = [row for row in self.grid if any(cell == 0 for cell in row)]
        cleared_lines = ROWS - len(new_grid)
        self.score += cleared_lines
        new_grid = [[0 for _ in range(COLS)] for _ in range(cleared_lines)] + new_grid
        self.grid = new_grid

    def drop(self):
        if self.valid_move(self.current_piece[0], (self.position[0], self.position[1] + 1)):
            self.position = (self.position[0], self.position[1] + 1)
        else:
            self.merge()
            self.clear_lines()
            self.current_piece = list(self.next_piece)
            self.next_piece = list(self.new_piece())
            self.position = (COLS // 2 - 1, 0)
            if not self.valid_move(self.current_piece[0], self.position):  
                return True
        return False

    def tick(self):
        self.fall_time += 1
        if self.fall_time >= FPS // 2:
            if self.drop():
                return True
            self.fall_time = 0
        return False

def draw_text(surface, text, size, color, pos):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    rect = text_surface.get_rect(center=pos)
    surface.blit(text_surface, rect)

def show_menu(screen):
    screen.fill(BLACK)
    draw_text(screen, "TETRIS", 48, WHITE, (WIDTH // 2, HEIGHT // 4))
    draw_text(screen, "Press ENTER to play", 24, WHITE, (WIDTH // 2, HEIGHT // 2))
    draw_text(screen, "Controls:", 24, WHITE, (WIDTH // 2, HEIGHT // 2 + 40))
    draw_text(screen, "Left key: Move left", 20, WHITE, (WIDTH // 2, HEIGHT // 2 + 70))
    draw_text(screen, "Right key: Move right", 20, WHITE, (WIDTH // 2, HEIGHT // 2 + 100))
    draw_text(screen, "Down key: Move faster", 20, WHITE, (WIDTH // 2, HEIGHT // 2 + 130))
    draw_text(screen, "Up key: Rotate", 20, WHITE, (WIDTH // 2, HEIGHT // 2 + 160))
    draw_text(screen, "H: Horizontal inversion", 20, WHITE, (WIDTH // 2, HEIGHT // 2 + 190))
    draw_text(screen, "G: Vertical inversion", 20, WHITE, (WIDTH // 2, HEIGHT // 2 + 220))
    pygame.display.flip()

def show_game_over(screen):
    screen.fill(BLACK)
    draw_text(screen, "Game Over!", 48, WHITE, (WIDTH // 2, HEIGHT // 4))
    draw_text(screen, "Press, Enter to play again", 24, WHITE, (WIDTH // 2, HEIGHT // 2))
    draw_text(screen, "Press ESC to exit", 24, WHITE, (WIDTH // 2, HEIGHT // 2 + 40))
    pygame.display.flip()

# Init
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tetris")
clock = pygame.time.Clock()

def main():
    game_started = False
    game_over = False
    game = None  

    while True:
        if not game_started:
            show_menu(screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN: 
                        game_started = True
                        game_over = False
                        game = Tetris()
        elif game_over:
            show_game_over(screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:  
                        game_started = True
                        game = Tetris()  
                        game_over = False
                    if event.key == pygame.K_ESCAPE:  
                        pygame.quit()
                        return
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        if game.valid_move(game.current_piece[0], (game.position[0] - 1, game.position[1])):
                            game.position = (game.position[0] - 1, game.position[1])
                    if event.key == pygame.K_RIGHT:
                        if game.valid_move(game.current_piece[0], (game.position[0] + 1, game.position[1])):
                            game.position = (game.position[0] + 1, game.position[1])
                    if event.key == pygame.K_DOWN:
                        game.drop()
                    if event.key == pygame.K_UP:
                        game.rotate()
                        if not game.valid_move(game.current_piece[0], game.position):
                            game.rotate()
                            game.rotate()
                            game.rotate()
                    if event.key == pygame.K_h:  
                        game.horizontal_flip()

                    if event.key == pygame.K_g:  
                        game.vertical_flip()

            screen.fill(BLACK)
            # Grid
            for y in range(ROWS):
                for x in range(COLS):
                    color = game.grid[y][x]
                    if color:
                        pygame.draw.rect(screen, color, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

            # Figure draw
            shape, color = game.current_piece
            for y, row in enumerate(shape):
                for x, cell in enumerate(row):
                    if cell:
                        pygame.draw.rect(screen, color, ((x + game.position[0]) * BLOCK_SIZE, (y + game.position[1]) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

            draw_text(screen, f"Счёт: {game.score}", 24, WHITE, (WIDTH // 2, 20))

            if game.tick():  # Game over test
                game_over = True

            pygame.display.flip()
            clock.tick(FPS)

if __name__ == "__main__":
    main()
