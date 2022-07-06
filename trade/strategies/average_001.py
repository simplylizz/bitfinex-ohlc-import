import dataclasses

from .base import BaseStrategy


@dataclasses.dataclass(kw_only=True)
class Params:
    window_size: int
    sell_bound: float
    buy_bound: float
    stop_loss_bound: float
    cool_down_period: int


class Strategy(BaseStrategy):
    """
    buy: if price is < than window on X%
    sell: if price is > than buy on Y% or lower on Z%

    * size of the window could be adjusted
    """

    buy_amount_in_second = 1000

    def __init__(
            self,
            params: Params,
            *args,
            **kwargs,
    ):
        super().__init__(*args, **kwargs)

        self.params = params
        self.name = f"Average 001 [{self.params}]"

        self.cool_down = self.params.window_size  # just to accumulate stats
        self.window = []
        self.window_i = 0
        self.sum = 0

    def add_to_window(self, price: float):
        self.sum += price
        if len(self.window) < self.params.window_size:
            self.window.append(price)
        else:
            self.sum -= self.window[self.window_i]
            self.window[self.window_i] = price
            self.window_i += 1
            if self.window_i == len(self.window):
                self.window_i = 0

    def get_avg(self):
        return self.sum / self.params.window_size

    def check_cool_down(self):
        if self.cool_down:
            self.cool_down -= 1
            return True
        return False

    def process_tick(self, current_price):
        super().process_tick(current_price)

        self.add_to_window(current_price)

        if self.check_cool_down():
            return

        if self.first_amount > 0:
            # check "stop loss"
            if current_price / self.first_price < self.params.stop_loss_bound:
                self.sell_first(self.first_amount)
                self.first_price = 0
                self.set_cool_down()
                return

            if current_price / self.first_price >= self.params.sell_bound:
                self.sell_first(self.first_amount)
                self.first_price = 0
                return

        if current_price / self.get_avg() <= self.params.buy_bound:
            self.buy_first(self.buy_amount_in_second / current_price)

    def set_cool_down(self):
        self.cool_down = self.params.cool_down_period
