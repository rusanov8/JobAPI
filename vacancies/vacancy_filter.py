class VacancyFilter:
    """Класс для фильтрации вакансий"""
    @staticmethod
    def filter_vacancies(filter_words, *vacancies):
        filter_words = filter_words.lower().split()
        matching_vacancies = []
        # Проверка на ввод пользователем Enter для пропуска фильтрации
        if not filter_words:
            for vacancy in vacancies:
                matching_vacancies.extend(vacancy)
        for vacancy_list in vacancies:
            for vacancy in vacancy_list:
                for word in filter_words:
                    if word.lower() in vacancy.title.lower() or word in vacancy.requirements.lower():
                        matching_vacancies.append(vacancy)

        return matching_vacancies