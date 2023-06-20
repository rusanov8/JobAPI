from abc import ABC, abstractmethod

class JobAPI(ABC):
    """Абстрактный класс для работы с api"""

    @abstractmethod
    def get_vacancies(self, keyword):
        pass