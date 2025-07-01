# config/logger_loader.py
# ------------------------------------------------------------
# Sets up a rotating logger using env.json config
# ------------------------------------------------------------

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from app.config.config_loader import config_loader
from app.utils.helpers import helpers


class LoggerConfig:
    """
    Configures a global rotating file logger for the application.
    """

    def __init__(self):
        self.logger = logging.getLogger("app_logger")
        self.logger.setLevel(logging.DEBUG)

        log_cfg = config_loader.config.get("log", {})
        dir_path = Path(log_cfg.get("filepath", "logs"))
        file_path = dir_path / log_cfg.get("filename", "app.log")

        helpers.ensure_directory_exists(dir_path)

        handler = RotatingFileHandler(
            filename=file_path,
            mode=log_cfg.get("filemode", "a"),
            maxBytes=log_cfg.get("filesize", 5) * 1024 * 1024,
            backupCount=log_cfg.get("backupCount", 2),
            encoding=log_cfg.get("encoding", "utf-8")
        )

        formatter = logging.Formatter(
            fmt=log_cfg.get("format", "{asctime} - {levelname} - {message}"),
            style=log_cfg.get("style", "{"),
            datefmt=log_cfg.get("datefmt", "%Y-%m-%d %H:%M")
        )

        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.info(f"Logger initialized. Writing to {file_path}")

    def get_logger(self):
        return self.logger


# Global logger instance
app_logger = LoggerConfig().get_logger()
