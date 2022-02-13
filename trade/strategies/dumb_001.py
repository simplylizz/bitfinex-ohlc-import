from .base import BaseStrategy


class Strategy(BaseStrategy):
    name = "Dumb Strategy 001"
    buy_amount_in_second = 1000
    sell_bound = 0.95

    def __init__(
            self,
            *args,
            **kwargs,
    ):
        super().__init__(*args, **kwargs)

        self.cool_down = 0

    def buy_first(self, max_amount):
        if self.check_cool_down():
            return
        super().buy_first(max_amount)
        self.sell_price = self.first_price * self.sell_bound
        self.set_cool_down()

    def sell_first(self, max_amount):
        super().sell_first(max_amount)
        self.set_cool_down()

    def check_cool_down(self):
        if self.cool_down:
            self.cool_down -= 1
            return True
        return False

    def process_tick(self, current_price):
        super().process_tick(current_price)

        if not self.first_price:
            self.buy_first(self.buy_amount_in_second / current_price)
        elif self.last_price < self.sell_price:
            self.sell_first(self.first_amount)
        elif self.last_price * self.sell_bound > self.sell_price:
            self.sell_price = self.last_price * self.sell_bound

    def set_cool_down(self):
        self.cool_down = 60 * 6 # 6 hours
