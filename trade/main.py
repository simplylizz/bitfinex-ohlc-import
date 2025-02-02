import engine
import datetime
import strategies


def get_strategies(pair):
    return (
        # strategies.dumb_001.Strategy(
        #     first_amount=0,
        #     first_price=0,
        #     second_amount=10_000,
        #     pair=pair,
        #     params=strategies.dumb_001.Params(
        #         sell_bound=.95,
        #         cool_down_period=24*60,
        #     ),
        # ),
        strategies.average_001.Strategy(
            first_amount=0,
            first_price=0,
            second_amount=10_000,
            pair=pair,
            params=strategies.average_001.Params(
                sell_bound=1.05,
                buy_bound=.95,
                stop_loss_bound=.9,
                window_size=60*6,  # in minutes
                cool_down_period=60*24*1,  # in minutes
            ),
        ),
        # strategies.anti_hodl.Strategy(
        #     first_amount=0,
        #     first_price=0,
        #     second_amount=10000,
        #     pair=pair,
        # ),
        # strategies.hodl.Strategy(
        #     first_amount=0,
        #     first_price=0,
        #     second_amount=10000,
        #     pair=pair,
        # ),
    )


def main():
    start_dates = {
        # "All": datetime.datetime(1970, 1, 1),
        "180d": datetime.datetime.now() - datetime.timedelta(days=180),
        "90": datetime.datetime.now() - datetime.timedelta(days=90),
        "30": datetime.datetime.now() - datetime.timedelta(days=30),
    }
    pairs = (
        ('btc', 'usd'),
        # ('eth', 'usd'),
        # ('eth', 'btc'),
    )

    for pair in pairs:
        for name, date in start_dates.items():
            print(f"Testing `{name}` window, pair: {pair}")

            eng = engine.HistoricalEngine(
                strategies=get_strategies(pair),
                pair=pair,
                start_date=int(date.timestamp() * 1000),
            )

            start = datetime.datetime.now()
            eng.run()
            end = datetime.datetime.now()
            print(f'Time: {end - start}')
        print("\n---\n")


if __name__ == '__main__':
    main()
