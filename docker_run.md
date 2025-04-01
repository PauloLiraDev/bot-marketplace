# Bot Marketplace

Este projeto contém a automação de processamento de dados para diferentes marketplaces. Ele permite integrar, tratar e realizar ações sobre dados provenientes de bancos de dados MongoDB e PostgreSQL.

## Dicas para Acompanhamento dos Dados

Se você quiser acompanhar os dados nos bancos de dados utilizados (MongoDB e PostgreSQL), pode usar as extensões do **MongoDB** e **PostgreSQL** no **VSCode**. Elas ajudam a visualizar e interagir diretamente com os dados armazenados em seu banco de dados 
(pode usar as connections strings do meu banco mongodb e postgres).

## Executando o Projeto com Docker

### Passos para Construir e Rodar o Docker

1. **Mude seu diretório atual para dentro da pasta `/app` do projeto:**

   Se você estiver fora da pasta `/app`, altere o diretório para garantir que você esteja no local correto:

   ```bash
   cd /caminho/para/seu/projeto/app
   ```

2. **Construir a Imagem Docker:**

   Execute o seguinte comando para criar a imagem Docker com o nome `mkt_bot`:

   ```bash
   docker build -t mkt_bot .
   ```

3. **Rodar a Imagem Docker:**

   Após a construção da imagem, você pode rodar o container usando o seguinte comando:

   ```bash
   docker run --name mkt_bot_container mkt_bot
   ```

   Isso irá rodar a bateria de testes contida no arquivo `tests.py` dentro do container.

### Observações

- O Docker irá executar a bateria de testes localizada no arquivo `tests.py` automaticamente.
- Certifique-se de que todos os arquivos de configuração e variáveis de ambiente estejam configurados corretamente para garantir que os testes sejam executados conforme o esperado.

## Dependências

Certifique-se de ter as dependências corretamente configuradas:

- **Docker** instalado no seu sistema.
- **VSCode** com as extensões **MongoDB** e **PostgreSQL** para monitoramento dos dados, caso deseje acompanhar o progresso nos bancos de dados.

## Agradecimentos

De antemão, eu, Paulo Lira, agradeço pela oportunidade de estar participando do processo seletivo. A empresa e os funcionários se mostraram muito profissionais em propor este desafio no processo de admissão.

---

Boa sorte e aproveite o processo da automação!
