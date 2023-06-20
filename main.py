from api.headhunter_api import HeadHunterApi
from api.superjob_api import SuperJobApi
from vacancies.vacancy import Vacancy
from vacancies.vacancy_storage import JsonStorage
from vacancies.vacancy_filter import VacancyFilter

def user_interaction():
    """Функция для взаимодействия с пользователем"""
    platforms = ['HeadHunter', 'SuperJob']
    # Вакансии пользователя полученные в текущей сессии работы программы
    user_vacancies = []
    json_store = JsonStorage()

    # Предоставляем пользователю выбор, с какой платформой он хочет работать
    # Программа будет работать пока пользователь не введет 0
    while True:
        user_platform = input(f'Выбери платформу, с которой хочешь начать работать:\n'
                              f'Введи 1 для выбора {platforms[0]}\n'
                              f'Введи 2 для выбора {platforms[1]}\n'
                              f'Введи 3 для выбора работы с обеими платформами\n'
                              f'Введи 0 для выхода из программы\n')

        if user_platform == '0':
            print('Работа программы завершена')
            break

        if user_platform not in ['1', '2', '3']:
            print('Некорректный ввод, попробуй еще раз')
            continue

        keyword = input('Введи поисковый запрос по которому ищем вакансии, '
                        'либо нажми Enter для работы со всеми вакансиями.\n')

        # Если появляется исключение, возвращаем пользователя в начало программы
        try:
            vacancies_count = int(input('Какое количество топ-вакансий ты хочешь получить?\n'))
            if vacancies_count <= 0:
                raise ValueError
        except ValueError:
            print('Некорректный ввод. Попробуй еще раз')
            continue

        filter_words = input('Введи ключевые слова для фильтрации вакансий, '
                             'либо нажми Enter чтобы пропустить фильтрацию.\n')

        # Создаем объекты классов
        hh = HeadHunterApi()
        sj = SuperJobApi()

        # Получаем списки отформатированных вакансий, распаковывая их через класс Vacancy
        hh_vacancies = [Vacancy(**vacancy) for vacancy in hh.get_vacancies(keyword)]
        sj_vacancies = [Vacancy(**vacancy) for vacancy in sj.get_vacancies(keyword)]

        # Выдаем пользователю список в зависимости от выбора
        if user_platform == '1':
            print(f'Выбранная платформа: {platforms[0]}')
            user_vacancies = sorted(VacancyFilter.filter_vacancies(filter_words, hh_vacancies)[:vacancies_count], reverse=True)

        elif user_platform == '2':
            print(f'Выбранная платформа: {platforms[1]}')
            user_vacancies = sorted(VacancyFilter.filter_vacancies(filter_words, sj_vacancies)[:vacancies_count], reverse=True)

        elif user_platform == '3':
            print(f'Выбранные платформы: {platforms[0]}, {platforms[1]}')
            user_vacancies = sorted(VacancyFilter.filter_vacancies(filter_words, hh_vacancies, sj_vacancies)[:vacancies_count], reverse=True)

        # Проверяем, были ли найдены вакансии по запросу пользователя
        if user_vacancies:
            print(f'Найдено вакансий по твоему запросу:{len(user_vacancies)}\n'
                  'Вот список:\n')
            for i, v in enumerate(user_vacancies, start=1):
                print(f'{i}. {v}\n')

            user_add_vacancy = input('Добавить вакансии в избранное? (да / нет)\n'
                                     'Если такая же вакансия есть в избранном, она не будет добавлена повторно.\n')  # Избранное - это файл JSON

            # Если пользователь отвечает 'да', добавляем все вакансии в файл
            if user_add_vacancy.lower() == 'да':
                for v in user_vacancies:
                    json_store.add_vacancy(v)
            elif user_add_vacancy.lower() == 'нет':
                print('Вакансии не добавлены')
            else:
                print('Некорректный ввод. Вакансии не добавлены')

        else:
            print('Вакансий по твоему запросу не найдено')

        # Список избранных вакансий пользователя (добавленных в файл JSON)
        favorite_vacancies = json_store.get_all_vacancies()

        # Выводим пользователю второе меню уже для работы с избранными вакансиями
        while True:
            print('\nДоступные опции:')
            print('1. Показать все вакансии из избранного')
            print('2. Поиск вакансий из избранного по зарплате')
            print('3. Удаление вакансии из избранного')
            print('0. Выход в главное меню')

            user_choice = input('Выбери опцию (введи номер): \n')

            if user_choice == '1':
                print('Все вакансии из избранного: \n')
                if favorite_vacancies:
                    for i, v in enumerate(favorite_vacancies, start=0):
                        v = Vacancy(**v)
                        print(f'{i+1}. {v}')
                else:
                    print('В избранном нет вакансий')

            elif user_choice == '2':
                if favorite_vacancies:
                    salary = input(('Введи минимальную зарплату. \n'
                                    'PS. Введи цифру. В случае некорректного ввода будут показаны все вакансии:\n'))
                    filtered_user_vacancies = json_store.get_vacancies_by_salary(salary)
                    if not filtered_user_vacancies:
                        print('Подходящих вакансий не найдено')
                    else:
                        print(f'Вакансии в диапазоне от {salary}:\n')
                        for v in filtered_user_vacancies:
                            print(str(Vacancy(**v)))
                else:
                    print('В избранном нет вакансий')

            elif user_choice == '3':
                try:
                    if favorite_vacancies:
                        vacancy_index = int(input('Введи номер вакансии для удаления: '))
                        all_user_vacancies = json_store.get_all_vacancies()
                        if 1 <= vacancy_index <= len(all_user_vacancies):
                            vacancy = all_user_vacancies[vacancy_index-1]
                            json_store.delete_vacancy(vacancy)
                            print(f'Вакансия "{Vacancy(**vacancy)}" удалена из Избранного.')
                        else:
                            print('Некорректный номер вакансии.')
                    else:
                        print('В избранном нет вакансий')
                except ValueError:
                    print('Некорректный номер вакансии. Введи число')

            elif user_choice == '0':
                print('Выход в главное меню.')
                break

            else:
                print('Некорректный выбор опции.')

        # Сохранение вакансий в файл JSON
        json_store.save_vacancies()

    else:
        print('Некорретный ввод, попробуй еще раз')

if __name__ == '__main__':
    user_interaction()