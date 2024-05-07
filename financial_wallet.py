import csv
import argparse
import logging
from typing import Tuple, List

logger = logging.getLogger(__name__)


class FinancialWallet:
    """
    Класс FinancialWallet.
    Этот класс представляет собой приложение финансового кошелька,
    которое может управлять записями о финансовых транзакциях.

    Attributes
    ----------
    filename: путь до файла CSV с записями

    Methods
    -------
    check_balance()
        Метод рассчитывает баланс, доход и расход.
    add_new_row(new_date, new_category, new_amount_money, new_description)
        Метод добавляет новую запись в файл CSV
    editing_row(date,new_category, new_amount_money, new_description)
        Метод изменяет строку в файле CSV по одному конкретному аргументу
    search_row(date, category, amount_money)
        Метод ищет записи по одному конкретному аргументу

    """

    def __init__(self, filename: str) -> None:
        self.filename = filename

    def check_balance(self) -> Tuple[int, int, int]:
        """
        Метод рассчитывает баланс, доход и расход.

        Return
        ------
        Tuple[int, int, int]: Кортеж с записями о балансе, доходе и расходе
        """
        balance = 0
        income = 0
        expenses = 0
        with open(self.filename, encoding="utf-8") as file:
            file_reader = csv.reader(file)
            for count, row in enumerate(file_reader):
                if count != 0:
                    amount_money = int(row[2])
                    if row[1] == "Расход":
                        balance -= amount_money
                        expenses += amount_money
                    else:
                        balance += amount_money
                        income += amount_money
        return balance, income, expenses

    def add_new_row(
        self,
        new_date: str,
        new_category: str,
        new_amount_money: str,
        new_description: str,
    ) -> None:
        """
        Метод добавляет новую запись в файл CSV.
        Parameters
        ----------
        new_date: str - дата
        new_category: str - категория
        new_amount_money: str - сумма денег
        new_description: str - описание
        """
        with open(self.filename, mode="a", encoding="utf-8") as file:
            file_writer = csv.writer(file, lineterminator="\r")
            file_writer.writerow(
                [new_date, new_category, new_amount_money, new_description]
            )

    def editing_row(
        self,
        date: str,
        new_category: str = None,
        new_amount_money: str = None,
        new_description: str = None,
    ) -> None:
        """
        Метод изменяет строку в файле CSV по одному конкретному аргументу.
        Parameters
        ----------
        date: str - дата
        new_category: str - категория
        new_amount_money: str - сумма денег
        new_description: str - описание
        """
        rows = []
        row_updated = False

        with open(self.filename, mode="r", newline="", encoding="utf-8") as file:
            file_reader = csv.reader(file)
            for row in file_reader:
                if row[0] == date:
                    if new_category:
                        row[1] = new_category
                    if new_amount_money:
                        row[2] = new_amount_money
                    if new_description:
                        row[3] = new_description
                    row_updated = True
                rows.append(row)

        if not row_updated:
            return logger.info("Строка не найдена или некорректный ввод")

        with open(self.filename, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerows(rows)

        logger.info("Строка успешно обновлена.")

    def search_row(
        self, date: str = None, category: str = None, amount_money: str = None
    ) -> List[List[str]]:
        """
        Метод ищет записи по одному конкретному аргументу.
        Parameters
        ----------
        date: str - дата
        category: str - категория
        amount_money: str - сумма денег

        Return
        ------
        List[List[str]]: Список со строками
        """
        find_rows = []
        with open(self.filename, mode="r", encoding="utf-8") as file:
            file_reader = csv.reader(file)
            for row in file_reader:
                if date:
                    if row[0] == date:
                        find_rows.append(row)
                if category:
                    if row[1] == category:
                        find_rows.append(row)
                if amount_money:
                    if row[2] == amount_money:
                        find_rows.append(row)
            if find_rows:
                return find_rows
            logger.info("Строки не найдена или некорректный ввод")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    parser = argparse.ArgumentParser(description="Личный финансовый кошелек")
    parser.add_argument("filename", help="CSV файл")
    args = parser.parse_args()

    wallet = FinancialWallet(args.filename)

    while True:
        print(
            "Выберете одно из следующих действий:\n"
            "1: Показать текущий баланс, а также отдельно доходы и расходы\n"
            "2: Добавить новую запись о доходе или расходе\n"
            "3: Изменить существующих записей о доходах и расходах\n"
            "4: Найти запись по категории, дате или сумме\n"
        )
        choice = input("Ввод: ")

        if choice == "1":
            balance, income, expenses = wallet.check_balance()
            print(f"Баланс: {balance}\nДоходы: {income}\nРасходы: {expenses}\n")

        elif choice == "2":
            new_date = input("Введите дату: ")
            new_category = input("Введите категорию (Расход или Доход): ")
            new_amount_money = input("Введите количество денег: ")
            new_description = input("Введите описание: ")
            wallet.add_new_row(
                new_date, new_category, new_amount_money, new_description
            )
            print("Новая запись успешно добавлена.\n")

        elif choice == "3":
            date = input("Введите дату: ")
            new_category = input(
                "Введите новую категорию (оставьте поле пустым если не хотите его изменять): "
            )
            new_amount_money = input(
                "Введите новую сумму денег (оставьте поле пустым если не хотите его изменять): "
            )
            new_description = input(
                "Введите новое описание (оставьте поле пустым если не хотите его изменять): "
            )
            wallet.editing_row(date, new_category, new_amount_money, new_description)

        elif choice == "4":
            search_date = input(
                "Введите дату для поиска (оставьте поле пустым если поиск не по дате): "
            )
            search_category = input(
                "Введите категорию(Расход или Доход) для поиска (оставьте поле пустым если поиск не по категории): "
            )
            search_amount = input(
                "Введите сумму денег для поиска (оставьте поле пустым если поиск не по сумме денег): "
            )
            results = wallet.search_row(search_date, search_category, search_amount)
            if results:
                for result in results:
                    print(result)
            print()

        else:
            print("Некорректный ввод, повторите попытку.\n")
