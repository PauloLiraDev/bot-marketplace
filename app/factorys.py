from marketplaces import shein, shopee
from databases import mongodb, postgres

class FactoryMarketplace:
    """ 
    Classe Fábrica de marketplaces para geração de dados fictícios.
    Ela cria instâncias de classes responsáveis para cada marketplace, tornando o projeto mais modular, fácil de manter e escalável.
    """
    
    def __init__(self, marketplace):
        self.marketplace = marketplace

    def create(self):
        """
        Método para criar uma instância do marketplace específico.
        Ele verifica qual marketplace foi solicitado e retorna a instância correspondente.
        Se o marketplace não estiver integrado, ele lança um erro.
        :return: Instância do marketplace específico.
        :raises ValueError: Se o marketplace não estiver integrado.
        """
    
        match self.marketplace:
            case 'shein':
                return shein.Shein()
            case 'shopee':
                return shopee.Shopee()
            case '*':
                return None
            case _:
                print(f"\033[91mMarketplace não integrado: {self.marketplace}\033[0m")
                raise ValueError(f"Marketplace não integrado: {self.marketplace}")


class FactoryDatabase:
    """
    Classe Fábrica de bancos de dados para conexão com SQL ou No-SQL.
    """

    def __init__(self, database):
        self.database = database

    def create(self, marketplace:str = None):
        """
        Método para criar uma instância do banco de dados específico.

        :return: Instância do banco de dados específico.
        :raises ValueError: Se o banco de dados não estiver integrado.
        """
        match self.database:
            case 'mongodb':
                db = mongodb.MongoDB(marketplace)
            case 'postgres':
                db = postgres.PostgresDB()
            case _:
                error_msg = f"\033[91mBanco de dados não integrado: {self.database}\033[0m"
                print(error_msg)
                raise ValueError(error_msg)
        
        db.connect()
        return db

