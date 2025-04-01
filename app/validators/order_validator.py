from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import datetime

# Definindo o modelo para validação
class Order(BaseModel):
    id_pedido: str
    nome_cliente: str
    email_cliente: str
    nome_produto: str
    preco_unitario: float
    preco_total: float
    quantidade: int
    data_pedido: datetime
    endereco_entrega: str
    codigo_postal: Optional[int] = None
    status: str

    # Validação do campo 'id_pedido' para ser uma string não vazia
    @field_validator('id_pedido')
    def id_pedido_must_not_be_empty(cls, v):
        if not v:
            raise ValueError('id_pedido não pode ser vazio')
        return v
    
    # Validação do campo 'nome_produto' para ser uma string não vazia
    @field_validator('nome_produto')
    def nome_produto_must_not_be_empty(cls, v):
        if not v:
            raise ValueError('nome_produto não pode ser vazio')
        return v
    
    # Validação para garantir que o campo 'email_cliente' tenha formato de email válido
    @field_validator('email_cliente')
    def email_must_be_valid(cls, v):
        if '@' not in v and '.com' not in v:
            raise ValueError('email_cliente precisa ser um endereço de email válido')
        return v

# Função para validar os dados
def validate_order(dados: dict):
    try:
        Order(**dados)
        return dados
    except ValueError as e:
        return False
