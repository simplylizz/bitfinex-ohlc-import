import datetime
import dataclasses
import sqlite3


@dataclasses.dataclass(
    slots=True,
    frozen=True,
    kw_only=True,
)
class Candle:
    time: datetime.datetime
    open: float
    close: float


class HistoricalEngine:
    def __init__(
            self,
            strategies,
            pair,
            path="./bitfinex.sqlite",
            start_date=0,
    ):
        self.strategies = strategies
        self.pair = pair
        self.con = sqlite3.connect(path)
        self.start_date = start_date

    def run(self):
        for i, candle in enumerate(self.get_candles()):
            print_stats = False # i % (24 * 60) == 0
            for strategy in self.strategies:
                strategy.process_tick(candle.open)
                if print_stats:
                    print(f"######### {strategy.name}")
                    print(f"Candle #{i}, date {candle.time}")
                    strategy.print_stats()
                    print("#########")

        for strategy in self.strategies:
            print(f"######### {strategy.name}")
            print(f"Candle #{i}, date {candle.time}")
            strategy.print_stats()
            print("#########")

    def get_candles(self):
        for row in self.con.cursor().execute(
                'select time, open, close from candles where symbol=? and time>=? order by time asc',
                (
                    "".join(self.pair),
                    self.start_date,
                ),
        ):
            assert len(row) == 3
            yield Candle(
                time=datetime.datetime.fromtimestamp(int(row[0]) / 1000),
                open=float(row[1]),
                close=float(row[2]),
            )
