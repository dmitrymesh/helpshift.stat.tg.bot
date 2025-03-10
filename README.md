# Helpshift Tickets Statistic Bot

## Overview
Helpshift Tickets Statistic Bot collects the number of tickets received in your Helpshift projects and sends statistics to your messenger at a specified interval. If the number of tickets exceeds a certain threshold, it sends multiple warning messages about it.

## Features
- Periodic polling of ticket statistics.
- Displaying statistics in Telegram and/or Mattermost.
- Alarm notifications in Telegram and/or Mattermost if the ticket threshold is exceeded for any project.

## Installation

### Configuration Setup
Before running the bot, configure it by editing the `config.json` file. The configuration should include:

```json
{
    "enabled_channels": ["telegram", "mattermost"], // List of enabled messaging channels

    "helpshift_api_url": "https://api.helpshift.com/v1/YOUR_COMPANY_NAME/issues", // Helpshift API endpoint for fetching ticket statistics (replace YOUR_COMPANY_NAME)
    "helpshift_api_key": "your_api_key_here", // API key for authentication with Helpshift (see [API Key Management](https://support.helpshift.com/hc/en/13-helpshift-technical-support/faq/769-in-app-support-guide-api-key-management/#1.-finding-your-api-keys))

    "telegram_bot_token": "your_telegram_bot_token_here", // Example: "bot552154641:ADGMGav2RYsV2G0QLs4TTelPoKdjT2Dkqvy" (see [Telegram Bot Guide](https://core.telegram.org/bots/tutorial))
    "telegram_chat_id": "your_main_chat_id_here", // Telegram chat ID where statistics are sent
    "telegram_alarm_chat_id": "your_alarm_chat_id_here", // Telegram chat ID for alarm notifications

    "mattermost_webhook_url": "https://your-mattermost-url/hooks/YOUR_WEBHOOK_ID", // Mattermost webhook for sending messages

    "lookback_period": 3600, // Time range (in seconds) to fetch ticket statistics
    "daemon_interval": 3600, // Interval (in seconds) between statistic updates
    "alert_repeats": 10, // Number of times an alert will be repeated if the threshold is exceeded

    "tracked_apps": {
        "Example Game 1": 50, // Application name and the ticket threshold for alerts (find app names in the Helpshift admin panel)
        "Example Game 2": 30,
        "Example Game 3": 20
    },

    "tracked_app_ids": {
        "your_app_id_here": 40 // Some ticket channels (e.g., email) don’t belong to any app; IDs look like "yourcompanyname_app_20160528241804559-5w0e487e221f35h" (see [Helpshift API Docs](https://apidocs.helpshift.com/) and send get issues request to obtain app_ids)
    }
}
```

Ensure you replace placeholders with actual values for your Helpshift, Telegram, and Mattermost accounts.

#### Steps to Install
1. **Clone the repository:**
   ```sh
   git clone https://github.com/dmitrymesh/helpshift.stat.tg.bot.git
   cd helpshift.stat.tg.bot
   ```
2. **Install dependencies:**
   ```sh
   pip3 install -r requirements.txt
   ```
3. **Create a systemd service file:**
   ```sh
   sudo nano /etc/systemd/system/helpshift-bot.service
   ```
4. # Helpshift Tickets Statistic Bot

## Overview
Helpshift Tickets Statistic Bot collects the number of tickets received in your Helpshift projects and sends statistics to your messenger at a specified interval. If the number of tickets exceeds a certain threshold, it sends multiple warning messages about it.

## Features
- Periodic polling of ticket statistics.
- Displaying statistics in Telegram and/or Mattermost.
- Alarm notifications in Telegram and/or Mattermost if the ticket threshold is exceeded for any project.

## Installation

### Configuration Setup
Before running the bot, configure it by editing the `config.json` file. The configuration should include:

