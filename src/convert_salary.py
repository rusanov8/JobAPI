class ConvertSalary:
    """Класс для конвертации зарплаты в int для сравнения и сортировки"""
    @staticmethod
    def convert_salary(salary):
        # Обрабатываем исключение, если будут переданы некорректные значения
        # В случае возникновения исключения возвращаем 0, чтобы программа продолжала работу
        # И при сортировке вакансий такие вакансии с некорректными значениями будут в конце списка
        # Метод обрабатывает все возможные значения, в том числе и строки из классов HeadHunterApi и SuperJobAPI
        try:
            if isinstance(salary, (int, float)):
                return int(salary)

            if isinstance(salary, str):
                salary = salary.replace(' ', '').replace('руб.', '').replace('руб', '').replace('.', '').replace(',', '')

                if '-' not in salary:
                    converted_salary = int(salary)
                else:
                    salary_from, salary_to = salary.split('-')
                    salary_from = salary_from.strip()
                    salary_to = salary_to.strip()

                    if salary_from.isdigit() and salary_to.isdigit():
                        converted_salary = int((int(salary_from) + int(salary_to)) / 2)
                    else:
                        converted_salary = 0

                return converted_salary

        except ValueError:
            return 0