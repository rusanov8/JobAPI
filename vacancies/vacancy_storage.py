import json
from abc import ABC, abstractmethod
from src.convert_salary import ConvertSalary
import os

class VacancyStorage(ABC):
    """Абстрактный класс для работы с файлом Json"""

    @abstractmethod
    def add_vacancy(self, vacancy):
        pass

    @abstractmethod
    def get_vacancies_by_salary(self, salary):
        pass

    @abstractmethod
    def delete_vacancy(self, vacancy):
        pass

# Константа для указания пути к файлу JSON
CURRENT_DIRECTORY = os.getcwd()
FILE_PATH = os.path.join(CURRENT_DIRECTORY, 'user_vacancies.json')

class JsonStorage(VacancyStorage):
    """Класс для добавления, удаления и поиска вакансий в файле Json"""

    def __init__(self):
        self.filename = FILE_PATH
        self.vacancies = self.load_vacancies()

    def load_vacancies(self):
        """Метод для загрузки вакансий из файла"""
        # Обрабатываем возможные исключения, если изначально файл Json пустой либо не существует
        try:
            with open(self.filename, 'r') as file:
                return json.load(file)
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f'Ошибка: {e}')
            return []

    def save_vacancies(self):
        """Метод для сохранения вакансий в файл"""
        # Обрабатываем возможные исключения
        try:
            with open(self.filename, 'w') as file:
                json.dump(self.vacancies, file, ensure_ascii=False, indent=2)
        except (IOError, FileNotFoundError):
            print('Ошибка при сохранении данных в файл')

    def add_vacancy(self, vacancy):
        """Метод для добавления вакансий"""
        # Добавляем вакансию только в случае, если ее еще нет в файле
        if vacancy.__dict__ not in self.vacancies:
            self.vacancies.append(vacancy.__dict__)
            self.save_vacancies()

    def get_vacancies_by_salary(self, salary):
        """Метод для поиска вакансий в файле по зарплате"""
        converted_salary = ConvertSalary.convert_salary(salary)
        matching_vacancies = []
        for vacancy in self.vacancies:
            # Поиск реализован по принципу, что пользователь вводит минимальную желаемую зарплату
            if ConvertSalary.convert_salary(vacancy['salary']) >= converted_salary:
                matching_vacancies.append(vacancy)
        return matching_vacancies

    def delete_vacancy(self, vacancy):
        """Метод для удаления вакансий из файла"""
        if vacancy in self.vacancies:
            self.vacancies.remove(vacancy)
            self.save_vacancies()

    def get_all_vacancies(self):
        """Метод для получения всех вакансий из файла"""
        return self.vacancies