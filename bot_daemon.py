#!/usr/bin/python
import time
import logging
from daemon import runner
from services.bot_logic import BotLogic
from helpers.config_loader import ConfigLoader

class BotDaemon:
    def __init__(self):
        config = ConfigLoader.load_config()

        self.stdin_path = '/dev/null'
        self.stdout_path = config.get("log_stdout_path", "/var/log/bot_daemon.log")
        self.stderr_path = config.get("log_stderr_path", "/var/log/bot_daemon_error.log")
        self.pidfile_path = config.get("pidfile_path", "/var/run/bot_daemon.pid")
        self.pidfile_timeout = 5
        self.interval = config.get("daemon_interval", 3600)

        self.bot = BotLogic(config_file='config.json')

    def run(self):
        while True:
            try:
                start_time = time.time()
                self.bot.run()
                elapsed_time = time.time() - start_time
                sleep_time = max(0, self.interval - elapsed_time)
                time.sleep(sleep_time)
            except Exception as e:
                logging.exception("Error during execution of BotLogic: {}".format(e))
                time.sleep(self.interval)

if __name__ == "__main__":
    daemon = BotDaemon()
    daemon_runner = runner.DaemonRunner(daemon)

    logger = logging.getLogger("BotDaemonLog")
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler(daemon.stdout_path)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    daemon_runner.daemon_context.files_preserve = [handler.stream]

    daemon_runner.do_action()
