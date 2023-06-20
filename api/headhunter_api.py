import requests
from api.job_api import JobAPI


class HeadHunterApi(JobAPI):
    """Класс для получения вакансий с Headhunter"""

    pages_count = 20
    base_url = 'https://api.hh.ru/vacancies'
    params = {
        'per_page': 100,
        'page': 0,
        'only_with_salary': True,
        'order_by': 'publication_time'
    }

    def search_vacancies(self, keyword):
        """Метод для поиска вакансий на Headhunter"""
        if keyword:
            self.params['text'] = keyword
        response = requests.get(self.base_url, params=self.params)
        # Вызываем исключение, если произошла ошибка при подключении
        response.raise_for_status()
        data = response.json()
        return data.get('items', [])

    @staticmethod
    def format_salary(salary):
        """Метод для форматирования зарплаты"""
        if salary is None:
            return 'Зарплата не указана'

        # Если зарплата указана в валютах из словаря ниже, преобразуем ее в рубли умножая на средний курс
        rates = {'RUR': 1, 'USD': 80, 'EUR': 85, 'KZT': 0.18, 'BYR': 32}
        currency = salary['currency']
        if currency in rates:
            rate = rates[currency]

            from_salary = salary['from']
            to_salary = salary['to']

            if from_salary is not None and to_salary is not None and from_salary != to_salary:
                formatted_salary = f"{from_salary * rate}-{to_salary * rate} руб."
            elif from_salary == to_salary:
                formatted_salary = f'{from_salary * rate} руб.'
            elif from_salary is None:
                formatted_salary = f'{to_salary * rate} руб.'
            elif to_salary is None:
                formatted_salary = f'{from_salary * rate} руб.'

            return formatted_salary

        # Если в вакансии будет валюта, которой нет в словаре, возвращаем строку
        return 'Неизвестная валюта'

    @staticmethod
    def format_vacancy(vacancy):
        """Метод для форматирования вакансии"""
        formatted_salary = HeadHunterApi.format_salary(vacancy.get('salary'))
        # Добавляем в новый словарь вакансии необходимые для работы ключи/значения
        formatted_vacancy = {
            'title': vacancy['name'],
            'company_name': vacancy['employer']['name'],
            'location': vacancy['area']['name'],
            'url': vacancy['url'],
            'salary': formatted_salary,
            'requirements': vacancy['snippet']['requirement'],
            'experience': vacancy['experience']['name']
        }

        return formatted_vacancy

    def get_vacancies(self, keyword):
        """Метод для получения итогового списка вакансий"""
        vacancies = []
        # Получаем список отформатированных вакансий
        # Обрабатываем исключение подключения по API
        try:
            vacancies_data = [vacancy for self.params['page'] in range(self.pages_count)
                              for vacancy in self.search_vacancies(keyword)]

            vacancies = [self.format_vacancy(vacancy) for vacancy in vacancies_data]

        except (requests.exceptions.HTTPError,
                requests.exceptions.ConnectionError,
                requests.exceptions.Timeout,
                requests.exceptions.TooManyRedirects,
                requests.exceptions.RequestException) as e:
            print(f'Произошла ошибка при запросу к API: {e}')

        return vacancies

