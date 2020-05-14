from application.salary import *
from application.db.people import *
from datetime import date


print(f'Программа "Бухгалтерия" ({date.today()})')


if __name__ == '__main__':
    calculate_salary()
    get_employees()
