from pytest import approx

from trade.strategies.average_001 import Strategy, Params


def test_profit():
    s = Strategy(
        first_amount=0,
        first_price=0,
        second_amount=10_000,
        pair=('BTC', 'USD'),
        params=Params(
            window_size=4,
            buy_bound=0.9,
            sell_bound=1.1,
            stop_loss_bound=0.8,
            cool_down_period=0,
        ),
    )

    def assert_(first_amount, first_price, avg):
        assert s.first_amount == approx(first_amount)
        assert s.first_price == approx(first_price)
        assert s.get_avg() == approx(avg)

    s.process_tick(current_price=10_000)
    s.process_tick(current_price=10_000)
    s.process_tick(current_price=10_000)
    s.process_tick(current_price=10_000)
    assert_(
        first_amount=0,
        first_price=0,
        avg=10_000,
    )

    s.process_tick(20_000)
    assert_(
        first_amount=0,
        first_price=0,
        avg=50_000 / 4,
    )

    s.process_tick(10_000)
    assert_(
        first_amount=0.1,
        first_price=10_000,
        avg=50_000 / 4,
    )

    s.process_tick(8_000)
    assert_(
        first_amount=0.225,
        first_price=(10_000 * .1 + 8_000 * .125) / .225,
        avg=48_000 / 4,
    )

    s.process_tick(100_000)
    assert_(
        first_amount=0,
        first_price=0,
        avg=138_000 / 4,
    )
    assert s.second_amount == 30_500
