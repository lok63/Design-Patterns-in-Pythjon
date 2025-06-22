"""
Demonstration: Thread safety issues with singleton patterns
"""

import threading
import time
from concurrent.futures import ThreadPoolExecutor


def unsafe_singleton(cls):
    """Decorator singleton - NOT thread safe"""
    instances = {}

    def get_instance(*args, **kwargs):
        if cls not in instances:
            # PROBLEM: Race condition here!
            # Multiple threads can pass this check simultaneously
            time.sleep(0.01)  # Simulate slow initialization
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance


def safe_singleton(cls):
    """Decorator singleton - Thread safe with lock"""
    instances = {}
    lock = threading.Lock()

    def get_instance(*args, **kwargs):
        if cls not in instances:
            with lock:  # Thread-safe with lock
                if cls not in instances:  # Double-check pattern
                    time.sleep(0.01)  # Simulate slow initialization
                    instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance


class ThreadSafeSingletonMeta(type):
    """Metaclass singleton - Naturally easier to make thread safe"""

    _instances = {}
    _lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            with cls._lock:
                if cls not in cls._instances:
                    time.sleep(0.01)  # Simulate slow initialization
                    cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


def demonstrate_unsafe_decorator():
    """Shows race condition with unsafe decorator singleton"""
    print("UNSAFE DECORATOR - RACE CONDITION")
    print("=" * 40)

    @unsafe_singleton
    class Database:
        def __init__(self):
            self.id = id(self)
            print(f"Database created with ID: {self.id}")

    def create_database():
        return Database()

    # Run multiple threads simultaneously
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(create_database) for _ in range(5)]
        instances = [future.result() for future in futures]

    # Check if all instances are the same
    unique_ids = set(inst.id for inst in instances)
    print(f"Number of unique instances created: {len(unique_ids)}")
    print(f"Should be 1, but got: {len(unique_ids)} (RACE CONDITION!)")

    if len(unique_ids) > 1:
        print("❌ FAILED: Multiple instances created!")
    else:
        print("✅ PASSED: Only one instance created")


def demonstrate_safe_decorator():
    """Shows thread-safe decorator singleton"""
    print("\nSAFE DECORATOR - WITH LOCK")
    print("=" * 40)

    @safe_singleton
    class Database:
        def __init__(self):
            self.id = id(self)
            print(f"Database created with ID: {self.id}")

    def create_database():
        return Database()

    # Run multiple threads simultaneously
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(create_database) for _ in range(5)]
        instances = [future.result() for future in futures]

    # Check if all instances are the same
    unique_ids = set(inst.id for inst in instances)
    print(f"Number of unique instances created: {len(unique_ids)}")

    if len(unique_ids) > 1:
        print("❌ FAILED: Multiple instances created!")
    else:
        print("✅ PASSED: Only one instance created")


def demonstrate_metaclass_safety():
    """Shows thread-safe metaclass singleton"""
    print("\nMETACLASS - THREAD SAFE")
    print("=" * 40)

    class Database(metaclass=ThreadSafeSingletonMeta):
        def __init__(self):
            self.id = id(self)
            print(f"Database created with ID: {self.id}")

    def create_database():
        return Database()

    # Run multiple threads simultaneously
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(create_database) for _ in range(5)]
        instances = [future.result() for future in futures]

    # Check if all instances are the same
    unique_ids = set(inst.id for inst in instances)
    print(f"Number of unique instances created: {len(unique_ids)}")

    if len(unique_ids) > 1:
        print("❌ FAILED: Multiple instances created!")
    else:
        print("✅ PASSED: Only one instance created")


if __name__ == "__main__":
    print("Testing thread safety with 5 concurrent threads...\n")

    # Run multiple times to increase chance of seeing race condition
    for attempt in range(3):
        print(f"\n--- Attempt {attempt + 1} ---")
        demonstrate_unsafe_decorator()
        demonstrate_safe_decorator()
        demonstrate_metaclass_safety()
        print()
