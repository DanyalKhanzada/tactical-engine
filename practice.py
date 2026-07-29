def greet(person_name):
    return "Hello, " + person_name + "!"


print(greet("Danny"))
print(greet("Vardaah"))


def convert_cad_to_usd(cad_amount, exchange_rate):
    usd_amount = cad_amount * exchange_rate
    return usd_amount


print(convert_cad_to_usd(100, 0.73))


def add_tax(price, tax_rate):
    total_price = price + (price * tax_rate)
    return total_price


print(add_tax(100, 0.13))

gap = 5
if gap > 2:
    print("late")
else:
    print("on time")


def is_settlement_late(trade_date, settlement_date):
    gap = settlement_date - trade_date
    if gap > 2:
        return True
    else:
        return False


print(is_settlement_late(1, 5))
print(is_settlement_late(1, 2))
