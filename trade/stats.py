import dataclasses


# class Stats:
#     def __init__(self, pair: list[str], balance_0: float, balance_1: float):
#         self.pair = pair
#         self.buys = 0
#         self.buys_amount = 0
#         self.sells = 0
#         self.sells_amount = 0
#         # balance in the first currency
#         self.balance_0 = balance_0
#         # balance in the second currency
#         self.balance_1 = balance_1
#         self.last_price = 0
#
#     def buy(self, amount: float, price: float):
#         self.buys += 1
#         self.buys_amount += amount
#         self.last_price = price
#
#         self.balance_1 += amount * price
#
#     def sell(self, amount: float, price: float):
#         self.sells += 1
#         self.sells_amount += amount
#         self.last_price = price
#
#     def balance_0_converted(self):
#         pass