```json
{
    "enabled_channels": ["telegram", "mattermost"], // List of enabled messaging channels

    "helpshift_api_url": "https://api.helpshift.com/v1/YOUR_COMPANY_NAME/issues", // Helpshift API endpoint for fetching ticket statistics (replace YOUR_COMPANY_NAME)
    "helpshift_api_key": "your_api_key_here", // API key for authentication with Helpshift (see [API Key Management](https://support.helpshift.com/hc/en/13-helpshift-technical-support/faq/769-in-app-support-guide-api-key-management/#1.-finding-your-api-keys))

    "telegram_bot_token": "your_telegram_bot_token_here", // Example: "bot552154641:ADGMGav2RYsV2G0QLs4TTelPoKdjT2Dkqvy" (see [Telegram Bot Guide](https://core.telegram.org/bots/tutorial))
    "telegram_chat_id": "your_main_chat_id_here", // Telegram chat ID where statistics are sent
    "telegram_alarm_chat_id": "your_alarm_chat_id_here", // Telegram chat ID for alarm notifications

    "mattermost_webhook_url": "https://your-mattermost-url/hooks/YOUR_WEBHOOK_ID", // Mattermost webhook for sending messages

    "lookback_period": 3600, // Time range (in seconds) to fetch ticket statistics
    "daemon_interval": 3600, // Interval (in seconds) between statistic updates
    "alert_repeats": 10, // Number of times an alert will be repeated if the threshold is exceeded

    "tracked_apps": {
        "Example Game 1": 50, // Application name and the ticket threshold for alerts (find app names in the Helpshift admin panel)
        "Example Game 2": 30,
        "Example Game 3": 20
    },

    "tracked_app_ids": {
        "your_app_id_here": 40 // Some ticket channels (e.g., email) don’t belong to any app; IDs look like "yourcompanyname_app_20160528241804559-5w0e487e221f35h" (see [Helpshift API Docs](https://apidocs.helpshift.com/))
    }
}
```

Ensure you replace placeholders with actual values for your Helpshift, Telegram, and Mattermost accounts. 

### Installation on a Linux Server

#### Prerequisites
Ensure the following dependencies are installed:
- Python 3.8+
- `pip`
- `virtualenv` (recommended but optional)

#### Steps to Install
1. **Clone the repository:**
   ```sh
   git clone https://github.com/your-repo/helpshift-tickets-bot.git
   cd helpshift-tickets-bot
   ```
2. **Install dependencies:**
   ```sh
   pip3 install -r requirements.txt
   ```
3. **Create a systemd service file:**
   ```sh
   sudo nano /etc/systemd/system/helpshift-bot.service
   ```
4. **Add the following configuration (do not forget to replace `/Your/HelpshiftBot/Directory` with the actual path to your bot's directory):**
   ```ini
   [Unit]
   Description=Helpshift Bot Service
   After=network.target

   [Service]
   ExecStart=/bin/bash -c 'cd /Your/HelpshiftBot/Directory && pip3 install -r requirements.txt --quiet && python3 bot_daemon.py'
   WorkingDirectory=/Your/HelpshiftBot/Directory
   Restart=always
   User=root
   StandardOutput=append:/var/log/helpshift-bot.log
   StandardError=append:/var/log/helpshift-bot-error.log

   [Install]
   WantedBy=multi-user.target
   ```

### Running, Stopping, and Restarting the Bot

#### Start the bot:
```sh
sudo systemctl start helpshift-bot
```

#### Check bot status:
```sh
sudo systemctl status helpshift-bot
```

#### View logs:
```sh
sudo journalctl -u helpshift-bot -f
```

#### Stop the bot:
```sh
sudo systemctl stop helpshift-bot
```

#### Restart the bot:
```sh
sudo systemctl restart helpshift-bot
```

   ```ini
   [Unit]
   Description=Helpshift Bot Service
   After=network.target

   [Service]
   ExecStart=/bin/bash -c 'cd /Your/HelpshiftBot/Directory && pip3 install -r requirements.txt --quiet && python3 bot_daemon.py'
   WorkingDirectory=/Your/HelpshiftBot/Directory
   Restart=always
   User=root
   StandardOutput=append:/var/log/helpshift-bot.log
   StandardError=append:/var/log/helpshift-bot-error.log

   [Install]
   WantedBy=multi-user.target
   ```

### Running, Stopping, and Restarting the Bot

#### Start the bot:
```sh
sudo systemctl start helpshift-bot
```

#### Check bot status:
```sh
sudo systemctl status helpshift-bot
```

#### View logs:
```sh
sudo journalctl -u helpshift-bot -f
```

#### Stop the bot:
```sh
sudo systemctl stop helpshift-bot
```

#### Restart the bot:
```sh
sudo systemctl restart helpshift-bot
```