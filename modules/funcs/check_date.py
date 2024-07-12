from datetime import datetime


def check_date(date: str) -> str:
    def is_valid_date(a: int, b: int, c: int) -> bool:
        """
        Проверяет, может ли данная дата a.b.20c быть действительной.

        :param a: День
        :param b: Месяц
        :param c: Год (последние две цифры)
        :return: True, если дата действительная, иначе False
        """
        if a < 1 or b < 1 or b > 12:
            return False

        year = 2000 + c
        max_days = max_days_in_month(year, b)

        return 1 <= a <= max_days

    def max_days_in_month(year: int, month: int) -> int:
        """
        Возвращает максимальное количество дней в указанном месяце и году.

        :param year: Год
        :param month: Месяц (1-12)
        :return: Максимальное количество дней в месяце
        """
        if month < 1 or month > 12:
            raise ValueError("Месяц должен быть в диапазоне от 1 до 12")

        if month == 2:
            if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
                return 29
            else:
                return 28
        elif month in [4, 6, 9, 11]:
            return 30
        else:
            return 31

    try:
        date = date.replace("/", ".").replace(",", ".").replace(".", " ").strip().split()
        if (len(date[0]) == 4 and 2 <= len(date[1]) + len(date[-1]) <= 4
                and 0 < int(date[1]) < 13 and 0 < int(date[-1]) <= max_days_in_month(int(date[0]), int(date[1]))):
            return '.'.join(date[::-1])
        elif (len(date[-1]) == 4 and 2 <= len(date[1]) + len(date[0]) <= 4
              and 0 < int(date[1]) < 13 and 0 < int(date[0]) <= max_days_in_month(int(date[-1]), int(date[1]))):
            return '.'.join(date)
        elif len(date) == 3 and len(date[0]) in [1, 2] and len(date[1]) in [1, 2] and len(date[2]) == 2:
            if is_valid_date(int(date[0]), int(date[1]), int(date[2])):
                return f"{'0'*(2 - len(date[0]))}{date[0]}.{'0'*(2 - len(date[1]))}{date[1]}.20{date[-1]}"
            elif is_valid_date(int(date[-1]), int(date[1]), int(date[0])):
                return f"{'0'*(2 - len(date[-1]))}{date[-1]}.{'0'*(2 - len(date[1]))}{date[1]}.20{date[0]}"
            return datetime.now().strftime('%d.%m.%Y')
        else:
            return datetime.now().strftime('%d.%m.%Y')
    except Exception as ex:
        return datetime.now().strftime('%d.%m.%Y')
