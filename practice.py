from pydantic import BaseModel


def greet(person_name):
    return "Hello, " + person_name + "!"


# print(greet("Danny"))
# print(greet("Vardaah"))


# def convert_cad_to_usd(cad_amount, exchange_rate):
#     usd_amount = cad_amount * exchange_rate
#     return usd_amount


# print(convert_cad_to_usd(100, 0.73))


def add_tax(price, tax_rate):
    total_price = price + (price * tax_rate)
    return total_price


# print(add_tax(100, 0.13))

# gap = 5
# if gap > 2:
#     print("late")
# else:
#     print("on time")


def is_settlement_late(trade_date, settlement_date):
    gap = settlement_date - trade_date
    if gap > 2:
        return True
    else:
        return False


# print(is_settlement_late(1, 5))
# print(is_settlement_late(1, 2))

# trade_gaps = [1, 3, 5, 2, 7]

# for gap in trade_gaps:
#     print(gap)

# trades = [(1, 5), (2, 3), (10, 11), (1, 8)]

# for trade in trades:
#     trade_date = trade[0]
#     settlement_date = trade[1]
#     late = is_settlement_late(trade_date, settlement_date)
#     print(late)

# print(trade_gaps[0])
# print(trade_gaps[1])
# print(trade_gaps[4])


# trade = {
#     "trade_date": 1,
#     "settlement_date": 5,
#     "amount_usd": 10000,
#     "counterparty": "Broker A"
# }

# print(trade["counterparty"])
# print(trade["amount_usd"])

trades = [
    {"trade_date": 1, "settlement_date": 5, "amount_usd": 10000},
    {"trade_date": 2, "settlement_date": 3, "amount_usd": 5000},
    {"trade_date": 10, "settlement_date": 11, "amount_usd": 25000},
]

for trade in trades:
    trade_date = trade["trade_date"]
    settlement_date = trade["settlement_date"]
    late = is_settlement_late(trade_date, settlement_date)
    print(trade["amount_usd"], "-> late:", late)


class Trade:
    def __init__(self, trade_date, settlement_date, amount_usd):
        self.trade_date = trade_date
        self.settlement_date = settlement_date
        self.amount_usd = amount_usd


t1 = Trade(1, 5, 10000)
t2 = Trade(2, 3, 5000)
print(t1.trade_date)
print(t1.amount_usd)
print(t2.trade_date)
print(t2.amount_usd)


class MetricRequirement(BaseModel):
    metric_name: str
    threshold: float
    weight: float


class RoleProfile(BaseModel):
    position: str
    formation: str
    tactical_toggles: dict
    requirements: list[MetricRequirement]


req1 = MetricRequirement(metric_name="tackles_per90",
                         threshold=2.0, weight=1.5)
req2 = MetricRequirement(
    metric_name="progressive_passes_per90", threshold=3.0, weight=1.0)

profile = RoleProfile(
    position="CDM",
    formation="4-3-3",
    tactical_toggles={},
    requirements=[req1, req2]
)

print(profile.requirements)
print(profile.requirements[0])
print(profile.requirements[0].metric_name)
