"""Модель учителя"""


class Teacher:
    id: int
    name: str
    grade: str
    sphere: str
    description: str
    nickname: str

    def __init__(self, id: int, name: str, grade: str, sphere: str, description: str, nickname: str):
        """
        :param id:  id telegram
        :param name: имя учителя
        :param grade: уровень знаний
        :param sphere: сфера деятельности
        :param description: описание
        :param nickname: ник в телеграмме, @nick
        """
        self.id = id
        self.name = name
        self.grade = grade
        self.sphere = sphere
        self.description = description
        self.nickname = nickname
