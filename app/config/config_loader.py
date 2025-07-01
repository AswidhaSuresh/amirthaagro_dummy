# config/config_loader.py
# ------------------------------------------------------------
# Loads environment config from env.json file
# ------------------------------------------------------------

import json
from pathlib import Path


class ConfigLoader:
    """
    Loads configuration settings from a JSON file.

    Attributes:
        config (dict): Parsed JSON configuration data.
    """

    def __init__(self, file_path='env.json'):
        self.config = self.load_config(file_path)

    def load_config(self, file_path):
        """
        Load and parse the config JSON.

        Args:
            file_path (str): Relative path to the JSON file.

        Returns:
            dict: Loaded config data.

        Raises:
            FileNotFoundError: If the file doesn't exist.
            ValueError: If the JSON is malformed.
        """
        config_path = Path(__file__).resolve().parents[2] / file_path
        if not config_path.is_file():
            raise FileNotFoundError(f"Configuration file not found at: {config_path}")
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in configuration file: {e}")


# Global config instance
config_loader = ConfigLoader()
