import unittest
from main import run

class TestMain(unittest.TestCase):

    def test_get_process(self):
        """Testa se o processo 'get' roda sem erros"""
        event = {"process": "get", "marketplace": "shopee", "test": True}
        response = run(event)
        self.assertEqual(response["status"], "success")

    def test_cancel_process(self):
        """Testa se o processo 'cancel' roda sem erros"""
        event = {"process": "cancel", "marketplace": "shopee", "test": True}
        response = run(event)
        self.assertEqual(response["status"], "success")
    
    def test_treat_process(self):
        """Testa se o processo 'treat' roda sem erros"""
        event = {"process": "treat", "marketplace": "shopee", "test": True}
        response = run(event)
        self.assertEqual(response["status"], "success")

    def test_to_spreadsheet_process(self):
        """Testa se o processo 'to_spreadsheet' roda sem erros"""
        event = {"process": "to_spreadsheet", "marketplace": "shopee", "test": True}
        response = run(event)
        self.assertEqual(response["status"], "success")

    def test_invalid_process(self):
        """Testa se um processo inválido retorna erro"""
        event = {"process": "invalid", "marketplace": "shopee", "test": True}
        response = run(event)
        self.assertEqual(response["status"], "error")

    def test_invalid_marketplace(self):
        """Testa se um marketplace inválido retorna erro"""
        event = {"process": "get", "marketplace": "invalid", "test": True}
        response = run(event)
        self.assertEqual(response["status"], "error")
    

if __name__ == "__main__":
    unittest.main()
