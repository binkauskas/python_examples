import time
import random

class Trade:
	#Simple class to represent a trade
	def __init__(self, timestamp, quantity, indicator, price):
		self.timestamp = timestamp
		self.quantity = quantity
		self.indicator = indicator
		self.price = price

class Stock:
	#Simple class to represent a stock
	def __init__(self, stock_symbol, stock_type, last_divident, fixed_divident, par_value):
		self.symbol = stock_symbol
		self.type = stock_type
		self.last_divident = last_divident
		self.fixed_divident = fixed_divident
		self.par_value = par_value
		self.trades = []

	def get_dividend_yield(self, market_price):
		try:
			if self.type == "Common":
				return self.last_divident / market_price
			elif self.type == "Preferred":
				return (self.fixed_divident * self.par_value) / market_price
			else:
				return None
		except ZeroDivisionError as e:
			print (self.symbol, "Dividend yield Err:", e)
			return None	

	def get_PE_ratio (self, market_price):
		try:
			return market_price / self.last_divident
		except ZeroDivisionError as e:
			print (self.symbol, "P/E ratio Err:", e)
			return None

	def record_trade(self, trade):
		if isinstance(trade, Trade):
			self.trades.append(trade)
		else:
			raise TypeError("Must pass a Trade object to Stock.record_trade()", trade)

	def get_volume_weighted_stock_price(self, time_margin_sec):
		#Ref basic arithmetic: divident/divisor = quatient
		divident = 0
		divisor = 0
		time_cut_off =  time.time() - time_margin_sec
		#asuming trade data comes in real time, this list will be chronologically sorted
		#traversing most recent data then becomes easy
		for trade in reversed(self.trades):
			if trade.timestamp < time_cut_off:
				break
			divident += trade.price * trade.quantity
			divisor += trade.quantity
		try:
			return divident / divisor
		except ZeroDivisionError as e:
			print (self.symbol, "Volume weighted stock price Err:", e)
			return None		

FIFTEEN_MINUTES = 15 * 60
PRINT_FORMAT = ".3f"

def generate_trade():
	return Trade(time.time(), random.randint(1,20), random.choice('BS'), random.randint(60, 500))

#Even though not utilized below, a dictionary to quickly look up a specific stock seems rational
stocks = {
	"TEA" : Stock("TEA","Common",0, None,100),
	"POP" : Stock("POP","Common",8, None,100),
	"ALE" : Stock("ALE","Common",23, None,60),
	"GIN" : Stock("GIN","Preferred",8, 0.02,100),
	"JOE" : Stock("JOE","Common",13, None,250)
}


#"Calculate the GBCE All Share Index using the geometric mean of prices for all stocks"
#TODO: Ask - Is this geometric mean supposed to be based on Volume Weighted Stock prices, or Market prices?


MP_geometric_mean = 1
VWSP_geometric_mean = 1


print("Stock, Market price, Divident yield, P/E Ratio, Volume Weighted Stock Price")
for stock in stocks.values():
	#Generate and record some random trades
	for i in range(1, random.randint(2,20)):
		stock.record_trade(generate_trade())
	#Generate random market price and calculate metrics	
	rmp	= random.randint(60, 500);
	div_yield = stock.get_dividend_yield(rmp)
	pe_ratio = stock.get_PE_ratio(rmp)
	vw_stock_price = stock.get_volume_weighted_stock_price(FIFTEEN_MINUTES)
	MP_geometric_mean *= rmp
	VWSP_geometric_mean *= vw_stock_price
	#printing table entries with somewhat nicer format
	print(
		stock.symbol, 
		rmp,
		"None" if div_yield is None else format(div_yield, PRINT_FORMAT),
		"None" if pe_ratio is None else format(pe_ratio, PRINT_FORMAT),
		"None" if vw_stock_price is None else format(vw_stock_price, PRINT_FORMAT))

#NOTE: pow(x, 1/n) returns nth root of x. 
#It is inaccurate due to floating point arithmetic, but seems like a commonly used solution
#EX: pow(5**6, 1/6) returned 4.999999999999999...
#Could use a more sophisticated library if required
print("All share Index (based on Market price):", pow(MP_geometric_mean, 1/len(stocks)))
print("All share Index (based on Volume Weighted stock price):", pow(VWSP_geometric_mean, 1/len(stocks)))





