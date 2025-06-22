"""
Demonstrates why having constructors in mixins is problematic in Python.

- Shows that only one mixin's __init__ is called in multiple inheritance, leading to bugs.
- Shows how constructor signatures become fragile and error-prone as you add more mixins and unique attributes.
- See section 6 of the README for a detailed explanation.
"""

#################
## EXAMPLE 1: ONLY ONE MIXIN'S __init__ IS CALLED
#################
class MixinA:
    def __init__(self):
        print("MixinA init")

class MixinB:
    def __init__(self):
        print("MixinB init")

class MyClass(MixinA, MixinB):
    def __init__(self):
        super().__init__()

#################
## EXAMPLE 2: MIXINS WITH REQUIRED ARGUMENTS AND UNIQUE ATTRIBUTES
#################
class NameMixin:
    def __init__(self, name):
        self.name = name

class ClassA(NameMixin):
    def __init__(self, name, a_value):
        # Must call NameMixin's __init__ with the right argument
        super().__init__(name)
        self.a_value = a_value

class ClassB(NameMixin):
    def __init__(self, name, b_value):
        # Must call NameMixin's __init__ with the right argument
        super().__init__(name)
        self.b_value = b_value

#################
## EXAMPLE 3: MULTIPLE MIXINS WITH REQUIRED ARGUMENTS
#################
class TimestampMixin:
    def __init__(self, timestamp):
        self.timestamp = timestamp

class ClassC(NameMixin, TimestampMixin):
    def __init__(self, name, timestamp, c_value):
        # Now you must manually call each mixin's __init__
        NameMixin.__init__(self, name)
        TimestampMixin.__init__(self, timestamp)
        self.c_value = c_value

if __name__ == "__main__":
    print("--- Example 1: Only one mixin's __init__ is called ---")
    obj = MyClass()  # Only MixinA's __init__ is called; MixinB's is skipped

    print("\n--- Example 2: Mixins with required arguments and unique attributes ---")
    a = ClassA("Alice", 123)
    b = ClassB("Bob", 456)
    print(f"ClassA: name={a.name}, a_value={a.a_value}")
    print(f"ClassB: name={b.name}, b_value={b.b_value}")

    print("\n--- Example 3: Multiple mixins with required arguments ---")
    c = ClassC("Carol", 1234567890, 789)
    print(f"ClassC: name={c.name}, timestamp={c.timestamp}, c_value={c.c_value}")

    print("\nThis is why the community recommends avoiding constructors in mixins.") 