import requests
import time
from api.job_api import JobAPI


class SuperJobApi(JobAPI):
    """Метод для получения вакансий с Superjob"""

    pages_count = 20
    base_url = 'https://api.superjob.ru/2.0/vacancies'
    api_key = 'v3.r.137609179.eb956284d01342da2b909062e33767f1abf856e0.b8761058fa096dbf70d434cd24bacb64f601adab'
    headers = {'X-Api-App-Id': api_key}
    params = {
        'count': 100,
        'page': 0,
        'no_agreement': 1,
        'sort_new': int(time.time())
    }

    def search_vacancies(self, keyword):
        """Метод для поиска вакансий на Superjob"""
        if keyword:
            self.params['keyword'] = keyword

        responce = requests.get(self.base_url, headers=self.headers, params=self.params)
        # Вызываем исключение, если произошла ошибка при подключении
        responce.raise_for_status()
        data = responce.json()
        return data.get('objects', [])

    @staticmethod
    def format_salary(salary_from, salary_to):
        """Метод для форматирования зарплаты"""
        if salary_from != 0 and salary_to != 0:
            formatted_salary = f"{salary_from}-{salary_to} руб."
        elif salary_from == salary_to:
            formatted_salary = f'{salary_from} руб.'
        elif salary_from == 0:
            formatted_salary = f'{salary_to} руб.'
        elif salary_to == 0:
            formatted_salary = f'{salary_from} руб.'
        else:
            formatted_salary = 'Зарплата не указана'

        return formatted_salary

    @staticmethod
    def format_vacancy(vacancy):
        """Метод для форматирования вакансий"""
        salary_from = vacancy.get('payment_from')
        salary_to = vacancy.get('payment_to')
        formatted_salary = SuperJobApi.format_salary(salary_from, salary_to)
        # Добавляем в новый словарь вакансии необходимые для работы ключи/значения
        formatted_vacancy = {
            'title': vacancy['profession'],
            'company_name': vacancy['firm_name'],
            'location': vacancy['town']['title'],
            'url': vacancy['link'],
            'salary': formatted_salary,
            'requirements': vacancy['candidat'],
            'experience': vacancy['experience']['title']
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
