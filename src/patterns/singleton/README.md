# Singleton Pattern Examples in Python

## How the __new__ Singleton Pattern Works

The most common way to implement a singleton in Python is to override the `__new__` method. This ensures that only one instance of the class is ever created:

```python
class Singleton:
    _instance = None
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
```

### Pitfall: Constructors Are Still Called
If your singleton class also defines an `__init__` constructor, **the constructor will be called every time you instantiate the class**—even though the same instance is returned. This can lead to unexpected behavior if your constructor modifies state or performs side effects.

**Example:**
```python
s1 = Singleton()
s2 = Singleton()
# s1 is s2, but Singleton.__init__ is called twice!
```

## Decorator and Metaclass Solutions

Both the decorator and metaclass approaches solve this problem by ensuring that the constructor is only called once:

- **Decorator Example:**
  - Wraps the class and manages instance creation, so `__init__` is only called once.
- **Metaclass Example:**
  - Controls instance creation at the metaclass level, ensuring both `__new__` and `__init__` are only called once for the singleton instance.

These approaches are more robust and avoid the double-constructor pitfall of the basic `__new__` pattern.

---

## Decorator Subclassing Pitfall

While the decorator approach can enforce the singleton pattern, it has a major pitfall: **it breaks inheritance**. When you decorate a class with a singleton decorator, the class becomes a function, not a type. This means:
- You cannot subclass the decorated class (subclassing raises a `TypeError`).
- `isinstance` and `issubclass` checks do not work as expected.

**Example:**
```python
@singleton_decorator
class Logger:
    ...

class FileLogger(Logger):  # TypeError: function() argument 'code' must be code, not str
    ...
```

See `04_decorator_subclassing_pitfall.py` for a demonstration of this issue, and how the metaclass approach solves it by preserving class identity and supporting inheritance.

---

## Thread Safety Issues with the Decorator Singleton

The decorator singleton approach is **not thread-safe** by default. In a multi-threaded environment, it is possible for two threads to simultaneously create two instances of the singleton, breaking the singleton guarantee.

- This can happen if two threads check for the instance at the same time and both see that it does not exist, so both create a new instance.
- To make a singleton truly thread-safe, you must use locks or other synchronization mechanisms.

See `05_decorator_thread_safety_issue.py` for a demonstration of this issue and how to address it.

---

See the following files for examples:
- `01_new_pitfall.py`: Shows the `__new__` singleton pattern and its constructor pitfall.
- `02_decorator_example.py`: Singleton via decorator (fixes the pitfall, but breaks inheritance).
- `03_metaclass_example.py`: Singleton via metaclass (fixes the pitfall and supports inheritance).
- `04_decorator_subclassing_pitfall.py`: Demonstrates the decorator subclassing issue and metaclass solution.
- `05_decorator_thread_safety_issue.py`: Demonstrates thread safety issues with the decorator singleton and solutions.
