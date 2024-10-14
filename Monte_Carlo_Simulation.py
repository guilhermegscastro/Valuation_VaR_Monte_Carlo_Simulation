import numpy as np
import numpy_financial as npf
import matplotlib.pyplot as plt
import yfinance as yf

np.random.seed(123)

class Monte_Carlo_Simulation:

    def __init__(self, ticker, discount_rate, perpetual_growth_rate, tax):
        self.ticker = ticker
        self.discount_rate = discount_rate    
        self.perpetual_growth_rate = perpetual_growth_rate
        self.tax = tax

        self.stock = yf.Ticker(ticker)
        self.income_statement = self.stock.quarterly_financials.T
        self.balance_sheet = self.stock.quarterly_balance_sheet.T
        self.balance_sheet_transpose = self.stock.quarterly_balance_sheet
        self.cashflow = self.stock.quarterly_cashflow.T
        self.info = self.stock.info
        self.Quarter = self.stock.quarterly_balance_sheet.columns

    def get_growth_revenue_stats(self):
        """
        Calculate the mean and standard deviation of the revenue growth over the last X years.
        """
        number_of_years = 4

        # Fetch the financial data
        financials = self.stock.financials.transpose()  # Transpose to get years as rows

        # Extract the revenue data
        revenue = financials['Total Revenue'][::-1]  # Reverse the order to get chronological order

        if len(revenue) < number_of_years:  # Need at least X years to calculate (X-1) years of growth
            raise ValueError("Not enough data to calculate the growth revenue statistics for the last 4 years.")

        # Calculate year-over-year growth revenue
        growth_revenue = revenue.pct_change().dropna()

        # Get the last (X-1) years of growth revenue
        last_years_growth = growth_revenue.tail(number_of_years - 1)
    
        # Calculate mean and standard deviation
        mean_growth = last_years_growth.mean()
        std_growth = last_years_growth.std()

        return mean_growth, std_growth

    def run_simulation(self):
        """
        Run the Monte Carlo simulation using the mean and standard deviation of revenue growth.
        """
        num_simulations = 1000

        # Get the revenue growth statistics
        revenue_growth_mean, revenue_growth_std = self.get_growth_revenue_stats()

        # Simulate revenue growth rates
        revenue_growth_values = np.random.normal(revenue_growth_mean, revenue_growth_std, num_simulations)

        return revenue_growth_values

    def calculate_valuation(self, revenue_growth):

        # Calculate historical values
        revenue = self.income_statement['Total Revenue'].iloc[:4].sum()
        cogs = self.income_statement['Cost Of Revenue'].iloc[:4].sum()
        gross_profit = revenue - cogs
        
        dep_and_amort = self.cashflow['Depreciation And Amortization'].iloc[:4].sum()
        sg_and_a = self.income_statement["Selling General And Administration"].iloc[:4].sum()
        
        ebit = gross_profit - sg_and_a
        income_tax_expense = self.income_statement['Tax Provision'].iloc[:4].sum()
        nopat = ebit - income_tax_expense
        
        capex = abs(self.cashflow["Capital Expenditure"].iloc[:4].sum())
        
        Property_and_Equipment = self.balance_sheet['Net PPE'].iloc[0]
        
        change_in_working_capital = ((self.balance_sheet_transpose[self.Quarter[0]]['Accounts Receivable'] + self.balance_sheet_transpose[self.Quarter[0]]['Inventory'] - self.balance_sheet_transpose[self.Quarter[0]]['Payables And Accrued Expenses']) - (self.balance_sheet_transpose[self.Quarter[4]]['Accounts Receivable'] + self.balance_sheet_transpose[self.Quarter[4]]['Inventory'] - self.balance_sheet_transpose[self.Quarter[4]]['Payables And Accrued Expenses']))
        
        fcff = nopat + dep_and_amort - capex - change_in_working_capital

        # Calculate projected FCFF for 10 years based on historical values 
        
        cogs_percent_revenue = cogs / revenue
        sg_and_a_percent_revenue = sg_and_a / revenue
        dep_percent_fixed_assets = dep_and_amort / Property_and_Equipment
        capex_percent_dep_and_amort = capex / dep_and_amort
        average_collection_period = (self.balance_sheet_transpose[self.Quarter[0]]['Accounts Receivable'] * 365) / revenue
        average_inventory_period = (self.balance_sheet_transpose[self.Quarter[0]]['Inventory'] * 365) / cogs
        average_payment_period = (self.balance_sheet_transpose[self.Quarter[0]]['Payables And Accrued Expenses'] * 365) / cogs
        
        projected_fcffs = []
        
        for i in range(10):
            
            receivable_1 = (average_collection_period * revenue) / 365
            inventory_1 = (average_inventory_period * cogs) / 365
            payment_1 = (average_payment_period * cogs) / 365
            
            revenue *= (1 + revenue_growth)
            cogs = revenue * cogs_percent_revenue
            gross_profit = revenue - cogs

            sg_and_a = revenue * sg_and_a_percent_revenue
            
            ebit = gross_profit - sg_and_a
            nopat = ebit * (1 - self.tax)
            
            Property_and_Equipment = Property_and_Equipment + capex - dep_and_amort
            
            dep_and_amort =  Property_and_Equipment * dep_percent_fixed_assets
            
            capex = dep_and_amort * capex_percent_dep_and_amort
            
            receivable_2 = (average_collection_period * revenue) / 365
            inventory_2 = (average_inventory_period * cogs) / 365
            payment_2 = (average_payment_period * cogs) / 365
            
            change_in_working_capital = (receivable_2 + inventory_2 - payment_2) - (receivable_1 + inventory_1 - payment_1)

            fcff = nopat + dep_and_amort - capex - change_in_working_capital
            projected_fcffs.append(fcff)
        
        # Calculate Terminal Value using Gordon Growth Model
        
        projected_fcffs_terminal = projected_fcffs[-1] + capex - dep_and_amort
        
        terminal_value = projected_fcffs_terminal * (1 + self.perpetual_growth_rate) / (self.discount_rate - self.perpetual_growth_rate)
        
        projected_fcffs.append(terminal_value)
        
        # Calculate NPV of projected FCFF
        npv_fcff = npf.npv(self.discount_rate, projected_fcffs)

        # Calculate Enterprise Value and Equity Value
        cash_equivalents = self.balance_sheet['Cash And Cash Equivalents'].iloc[0]
        debt = self.balance_sheet['Total Debt'].iloc[0]

        enterprise_value = npv_fcff
        equity_value = enterprise_value + cash_equivalents - debt

        # Calculate target price
        shares_outstanding = self.info['sharesOutstanding']
        target_price = equity_value / shares_outstanding

        return target_price
    
    def show_info(self, target_prices):
        plt.hist(target_prices, bins=50, color='blue', edgecolor='black')
        plt.title('Monte Carlo Simulation of Target Prices')
        plt.axvline(0, color = 'k', linestyle='dashed')
        plt.xlabel('Target Price')
        plt.ylabel('Frequency')
        plt.savefig('monte_carlo_chart.png')

            # Plot a histogram of the target prices
        print("min  Target Price =",round(min(target_prices)))
        print("mean Target Price =",round(np.mean(target_prices)))
        print("max  Target Price =",round(max(target_prices)))

if __name__ == "__main__":
    ticker = "WMT"
    discount_rate = 0.067
    perpetual_growth_rate = 0.03
    tax = 0.25

    model = Monte_Carlo_Simulation(ticker, discount_rate, perpetual_growth_rate, tax)

    # Run the simulation to get multiple revenue growth values
    revenue_growth_values = model.run_simulation()

    # Calculate target prices for each simulated revenue growth value
    target_prices = [model.calculate_valuation(rg) for rg in revenue_growth_values]

    Monte_Carlo_Simulation.show_info(model, target_prices)
    