class PlainPizza:
    def __init__(self):
        self.toppings = []

    def show_toppings(self):
        return f"Toppings: {', '.join(self.toppings) if self.toppings else 'none'}"


class OlivesMixin:
    def add_olives(self):
        print("Adding olives!")
        self.toppings += ["olives"]  # ✅ Modifies subclass state


class CheeseMixin:
    def add_cheese(self):
        print("Adding cheese!")
        self.toppings += ["cheese"]


class PepperoniMixin:
    def add_pepperoni(self):
        print("Adding pepperoni!")
        self.toppings += ["pepperoni"]


class DeluxePizza(OlivesMixin, CheeseMixin, PepperoniMixin, PlainPizza):
    def prepare_pizza(self):
        self.add_olives()
        self.add_cheese()
        self.add_pepperoni()


class VeggiePizza(OlivesMixin, CheeseMixin, PlainPizza):
    def prepare_pizza(self):
        self.add_olives()
        self.add_cheese()


if __name__ == "__main__":
    deluxe = DeluxePizza()
    deluxe.prepare_pizza()
    print("DeluxePizza:", deluxe.show_toppings())

    veggie = VeggiePizza()
    veggie.prepare_pizza()
    print("VeggiePizza:", veggie.show_toppings())
