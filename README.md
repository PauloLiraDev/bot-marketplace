**Automação Gerenciadora de Loja em Marketplaces**

**Visão Geral**

Este projeto tem como objetivo centralizar e padronizar os dados de uma loja que vende em diferentes marketplaces. 
Cada marketplace utiliza uma estrutura diferente de dados, podendo vir algumas colunas ou chaves em português, inglês, snake_case, camelCase, nas apis dos marketplaces.

Para desenvolver essa solução, criei algumas automações. 
Utilizei um banco NoSQL para armazenar os dados brutos e, posteriormente, fiz a normalização e migração para um banco relacional. Isso me permite gerar planilhas e outras formas de análise estruturada.

**Funcionamento**

[Assista ao vídeo no YouTube](https://youtu.be/uXqIMqcdddQ)

Ingestão de Dados: o método 'get' alimenta um banco NoSQL com os dados fictíceis que foram gerados de cada marketplace.

Processamento & Padronização: Um sistema verifica os dados, padroniza conforme regras pré-definidas e os transfere para um banco relacional.

Monitoramento de Status: Cada dado bruto no banco não-relacional receberá um status ('bot_processed': true), indicando se foi processado, caso ocorra algum problema, ele será coletado novamente pelo processo de tratamento ('treat').

Escalabilidade: O projeto segue o Design Pattern Factory, permitindo a fácil integração de novos marketplaces ou novos bancos de dados (SQL e No-SQL) conforme necessário.

🏗️ Arquitetura do Projeto

🔹 Banco NoSQL

Armazena os dados brutos coletados dos marketplaces.

🔹 Banco Relacional

Armazena os dados já padronizados e normalizados.

Permite consultas estruturadas e geração de relatórios.

🔹 Factory Pattern

Facilita a adição de novos marketplaces e bancos de dados sem modificar o código principal.

Cada marketplace ou banco de dados tem sua própria implementação para conversão de dados.

🛠️ Tecnologias Utilizadas

Python → Processamento e normalização dos dados.

MongoDB (NoSQL) → Armazenamento inicial dos dados brutos dos marketplaces.

PostgreSQL (Relacional) → Armazenamento dos dados padronizados.

Docker (Container) → Para que o projeto possa ser executado na AWS Lambda.
