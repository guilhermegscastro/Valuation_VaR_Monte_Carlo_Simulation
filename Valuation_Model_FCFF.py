import numpy_financial as npf
import yfinance as yf

class Valuation_Model_FCFF:
    def __init__(self, ticker, revenue_growth, discount_rate, perpetual_growth_rate, tax):
        self.ticker = ticker
        self.revenue_growth = revenue_growth
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

    def show_info(self):

        print("Income Statement Columns:", self.income_statement.columns)
        print("Balance Sheet Columns:", self.balance_sheet.columns)
        print("Cash Flow Columns:", self.cashflow.columns)

    def calculate_valuation(self):

        # Calculate historical values
        revenue = self.income_statement['Total Revenue'].iloc[:4].sum()
        cogs = self.income_statement['Cost Of Revenue'].iloc[:4].sum()
        gross_profit = revenue - cogs

        print("Revenue:", revenue)
        print("COGS:", cogs)
        print("Gross Profit:", gross_profit)
        
        dep_and_amort = self.cashflow['Depreciation And Amortization'].iloc[:4].sum()
        sg_and_a = self.income_statement["Selling General And Administration"].iloc[:4].sum()

        print("SG&A:", sg_and_a)
        print("Depreciation and Amortization:", dep_and_amort)
        
        ebit = gross_profit - sg_and_a
        income_tax_expense = self.income_statement['Tax Provision'].iloc[:4].sum()
        nopat = ebit - income_tax_expense

        print("EBIT:", ebit)
        print("Income Tax Expense:", income_tax_expense)
        print("NOPAT:", nopat)
        
        capex = abs(self.cashflow["Capital Expenditure"].iloc[:4].sum())
        
        Property_and_Equipment = self.balance_sheet['Net PPE'].iloc[0]
        
        change_in_working_capital = ((self.balance_sheet_transpose[self.Quarter[0]]['Accounts Receivable'] + self.balance_sheet_transpose[self.Quarter[0]]['Inventory'] - self.balance_sheet_transpose[self.Quarter[0]]['Payables And Accrued Expenses']) - (self.balance_sheet_transpose[self.Quarter[4]]['Accounts Receivable'] + self.balance_sheet_transpose[self.Quarter[4]]['Inventory'] - self.balance_sheet_transpose[self.Quarter[4]]['Payables And Accrued Expenses']))

        print("Capex:", capex)
        print("Property and Equipment:", Property_and_Equipment)
        print("Change in Working Capital:", change_in_working_capital)

        fcff = nopat + dep_and_amort - capex - change_in_working_capital
        
        print("FCFF:", fcff)

        # Calculate projected FCFF for 10 years based on historical values 
        
        cogs_percent_revenue = cogs / revenue
        sg_and_a_percent_revenue = sg_and_a / revenue
        dep_percent_fixed_assets = dep_and_amort / Property_and_Equipment
        capex_percent_dep_and_amort = capex / dep_and_amort
        average_collection_period = (self.balance_sheet_transpose[self.Quarter[0]]['Accounts Receivable'] * 365) / revenue
        average_inventory_period = (self.balance_sheet_transpose[self.Quarter[0]]['Inventory'] * 365) / cogs
        average_payment_period = (self.balance_sheet_transpose[self.Quarter[0]]['Payables And Accrued Expenses'] * 365) / cogs
        
        print("COGS Percent Revenue:", round(cogs_percent_revenue,2))
        print("SG&A Percent Revenue:", round(sg_and_a_percent_revenue,2))
        print("Depreciation Percent Fixed Assets:", round(dep_percent_fixed_assets,2))
        print("Capex percent Depreciation:", round(capex_percent_dep_and_amort,2))
        print("Average Collection Period - Days:", round(average_collection_period,0))
        print("Average Inventory Period - Days:", round(average_inventory_period,0))
        print("Average Payment Period - Days:", round(average_payment_period,0))
        
        projected_fcffs = []
        
        for i in range(10):
            
            receivable_1 = (average_collection_period * revenue) / 365
            inventory_1 = (average_inventory_period * cogs) / 365
            payment_1 = (average_payment_period * cogs) / 365
            
            revenue *= (1 + self.revenue_growth)
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
            
            print(f"Year {i+1} Projected FCFF:", round(fcff,2))
        
        # Calculate Terminal Value using Gordon Growth Model
        
        projected_fcffs_terminal = projected_fcffs[-1] + capex - dep_and_amort
        
        print(f"projected_fcffs_terminal:", round(projected_fcffs_terminal,2))
        
        terminal_value = projected_fcffs_terminal * (1 + self.perpetual_growth_rate) / (self.discount_rate - self.perpetual_growth_rate)
        
        projected_fcffs.append(terminal_value)

        print(f"Terminal Value:", round(terminal_value,2))
        
        # Calculate NPV of projected FCFF
        npv_fcff = npf.npv(self.discount_rate, projected_fcffs)
        
        print("NPV of Projected FCFF:", round(npv_fcff,2))

        # Calculate Enterprise Value and Equity Value
        cash_equivalents = self.balance_sheet['Cash And Cash Equivalents'].iloc[0]
        debt = self.balance_sheet['Total Debt'].iloc[0]
        
        print("Cash Equivalents:", round(cash_equivalents,2))
        print("Debt:", round(debt,2))

        enterprise_value = npv_fcff
        equity_value = enterprise_value + cash_equivalents - debt
        
        print("Enterprise Value:", round(enterprise_value,2))
        print("Equity Value:", round(equity_value,2))

        # Calculate target price
        shares_outstanding = self.info['sharesOutstanding']
        target_price = equity_value / shares_outstanding

        return target_price

if __name__ == "__main__":
    ticker = "WMT"
    revenue_growth = 0.05
    discount_rate = 0.067
    perpetual_growth_rate = 0.03
    tax = 0.25

    model = Valuation_Model_FCFF(ticker, revenue_growth, discount_rate, perpetual_growth_rate, tax)

    target_price = model.calculate_valuation()

    print(f"The target price for {ticker} is: ${target_price:.2f}")

    Valuation_Model_FCFF.show_info(model)