from functools import total_ordering

from src.convert_salary import ConvertSalary

@total_ordering
class Vacancy:
    """Класс для работы с вакансиями"""

    def __init__(self, title, company_name, location, url, salary, requirements, experience):
        """Метод инициализации вакансий по выбранным параметрам"""
        self.title = self.validate_title(title)
        self.company_name = self.validate_company_name(company_name)
        self.location = self.validate_location(location)
        self.url = self.validate_url(url)
        self.salary = self.validate_salary(salary)
        self.requirements = self.validate_requirements(requirements)
        self.experience = self.validate_experience(experience)

    def validate_title(self, title):
        """Метод валидации параметра Название Вакансии"""
        try:
            if isinstance(title, str) or len(title.strip()) > 0:
                return title.strip()
        except (ValueError, AttributeError):
            pass
        return 'Не указано'

    def validate_company_name(self, company_name):
        """Метод валидации параметра Название Компании"""
        try:
            if isinstance(company_name, str) or len(company_name.strip()) > 0:
                return company_name.strip()
        except (ValueError, AttributeError):
            pass
        return 'Не указано'

    def validate_location(self, location):
        """Метод валидации параметра Город"""
        try:
            if isinstance(location, str) or len(location.strip()) > 0:
                return location.strip()
        except (ValueError, AttributeError):
            pass
        return 'Не указано'

    def validate_url(self, url):
        """Метод валидации параметра Ссылка на вакансию"""
        try:
            if isinstance(url, str) or len(url.strip()) > 0:
                return url.strip()
        except (ValueError, AttributeError):
            pass
        return 'Не указано'
    def validate_salary(self, salary):
        """Метод валидации параметра Зарплата"""
        try:
            if isinstance(salary, str) or len(salary.strip()) > 0:
                return salary.strip()
        except (ValueError, AttributeError):
            pass
        return 'Не указано'

    def validate_requirements(self, requirements):
        """Метод валидации параметра Требования"""
        try:
            if isinstance(requirements, str) or len(requirements.strip()) > 0:
                return requirements.strip()
        except (ValueError, AttributeError):
            pass
        return 'Не указано'

    def validate_experience(self, experience):
        """Метод валидации параметра Опыт работы"""
        try:
            if isinstance(experience, str) or len(experience.strip()) > 0:
                return experience.strip()
        except (ValueError, AttributeError):
            pass
        return 'Не указано'

    def __lt__(self, other):
        """Метод для сравнения вакансий"""
        return ConvertSalary.convert_salary(self.salary) < ConvertSalary.convert_salary(other.salary)

    # Остальные методы сравнения будут добавлены декоратором total @total_ordering

    def __str__(self):
        """Метод для вывода вакансии на печать для пользователя"""
        return f'Название вакансии: {self.title},\n' \
               f'Название компании: {self.company_name}\n' \
               f'Город: {self.location}\n' \
               f'Ссылка на вакансию: {self.url}\n' \
               f'Зарплата: {self.salary}\n' \
               f'Требования: {self.requirements}\n' \
               f'Опыт работы: {self.experience}\n'

