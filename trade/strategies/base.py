import abc


class BaseStrategy(abc.ABC):
    def __init__(
            self,
            first_amount: int,
            first_price: int,
            second_amount: int,
            pair: tuple,
    ):
        self.pair = pair
        self.first_amount = first_amount
        self.first_price = first_price
        self.second_amount = second_amount

        self.sell_price = 0
        self.last_price = 0

        self.max_total_second = float("-inf")
        self.min_total_second = float("inf")
        self.max_total_first = float("-inf")
        self.min_total_first = float("inf")
        self.buys = 0
        self.sells = 0

    def process_tick(self, current_price):
        self.last_price = current_price
        self.update_stats()

    def buy_first(self, max_amount):
        if self.second_amount > 0:
            self.buys += 1
            buy_amount = min(self.second_amount / self.last_price, max_amount)

            self.first_price = (self.first_amount * self.first_price + buy_amount * self.last_price) / (self.first_amount + buy_amount)
            self.first_amount += buy_amount
            self.second_amount -= buy_amount * self.last_price

    def sell_first(self, max_amount):
        if self.first_amount > 0:
            self.sells += 1
            self.second_amount += self.first_amount * self.last_price
            self.first_amount = 0
            self.first_price = 0

    def print_stats(self):
        print(f"In {self.pair[1]}: {self.second_amount}")
        print(f"In {self.pair[0]}: {self.first_amount}")
        # print('\033[1', 'Totals', '\033[0m')
        print("**Totals**")
        print(f"In {self.pair[1]}: {self.get_converted_second()}")
        print(f"In {self.pair[0]}: {self.get_converted_first()}")
        print("###")
        print(f"Max in {self.pair[1]}: {self.max_total_second}")
        print(f"Min in {self.pair[1]}: {self.min_total_second}")
        print(f"Max in {self.pair[0]}: {self.max_total_first}")
        print(f"Min in {self.pair[0]}: {self.min_total_first}")
        print("###")
        print(f"Buys: {self.buys}")
        print(f"Sells: {self.sells}")

    def get_converted_second(self):
        return self.second_amount + self.first_amount * self.last_price

    def get_converted_first(self):
        return self.first_amount + self.second_amount / self.last_price

    def update_stats(self):
        self.max_total_second = max(self.max_total_second, self.get_converted_second())
        self.min_total_second = min(self.min_total_second, self.get_converted_second())
        self.max_total_first = max(self.max_total_first, self.get_converted_first())
        self.min_total_first = min(self.min_total_first, self.get_converted_first())
