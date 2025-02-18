import yfinance as yf, math, datetime as dt
from statistics import NormalDist

while True:
    ticker = input("Ticker: ")
    K = float(input("Strike: "))
    exp = input("Expiry (YYYY-MM-DD): ")
    cp = input("Call or Put (C/P): ").upper()
    r = float(input("Risk-free rate (e.g. 0.025): "))

    data = yf.Ticker(ticker).history(period="1y")
    S = data["Close"].iloc[-1]
    rets = data["Close"].pct_change().dropna()
    sigma = rets.std() * math.sqrt(252)

    T = (dt.datetime.strptime(exp, "%Y-%m-%d") - dt.datetime.now()).days / 365
    d1 = (math.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)
    N = NormalDist().cdf

    call_val = S * N(d1) - K * math.exp(-r * T) * N(d2)
    put_val = K * math.exp(-r * T) * N(-d2) - S * N(-d1)
    premium = call_val if cp == 'C' else put_val

    print(f"Black–Scholes {('Call' if cp=='C' else 'Put')} premium: {premium:.2f}")

    again = input("Try another? (y/n): ").strip().lower()
    if again != 'y':
        break
