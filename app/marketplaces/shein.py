from marketplaces.interface import Marketplace
import random
from typing import List
import httpx
from typing import Dict, Any
import hashlib


class Shein(Marketplace):
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
                "order_id": 'SHE-' + hashlib.sha256(self.fake.uuid4().encode()).hexdigest()[:12].upper(),
                "customer_name": self.fake.name(),
                "customer_email": self.fake.email(),
                "product_name": self.fake.random_element(elements=("Celular", "Notebook", "PC", "Console", "Monitor", "Smart TV", "")),
                "product_price": self.fake.random_number(digits=4),
                "order_date": self.fake.date_time_this_year(),
                "shipping_address": {
                    "street": self.fake.street_address(),
                    "complement": self.fake.secondary_address(),
                    "city": self.fake.city(),
                    "state": self.fake.state(),
                    "zip_code": self.fake.random_number(digits=8),
                },
                "status": self.fake.random_element(elements=("Pending", "Shipped", "Delivered", "Cancelled"))
            }
            orders_data.append(order_data)
        
        return orders_data
    
    def process_data(self, order: Dict[str, Any]) -> None:
        """
        Processa os dados do pedido da Shopee que já estão no MongoDB mas agora precisam ser processados.
        
        Aqui você pode adicionar lógica para processar os dados, como validações ou transformações"
        """
        try:
            processed_order = dict()
            processed_order["id_pedido"] = str(order["order_id"])
            processed_order["nome_cliente"] = str(order["customer_name"])
            processed_order["email_cliente"] = str(order["customer_email"])
            processed_order["nome_produto"] = str(order["product_name"])
            processed_order["preco_unitario"] = float(order["product_price"])
            processed_order["preco_total"] = float(order["product_price"])
            processed_order["quantidade"] = 1
            processed_order["data_pedido"] = order["order_date"]
            processed_order["endereco_entrega"] = order["shipping_address"]['street'] + ', ' + order["shipping_address"]['complement'] + ', ' + order["shipping_address"]['city'] + ', ' + order["shipping_address"]['state']
            processed_order["status"] = order["status"]
            return processed_order

        except Exception as e:
            # Poderia-se enviar para um sistema de monitoramento
            print(f"Erro ao processar o pedido: {e}")

    async def cancel_order(self, order: Dict[str, Any]) -> None:
        """
        Simula uma requisição na API pra cancelar um pedido.
        """
        async with httpx.AsyncClient() as client:
            print(f"Cancelando pedido {order['id_pedido']}...")
            response = await client.get('https://www.google.com.br', params={'id_pedido': order['id_pedido']})
            # Apenas depois que a requisição for feita, o print final será exibido
            print(f"Pedido cancelado {order['id_pedido']}...")