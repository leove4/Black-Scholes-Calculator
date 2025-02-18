# Black-Scholes-Calculator
A python tool to price options including automatic volatility calculation

## Requirements
- yfinance

  ```bash
  pip install yfinance
  ````

## How to install

  ```bash
  git clone https://github.com/leove4/Black-Scholes-Calculator
  cd Black-Scholes-Calculator
  ```

## How it works

  ```bash
  python calc.py
  ````

- Just define stock ticker, strike, expiry date, call/put and risk free rate (example : between 0.025 and 0.03 in France currently)
- with price data from yfinance the program computes the annualized historical volatility

$$\sigma_{\text{annual}} = \sqrt{252} \times \sqrt{\frac{1}{n-1} \sum_{i=1}^{n}\bigl(r_i - \bar{r}\bigr)^2}$$


- Returns the premium estimated by BSM equations.

$$d_1 = \frac{\ln\!\Bigl(\frac{S}{K}\Bigr) + \Bigl(r + \frac{\sigma^2}{2}\Bigr) \, T}{\sigma \,\sqrt{T}}, 
\quad
d_2 = d_1 - \sigma \sqrt{T}$$

For a Call option:

$$\text{Call Price} = S \,\Phi(d_1)\; -\; K \, e^{-rT} \,\Phi(d_2)$$


For a Put option:

$$\text{Put Price} = K \, e^{-rT}\,\Phi(-d_2)\; -\; S \,\Phi(-d_1)$$

## Comparing with prices from actual option chains

  ```bash
  python opcheck.py
  ````
- Enter a ticker and the risk free rate
- this program will compare in a table market prices (from yfinance option chain) and our price in 2 columns : absdiff (absolute difference) and pctdiff (percentage difference)
