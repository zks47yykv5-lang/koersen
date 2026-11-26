"""Haalt koersen op via Yahoo Finance en schrijft koersen.json.
Per markt: laatste slotkoers, peildatum, verandering over een maand en een jaar."""
import json, sys, time
from datetime import datetime, timezone
import pandas as pd
import yfinance as yf

MARKTEN = {
    "Energie": "XLE", "Gezondheidszorg": "XLV", "Dagelijkse consumptie": "XLP",
    "Basismaterialen": "XLB", "Vastgoed": "XLRE", "Technologie": "XLK",
    "Industrie": "XLI", "Nutsbedrijven": "XLU", "Financiële waarden": "XLF",
    "Cyclische consumptie": "XLY", "Communicatiediensten": "XLC",
    "S&P 500": "^GSPC", "Goud": "GC=F", "Olie (Brent)": "BZ=F", "Bitcoin": "BTC-USD",
    "Euro Stoxx 50": "^STOXX50E", "AEX": "^AEX", "DAX": "^GDAXI",
    "Staatsobligaties VS (10 jaar)": "^TNX",
    "Zilver": "SI=F", "Koper": "HG=F", "Aardgas Europa (TTF)": "TTF=F",
    "Aardgas VS (Henry Hub)": "NG=F", "Tarwe": "ZW=F",
    "Ether": "ETH-USD", "Solana": "SOL-USD", "XRP": "XRP-USD", "Euro (EUR/USD)": "EURUSD=X",
    "TSMC": "TSM", "Nvidia": "NVDA", "ASML": "ASML.AS", "Apple": "AAPL", "Microsoft": "MSFT",
    "Alphabet": "GOOGL", "Amazon": "AMZN", "Tesla": "TSLA", "JPMorgan Chase": "JPM",
    "ExxonMobil": "XOM", "Lockheed Martin": "LMT", "Rheinmetall": "RHM.DE",
    "BAE Systems": "BA.L", "Saab": "SAAB-B.ST", "Thales": "HO.PA",
    "CVS Health": "CVS", "Cigna": "CI", "UnitedHealth": "UNH", "Coinbase": "COIN",
}
RENTE = {"^TNX"}  # koers is een rente in procenten

def eerder(reeks, maanden):
    doel = reeks.index[-1] - pd.DateOffset(months=maanden)
    deel = reeks[reeks.index <= doel]
    return float(deel.iloc[-1]) if len(deel) else None

rijen, fouten = [], []
for markt, symbool in MARKTEN.items():
    try:
        h = yf.Ticker(symbool).history(period="2y", interval="1d", auto_adjust=False)
        reeks = h["Close"].dropna()
        if len(reeks) < 30:
            raise ValueError("te weinig koersen")
        nu, m1, j1 = float(reeks.iloc[-1]), eerder(reeks, 1), eerder(reeks, 12)
        if symbool in RENTE:
            r1m = None if m1 is None else round(-8 * (nu - m1), 1)
            r1j = None if j1 is None else round(-8 * (nu - j1), 1)
        else:
            r1m = None if m1 is None else round((nu / m1 - 1) * 100, 2)
            r1j = None if j1 is None else round((nu / j1 - 1) * 100, 2)
        rijen.append({"sector": markt, "symbool": symbool, "koers": round(nu, 4),
                      "r1m": r1m, "r1j": r1j, "peildatum": reeks.index[-1].strftime("%Y-%m-%d")})
        print(f"{markt:32s} {nu:12.2f}  1m {r1m}  ({reeks.index[-1].date()})")
    except Exception as e:
        fouten.append({"sector": markt, "symbool": symbool, "fout": str(e)[:120]})
        print(f"{markt:32s} MISLUKT: {str(e)[:80]}")
    time.sleep(0.5)

uit = {"bijgewerkt": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
       "bron": "Yahoo Finance via yfinance", "rows": rijen, "fouten": fouten}
with open(sys.argv[1] if len(sys.argv) > 1 else "koersen.json", "w") as f:
    json.dump(uit, f, ensure_ascii=False, indent=1)
print(f"\n{len(rijen)} markten gelukt, {len(fouten)} mislukt")
