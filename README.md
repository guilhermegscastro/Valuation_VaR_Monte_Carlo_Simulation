# Valuation, Value at Risk and Monte Carlo Simulation

## Valuation_Model_FCFF.py:

- This file focuses on the valuation of a company using the Free Cash Flow to the Firm (FCFF) model.
- It calculates the present value of future free cash flows, taking into account discount rates, growth rates, tax and perpetual growth rate.
- The model provides an estimate of the intrinsic value of a firm based on its financial performance and assumptions about future growth, using Yahoo Finance as Data Base.

 Output: <br/>
- Revenue: 665035000000.0
- COGS: 501249000000.0
- Gross Profit: 163786000000.0
- SG&A: 135549000000.0
- Depreciation and Amortization: 12442000000.0
- EBIT: 28237000000.0
- Income Tax Expense: 5342000000.0
- NOPAT: 22895000000.0
- Capex: 21897000000.0
- Property and Equipment: 133738000000.0
- Change in Working Capital: 1009000000.0
- FCFF: 12431000000.0
- COGS Percent Revenue: 0.75
- SG&A Percent Revenue: 0.2
- Depreciation Percent Fixed Assets: 0.09
- Capex percent Depreciation: 1.76
- Average Collection Period - Days: 5.0
- Average Inventory Period - Days: 40.0
- Average Payment Period - Days: 64.0
- Year 1 Projected FCFF: 13314688555.05
- Year 2 Projected FCFF: 13770888527.19
- Year 3 Projected FCFF: 14235084845.29
- Year 4 Projected FCFF: 14706630032.04
- Year 5 Projected FCFF: 15184770194.72
- Year 6 Projected FCFF: 15668634469.79
- Year 7 Projected FCFF: 16157223569.76
- Year 8 Projected FCFF: 16649397361.05
- Year 9 Projected FCFF: 17143861396.54
- Year 10 Projected FCFF: 17639152320.51
- projected_fcffs_terminal: 36360244033.73
- Terminal Value: 1012190577155.3
- NPV of Projected FCFF: 644641395114.27
- Cash Equivalents: 8811000000.0
- Debt: 61305000000.0
- Enterprise Value: 644641395114.27
- Equity Value: 592147395114.27
- The target price for WMT is: $73.67

## Monte_Carlo_Simulation.py:

- This script performs a Monte Carlo simulation to model stock target price movements using the normal distribution approach for future revenue growth.
- It generates multiple price paths for a given stock, based on Revenue Growth rates and Standard Deviation of the last years, and visualizes the results using plots.
- It includes parameters such as the initial basic valuation parameters used in the previous file (Valuation_Model_FCFF.py), as well as the historical revenue growth per year (for the last 4 years) and the number of simulations.

 Monte Carlo Simulation: <br/>
<img src="https://imgur.com/yylthZH.png" height="60%" width="80%" alt="Valuation_VaR_MonteCarlo"/>
<br />
Output: <br/>
- min  Target Price = 27
- mean Target Price = 75
- max  Target Price = 177

## VaR_Model.py:

- The script calculates Value at Risk (VaR) for a portfolio using both the historical and variance-covariance methods.
- It quantifies the potential loss in the portfolio's value (1000 shares of Walmart Stocks) over a specified time frame (30-days), given a certain confidence level (90%, 95% and 99%).
- The code also includes risk measures and visualizations to interpret the VaR results effectively.

 Value at Risk: <br/>
<img src="https://imgur.com/NUlEu7S.png" height="60%" width="80%" alt="Valuation_VaR_MonteCarlo"/>
<br />
Output: <br/>
- VaR at 90% confidence level: $-5,279
- VaR at 95% confidence level: $-6,829
- VaR at 99% confidence level: $-10,036

## Dependencies
- yfinance (Yahoo Finance)
- Numpy
- Pandas
- Matplotlib
- Scipy (for the VaR Model)

<h2>Purpose and Conclusion </h2>
The primary purpose of this project study is to provide a comprehensive analysis of Walmart's fair value, using Valuation metrics, Value at Risk and Monte Carlo Simulation with Python. THIS ANALYSIS ALONE CANNOT BE USED BY FINANCIAL ANALYSTS, INVESTORS, AND DECISION-MAKERS TO UNDERSTAND WALMART'S FAIR VALUE AND IDENTIFY POTENTIAL RISKS.
<br />

</p>

<!--
 ```diff
- text in red
+ text in green
! text in orange
# text in gray
@@ text in purple (and bold)@@
```
--!>
