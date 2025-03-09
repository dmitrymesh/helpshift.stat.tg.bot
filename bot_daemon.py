import time
import logging
from services.bot_logic import BotLogic
from helpers.config_loader import ConfigLoader


def main():
    config = ConfigLoader.load_config()
    interval = config.get("daemon_interval", 3600)

    bot = BotLogic()

    while True:
        try:
            start_time = time.time()
            bot.run()
            elapsed_time = time.time() - start_time
            sleep_time = max(0, interval - elapsed_time)
            time.sleep(sleep_time)
        except Exception as e:
            logging.exception(f"Error in bot execution: {e}")
            time.sleep(interval)


if __name__ == "__main__":
    logging.basicConfig(
        filename="/var/log/helpshift-bot.log",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )
    logging.info("Helpshift Bot Service started")

    main()
