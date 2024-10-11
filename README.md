# Valuation, Value at Risk and Monte Carlo Simulation

## Valuation_Model_FCFF.py:

- This file focuses on the valuation of a company using the Free Cash Flow to the Firm (FCFF) model.
- It calculates the present value of future free cash flows, taking into account discount rates, growth rates, and terminal values.
- The model provides an estimate of the intrinsic value of a firm based on its financial performance and assumptions about future growth.

 Data Import: <br/>
<img src="https://imgur.com/oZp9CZA.png" height="60%" width="80%" alt="Valuation_VaR_MonteCarlo"/>
<br />

## Monte_Carlo_Simulation.py:

- This script performs a Monte Carlo simulation to model stock price movements using the Geometric Brownian Motion (GBM) approach.
- It generates multiple price paths for a given stock, analyzes the expected return and risk, and visualizes the results using plots.
- It includes parameters such as the initial stock price, expected return, volatility, time period, and number of simulations.

 Monte Carlo Simulation: <br/>
<img src="https://imgur.com/yylthZH.png" height="60%" width="80%" alt="Valuation_VaR_MonteCarlo"/>
<br />

## VaR_Model.py:

- The script calculates Value at Risk (VaR) for a portfolio using both the historical and variance-covariance methods.
- It quantifies the potential loss in the portfolio's value over a specified time frame, given a certain confidence level.
- The code also includes risk measures and visualizations to interpret the VaR results effectively.

 Value at Risk: <br/>
<img src="https://imgur.com/NUlEu7S.png" height="60%" width="80%" alt="Valuation_VaR_MonteCarlo"/>
<br />
- VaR at 90% confidence level: $-5,279
- VaR at 95% confidence level: $-6,829
- VaR at 99% confidence level: $-10,036

## Dependencies
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
