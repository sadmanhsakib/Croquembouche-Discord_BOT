# Croquembouche Discord Bot

A feature-rich Discord bot designed to serve as a personal assistant. It tracks countdowns, logs user activity, and offers dynamic configuration via a PostgreSQL database.

## Invite?
This BOT is only designed to manage my personal server. Thus, I can't allow it to be added to other servers.<br>
Instead, I have a much better version of this bot that is available for public use. <br>
If you want to add that BOT a.k.a **Croissant** in your Discord server, feel free to add it to your server by clicking [here](https://discord.com/oauth2/authorize?client_id=1419550251739516959&permissions=1374389746800&integration_type=0&scope=bot).

## 🚀 Features

- **Countdown Tracker**: Create, manage, and track countdowns to specific dates. The bot sends reminders when you come online.
- **Activity Logging**: Automatically logs when a specific user comes online and goes offline, calculating the duration of their session.
- **Dynamic Configuration**: Manage bot settings (prefix, logging status, channels) directly through Discord commands without restarting.
- **General Utilities**:
  - `bonjour`: Friendly greeting.
  - `status`: Check bot availability.
  - `ping`: Monitor latency.
  - `del`: Bulk delete messages.
- **Database Integration**: Robust data persistence using PostgreSQL.

## 🛠️ Prerequisites

- **Python 3.8+**
- **PostgreSQL Database**
- **Discord Bot Token**

## 📦 Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/yourusername/Croquembouche-Discord_BOT.git
    cd Croquembouche-Discord_BOT
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Set up environment variables:**
    Create a `.env` file in the root directory and add the following:
    ```env
    BOT_TOKEN=your_discord_bot_token
    DATABASE_URL=your_postgresql_connection_string
    USER_ID=target_user_discord_id
    ```

4.  **Run the bot:**
    ```bash
    python main.py
    ```

## ⚙️ Configuration

The bot uses a PostgreSQL database to store dynamic configurations. The database schema is automatically created on the first run.

### Environment Variables (.env)
| Variable | Description |
| :--- | :--- |
| `BOT_TOKEN` | Your Discord Bot Token. |
| `DATABASE_URL` | Connection URL for your PostgreSQL database. |
| `USER_ID` | The Discord User ID to track for activity logging. |

## 🎮 Commands

### General
- `bonjour`: Greets the user.
- `status`: Checks if the bot is online.
- `ping`: Displays the bot's latency.
- `help`: Shows the help menu.

### Countdown Management
- `add countdown <NAME> <DATE>`: Adds a new countdown.
  - Format: `YYYY-MM-DD`
  - Example: `.add countdown Birthday 2024-12-25`
- `rmv countdown <NAME>`: Removes an existing countdown.
- `list`: Lists all active countdowns.

### Administration
- `del <amount>`: Deletes the specified number of messages.
- `set <VARIABLE> <VALUE>`: Updates a configuration variable.
  - **Variables**: `PREFIX`, `SHOULD_LOG`, `COUNTDOWN_CHANNEL_ID`
  - Example: `.set PREFIX !`


## Contributing

This project is the work of a sole contributor.

- **Lead Developer & Maintainer**: [Sadman Sakib](https://github.com/sadmanhsakib)

If you have suggestions, bug reports, or feature requests, please open an issue on the GitHub repository. While external contributions are welcome via Pull Requests, please note that the core vision and maintenance are handled by the author.

## 📄 License

This project is licensed under the PolyForm Noncommercial License 1.0.0 - see the [LICENSE](LICENSE) file for details.