from abc import ABC, abstractmethod
from typing import List, Dict, Any
from faker import Faker

class Marketplace(ABC):

    """Classe abstrata para geração, processamento e armazenamento de dados fictícios dos marketplaces.
    Nota: 
        Uma classe abstrata é uma classe que não pode ser instanciada diretamente e serve como um modelo para outras classes.
        Ela pode conter métodos abstratos (sem implementação) que devem ser implementados pelas subclasses.
    """

    
    def __init__(self):
        self.fake = Faker()  # Inicializa o gerador de dados fictícios

    @abstractmethod
    def get_external_data(self) -> List[Dict[str, Any]]:
        """
        Método abstrato para pegar dados fictícios gerados e colocá-los no banco.
        Deve ser implementado por subclasses para gerar dados de cada marketplace.
        """
        pass

    @abstractmethod
    def process_data(self, order: Dict[str, Any]) -> None:
        """
        Método abstrato para processar os dados do pedido.
        Deve ser implementado por subclasses para processar os dados de cada marketplace.
        """
        pass

    @abstractmethod
    async def cancel_order(self, order: dict) -> None:
        """
        Simula uma requisição na API pra cancelar um pedido.
        """
        pass
