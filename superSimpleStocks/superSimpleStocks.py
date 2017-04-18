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

	#Simple class to represent a Stock superclass
	#From test data given, assume that all stocks will have these fields
	def __init__(self, stock_symbol, last_dividend, par_value):
		self.symbol = stock_symbol
		self.last_dividend = last_dividend
		self.par_value = par_value
		self.trades = []

	def get_dividend_yield(self, market_price):
		raise NotImplementedError("get_dividend_yield not implemented yet")

	def get_PE_ratio (self, market_price):
		try:
			return market_price / self.last_dividend
		except ZeroDivisionError as e:
			print (self.symbol, "P/E ratio Err:", e)
			return None

	def record_trade(self, trade):
		if isinstance(trade, Trade):
			self.trades.append(trade)
		else:
			raise TypeError("Must pass a Trade object to Stock.record_trade()", trade)

	def get_volume_weighted_stock_price(self, time_margin_sec):
		#Ref basic arithmetic: dividend/divisor = quatient
		dividend = 0
		divisor = 0
		time_cut_off =  time.time() - time_margin_sec
		#asuming trade data comes in real time, this list will be chronologically sorted
		#traversing most recent data then becomes easy
		for trade in reversed(self.trades):
			if trade.timestamp < time_cut_off:
				break
			dividend += trade.price * trade.quantity
			divisor += trade.quantity
		try:
			return dividend / divisor
		except ZeroDivisionError as e:
			print (self.symbol, "Volume weighted stock price Err:", e)
			return None

class CommonStock(Stock):
	#Stock class extention to represent a Common Stock
	def __init__(self, stock_symbol, last_dividend, par_value):
		super().__init__(stock_symbol, last_dividend, par_value)

	def get_dividend_yield(self, market_price):
		try:
			return self.last_dividend / market_price
		except ZeroDivisionError as e:
			print (self.symbol, "Dividend yield Err:", e)
			return None		

class PreferredStock(Stock):
	#Stock class extention to represent a Preferred Stock
	def __init__(self, stock_symbol, last_dividend, fixed_dividend, par_value):
		super().__init__(stock_symbol, last_dividend, par_value)
		self.fixed_dividend = fixed_dividend

	def get_dividend_yield(self, market_price):			
		try:
			return (self.fixed_dividend * self.par_value) / market_price
		except ZeroDivisionError as e:
			print (self.symbol, "Dividend yield Err:", e)
			return None		


FIFTEEN_MINUTES = 15 * 60
PRINT_FORMAT = ".3f"

def generate_trade():
	return Trade(time.time(), random.randint(1,20), random.choice('BS'), random.randint(60, 500))

#Even though not utilized below, a dictionary to quickly look up a specific stock seems rational
stocks = {
	"TEA" : CommonStock("TEA", 0, 100),
	"POP" : CommonStock("POP", 8, 100),
	"ALE" : CommonStock("ALE", 23, 60),
	"GIN" : PreferredStock("GIN", 8, 0.02, 100),
	"JOE" : CommonStock("JOE", 13, 250)
}


#"Calculate the GBCE All Share Index using the geometric mean of prices for all stocks"
#TODO: Ask - Is this geometric mean supposed to be based on Volume Weighted Stock prices, or Market prices?


MP_geometric_mean = 1
VWSP_geometric_mean = 1


print("Stock, Market price, Dividend yield, P/E Ratio, Volume Weighted Stock Price")
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





