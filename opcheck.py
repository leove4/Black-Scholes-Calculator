import yfinance as yf, pandas as pd, math, datetime as dt
from statistics import NormalDist

pd.set_option('display.max_rows', None)
pd.set_option('display.float_format', '{:.4f}'.format)

while True:
    t = input("Ticker: ")
    r = float(input("Risk-free rate (decimal): "))
    closes = yf.Ticker(t).history(period="1y")["Close"]
    S = closes.iloc[-1]
  
    sig = closes.pct_change().std() * math.sqrt(252)
    exps = yf.Ticker(t).options
    dfs = []
    for e in exps:
        c = yf.Ticker(t).option_chain(e)
        for d,o in [(c.calls,"CALL"),(c.puts,"PUT")]:
            d["optionType"] = o
            d["expiration"] = e
            dfs.append(d)
    df = pd.concat(dfs, ignore_index=True)

    def T(e): 
        return max((dt.datetime.strptime(e, "%Y-%m-%d") - dt.datetime.now()).days, 0)/365

    N = NormalDist().cdf
    def bs_price(S, K, r, T, sigma, opt):
        if T <= 0: return 0
        d1 = (math.log(S/K) + (r + 0.5*sigma*sigma)*T) / (sigma*math.sqrt(T))
        d2 = d1 - sigma*math.sqrt(T)
        return (S*N(d1) - K*math.exp(-r*T)*N(d2)) if opt=="CALL" else (K*math.exp(-r*T)*N(-d2) - S*N(-d1))

    df["T"] = df["expiration"].apply(T)
    df["bsPremium"] = df.apply(lambda x: bs_price(S, x["strike"], r, x["T"], sig, x["optionType"]), axis=1)
    df["absDiff"] = df["bsPremium"] - df["lastPrice"]
    df["pctDiff"] = 100*df["absDiff"] / df["lastPrice"].replace(0, float("nan"))
    df = df.sort_values(by="pctDiff", ascending=False)
    


    print(df[["contractSymbol","optionType","expiration","strike","lastPrice","bsPremium","absDiff","pctDiff"]])

    again = input("Try another? (y/n): ").strip().lower()
    if again != 'y':
        break
