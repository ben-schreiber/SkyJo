class EmptyPileError(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__("The pile is empty, you cannot pick a card from it!", *args, **kwargs)