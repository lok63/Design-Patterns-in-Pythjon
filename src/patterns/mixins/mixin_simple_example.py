#################
## BASE CLASS
#################
class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        return f"{self.name} makes a sound."


#################
## MIXINS
#################
class FlyMixin:
    def fly(self):
        # Assumes self has a 'name' attribute from the base class
        return f"{self.name} is flying!"  # type: ignore[attr-defined]


class WalkMixin:
    def walk(self):
        # Assumes self has a 'name' attribute from the base class
        return f"{self.name} is walking."  # type: ignore[attr-defined]


class SwimMixin:
    def swim(self):
        # Assumes self has a 'name' attribute from the base class
        return f"{self.name} is swimming."  # type: ignore[attr-defined]


#################
## SUBCLASSES
#################
class Duck(FlyMixin, WalkMixin, SwimMixin, Animal):
    def speak(self):
        return f"{self.name} says quack!"


class Dog(WalkMixin, SwimMixin, Animal):
    def speak(self):
        return f"{self.name} says woof!"


class Eagle(FlyMixin, WalkMixin, Animal):
    def speak(self):
        return f"{self.name} screeches!"


class Fish(SwimMixin, Animal):
    def speak(self):
        return f"{self.name} blubs."


if __name__ == "__main__":
    duck = Duck("Daffy")
    print(duck.speak())
    print(duck.fly())
    print(duck.walk())
    print(duck.swim())

    dog = Dog("Rex")
    print(dog.speak())
    print(dog.walk())
    print(dog.swim())

    eagle = Eagle("Eddie")
    print(eagle.speak())
    print(eagle.fly())
    print(eagle.walk())

    fish = Fish("Nemo")
    print(fish.speak())
    print(fish.swim())
