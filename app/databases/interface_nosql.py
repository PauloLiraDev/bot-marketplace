from abc import ABC, abstractmethod
from typing import Dict, Any


class InterfaceNoSQL(ABC):
    """Interface para interação com o banco não relacional."""

    @abstractmethod
    def connect(self):
        """Conecta ao banco de dados."""
        pass

    @abstractmethod
    def disconnect(self):
        """Desconecta do banco de dados."""
        pass

    @abstractmethod
    def save_data(self, data: Dict[str, Any]):
        """Salva os dados no banco de dados."""
        pass

    @abstractmethod
    def fetch_data(self, query: Dict[str, Any], processed: bool) -> Dict[str, Any]:
        """Encontra dados no banco de dados com base na consulta."""
        pass

    @abstractmethod
    def update_data(self, query: Dict[str, Any], update: Dict[str, Any]):
        """Atualiza dados no banco de dados com base na consulta."""
        pass