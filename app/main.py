import settings
from validators.process_entry import process_entry_validator
from factorys import FactoryMarketplace, FactoryDatabase
from handles import get, treat, cancel, to_spreadsheet
import time
import asyncio
import traceback


def run(event:dict, context=None):
    """
     Esse bot foi projetado para rodar localmente ou serverless,
     possibilitando a chamada de diversas instâncias simultaneamente na AWS Lambda pensando em escalabilidade.
     Se conecta ao banco de dados via connection string e executa um processo definido.
    :param event: dicionário que contém o processo a ser executado e o marketplace.
    :param context: parâmetro obrigatório na AWS Lambda, mas não utilizado aqui.
    """
    try:
        settings.TESTING = event.get('testing', 'False')
        process = event.get('process', '').lower()
        marketplace = event.get('marketplace', '').lower()
        
        # Valida o processo e o marketplace
    
        process_entry_validator(process, marketplace)

        print(f"\033[92mIniciando o processo [{process}] para o marketplace [{marketplace}]\033[0m")

        # Cria a instância do marketplace
        marketplace_instance = FactoryMarketplace(marketplace).create()
        

        # Executa o processo de acordo com o evento recebido

        match process:
            case "get":
                nosql_db = FactoryDatabase(settings.NO_SQL).create(marketplace)
                get(marketplace_instance, nosql_db)
                nosql_db.disconnect()
            case "treat":
                nosql_db = FactoryDatabase(settings.NO_SQL).create(marketplace)
                sql_db = FactoryDatabase(settings.SQL).create()
                treat(marketplace_instance, sql_db, nosql_db)
                sql_db.disconnect()
                nosql_db.disconnect()
            case 'cancel':
                nosql_db = FactoryDatabase(settings.NO_SQL).create(marketplace)
                asyncio.run(cancel(marketplace_instance, nosql_db))
                nosql_db.disconnect()
            case 'to_spreadsheet':
                sql_db = FactoryDatabase(settings.SQL).create()
                to_spreadsheet(marketplace_instance, sql_db)
                sql_db.disconnect()
    

        return {
            "status": 'success',
            "body": {
                "message": f"Processo [{process}] para o marketplace [{marketplace}] concluído com sucesso!"
            }
        }
    
    except Exception as e:

        return {
            "status": 'error',
            "body": {
                "error": traceback.format_exc(),
                "message": str(e),
            }
        }

                       
if __name__ == "__main__":
    """ Executa o bot localmente """
    start_time = time.time()
    event = {"process": "get", "marketplace": "shopee"}
    run(event)
    # event = {"process": "treat", "marketplace": "shopee"}
    # run(event)
    # event = {"process": "cancel", "marketplace": "shopee"}
    # run(event)
    # event = {"process": "to_spreadsheet", "marketplace": "shopee"}
    # run(event)
    end_time = time.time()
    execution_time = end_time - start_time  # Calcula o tempo de execução
    print(f"\033[92mTempo de execução: {execution_time:.2f} segundos\033[0m")
