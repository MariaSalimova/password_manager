import random
import sets_of_characters
# с помощью данного класса реализованы функции генерации и проверки надежности пароля


class Password:
    def __init__(self, length=None, set_of_characters=None, password=''):
        self.length = length
        self.set_of_characters = set_of_characters
        self.password = password

    def generate_password(self):
        self.password = ''.join([random.choice(list(self.set_of_characters)) for i in range(self.length)])
        return self.password

    # метод password_reliability_check используется для проверки пароля введенного пользователем
    # или сгенерированого программой
    @ staticmethod
    def password_reliability_check(password):
        if len(password) < 8:
            length_status = 1
        elif 8 <= len(password) <= 32:
            length_status = 2
        else:
            length_status = 3
        if len(set(password)) == 1 or len(password) == 0:
            unique_characters = 1
        elif len(password) // 2 <= len(set(password)) <= len(password):
            unique_characters = 2
        else:
            unique_characters = 1
        if str.lower(password) == password or str.upper(password) == password:
            capitals_and_lowercase = 1
        else:
            capitals_and_lowercase = 2
        if len(set(password).intersection(sets_of_characters.symbols)) == 0:
            symbols_status = 1
        elif 0 < len(set(password).intersection(sets_of_characters.symbols)) <= 8:
            symbols_status = 2
        else:
            symbols_status = 3
        if len(set(password).intersection(sets_of_characters.numbers)) == 0:
            numbers_status = 1
        elif 0 < len(set(password).intersection(sets_of_characters.numbers)) <= 8:
            numbers_status = 2
        else:
            numbers_status = 3
        password_status = length_status + unique_characters + capitals_and_lowercase + numbers_status + symbols_status
        if password_status == 1:
            return 'Ненадежный пароль'
        elif password_status == 2:
            return 'Пароль среднего уровня надежности'
        else:
            return 'Надежный пароль'
