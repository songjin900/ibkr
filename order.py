from ib_insync import *
# util.startLoop()  # uncomment this line when in a notebook
# python3 demo.py
ib = IB()
ib.connect('127.0.0.1', 7497, clientId=1)

# stock = Stock('AMD','SMART', 'USD')

# order = LimitOrder('BUY', 5, 91.33)
# #order=MarketOrder('10')
# trade = ib.placeOrder(stock,order)

# print(trade)

def orderFilled(trade, fill):
    print("order has been filled")
    print(order)
    print(fill)

# trade.fillEvent += orderFilled

ib.sleep(3)

for trade in ib.trades():
    print("== this is one of my trades =")
    print(trade)

for order in ib.orders():
    print("== this is one of my orders =")
    print(order)

ib.run()

