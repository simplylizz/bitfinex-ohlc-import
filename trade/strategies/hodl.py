from . import base


class Strategy(base.BaseStrategy):
    name = "HODL"

    def process_tick(self, current_price):
        super().process_tick(current_price)
        self.buy_first(self.second_amount / current_price)
