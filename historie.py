"""Haalt volledige dagreeksen op voor de terugrekening en zet ze in de map historie."""
import os, time
import yfinance as yf

REEKSEN = {
    "sp500": "^GSPC", "nasdaq": "^IXIC", "vix": "^VIX", "rente_vs_10j": "^TNX",
    "dollarindex": "DX-Y.NYB", "goud": "GC=F", "zilver": "SI=F", "koper": "HG=F",
    "brent": "BZ=F", "wti": "CL=F", "aardgas_vs": "NG=F", "tarwe": "ZW=F",
    "bitcoin": "BTC-USD", "ether": "ETH-USD", "eurusd": "EURUSD=X",
    "eurostoxx50": "^STOXX50E", "aex": "^AEX", "dax": "^GDAXI",
    "energie": "XLE", "gezondheidszorg": "XLV", "dagelijkse_consumptie": "XLP",
    "basismaterialen": "XLB", "vastgoed": "XLRE", "technologie": "XLK",
    "industrie": "XLI", "nutsbedrijven": "XLU", "financiele_waarden": "XLF",
    "cyclische_consumptie": "XLY", "communicatiediensten": "XLC",
    "defensie_vs": "ITA", "banken_regionaal": "KRE",
}
os.makedirs("historie", exist_ok=True)
for naam, symbool in REEKSEN.items():
    try:
        h = yf.Ticker(symbool).history(period="max", interval="1d", auto_adjust=True)["Close"].dropna()
        h.index = h.index.strftime("%Y-%m-%d")
        h.round(4).to_csv(f"historie/{naam}.csv", header=["Close"], index_label="Date")
        print(f"{naam:24s} {len(h):6d} dagen  {h.index[0]} t/m {h.index[-1]}")
    except Exception as e:
        print(f"{naam:24s} MISLUKT: {str(e)[:80]}")
    time.sleep(0.5)
