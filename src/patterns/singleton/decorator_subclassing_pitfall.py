"""
Simple demonstration: Why decorator singletons break inheritance
"""

from src.patterns.singleton.decorator_example import singleton_decorator
from src.patterns.singleton.metaclass_example import SingletonMeta


def demonstrate_decorator_issue():
    """Shows why decorator singleton breaks inheritance"""

    print("DECORATOR APPROACH - INHERITANCE FAILS")
    print("=" * 40)

    @singleton_decorator
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
