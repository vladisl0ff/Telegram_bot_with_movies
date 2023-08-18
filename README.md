# Telegram bot with movies
This project entails a Telegram bot developed using Python and the aiogram framework. The bot is designed to provide film enthusiasts with a range of features, including access to film information, subscription management, and random film suggestions. The project showcases how to integrate with the Telegram Bot API, manage user interactions, and interact with a film database.

**Key Features:**

1. **Film Information:** The bot offers users the ability to access detailed information about films. Users can input film numbers to retrieve film details, such as title, rating, country, release date, genre, and a link to watch the film online.

2. **Subscription Management:** Users can subscribe to specific channels and genres. The bot checks the user's subscription status and provides tailored recommendations based on their preferences.

3. **Random Film Suggestions:** Users can receive random film suggestions. The bot ensures that these suggestions align with the user's subscription preferences, enhancing their film discovery experience.

4. **Administration Commands:** Administrators have access to commands for managing the film database. They can add, update, and delete film entries, as well as perform bulk messaging operations.

5. **Error Handling:** The bot handles errors gracefully, ensuring that users receive appropriate responses even in case of incorrect inputs or issues.

**Dependencies:**

- aiogram: Python framework for interacting with the Telegram Bot API.
- hdrezka_pars: Custom module for parsing film information from a website.
- config: Configuration module for storing bot-related settings.
- keyboards: Custom module providing keyboard layouts for user interaction.
- db: Custom module for managing user data in a SQLite database.
- db_films: Custom module for managing film data in a separate SQLite database.

**Usage:**

1. Users initiate interactions with the bot using the "/start" command.
2. The bot guides users through available commands, including film search, subscription management, and more.
3. Users can request film information using film numbers and receive details such as rating, country, and genre.
4. Subscription management allows users to customize their film suggestions based on channels and genres.
5. Administrators have access to commands for managing the film database and performing bulk messaging.

Note: This project demonstrates interaction with a specific film-related website and database setup. Users can further customize and expand the bot's capabilities to suit their preferences.

Feel free to explore the code and adapt it for your own projects. If you have any questions or require assistance, please don't hesitate to ask.
