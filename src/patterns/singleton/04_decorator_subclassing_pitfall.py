#!/usr/bin/env python3
"""
Simple demonstration: Why decorator singletons break inheritance
"""


def demonstrate_decorator_issue():
    """Shows why decorator singleton breaks inheritance"""

    def singleton(cls):
        instances = {}

        def get_instance(*args, **kwargs):
            if cls not in instances:
                instances[cls] = cls(*args, **kwargs)
            return instances[cls]

        return get_instance

    print("DECORATOR APPROACH - INHERITANCE FAILS")
    print("=" * 40)

    @singleton
    class Logger:
        def __init__(self, name="Logger"):
            self.name = name
            print(f"Created {self.name}")

    print(f"Logger type: {type(Logger)}")  # <class 'function'> - Problem!

    # This will fail because Logger is now a function, not a class
    try:

        class FileLogger(Logger):  # Can't inherit from a function!
            pass

    except TypeError as e:
        print(f"Error: {e}")


def demonstrate_metaclass_solution():
    """Shows how metaclass singleton supports inheritance"""

    class SingletonMeta(type):
        _instances = {}

        def __call__(cls, *args, **kwargs):
            if cls not in cls._instances:
                cls._instances[cls] = super().__call__(*args, **kwargs)
            return cls._instances[cls]

    print("\nMETACLASS APPROACH - INHERITANCE WORKS")
    print("=" * 40)

    class Logger(metaclass=SingletonMeta):
        def __init__(self, name="Logger"):
            self.name = name
            print(f"Created {self.name}")

    class FileLogger(Logger):  # This works perfectly!
        def __init__(self, filename):
            super().__init__(f"FileLogger({filename})")
            self.filename = filename

    print(f"Logger type: {type(Logger)}")  # <class '__main__.SingletonMeta'>

    # Test inheritance
    file1 = FileLogger("app.log")
    file2 = FileLogger("other.log")
    print(f"Same FileLogger instance: {file1 is file2}")  # True
    print(f"Filename: {file1.filename}")

    # Different classes = different singletons
    log1 = Logger("base")
    print(f"Logger vs FileLogger: {log1 is file1}")  # False - correct!


if __name__ == "__main__":
    demonstrate_decorator_issue()
    demonstrate_metaclass_solution()
