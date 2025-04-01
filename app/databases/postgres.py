from databases.interface_sql import InterfaceSQL
import settings
import psycopg2
from psycopg2.extras import RealDictCursor
from typing import Dict, List, Any, Optional
from dotenv import load_dotenv
import os

load_dotenv()

class PostgresDB(InterfaceSQL):
    def __init__(self):
        """Inicializa a conexão com o PostgreSQL."""
        self.dsn = os.getenv("POSTGRES_URI")
        self.conn = None
        self.cursor = None

    def connect(self):
        """Conecta ao banco de dados."""
        self.conn = psycopg2.connect(self.dsn, cursor_factory=RealDictCursor)
        self.cursor = self.conn.cursor()
        self._create_orders_table()

        print("\033[92mConectado ao PostgreSQL\033[0m")

    def disconnect(self):
        """Desconecta do banco de dados."""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
        print("Desconectado do PostgreSQL")

    def save_data(self, marketplace:str, validated_orders: List[Dict[str, Any]]):
        try:
            """Salva os dados em massa na tabela orders."""
            
            table = 'orders' if not settings.TESTING else 'orders_test'
            query = f"""
            INSERT INTO {table} (id_pedido, marketplace, nome_cliente, email_cliente, nome_produto, preco_unitario, preco_total, quantidade, data_pedido, endereco_entrega, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            # Prepare os dados para inserir como uma lista de tuplas
            data_to_insert = [
                (
                    order["id_pedido"], marketplace, order["nome_cliente"], order["email_cliente"],
                    order["nome_produto"], order["preco_unitario"], order["preco_total"], order["quantidade"],
                    order["data_pedido"], str(order["endereco_entrega"]), order["status"]
                )
                for order in validated_orders
            ]

            # Use o executemany para inserir todos os pedidos de uma vez
            self.cursor.executemany(query, data_to_insert)
            self.conn.commit()
        except psycopg2.errors.UniqueViolation as e:
            print('\033[91mErro: Violação de chave única. Um ou mais pedidos já existem na tabela.\033[0m')
            id_pedido = str(e).split('id_pedido)=(')[1].split(')')[0] # Pega o id do pedido vindo no erro
            # remover pedido da lista e chamar a função novamente
            validated_orders = [order for order in validated_orders if order["id_pedido"] != id_pedido]
            print(f'\033[92mPedido {id_pedido} removido da lista e inserido novamente\033[0m')
            self.conn.rollback()
            self.save_data(marketplace, validated_orders)
            

    def fetch_data(self, marketplace:str) -> Optional[List[Dict[str, Any]]]:
        """Retorna dados na tabela orders com base no marketplace."""
        sql = "SELECT * FROM orders"
        if marketplace != '*':
            sql += " WHERE marketplace = %s"
        # Se o marketplace for 'marketplace' (classe pai/interface), retorna todos os dados
        self.cursor = self.conn.cursor(cursor_factory=RealDictCursor)
        self.cursor.execute(sql) if marketplace == '*' else self.cursor.execute(sql, (marketplace,))

        results = self.cursor.fetchall()
        results = [dict(row) for row in results]
        return results
    

    def delete_data(self, query: Dict[str, str]):
        """Deleta dados da tabela orders."""
        sql = "DELETE FROM orders WHERE id_pedido = %s"
        self.cursor.execute(sql, (query["id_pedido"],))
        self.conn.commit()


    def _create_orders_table(self):
        """Cria a tabela orders do marketplace se não existir."""
        table = 'orders' if not settings.TESTING else 'orders_test'
        create_table_query = f"""
        CREATE TABLE IF NOT EXISTS {table} (
            id_pedido TEXT PRIMARY KEY,
            marketplace TEXT,
            nome_cliente TEXT,
            email_cliente TEXT,
            nome_produto TEXT,
            preco_unitario NUMERIC,
            preco_total NUMERIC,
            quantidade INT,
            data_pedido TIMESTAMP,
            endereco_entrega TEXT,
            status TEXT,
            data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        self.cursor.execute(create_table_query)
        self.conn.commit()