import sqlite3


class ApplicationDB:
    def __init__(self, db_name='applications.db'):
        self.db_name = db_name

    def _connect(self):
        return sqlite3.connect(self.db_name)

    def add_application(self, name, position, day, status, link, description, place):
        con = self._connect()
        cursor = con.cursor()
        cursor.execute(
            "INSERT INTO Applications (NAME_OF_COMPANY, NAME_OF_POSITION, DAY_OF_APPLICATION, STATUS_OF_APPLICATION, LINK_TO_APPLICATION, DESCRIPTION_OF_APPLICATION, PLACE_OF_APPLICATION) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (name, position, day, status, link, description, place))
        con.commit()
        cursor.close()
        con.close()

    def view_all_applications(self):
        con = self._connect()
        cursor = con.cursor()
        cursor.execute("SELECT * FROM Applications")
        applications = cursor.fetchall()
        cursor.close()
        con.close()
        return applications

    def update_application_status(self, app_id, new_status):
        con = self._connect()
        cursor = con.cursor()
        cursor.execute("UPDATE Applications SET STATUS_OF_APPLICATION = ? WHERE ID = ?", (new_status, app_id))
        con.commit()
        cursor.close()
        con.close()

    def delete_application(self, app_id):
        con = self._connect()
        cursor = con.cursor()
        cursor.execute("DELETE FROM Applications WHERE ID = ?", (app_id,))
        con.commit()
        cursor.close()
        con.close()

    def delete_all_applications(self):
        con = self._connect()
        cursor = con.cursor()
        cursor.execute("DELETE FROM Applications")
        con.commit()
        cursor.close()
        con.close()

    def find_application(self, word):
        con = self._connect()
        cursor = con.cursor()
        query = """
            SELECT * FROM Applications 
            WHERE 
                NAME_OF_COMPANY LIKE ? OR 
                NAME_OF_POSITION LIKE ? OR 
                DESCRIPTION_OF_APPLICATION LIKE ?
        """
        # Используем wildcard '%' для поиска вхождений слова в текстовые поля
        search_pattern = f'%{word}%'
        cursor.execute(query, (search_pattern, search_pattern, search_pattern))
        applications = cursor.fetchall()
        cursor.close()
        con.close()
        return applications
