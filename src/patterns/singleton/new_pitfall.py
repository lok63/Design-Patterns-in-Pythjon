import os
from random import randint


class ConfigManager:
    _instance = None
    _config = None

    def __init__(self):
        # print a random number to demonstrate singleton behavior
        print(randint(1, 100))

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._load_config()
        return cls._instance

    def _load_config(self):
        # Load from file, environment variables, etc.
        self._config = {
            "api_key": os.getenv("API_KEY"),
            "debug_mode": os.getenv("DEBUG", "False").lower() == "true",
            "max_connections": int(os.getenv("MAX_CONN", "10")),
        }

    def get(self, key, default=None):
        return self._config.get(key, default)


if __name__ == "__main__":
    # Usage: Configuration loaded once, shared everywhere
    c1 = ConfigManager()
    c2 = ConfigManager()
    print(c1 == c2)  # Should be True, both are the same instance
