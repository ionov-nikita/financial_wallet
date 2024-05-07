import unittest
from financial_wallet import FinancialWallet


class TestFinancialWallet(unittest.TestCase):
    def setUp(self) -> None:
        self.wallet = FinancialWallet("finances_data_example.csv")

    def test_check_balance(self):
        """
        Тест проверяет валидность вывода баланса, суммы доходов и суммы расходов
        """
        balance, income, expenses = self.wallet.check_balance()
        self.assertEqual(balance, 17500)
        self.assertEqual(income, 20000)
        self.assertEqual(expenses, 2500)

    def test_search_row_by_date(self):
        """
        Тест проверяет валидность метода search_row() с аргументом date
        """
        date = "2024-06-01"
        desired_result = ["2024-06-01", "Расход", "1500", "Покупка продуктов"]
        result = self.wallet.search_row(date=date)
        self.assertEqual(result[0], desired_result)

    def test_search_row_by_category(self):
        """
        Тест проверяет валидность метода search_row() c аргументом category
        """
        category = "Расход"
        desired_result = [
            ["2024-06-01", "Расход", "1500", "Покупка продуктов"],
            ["2024-06-03", "Расход", "1000", "Покупка продуктов"],
        ]
        result = self.wallet.search_row(category=category)
        self.assertEqual(result, desired_result)

    def test_search_row_by_money(self):
        """
        Тест проверяет валидность метода search_row() c аргументом amount_money
        """
        amount_money = "20000"
        desired_result = ["2024-06-02", "Доход", "20000", "Зарплата"]
        result = self.wallet.search_row(amount_money=amount_money)
        self.assertEqual(result[0], desired_result)


if __name__ == "__main__":
    unittest.main()
