from statsbombpy import sb
from pydantic import BaseModel


def greet(person_name):
    return "Hello, " + person_name + "!"


def add_tax(price, tax_rate):
    total_price = price + (price * tax_rate)
    return total_price


def is_settlement_late(trade_date, settlement_date):
    gap = settlement_date - trade_date
    if gap > 2:
        return True
    else:
        return False


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


class Player:
    def __init__(self, name, position, goals):
        self.name = name
        self.position = position
        self.goals = goals

    @classmethod
    def new_player(cls, name, position):
        return cls(name, position, 0)


p1 = Player("Rodri", "CDM", 8)
print(p1.name)
print(p1.goals)
print(f"{p1.name} plays {p1.position} and scored {p1.goals} goals")

p3 = Player.new_player("Haaland", "ST")
print(p3.goals)

big_trades = [t for t in trades if t["amount_usd"] > 8000]
print(big_trades)

trade_dates = [t["trade_date"] for t in trades]
print(trade_dates)

small_trades = [t for t in trades if t["amount_usd"] < 8000]
print(small_trades)

trade = {"amount_usd": 10000}
print(trade.get("amount_usd"))
print(trade.get("counterparty"))
print(trade.get("counterparty", "Unknown"))

side_a = [
    {"trade_id": "T1", "amount_usd": 10000},
    {"trade_id": "T2", "amount_usd": 5000},
    {"trade_id": "T3", "amount_usd": 25000},
    {"trade_id": "T4", "amount_usd": 7000},
]

side_b = [
    {"trade_id": "T1", "amount_usd": 10000},
    {"trade_id": "T2", "amount_usd": 5500},
    {"trade_id": "T3", "amount_usd": 25000},
]

side_b_lookup = {}
for trade in side_b:
    side_b_lookup[trade["trade_id"]] = trade

print(side_b_lookup)

for trade in side_a:
    trade_id = trade["trade_id"]
    amount_a = trade["amount_usd"]
    matching_trade = side_b_lookup.get(trade_id)

    if matching_trade is None:
        print(f"Missing on side_b: {trade_id}")
        continue

    amount_b = matching_trade["amount_usd"]
    if amount_a != amount_b:
        print(f"Break on {trade_id}: side_a={amount_a}, side_b={amount_b}")

clock = "45:30"
mm, ss = clock.split(":")
print(mm)
print(ss)


matches = sb.matches(competition_id=11, season_id=90)
match_id = matches["match_id"].iloc[0]
events = sb.events(match_id=match_id)

print(events.columns.tolist())
