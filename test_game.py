# test_game.py
import pytest
import pygame
import numpy as np
from unittest.mock import Mock, patch
from game import SudokuUI
from game_logic import SudokuGame

class TestSudokuUI:
    @pytest.fixture
    def mock_game(self):
        """Fixture para criar um mock do SudokuGame"""
        game = Mock(spec=SudokuGame)
        game.original = np.array([
            [5, 3, 4, 6, 7, 8, 9, 1, 2],
            [6, 7, 2, 1, 9, 5, 3, 4, 8],
            [1, 9, 8, 3, 4, 2, 5, 6, 7],
            [8, 5, 9, 7, 6, 1, 4, 2, 3],
            [4, 2, 6, 8, 5, 3, 7, 9, 1],
            [7, 1, 3, 9, 2, 4, 8, 5, 6],
            [9, 6, 1, 5, 3, 7, 2, 8, 4],
            [2, 8, 7, 4, 1, 9, 6, 3, 5],
            [3, 4, 5, 2, 8, 6, 1, 7, 9]
        ])
        game.change = game.original.copy()
        # Remove algumas células para simular puzzle
        game.change[0][0] = 0
        game.change[0][1] = 0
        return game

    @pytest.fixture
    def ui(self, mock_game):
        """Fixture para criar instância do SudokuUI"""
        with patch('pygame.init'), \
             patch('pygame.display.set_mode'), \
             patch('pygame.display.set_caption'):
            ui = SudokuUI(mock_game)
            return ui

    def test_init(self, ui, mock_game):
        """Testa inicialização do SudokuUI"""
        assert ui.game == mock_game
        assert ui.width == 540
        assert ui.height == 630
        assert ui.cell_size == 60
        assert ui.selected is None
        assert ui.suggestion_mode == False
        assert ui.errors == 0
        assert ui.max_errors == 5
        assert ui.hints_used == 0
        assert ui.max_hints == 3
        assert ui.running == True
        assert ui.game_over == False
        assert ui.victory == False
        assert np.array_equal(ui.player_grid, mock_game.change)
        assert ui.suggestions.shape == (9, 9)
        assert len(ui.hint_cells) == 0

    def test_handle_click_valid_cell(self, ui):
        """Testa clique em célula vazia válida"""
        ui.handle_click((30, 30), 1)  # Botão esquerdo
        assert ui.selected == (0, 0)
        assert ui.suggestion_mode == False

    def test_handle_click_suggestion_mode(self, ui):
        """Testa clique com botão direito para modo sugestão"""
        ui.handle_click((30, 30), 3)  # Botão direito
        assert ui.selected == (0, 0)
        assert ui.suggestion_mode == True

    def test_handle_click_original_cell(self, ui, mock_game):
        """Testa clique em célula original (não deve selecionar)"""
        mock_game.change[0][2] = 4  # Célula original preenchida
        ui.handle_click((150, 30), 1)
        assert ui.selected != (0, 2)

    def test_handle_key_number_correct(self, ui):
        """Testa inserção de número correto"""
        ui.selected = (0, 0)
        ui.handle_key(pygame.K_5)  # Número correto para (0,0)
        
        assert ui.player_grid[0][0] == 5
        assert ui.errors == 0

    def test_handle_key_number_incorrect(self, ui):
        """Testa inserção de número incorreto"""
        ui.selected = (0, 0)
        ui.handle_key(pygame.K_1)  # Número incorreto para (0,0)
        
        assert ui.player_grid[0][0] == 1
        assert ui.errors == 1

    def test_handle_key_suggestion_mode(self, ui):
        """Testa inserção de sugestão"""
        ui.selected = (0, 0)
        ui.suggestion_mode = True
        ui.handle_key(pygame.K_5)
        
        assert ui.suggestions[0][0] == 5
        assert ui.player_grid[0][0] == 0  # Grid principal não alterado

    def test_handle_key_hint_available(self, ui, mock_game):
        """Testa uso de dica quando disponível"""
        with patch('random.choice') as mock_choice:
            mock_choice.return_value = (0, 0)
            ui.handle_key(pygame.K_h)
            
            assert ui.hints_used == 1
            assert ui.player_grid[0][0] == mock_game.original[0][0]
            assert (0, 0) in ui.hint_cells

    def test_handle_key_hint_unavailable(self, ui):
        """Testa uso de dica quando esgotada"""
        ui.hints_used = 3
        ui.handle_key(pygame.K_h)
        
        assert ui.hints_used == 3  # Não deve aumentar

    def test_handle_key_restart(self, ui, mock_game):
        """Testa reinício do jogo"""
        ui.errors = 3
        ui.hints_used = 2
        ui.selected = (1, 1)
        
        with patch.object(mock_game, 'generate') as mock_generate:
            ui.handle_key(pygame.K_r)
            
            mock_generate.assert_called_once()
            assert ui.errors == 0
            assert ui.hints_used == 0
            assert ui.selected is None
            assert ui.running == True

    def test_handle_key_no_selection(self, ui):
        """Testa pressionar tecla sem célula selecionada"""
        ui.selected = None
        ui.handle_key(pygame.K_5)
        
        # Não deve causar erro ou alterar estado

    def test_handle_key_original_cell(self, ui, mock_game):
        """Testa tentativa de alterar célula original"""
        mock_game.change[0][2] = 4  # Célula original
        ui.selected = (0, 2)
        ui.handle_key(pygame.K_1)
        
        assert ui.player_grid[0][2] == 4  # Não deve alterar

    def test_handle_key_hint_cell(self, ui):
        """Testa tentativa de alterar célula com dica"""
        ui.hint_cells.add((0, 0))
        ui.selected = (0, 0)
        ui.handle_key(pygame.K_1)
        
        assert ui.player_grid[0][0] == 0  # Não deve alterar

    def test_handle_key_correct_cell(self, ui):
        """Testa tentativa de alterar célula já correta"""
        ui.player_grid[0][0] = 5  # Número correto
        ui.selected = (0, 0)
        ui.handle_key(pygame.K_1)
        
        assert ui.player_grid[0][0] == 5  # Não deve alterar

    def test_game_over_on_max_errors(self, ui):
        """Testa game over ao atingir máximo de erros"""
        ui.selected = (0, 0)
        ui.errors = 4
        
        ui.handle_key(pygame.K_1)  # Erro que atinge máximo
        
        assert ui.errors == 5
        assert ui.running == False

    def test_victory_on_completion(self, ui, mock_game):
        """Testa vitória ao completar o puzzle"""
        ui.player_grid = mock_game.original.copy()
        ui.player_grid[0][0] = 0  # Última célula vazia
        ui.selected = (0, 0)
        
        with patch.object(ui, 'draw_victory') as mock_draw:
            ui.handle_key(pygame.K_5)  # Último número correto
            
            mock_draw.assert_called_once()
            assert ui.running == False

    def test_reset_game(self, ui, mock_game):
        """Testa reset completo do jogo"""
        ui.errors = 3
        ui.hints_used = 2
        ui.selected = (1, 1)
        ui.suggestion_mode = True
        ui.running = False
        ui.victory = True
        ui.game_over = True
        ui.player_grid[0][0] = 1
        ui.suggestions[0][0] = 2
        ui.hint_cells.add((0, 0))
        
        with patch.object(mock_game, 'generate') as mock_generate:
            ui.reset_game()
            
            mock_generate.assert_called_once()
            assert ui.errors == 0
            assert ui.hints_used == 0
            assert ui.selected is None
            assert ui.suggestion_mode == False
            assert ui.running == True
            assert ui.victory == False
            assert ui.game_over == False
            assert np.array_equal(ui.player_grid, mock_game.change)
            assert np.all(ui.suggestions == 0)
            assert len(ui.hint_cells) == 0

# Testes de integração
class TestIntegration:
    def test_complete_game_flow(self):
        """Testa fluxo completo do jogo"""
        with patch('pygame.init'), \
             patch('pygame.display.set_mode'), \
             patch('pygame.display.set_caption'):
            
            game = SudokuGame(n_remove=5)
            game.generate()
            ui = SudokuUI(game)
            
            # Verifica estado inicial
            assert ui.running == True
            assert ui.errors == 0
            
            # Simula algumas jogadas
            empty_cells = [(i, j) for i in range(9) for j in range(9) 
                          if game.change[i][j] == 0]
            if empty_cells:
                row, col = empty_cells[0]
                ui.selected = (row, col)
                correct_num = game.original[row][col]
                
                # Testa número correto
                key = pygame.K_0 + correct_num
                ui.handle_key(key)
                assert ui.player_grid[row][col] == correct_num
                assert ui.errors == 0