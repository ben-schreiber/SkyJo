class Card:
    def __init__(self, value: int):
        if value < -2 or value > 12:
            raise ValueError(
                f"The value {value} is not legal. Must be in the range [-2, 12]"
            )
        self.value: int = value
        self.hidden: bool = False

    def is_hidden(self) -> bool:
        return self.hidden

    def flip_over(self):
        self.is_hidden = False

    def get_value(self) -> int:
        return self.value

    def __eq__(self, other):
        return self.value == other.get_value()