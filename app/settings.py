TESTING = False
SQL = 'postgres'
NO_SQL = "mongodb"
REGISTERED_PROCESSES = ["get", "treat", "cancel", 'to_spreadsheet']
REGISTERED_MARKETPLACES = ["shopee", "shein", "*"] # * é um wildcard para 'to_spreadsheet' gerar planilha contendo dados de todos os marketplaces