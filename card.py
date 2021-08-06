class Card:
    def __init__(self, value: int):
        if value < -2 or value > 12:
            raise ValueError(
                f"The value {value} is not legal. Must be in the range [-2, 12]"
            )
        self.value: int = value
        self.hidden: bool = True

    def is_hidden(self) -> bool:
        return self.hidden

    def flip_over(self, facing: str = 'down'):
        if facing == 'down':
            self.hidden = True
        elif facing == 'up':
            self.hidden = False
        else:
            raise ValueError(f'`facing` can only be "up" or "down"; you provided {facing}')

    def get_value(self) -> int:
        return self.value

    def __eq__(self, other):
        return self.value == other.get_value()