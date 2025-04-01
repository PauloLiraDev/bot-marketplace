from settings import REGISTERED_PROCESSES, REGISTERED_MARKETPLACES

def process_entry_validator(process, marketplace):
    """
    Valida o processo e o marketplace.
    :param process: processo a ser executado
    :param marketplace: marketplace a ser utilizado
    :raises ValueError: se o processo ou marketplace não forem válidos
    """
    # Verifica se o processo é válido
    if marketplace == "*" and process != 'to_spreadsheet':
        print(f"\033[91mO wildcard '*' só pode ser utilizado com o processo 'to_spreadsheet'.\033[0m")
        raise ValueError(f"O wildcard '*' só pode ser utilizado com o processo 'to_spreadsheet'.")
    
    if process == '' or process == '':
        raise ValueError("o json (event) deve conter a chave e valor do 'processo' e o 'marketplace'.")
    
    if process not in REGISTERED_PROCESSES:
        print(f"\033[91mMétodo de processo inválido: {process}, métodos disponíveis: {REGISTERED_PROCESSES}\033[0m")
        raise ValueError(f"Método de processo inválido: {process}, métodos disponíveis: {REGISTERED_PROCESSES}")
    
    # Verifica se o marketplace é válido
    if marketplace not in REGISTERED_MARKETPLACES:
        print(f"\033[91mMarketplace inválido: {marketplace}, marketplaces disponíveis: {REGISTERED_MARKETPLACES}\033[0m")
        raise ValueError(f"Método de processo inválido: {process}, métodos disponíveis: {REGISTERED_PROCESSES}")