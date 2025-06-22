import pytest
import threading

from src.patterns.singleton.decorator_example import singleton_decorator
from src.patterns.singleton import (
    new_pitfall,
    decorator_example,
    metaclass_example,
    decorator_thread_safety_issue,
)


class TestNewPitfall:
    """
    Tests the classic __new__ singleton pattern.
    - Ensures only one instance is created.
    - Demonstrates the pitfall: __init__ is called every time, not just once.
    """
    def test_singleton_instance(self):
        a = new_pitfall.ConfigManager()
        b = new_pitfall.ConfigManager()
        assert a is b

    def test_init_called_twice(self, capsys):
        new_pitfall.ConfigManager._instance = None  # Reset for test
        a = new_pitfall.ConfigManager()
        b = new_pitfall.ConfigManager()
        captured = capsys.readouterr().out
        # Should see two random numbers printed (init called twice)
        assert (
            len([line for line in captured.splitlines() if line.strip().isdigit()]) == 2
        )


class TestDecoratorSingleton:
    """
    Tests the singleton pattern using a decorator.
    - Ensures only one instance is created.
    - Confirms shared state between instances.
    """
    def test_singleton_instance(self):
        a = decorator_example.ConfigManager()
        b = decorator_example.ConfigManager()
        assert a is b

    def test_config_shared(self):
        a = decorator_example.ConfigManager()
        b = decorator_example.ConfigManager()
        a._config["test"] = 123
        assert b._config["test"] == 123


class TestMetaclassSingleton:
    """
    Tests the singleton pattern using a metaclass.
    - Ensures only one instance is created.
    - Confirms shared state between instances.
    """
    def test_singleton_instance(self):
        a = metaclass_example.ConfigManager()
        b = metaclass_example.ConfigManager()
        assert a is b

    def test_config_shared(self):
        a = metaclass_example.ConfigManager()
        b = metaclass_example.ConfigManager()
        a._config["test"] = 456
        assert b._config["test"] == 456


class TestDecoratorSubclassingPitfall:
    """
    Tests the pitfall of using a singleton decorator:
    - Shows that subclassing a decorated class raises a TypeError.
    """
    def test_subclassing_raises_typeerror(self):
        with pytest.raises(TypeError):

            @singleton_decorator
            class Logger:
                pass

            class FileLogger(Logger):
                pass


class TestDecoratorThreadSafety:
    """
    Tests thread safety of singleton patterns.
    - Shows that a naive decorator is not thread-safe.
    - Shows that a decorator with a lock is thread-safe.
    - Shows that a metaclass singleton can be made thread-safe.
    """
    def test_unsafe_decorator_race_condition(self):
        # Use the unsafe_singleton from the thread safety example
        unsafe_singleton = decorator_thread_safety_issue.unsafe_singleton
        results = []

        class Database:
            pass

        Singleton = unsafe_singleton(Database)

        def create_instance():
            results.append(Singleton())

        threads = [threading.Thread(target=create_instance) for _ in range(10)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        # If not thread-safe, there may be more than one unique instance
        assert len(set(id(obj) for obj in results)) > 1

    def test_safe_decorator_thread_safe(self):
        safe_singleton = decorator_thread_safety_issue.safe_singleton
        results = []

        class Database:
            pass

        Singleton = safe_singleton(Database)

        def create_instance():
            results.append(Singleton())

        threads = [threading.Thread(target=create_instance) for _ in range(10)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        # Should only be one unique instance
        assert len(set(id(obj) for obj in results)) == 1

    def test_metaclass_thread_safe(self):
        ThreadSafeSingletonMeta = decorator_thread_safety_issue.ThreadSafeSingletonMeta
        results = []

        class Database(metaclass=ThreadSafeSingletonMeta):
            pass

        def create_instance():
            results.append(Database())

        threads = [threading.Thread(target=create_instance) for _ in range(10)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        assert len(set(id(obj) for obj in results)) == 1
