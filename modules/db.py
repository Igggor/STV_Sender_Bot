import sqlite3


class UserDatabase:
    def __init__(self, db_name="users.db"):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users
                               (id INTEGER PRIMARY KEY, family_name TEXT)''')
        self.connection.commit()

    def add_user(self, user_id, family_name):
        if not self.user_exists(user_id):
            self.cursor.execute("INSERT INTO users (id, family_name) VALUES (?, ?)", (user_id, family_name))
            self.connection.commit()
        else:
            print(f"User with ID {user_id} already exists.")

    def get_family_name(self, user_id):
        self.cursor.execute("SELECT family_name FROM users WHERE id = ?", (user_id,))
        result = self.cursor.fetchone()
        if result:
            return result[0]
        return None

    def update_family_name(self, user_id, new_family_name):
        if self.user_exists(user_id):
            self.cursor.execute("UPDATE users SET family_name = ? WHERE id = ?", (new_family_name, user_id))
            self.connection.commit()
        else:
            self.add_user(user_id=user_id, family_name=new_family_name)
            print(f"User with ID {user_id} does not exist.")

    def user_exists(self, user_id):
        self.cursor.execute("SELECT 1 FROM users WHERE id = ?", (user_id,))
        return self.cursor.fetchone() is not None

    def close(self):
        self.connection.close()


# Пример использования
if __name__ == "__main__":
    db = UserDatabase()

    # Добавление пользователя
    db.add_user(1, "Ivanov")

    # Проверка существования пользователя
    print(db.user_exists(1))  # True
    print(db.user_exists(2))  # False

    # Получение фамилии пользователя
    print(db.get_family_name(1))  # Ivanov

    # Обновление фамилии пользователя
    db.update_family_name(1, "Petrov")

    # Проверка обновления фамилии
    print(db.get_family_name(1))  # Petrov

    # Закрытие базы данных
    db.close()
