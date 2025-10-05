from game_logic import SudokuGame
import sys
import pygame
import random
import numpy as np

class SudokuUI:
    def __init__(self, game, width=540, height=630):
        pygame.init()
        self.game = game
        self.width = width
        self.height = height
        self.cell_size = width // 9
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Sudoku")
        self.font = pygame.font.SysFont("Arial", 32)
        self.small_font = pygame.font.SysFont("Arial", 18)
        self.selected = None
        self.suggestion_mode = False
        self.errors = 0
        self.max_errors = 5
        self.hints_used = 0
        self.max_hints = 3
        self.running = True
        self.game_over = False
        self.victory = False
        self.player_grid = self.game.change.copy()
        self.suggestions = np.zeros((9, 9), dtype=int)
        self.hint_cells = set()  # armazenar posições reveladas

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
        if self.selected:
            row, col = self.selected
            pygame.draw.rect(
                self.screen, (0, 0, 200),
                (col * self.cell_size, row * self.cell_size, self.cell_size, self.cell_size),
                3
            )
        if self.suggestion_mode and self.selected:
            row, col = self.selected
            pygame.draw.rect(
                self.screen, (128, 128, 128),
                (col * self.cell_size, row * self.cell_size, self.cell_size, self.cell_size),
                3
            )

    def draw_numbers(self):
        for i in range(9):
            for j in range(9):
                x = j * self.cell_size + 20
                y = i * self.cell_size + 10
                num = self.player_grid[i][j]

                # Sugestão (em cinza)
                if self.suggestions[i][j] != 0 and num == 0:
                    text = self.small_font.render(str(self.suggestions[i][j]), True, (128, 128, 128))
                    self.screen.blit(text, (x, y))
                    continue

                # Número revelado por dica (verde)
                if (i, j) in self.hint_cells:
                    correct_num = self.game.original[i][j]
                    text = self.font.render(str(correct_num), True, (0, 180, 0))
                    self.screen.blit(text, (x, y))
                    continue

                # Número normal (preto, azul ou vermelho)
                if num != 0:
                    if self.game.change[i][j] != 0:
                        color = (0, 0, 0)  # número original
                    else:
                        color = (0, 0, 255) if num == self.game.original[i][j] else (255, 0, 0)
                    text = self.font.render(str(num), True, color)
                    self.screen.blit(text, (x, y))

    def draw_victory(self):
        overlay = pygame.Surface((self.width, self.height))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        text = self.font.render("VOCÊ VENCEU!", True, (0, 255, 0))
        text2 = pygame.font.Font(None, 40).render("Pressione R para reiniciar", True, (255, 255, 255))
        self.screen.blit(text, (180, 250))
        self.screen.blit(text2, (140, 300))
        self.victory = True
        pygame.display.flip()

    def draw_game_over(self):
        overlay = pygame.Surface((self.width, self.height))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        text = self.font.render("GAME OVER!", True, (255, 0, 0))
        text2 = pygame.font.Font(None, 40).render("Pressione R para reiniciar", True, (255, 255, 255))
        self.screen.blit(text, (180, 250))
        self.screen.blit(text2, (140, 300))
        self.game_over = True
        pygame.display.flip()

    def reset_game(self, n_remove=3):
        """
        Reinicia o jogo: gera novo Sudoku, reseta todos os estados do UI.
        """
        # recria/gera um novo puzzle
        self.game = SudokuGame()
        self.game.generate(n_remove=n_remove)

        # reseta estados do UI
        self.player_grid = self.game.change.copy()
        self.suggestions.fill(0)
        self.selected = None
        self.suggestion_mode = False
        self.errors = 0
        self.hints_used = 0
        self.hint_cells.clear()
        self.running = True

    def handle_click(self, pos, button):
        if not self.running:
            return
        x, y = pos
        row, col = y // self.cell_size, x // self.cell_size
        if row < 9 and col < 9 and self.game.change[row][col] == 0:
            self.selected = (row, col)
            self.suggestion_mode = (button == 3)  # botão direito ativa modo sugestão

    def handle_key(self, key):

        # permitir sempre reiniciar com 'R', mesmo após game over / vitória
        if key == pygame.K_r:
            self.reset_game(n_remove=3)
            return
        
        elif key == pygame.K_h:  # tecla H para pedir ajuda
            if self.hints_used < self.max_hints:
                empty_positions = [(i, j) for i in range(9) for j in range(9)
                                if self.player_grid[i][j] == 0 and (i, j) not in self.hint_cells]
                if empty_positions:
                    pos = random.choice(empty_positions)
                    i, j = pos
                    correct_num = self.game.original[i][j]

                    # preenche automaticamente o número correto
                    self.player_grid[i][j] = correct_num
                    self.hint_cells.add(pos)
                    self.hints_used += 1

                    # verifica vitória automaticamente
                    if np.array_equal(self.player_grid, self.game.original):
                        self.draw_victory()
                        pygame.display.flip()
                        pygame.time.wait(2000)
                        self.running = False
                        

        # if not self.running or self.selected is None:
        if not self.running or self.selected is None:
            return
        
        row, col = self.selected

        # Impede alterações em números originais, corretos ou revelados por dica
        if self.game.change[row][col] != 0:
            return  # número original do puzzle
        if (row, col) in self.hint_cells:
            return  # célula com dica revelada
        if self.player_grid[row][col] == self.game.original[row][col]:
            return  # número já correto
        
        if pygame.K_1 <= key <= pygame.K_9:
            num = key - pygame.K_0
            if self.suggestion_mode:
                # adiciona ou remove sugestão
                self.suggestions[row][col] = num if self.suggestions[row][col] != num else 0
            else:
                self.player_grid[row][col] = num
                self.suggestions[row][col] = 0  # remove sugestão anterior
                if num != self.game.original[row][col]:
                    self.errors += 1
                    if self.errors >= self.max_errors:
                        self.running = False
                else:
                    if np.array_equal(self.player_grid, self.game.original):
                        self.draw_victory()
                        pygame.display.flip()
                        pygame.time.wait(2500)
                        self.running = False
        

    def draw_hud(self):
        text = self.font.render(f"Erros: {self.errors}/{self.max_errors}", True, (200, 0, 0))
        hints = self.font.render(f"Ajudas: {self.hints_used}/{self.max_hints}", True, (0, 150, 0))
        restart = self.font.render("Pressione 'R' para reiniciar", True, (0, 0, 0))
        self.screen.blit(text, (10, self.width + 10))
        self.screen.blit(hints, (220, self.width + 10))
        self.screen.blit(restart, (10, self.width + 45))

    def run(self):
        clock = pygame.time.Clock()
        while True:
            self.screen.fill((255, 255, 255))
            self.draw_grid()
            self.draw_numbers()
            self.draw_hud()

            if not self.running and self.errors >= self.max_errors:
                self.draw_game_over()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(event.pos, event.button)
                elif event.type == pygame.KEYDOWN:
                    self.handle_key(event.key)

            pygame.display.flip()
            clock.tick(30)


# ---------- main ----------
if __name__ == "__main__":
    game = SudokuGame()
    game.generate(n_remove=3)
    ui = SudokuUI(game)
    ui.run()
