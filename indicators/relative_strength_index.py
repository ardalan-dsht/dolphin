import pandas as pd

class RelativeStrengthIndex :
    def __init__(self, prices: pd.Series, period:int)->pd.Series:
        self.prices = prices
        self.period = period
    
    def rsi_in_point_p(self, prices) -> float:
        delta = self.prices.diff()
        delta = delta[1:]
        up, down = delta.copy(), delta.copy()
        up[up < 0] = 0
        down[down > 0] = 0
        roll_up = up.ewm(span=self.period).mean()
        roll_down = down.abs().ewm(span=self.period).mean()
        rs = roll_up / roll_down
        return 100 - (100/rs+1)


    def __call__(self)-> pd.Series:
        rsi = []
        for each_price_point in range(self.period,len(self.prices)):
            slice_of_prices = self.prices[each_price_point-self.period:each_price_point]
            moving_average_in_point_p = self.rsi_in_point_p(slice_of_prices)
            rsi.append(moving_average_in_point_p)
        return pd.Series(rsi)