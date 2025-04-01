# Estrutura do Projeto Bot Marketplace

Este projeto foi desenvolvido para gerenciar processos em diferentes marketplaces, como coleta, tratamento, cancelamento e exportação de dados.

## Estrutura de Diretórios e Arquivos

```
bot_marketplace/
├── app/
│   ├── main.py                # Arquivo principal que executa o bot
│   ├── handles.py             # Contém as funções para manipulação de processos
│   ├── factorys.py            # Fábricas para criação de instâncias de marketplace e banco de dados
│   ├── settings.py            # Configurações globais do projeto
│   ├── constants.py           # Constantes utilizadas no projeto
│   └── validators/
│       ├── __init__.py        # Inicializador do módulo de validação
│       └── process_entry.py   # Validação de processos e marketplaces
├── tests/
│   ├── __init__.py            # Inicializador do módulo de testes
│   └── test_main.py           # Testes unitários para o arquivo main.py
├── requirements.txt           # Lista de dependências do projeto
└── README.md                  # Documentação do projeto
```

## Descrição dos Diretórios e Arquivos

- **app/**: Contém a lógica principal do bot, incluindo manipulação de processos, validações e configurações.
  - **main.py**: Arquivo principal que executa o bot.
  - **handles.py**: Contém as funções responsáveis por manipular os processos, como `get`, `treat`, `cancel` e `to_spreadsheet`.
  - **factorys.py**: Fábricas para criar instâncias de marketplaces e bancos de dados.
  - **settings.py**: Configurações globais, como variáveis de ambiente e flags de teste.
  - **constants.py**: Constantes utilizadas em todo o projeto.
  - **validators/**: Diretório com a lógica de validação.
    - **process_entry.py**: Valida os processos e marketplaces recebidos como entrada.

- **tests/**: Contém os testes unitários do projeto.
  - **test_main.py**: Testes para as funcionalidades do arquivo `main.py`.

- **requirements.txt**: Lista de dependências necessárias para rodar o projeto.

- **README.md**: Documentação do projeto.