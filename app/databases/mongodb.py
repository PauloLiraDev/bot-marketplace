import settings
import os
from databases.interface_nosql import InterfaceNoSQL
from typing import List
from pymongo import MongoClient, errors

class MongoDB(InterfaceNoSQL):
    """Classe para interação com o banco de dados MongoDB."""

    def __init__(self, marketplace:str):
        self.mongodb_url = os.getenv("MONGO_URI")
        if not self.mongodb_url:
            self._log_error("URI do MongoDB não encontrada.")
            raise ValueError("A URI do MongoDB não foi definida na variável de ambiente MONGO_URI.")
        self.connection = None
        self.mongodb = None
        self.marketplace = marketplace

    def connect(self):
        """Conecta ao banco de dados MongoDB."""
        if self.connection is None:
            try:
                self.connection = MongoClient(self.mongodb_url)
                self.mongodb = self.connection.get_database(name='orders-db')
                self._log_success("Conectado ao MongoDB")
            except errors.ConnectionError as e:
                self._handle_connection_error(e)
            except Exception as e:
                self._handle_unexpected_error(e, "Erro inesperado ao conectar")
        else:
            self._log_warning("Já conectado ao MongoDB")
        return self.mongodb

    
    def disconnect(self):
        """Desconecta do banco de dados MongoDB."""
        if self.connection is not None:
            try:
                self.connection.close()
                self._log_success("Desconectado do MongoDB")
            except Exception as e:
                self._log_error(f"Erro ao desconectar: {e}")
        else:
            self._log_warning("Já desconectado do MongoDB")

    
    def fetch_data(self) -> List[dict]:
        """Obtém dados do banco de dados MongoDB."""
        if not self._is_connected():
            return None
        try:
            # Consulta os dados não processados anteriormente.
            query = {"bot_processed": {"$exists": False}}
            collection = self._get_collection()
            documents_order = collection.find(query)

            # Transformar o resultado em uma lista
            documents_list = list(documents_order)
            return documents_list
        
        except errors.PyMongoError as e:
            self._log_error(f"Erro ao buscar dados: {e}")
            return None

    
    def save_data(self, data: dict):
        """Salva os dados no banco de dados MongoDB."""
        if not self._is_connected():
            return
        try:
            collection = self._get_collection()
            collection.insert_many(data)
            self._log_success("Dados inseridos com sucesso.")
        except errors.PyMongoError as e:
            self._log_error(f"Erro ao inserir dados: {e}")
        except Exception as e:
            self._handle_unexpected_error(e, "Erro inesperado ao inserir dados")
    
    
    def update_data(self, orders: List[dict]):
        """
        Atualiza status para marcar como processado pelo bot no banco de dados MongoDB.
        {bot_processed:true}
        """
        if not self._is_connected():
            return
        try:
            collection = self._get_collection()
            collection.update_many(
                {"id_pedido": {"$in": [order["id_pedido"] for order in orders]}},
                {"$set": {"bot_processed": True}}
            )
            self._log_success("Dados atualizados com sucesso.")

        except errors.PyMongoError as e:
            self._log_error(f"Erro ao atualizar dados: {e}")
        except Exception as e:
            self._handle_unexpected_error(e, "Erro inesperado ao atualizar dados")


    def _get_collection(self):
        """Obtém a coleção específica do marketplace."""
        return self.mongodb[f"orders_{self.marketplace}"] if not settings.TESTING else self.mongodb[f"orders_{self.marketplace}_test"]

    def _is_connected(self) -> bool:
        """Verifica se há uma conexão ativa com o MongoDB."""
        if self.mongodb is None:
            self._log_error("Erro: Não conectado ao MongoDB.")
            return False
        return True

    def _log_success(self, message: str):
        """Exibe mensagens de sucesso."""
        print(f"\033[92m{message}\033[0m")

    def _log_warning(self, message: str):
        """Exibe mensagens de aviso."""
        print(f"\033[93m{message}\033[0m")

    def _log_error(self, message: str):
        """Exibe mensagens de erro."""
        print(f"\033[91m{message}\033[0m")

    def _handle_connection_error(self, error: Exception):
        """Trata erros de conexão."""
        self._log_error(f"Erro de conexão: {error}")
        self.connection = None
        self.mongodb = None
        raise

    def _handle_unexpected_error(self, error: Exception, context: str):
        """Trata erros inesperados."""
        self._log_error(f"{context}: {error}")
        self.connection = None
        self.mongodb = None
        raise
