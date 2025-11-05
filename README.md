# MTG Card Scanner

Scanner de cartas Magic: The Gathering usando visão computacional e Scryfall API.

## Estrutura

mtg-scanner/
├── backend/ # API Flask
├── frontend/ # Interface web
├── docs/ # Documentação
└── scripts/ # Scripts de auxílio

## Instalação

1. Clone o repositório
2. Execute `scripts/setup-venv.sh` (Linux/Mac) ou `scripts\setup-venv.bat` (Windows)
3. Siga as instruções em `docs/INSTALL.md`

## Uso

1. Inicie o backend: `python backend/run.py`
2. Abra `frontend/Front_End_Scanner.html` no navegador
3. Selecione uma imagem de cartas MTG e clique em "Listar Cards"
