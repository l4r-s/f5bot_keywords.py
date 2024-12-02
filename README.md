[![Sponsor](https://img.shields.io/badge/Sponsor-❤-EA4AAA.svg)](https://github.com/sponsors/l4r-s)

# f5bot_keywords.py

This script automates the process of adding keywords to F5Bot. It supports loading keywords from a YAML file and uses a session-based approach for authentication and interaction with F5Bot's web interface.

## Features

- Automates keyword addition to F5Bot.
- Reads keywords, settings, and flags from a YAML configuration file.
- Logs in to F5Bot using credentials (from command-line arguments or environment variables).
- Handles optional configurations like enabling/disabling keywords and matching whole words.
- Implements error handling for adding keywords.
- Uses a random delay between requests to avoid overloading the server.

## Responsible Usage and Fair Use of F5Bot

**F5Bot** is a **free service** that helps users monitor mentions of keywords across various platforms. It is provided at no cost by the F5Bot creators, who dedicate their time and resources to maintain this valuable tool. 

### Use Responsibly

While this script is designed to make managing your F5Bot account easier, **it is crucial to use it responsibly**. Adding an excessive number of keywords or creating unnecessary traffic can strain F5Bot's infrastructure, negatively affecting other users and the service itself.

To prevent overloading F5Bot:
- The script includes a **random delay** (between 1 to 7 seconds) between each keyword addition. This delay reduces the risk of overwhelming F5Bot's servers with rapid requests, helping to ensure fair usage.
- Avoid adding an unreasonable number of keywords in a single session. If you need advanced functionality, consider reaching out to F5Bot for support or feature requests.

### Unfair Use Is Uncool

**Abusing F5Bot is not only unfair to its creators but also uncool.** By respecting the service and its limitations, you contribute to keeping it available and free for everyone. Let’s support free tools like F5Bot by using them ethically and responsibly. 🌟

Remember: Good tools deserve good users.

## Requirements

Install the required Python packages using the following command:

```bash
pip install -r req.txt
```

## Usage

### Command-Line Arguments

```bash
./f5bot_keywords.py -h
usage: f5bot_keywords.py [-h] [-u USERNAME] [-p PASSWORD] -i INPUT

Add keywords to F5Bot.

options:
  -h, --help            Show this help message and exit
  -u USERNAME, --username USERNAME
                        Username for F5Bot (can also be set via `F5BOT_USERNAME` environment variable)
  -p PASSWORD, --password PASSWORD
                        Password for F5Bot (can also be set via `F5BOT_PASSWORD` environment variable)
  -i INPUT, --input INPUT
                        Input YAML file with keywords
```

### Example Command

```bash
./f5bot_keywords.py -u "your_username" -p "your_password" -i keywords.example.yml
```

## YAML Configuration File

The script uses a YAML file to define the keywords to track. Below is an example configuration (`keywords.example.yml`):

```yaml
track_keywords:
  - keyword: "Keyword to watch 1"
    enabled: true
  - keyword: "Keyword to watch 2"
    enabled: false
    whole_word: true
    flags: "no-reddit, no-posts"
```

### Explanation of Fields:
- `keyword`: The keyword to be added to F5Bot.
- `enabled`: Whether the keyword is enabled (default: `true`).
- `whole_word`: Whether the keyword should match only whole words (default: `false`).
- `flags`: Flags to customize alerts (optional).

## Environment Variables

Instead of passing credentials via command-line arguments, you can set the following environment variables:

- `F5BOT_USERNAME`: Your F5Bot username.
- `F5BOT_PASSWORD`: Your F5Bot password.

Example:
```bash
export F5BOT_USERNAME="your_username"
export F5BOT_PASSWORD="your_password"
```

## License

This project is licensed under the MIT License. See `LICENSE` for details.

---

Enjoy automating your F5Bot keyword management! 🚀