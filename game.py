from game_logic import SudokuGame
import sys
import pygame 

class SudokuUI:
    def __init__(self, game = SudokuGame, width=540, height=600):
        pygame.init()
        self.game = game
        self.width = width
        self.height = height
        self.cell_size = width // 9
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Sudoku")
        self.font = pygame.font.SysFont("Arial", 32)
        self.big_font = pygame.font.SysFont("arial", 18)
        self.selected = None
        self.errors = 0
        self.max_errors = 5
        self.running = True

        # grade que o jogador vai preencher (cópia do puzzle com zeros)
        self.player_grid = self.game.change.copy()

    def draw_grid(self):
        for i in range(10):
            line_width = 3 if i % 3 == 0 else 1
            pygame.draw.line(
                self.screen, (0, 0, 0),
                (i * self.cell_size, 0),
                (i * self.cell_size, self.width),
                line_width
            )
            pygame.draw.line(
                self.screen, (0, 0, 0),
                (0, i * self.cell_size),
                (self.width, i * self.cell_size),
                line_width
            )

    def draw_numbers(self):
        for i in range(9):
            for j in range(9):
                num = self.player_grid[i][j]
                if num != 0:
                    # número original → preto
                    if self.game.change[i][j] != 0:
                        color = (0, 0, 0)
                    else:
                        # número digitado pelo jogador
                        if num == self.game.original[i][j]:
                            color = (0, 0, 255)  # correto → azul
                        else:
                            color = (255, 0, 0)  # errado → vermelho
                    text = self.font.render(str(num), True, color)
                    self.screen.blit(
                        text,
                        (j * self.cell_size + 20, i * self.cell_size + 10)
                    )

    def draw_victory(self):
        overlay = pygame.Surface((self.width, self.height))
        overlay.set_alpha(200)
        overlay.fill((255, 255, 255))
        self.screen.blit(overlay, (0, 0))
        msg = self.big_font.render("VOCÊ VENCEU!", True, (0, 150, 0))
        rect = msg.get_rect(center=(self.width // 2, self.height // 2))
        self.screen.blit(msg, rect)

    def draw_game_over(self):
        overlay = pygame.Surface((self.width, self.height))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        msg = self.big_font.render("SE FODEU", True, (255, 0, 0))
        rect = msg.get_rect(center=(self.width // 2, self.height // 2))
        self.screen.blit(msg, rect)

    def handle_click(self, pos):
        if not self.running:
            return
        x, y = pos
        row, col = y // self.cell_size, x // self.cell_size
        if row < 9 and col < 9 and self.game.change[row][col] == 0:
            self.selected = (row, col)

    def handle_key(self, key):
        if not self.running or self.selected is None:
            return
        row, col = self.selected
        if pygame.K_1 <= key <= pygame.K_9:
            num = key - pygame.K_0
            self.player_grid[row][col] = num
            if num != self.game.original[row][col]:
                self.errors += 1
                if self.errors >= self.max_errors:
                    self.running = False

    def draw_error_count(self):
        text = self.font.render(f"Erros: {self.errors}/{self.max_errors}", True, (200, 0, 0))
        self.screen.blit(text, (10, self.width + 10))

    def run(self):
        clock = pygame.time.Clock()
        while True:
            self.screen.fill((255, 255, 255))
            self.draw_grid()
            self.draw_numbers()
            self.draw_error_count()

            if not self.running:
                self.draw_game_over()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(event.pos)
                if event.type == pygame.KEYDOWN:
                    self.handle_key(event.key)

            pygame.display.flip()
            clock.tick(30)


# ---------- main ----------
if __name__ == "__main__":
    game = SudokuGame()
    game.generate(n_remove=30)
    ui = SudokuUI(game)
    ui.run()