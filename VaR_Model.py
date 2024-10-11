import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf

class VaR:

    def __init__(self, ticker, shares, risk_free_rate, volatility, simulations, time_in_a_year):
        self.ticker = ticker
        self.shares = shares
        self.risk_free_rate = risk_free_rate
        self.volatility = volatility
        self.simulations = simulations
        self.time_in_a_year = time_in_a_year

    def get_price(self):
        price = yf.Ticker(self.ticker)
        price = price.history().tail(1)['Close'].iloc[0]
        return price

    def get_value(self):
        price = self.get_price()
        value = price * self.shares
        return value

    def calculate(self):
        value = self.get_value()
        end_value = value * np.exp((self.risk_free_rate - .5 * self.volatility ** 2) * self.time_in_a_year + np.random.standard_normal(
            self.simulations) * self.volatility * np.sqrt(self.time_in_a_year))
        returns = end_value - value
        return returns

    def plot(self, returns):
        plt.hist(returns, bins=100, color='blue', edgecolor='black')

    def show_VaR(self, returns):
        percentiles = [10,5,1]
        for i in percentiles:
            confidence = (100-i)/100
            value = np.percentile(returns, i)
            print("VaR at {:.0%} confidence level: ${:,.0f}".format(confidence, value))
            plt.title('Value at Risk')
            plt.xlabel('Value')
            plt.ylabel('Frequency')
            plt.axvline(value, color = 'k', linestyle='dashed')
            plt.savefig('var_chart.png')


if __name__ == "__main__":
    ticker = "WMT" 
    shares = 1000 
    risk_free_rate = 0.0475
    volatility = 0.1955 
    simulations = 5000 
    time_in_a_year = 21/252

    var = VaR(ticker, shares, risk_free_rate, volatility, simulations, time_in_a_year)

    returns = var.calculate()
    var.plot(returns)
    var.show_VaR(returns)