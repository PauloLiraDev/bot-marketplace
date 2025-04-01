# Tutorial de Instalação e Execução do Bot Marketplace

Este tutorial explica como configurar o projeto **Bot Marketplace**, executar os processos disponíveis e utilizar os principais comandos de entrada. Este projeto foi projetado para ser executado localmente ou em uma arquitetura serverless, como a AWS Lambda, utilizando o dicionário `event` como entrada.

---

### Processos Disponíveis  

- **`get`** → Coleta os pedidos do marketplace.  
- **`treat`** → Processa e normaliza os pedidos coletados.  
- **`cancel`** → Cancela pedidos específicos.  
- **`to_spreadsheet`** → Exporta os dados processados para uma planilha.  

### Marketplaces Suportados  

Atualmente, o sistema suporta **shopee** e **shein**, cada um com sua própria implementação de extração e tratamento de dados. 

Exemplo: para coleta de pedidos Shopee, o event (input) precisa ser event{"process":"get", "marketplace":"shopee"}
Exemplo 2: para coleta de pedidos Shein, o event (input) precisa ser event{"process":"get", "marketplace":"shein"}
Exemplo 3: para tratamento de pedidos Shopee, o event (input) precisa ser event{"process":"treat", "marketplace":"shopee"}
Exemplo 4: para cancelamento de pedidos Shopee, o event (input) precisa ser event{"process":"cancel", "marketplace":"shein"}

E assim por diante.

## 1. Instalação Inicial

### Passo 1: Clonar o Repositório
Clone o repositório do projeto para sua máquina local:
```bash
git clone <url-do-repositorio>
cd bot_marketplace
```

### Passo 2: Criar o Arquivo `.env`
Crie um arquivo `.env` dentro da pasta `app` com as seguintes variáveis de ambiente:
```
MONGO_URI=<sua-string-de-conexao-mongodb>
POSTGRES_URI=<sua-string-de-conexao-postgresql>
```
As URIs são strings de conexão para os bancos de dados MongoDB e PostgreSQL.

### Passo 3: Criar um Ambiente Virtual (Opcional, mas Recomendado)
Crie e ative um ambiente virtual para isolar as dependências do projeto:
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/MacOS
venv\Scripts\activate     # Windows
```

### Passo 4: Instalar Dependências
Instale as dependências listadas no arquivo `requirements.txt`:
```bash
pip install -r requirements.txt
```

---

## 2. Executando o Bot

### Passo 1: Configurar o Evento
O bot utiliza um dicionário chamado `event` como entrada, que é compatível com a arquitetura serverless da AWS Lambda. No arquivo `main.py`, localize o bloco `if __name__ == "__main__":` e configure o dicionário `event` com os valores desejados. Exemplo:
```python
event = {"process": "get", "marketplace": "shopee"}
```

### Passo 2: Rodar o Bot
Execute o bot localmente com o seguinte comando:
```bash
python app/main.py
```

---

## 3. Principais Comandos de Entrada

O dicionário `event` define o processo e o marketplace que serão executados. Abaixo estão os principais parâmetros:

### Parâmetros do `event`
- **process**: Define o processo a ser executado. Os valores possíveis são:
  - `"get"`: Coleta dados do marketplace.
  - `"treat"`: Processa e valida os dados coletados.
  - `"cancel"`: Cancela pedidos inválidos.
  - `"to_spreadsheet"`: Exporta os dados para uma planilha Excel.
- **marketplace**: Define o marketplace a ser processado. Exemplos:
  - `"shopee"`: Executa o processo para o marketplace Shopee.
  - `"mercadolivre"`: Executa o processo para o Mercado Livre.
  - `"*"`: O coringa `"*"` indica que o processo envolve **todos os marketplaces**, atualmente, apenas o `"to_spreadsheet"` funciona com o coringa, ou seja, gerará uma planilha contendo dados de todos os marketplaces.

### Exemplo de Configuração do `event`
```python
event = {"process": "to_spreadsheet", "marketplace": "*"}
```
Neste exemplo:
- O processo `to_spreadsheet` será executado.
- Os dados de **todos os marketplaces** serão exportados para uma planilha.

---

## 4. Estrutura de Saída

Após a execução, o bot retorna um dicionário com o status e a mensagem do processo. Exemplo:
```json
{
  "status": "success",
  "body": {
    "message": "Processo [get] para o marketplace [shopee] concluído com sucesso!"
  }
}
```

---

## 5. Dicas Adicionais

- Para rodar os testes unitários, utilize:
  ```bash
  pytest tests/
  ```
- Certifique-se de que o diretório `spreadsheets/` existe para que as planilhas sejam geradas corretamente.

---

Se tiver dúvidas, consulte a documentação no arquivo `README.md` que possui informações gerais do projeto, ou, abra uma issue no repositório.
