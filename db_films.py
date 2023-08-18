import sqlite3

from typing import List, Any


class Database_film:
    def __init__(self, db_file: str) -> None:
        """
        Initializes a Database_film object.

        Args:
            db_file (str): The path to the SQLite database file.
        """
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

    def films_exists(self, film_id: int) -> bool:
        """
        Checks if a film with the given film_id exists in the database.

        Args:
            film_id (int): The ID of the film to check.

        Returns:
            bool: True if the film exists, False otherwise.
        """
        with self.connection:
            result = self.cursor.execute("SELECT * FROM `films` WHERE `film_id` = ?", (film_id,)).fetchmany(1)
            return bool(len(result))

    def film(self, film_id: int) -> tuple:
        """
        Retrieves information about a film with the given film_id.

        Args:
            film_id (int): The ID of the film to retrieve.

        Returns:
            tuple: A tuple containing information about the film.
        """
        with self.connection:
            return self.cursor.execute("SELECT * FROM `films` WHERE `film_id` = ?", (film_id,)).fetchone()

    def add_film(self, film_id: int, img: str, name: str, rating: float, country: str, data: str, genre: str, url: str) -> None:
        """
        Adds a new film to the database.

        Args:
            film_id (int): The ID of the new film.
            img (str): URL or path to the film's image.
            name (str): The name of the film.
            rating (float): The rating of the film.
            country (str): The country of origin of the film.
            data (str): Release date or other relevant data.
            genre (str): The genre of the film.
            url (str): URL or path to the film's resource.

        Returns:
            None
        """
        with self.connection:
            self.cursor.execute("INSERT INTO `films` (`film_id`, `img`, `name`, `rating`, `country`, `data`, `genre`, `URL`) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                               (film_id, img, name, rating, country, data, genre, url))

    def update_film(self, film_id: int, img: str, name: str, rating: float, country: str, data: str, genre: str, url: str) -> None:
        """
        Updates information about a film in the database.

        Args:
            film_id (int): The ID of the film to update.
            img (str): URL or path to the film's image.
            name (str): The name of the film.
            rating (float): The rating of the film.
            country (str): The country of origin of the film.
            data (str): Release date or other relevant data.
            genre (str): The genre of the film.
            url (str): URL or path to the film's resource.

        Returns:
            None
        """
        with self.connection:
            self.cursor.execute("UPDATE `films` SET `img` = ?, `name` = ?, `rating` = ?, `country` = ?, `data` = ?, `genre` = ?, `URL` = ?  WHERE `film_id` = ?",
                               (img, name, rating, country, data, genre, url, film_id,))

    def films_len(self) -> list:
        """
        Retrieves the names of all films in the database.

        Returns:
            list: A list containing the names of all films.
        """
        with self.connection:
            return self.cursor.execute("SELECT `name` FROM `films`").fetchall()

    def id_film(self, id_f: int) -> List[Any]:
        """
        Retrieves the film_id of a film with the given id.

        Args:
            id_f (int): The id of the film.

        Returns:
            tuple: A tuple containing the film_id.
        """
        with self.connection:
            return self.cursor.execute("SELECT `film_id` FROM `films` WHERE `id` = ?",
                                       (id_f,)).fetchmany(1)

    def img_overwriting(self, film_id: int, img: str) -> None:
        """
        Overwrites the image URL of a film with the given film_id.

        Args:
            film_id (int): The ID of the film.
            img (str): URL or path to the new image.

        Returns:
            None
        """
        with self.connection:
            self.cursor.execute("UPDATE `films` SET `img` = ? WHERE `film_id` = ?", (img, film_id,))

    def del_film(self, film_id: int) -> None:
        """
        Deletes a film with the given film_id from the database.

        Args:
            film_id (int): The ID of the film to delete.

        Returns:
            None
        """
        with self.connection:
            self.cursor.execute("DELETE FROM `films` WHERE `film_id` = ?", (film_id,))

    def film_genre(self, genre: str) -> list:
        """
        Retrieves information about films of a specific genre.

        Args:
            genre (str): The genre to filter by.

        Returns:
            list: A list containing information about films of the specified genre.
        """
        with self.connection:
            return self.cursor.execute("SELECT * FROM films WHERE genre LIKE ?", ('%'+genre+'%',)).fetchall()

    def add_video(self, film_id: int, URL_film: str) -> None:
        """
        Adds a video URL for a film with the given film_id.

        Args:
            film_id (int): The ID of the film.
            URL_film (str): URL or path to the film's video.

        Returns:
            None
        """
        with self.connection:
            self.cursor.execute("UPDATE `films` SET `URL_film` = ? WHERE `film_id` = ?", (URL_film, film_id,))
