import uuid


class User:
    def __init__(self, nickname, picture, login, email):
        self._id = str(uuid.uuid4())
        self._nickname = nickname
        self.picture = picture
        self._login = login
        self._email = email

    def nickname(self):
        return self._nickname

    def picture(self):
        return self.picture

    def login(self):
        return self._login

    def email(self):
        return self._email

mock_user = User("Dr.Pepper", "image.jpg", "dr_pepper", "drpepper@gmail.com" )