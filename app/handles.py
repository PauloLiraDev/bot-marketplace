from settings import NO_SQL, SQL, TESTING
from validators.order_validator import validate_order
import asyncio
import pandas as pd


def get(marketplace_instance:object, nosql_db:object):
    """
    Função para buscar os pedidos do marketplace
    param: marketplace_instance: instância do marketplace a ser processado
    """
    # Cria uma instância do banco de dados No-SQL informando o marketplace a ser processado.
    marketplace = marketplace_instance.__class__.__name__.lower()

    # Simula uma consulta dos pedidos do marketplace
    orders_list = marketplace_instance.get_external_data() 
    print(f"\033[92mForam coletados {len(orders_list)} novos pedidos do {marketplace}.\033[0m")

    # O marketplace é passado para salvar na sua respectiva coleção
    # Salva os pedidos no banco de dados No-SQL
    nosql_db.save_data(data=orders_list) 

    print(f"\033[92mOs {len(orders_list)} pedidos foram salvos no banco No-SQL\033[0m")


def treat(marketplace_instance:object, sql_db:object, nosql_db:object):
    """
    Função para tratar os pedidos do marketplace
    param: marketplace_instance: instância do marketplace a ser processado
    """
    # Cria uma instância do banco de dados No-SQL informando o marketplace a ser processado.
    marketplace = marketplace_instance.__class__.__name__.lower()
    
    
    # Busca os pedidos não processados do marketplace atual no banco No-SQL
    gross_orders_list = nosql_db.fetch_data()

    print(f"\033[34mExistem {len(gross_orders_list)} pedidos para serem processados.\033[0m")

    # Processa os dados dos pedidos
    processed_orders = [marketplace_instance.process_data(order) for order in gross_orders_list]
    print(f"\033[34mForam processados {len(processed_orders)} pedidos.\033[0m")

    # Valida os pedidos processados
    validated_orders = [order for order in processed_orders if validate_order(order)]

    print(f"\033[34mForam validados {len(validated_orders)} pedidos.\033[0m")

    # Salva os pedidos validados no banco SQL
    print(f"\033[34mSalvando {len(validated_orders)} pedidos no banco SQL\033[0m")

    sql_db.save_data(marketplace=marketplace, validated_orders=validated_orders)

    print(f"\033[34mOs pedidos foram salvos no banco SQL\033[0m")

    # Só atualiza os pedidos no No-SQL se os pedidos forem validados e salvos no SQL.
    nosql_db.update_data(orders=validated_orders)


async def cancel(marketplace_instance:object, nosql_db:object):
    """
    Função assíncrona para cancelar pedidos
    param: marketplace_instance: instância do marketplace a ser processado
    """
    gross_orders_list = nosql_db.fetch_data()
    processed_orders = [marketplace_instance.process_data(order) for order in gross_orders_list]
    invalid_orders = [order for order in processed_orders if not validate_order(order)]
    await asyncio.gather(*(marketplace_instance.cancel_order(order) for order in invalid_orders))
    print(f"\033[34mForam cancelados {len(invalid_orders)} pedidos.\033[0m")
    nosql_db.update_data(orders=invalid_orders)



def to_spreadsheet(marketplace_instance:object|None, sql_db:object):
    """
    Função para gerar uma planilha com os dados de um ou todos os marketplaces"
    """
    marketplace = marketplace_instance.__class__.__name__.lower() if marketplace_instance else '*'
    data = sql_db.fetch_data(marketplace=marketplace)
    df = pd.DataFrame(data)
    marketplace = marketplace if marketplace != '*' else 'all'
    name = 'orders' if not TESTING else 'orders_test'
    df.to_excel(f'spreadsheets/{marketplace}_{name}.xlsx', index=False)
    print(f"\033[34mPlanilha {marketplace}_orders.xlsx gerada com sucesso!\033[0m")



