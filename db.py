import sqlite3


class Database:
    def __init__(self, db_file: str) -> None:
        """
        Initializes a Database object.

        Args:
            db_file (str): The path to the SQLite database file.
        """
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

    def user_exists(self, user_id: int) -> bool:
        """
        Checks if a user with the given user_id exists in the database.

        Args:
            user_id (int): The ID of the user to check.

        Returns:
            bool: True if the user exists, False otherwise.
        """
        with self.connection:
            result = self.cursor.execute("SELECT * FROM `users` WHERE `user_id` = ?", (user_id,)).fetchmany(1)
            return bool(len(result))

    def add_user(self, user_id: int) -> None:
        """
        Adds a new user to the database.

        Args:
            user_id (int): The ID of the new user.

        Returns:
            None
        """
        with self.connection:
            self.cursor.execute("INSERT INTO `users` (`user_id`) VALUES (?)", (user_id,))

    def set_active(self, user_id: int, active: bool) -> None:
        """
        Sets the active status of a user.

        Args:
            user_id (int): The ID of the user.
            active (bool): The active status to set.

        Returns:
            None
        """
        with self.connection:
            self.cursor.execute("UPDATE `users` SET `active` = ? WHERE `user_id` = ?", (active, user_id,))

    def get_users(self) -> list:
        """
        Retrieves user IDs and their active status from the database.

        Returns:
            list: A list containing tuples of user IDs and their active status.
        """
        with self.connection:
            return self.cursor.execute("SELECT `user_id`, `active` FROM `users`").fetchall()

    def get_request(self, user_id: int) -> tuple:
        """
        Retrieves and updates the request count for a user.

        Args:
            user_id (int): The ID of the user.

        Returns:
            tuple: A tuple containing the cursor execute result and the updated request count.
        """
        with self.connection:
            request = self.cursor.execute("SELECT `request` FROM `users` WHERE `user_id` = ?", (user_id,)).fetchmany(1)
            request = int(request[0][0]) + 1
            result = self.cursor.execute("UPDATE `users` SET `request` = ? WHERE `user_id` = ?", (request, user_id,))
            return result, request

    def total_request(self, user_id: int) -> int:
        """
        Retrieves the total request count for a user.

        Args:
            user_id (int): The ID of the user.

        Returns:
            int: The total request count for the user.
        """
        with self.connection:
            return self.cursor.execute("SELECT `request` FROM `users` WHERE `user_id` = ?", (user_id,)).fetchmany(1)[0][0]

    def sum_request(self) -> int:
        """
        Calculates and retrieves the total sum of request counts from all users.

        Returns:
            int: The total sum of request counts.
        """
        with self.connection:
            return self.cursor.execute("SELECT SUM(`request`) FROM `users`").fetchall()[0][0]
