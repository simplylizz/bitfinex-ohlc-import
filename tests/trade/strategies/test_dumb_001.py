from pytest import approx

from trade.strategies.dumb_001 import Strategy, Params


def test_profit():
    s = Strategy(
        first_amount=0,
        first_price=0,
        second_amount=10_000,
        pair=('BTC', 'USD'),
        params=Params(
            sell_bound=.95,
            cool_down_period=0,
        ),
    )

    s.process_tick(current_price=10_000)

    assert s.first_amount == approx(0.1)
    assert s.first_price == approx(10_000)
    assert s.second_amount == approx(9_000)
    assert s.sell_price == approx(10_000 * 0.95)

    s.process_tick(current_price=10_000)

    assert s.first_amount == approx(0.2)
    assert s.first_price == approx(10_000)
    assert s.second_amount == approx(8_000)
    assert s.sell_price == approx(10_000 * 0.95)

    s.process_tick(current_price=20_000)

    assert s.first_amount == approx(0.25)
    assert s.first_price == approx((10_000 + 10_000 + 20_000 * 0.5) / 2.5)
    assert s.second_amount == approx(7_000)
    assert s.sell_price == approx(20_000 * 0.95)

    s.process_tick(current_price=10_000)

    assert s.first_amount == approx(0)
    assert s.first_price == approx(0)
    assert s.second_amount == approx(7_000 + 0.25 * 10_000)
    assert s.sell_price == approx(0)
