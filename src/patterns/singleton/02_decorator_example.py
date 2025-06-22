import os
from random import randint


def singleton(cls):
    instances = {}

    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance


@singleton
class ConfigManager:
    def __init__(self):
        print(f"Initializing with random number: {randint(1, 100)}")
        self._load_config()

    def _load_config(self):
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
