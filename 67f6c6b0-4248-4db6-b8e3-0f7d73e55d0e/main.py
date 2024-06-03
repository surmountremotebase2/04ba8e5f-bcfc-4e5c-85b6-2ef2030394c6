from surmount.base_class import Strategy, TargetAllocation
from surmount.data import Asset, Fundamental
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        # Assuming we have access to fundamental data about Nike and SPY for revenue analysis
        self.tickers = ["NKE", "SPY"]  # NKE for Nike, SPY as a proxy for broader market/GAAP revenue
        # Initialize data list with fundamental data objects if available
        self.data_list = [Fundamental(i) for i in self.tickers]

    @property
    def interval(self):
        return "1day"

    @property
    def assets(self):
        return self.tickers

    @property
    def data(self):
        return self.data_list

    def run(self, data):
        allocation_dict = {"NKE": 0, "SPY": 0}  # Initialize allocation with no investment
        
        # Extract fundamental data for Nike and SPY
        nike_fundamentals = data.get(("fundamental", "NKE"), {})
        spy_fundamentals = data.get(("fundamental", "SPY"), {})
        
        # Check for data availability
        if nike_fundamentals and spy_fundamentals:
            # Assuming 'revenue' is a key in the fundamental data and it is a list of dictionaries
            # Where each dictionary represents a quarterly data point with 'value' and 'date' keys
            nike_latest_revenue = nike_fundamentals.get('revenue', [{}])[-1].get('value', 0)
            spy_latest_revenue = spy_fundamentals.get('revenue', [{}])[-1].get('value', 0)
            spy_previous_revenue = spy_fundamentals.get('revenue', [{}])[-2].get('value', 0)
            
            # Strategy logic: Buy NKE if Nike's latest revenue is positive and SPY's latest revenue declined compared to the previous period
            if nike_latest_revenue > 0 and spy_latest_revenue < spy_previous_revenue:
                log("Buying Nike as revenue is positive and general market (GAAP) revenue is declining.")
                allocation_dict["NKE"] = 1  # Allocate 100% to Nike
            else:
                log("Conditions not met for buying Nike.")
        else:
            log("Fundamental data missing for NKE or SPY.")

        return TargetAllocation(allocation_dict)