from marketplaces.interface import Marketplace
from typing import List, Dict, Any
import random
import hashlib
import httpx


class Shopee(Marketplace):
    """Classe para consulta e tratamento de dados para o Shopee."""
    
    def __init__(self):
        super().__init__()  # Chama o construtor da classe pai
    
    def get_external_data(self) -> List[Dict[str, Any]]:
        """Gera dados fictícios para um pedido da Shopee.
        Em um cenário real poderia ser uma chamada para a API do marketplace.
        """
        
        orders_data = list()

        for _ in range(random.randint(10, 20)):

            order_data = {
                "id_pedido": 'SHP-' + hashlib.sha256(self.fake.uuid4().encode()).hexdigest()[:12].upper(),
                "cliente": self.fake.name(),
                "email_cliente": self.fake.email(),
                "nome_produto": self.fake.random_element(elements=("Celular", "Notebook", "PC", "Console", "Monitor", "Smart TV", "")),
                "preco_unitario": self.fake.random_number(digits=4),
                "quantidade": self.fake.random_int(min=1, max=3),
                "data_pedido": self.fake.date_time_this_year(),
                "endereco_entrega": {
                    "rua": self.fake.street_address(),
                    "complemento": self.fake.secondary_address(),
                    "cidade": self.fake.city(),
                    "estado": self.fake.state(),
                    "codigo_postal": self.fake.random_number(digits=8),
                },
                "status": self.fake.random_element(elements=("Pending", "Shipped", "Delivered", "Cancelled"))
            }
            orders_data.append(order_data)
        
        return orders_data
    
    def process_data(self, order: Dict[str, Any]) -> None:
        """
        Processa os dados do pedido da Shopee que já estão no MongoDB mas agora precisam ser processados.
        
        Aqui você pode adicionar lógica para processar os dados, como validações ou transformações
        Por exemplo, você pode querer verificar se o pedido já existe antes de salvá-lo
        Verifique o template de validação para garantir que os dados e a tipagem estejam corretas

        Utilize o modelo de validação que se encontra em app/validators/order_validator.py:
        """
        try:
            processed_order = dict()
            processed_order["id_pedido"] = str(order["id_pedido"])
            processed_order["nome_cliente"] = str(order["cliente"])
            processed_order["email_cliente"] = str(order["email_cliente"])
            processed_order["nome_produto"] = str(order["nome_produto"])
            processed_order["preco_unitario"] = float(order["preco_unitario"])
            processed_order["preco_total"] = float(order["preco_unitario"]) * int(order["quantidade"])
            processed_order["quantidade"] = int(order["quantidade"])
            processed_order["data_pedido"] = str(order["data_pedido"])
            
            # Montando o endereço de entrega
            processed_order["endereco_entrega"] = f"{str(order['endereco_entrega']['rua'])},\
                  {str(order['endereco_entrega']['complemento'])},\
                  {str(order['endereco_entrega']['cidade'])}, \
                  {str(order['endereco_entrega']['estado'])}"
            
            processed_order["complemento"] = str(order["endereco_entrega"]["complemento"])
            processed_order["codigoPostal"] = int(order["endereco_entrega"]["codigo_postal"])
            processed_order["status"] = str(order["status"])
            
            return processed_order

        except Exception as e:
            # Poderia-se enviar para algum serviço de monitoramento
            print(f"Erro ao processar os dados de um pedido do Marketplace {self.__class__.__name__}: {e}")
    
    async def cancel_order(self, order: Dict[str, Any]) -> None:
        """
        Simula uma requisição na API pra cancelar um pedido.
        """
        # Aqui você pode adicionar lógica para cancelar o pedido
        async with httpx.AsyncClient() as client:
            print(f"Cancelando pedido {order['id_pedido']}...")
            response = await client.get('https://www.google.com.br', params={'id_pedido': order['id_pedido']})
            # Apenas depois que a requisição for feita, o print final será exibido
            print(f"Pedido cancelado {order['id_pedido']}...")

    
        


