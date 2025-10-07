# 🎮 Sudoku Game - Projeto Final de Teste de Software

Um jogo de Sudoku desenvolvido em Python com Pygame, seguindo princípios de Clean Code e SOLID, com suite completa de testes.

## 📋 Pré-requisitos

- Python 3.8+
- pip (gerenciador de pacotes Python)

## 🚀 Instalação

```bash
# Clone o repositório
git clone <seu-repositorio>
cd Projeto_Final-Teste_Software

# Crie um ambiente virtual (opcional mas recomendado)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Instale as dependências
pip install -r requirements.txt
```

## 🧪 Execução dos Testes

```bash
# Executar todos os testes
pytest

# Executar com detalhes
pytest -v

# Executar testes específicos
pytest test_game_logic.py -v
pytest test_game.py -v

# Executar testes rápidos (exclui testes lentos)
pytest -m "not slow"

# Executar com relatório de cobertura
pytest --cov=game_logic --cov=game --cov-report=html

# Executar testes e gerar relatório XML (para CI/CD)
pytest --junitxml=test-results.xml
```

## 🎮 Executar o Jogo

```bash
# Executar diretamente com Python
python game.py
```

## 📦 Gerar Executável

### Para Linux

```bash
pyinstaller --onefile --console --name SudokuGame --add-data "game_logic.py:." --hidden-import numpy --hidden-import pygame game.py
```

### Para Windows

```bash
pyinstaller --onefile --console --name SudokuGame --add-data "game_logic.py;." --hidden-import numpy --hidden-import pygame game.py
```

### Para Release (sem console)

```bash
# Linux
pyinstaller --onefile --name SudokuGame --add-data "game_logic.py:." --hidden-import numpy --hidden-import pygame game.py

# Windows  
pyinstaller --onefile --windowed --name SudokuGame --add-data "game_logic.py;." --hidden-import numpy --hidden-import pygame game.py
```

## 🎯 Controles do Jogo

- **Mouse**: Clique para selecionar células
- **Botão Esquerdo**: Modo de inserção normal
- **Botão Direito**: Modo de sugestão (números em cinza)
- **Teclas 1-9**: Inserir números
- **Tecla H**: Usar dica (máximo 3 por jogo)
- **Tecla R**: Reiniciar jogo
- **Tecla ESC**: Sair do jogo

## 📊 Funcionalidades

- ✅ Geração aleatória de puzzles Sudoku
- ✅ Sistema de dicas limitadas
- ✅ Contador de erros (máximo 5)
- ✅ Modo de sugestões
- ✅ Detecção automática de vitória/derrota
- ✅ Interface colorida com feedback visual
- ✅ Números originais (pretos) vs. inseridos (azul/vermelho)

## 🧩 Estrutura do Projeto

```
Projeto_Final-Teste_Software/
├── game.py              # Interface gráfica e controle do jogo
├── game_logic.py        # Lógica do Sudoku (geração e validação)
├── test_game.py         # Testes da interface
├── test_game_logic.py   # Testes da lógica
├── requirements.txt     # Dependências do projeto
└── README.md           # Este arquivo
```

## 🔧 Desenvolvimento

### Padrões Utilizados

- **SOLID Principles**
- **Clean Code**
- **Test-Driven Development (TDD)**
- **Behavior-Driven Development (BDD)** com Gherkin

### Suite de Testes

- **29 testes** cobrindo funcionalidades principais
- **Mocking** de dependências externas
- **Testes de integração** entre módulos
- **Cobertura** de código verificável

## 📈 Relatórios

Após executar os testes com cobertura, abra:

```bash
# Gerar relatório HTML
pytest --cov=game_logic --cov=game --cov-report=html

# Abrir relatório no navegador
open htmlcov/index.html  # Linux/Mac
start htmlcov/index.html  # Windows
```

## 🐛 Solução de Problemas

### Erros Comuns

**Problema**: PyInstaller não encontrado

```bash
pip install pyinstaller
```

**Problema**: Módulos não encontrados no build

```bash
# Adicione explicitamente os hidden imports
pyinstaller ... --hidden-import numpy --hidden-import pygame
```

**Problema**: Executável muito grande

```bash
# Use UPX para compactação
pip install upx
pyinstaller ... --upx-dir $(which upx)
```

## 📝 Licença

Este projeto foi desenvolvido para a disciplina de Teste de Software da UFPB.

## 👥 Desenvolvido por

[José] - Aluno de CDIA
[Matheus] - Aluno de CDIA
