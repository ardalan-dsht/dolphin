import pandas as pd

class MovingAverage:
    def __init__(self, prices:pd.Series, period:int = 14):
        self.prices = prices
        self.period = period

    def ma_in_point_p(self, prices) -> float:
        raise NotImplementedError("You can not use this method, Child class must implement this method.")

    def __call__(self)-> pd.Series:
        moving_average_line = []
        for i in range(self.period):
            moving_average_line.append(0.0)
        for each_price_point in range(self.period,len(self.prices)):
            slice_of_prices = self.prices[each_price_point-self.period:each_price_point]
            moving_average_in_point_p = self.ma_in_point_p(slice_of_prices)
            moving_average_line.append(moving_average_in_point_p)
        return pd.Series(moving_average_line)


class SimpleMovingAverage(MovingAverage):
    def ma_in_point_p(self, prices) -> float:
        sma = sum(prices)/len(prices)
        return round(sma,4)
    
    
class WeightedMovingAverage(MovingAverage):
    def ma_in_point_p(self, prices)-> float:
        wma = 0
        for index, price in enumerate(prices):
            wma += index* price
        return wma


class ExponentialMovingAverage(MovingAverage):
    def ma_in_point_p(self, prices) -> float:
        ema = 0
        k = 2/(len(prices)+1)
        for index, price in enumerate(prices):
            ema = (price*k) + (ema * (1-k))
        return ema


class TriangularMovingAverage(MovingAverage):
    def ma_in_point_p(self, prices) -> float:
        down = (len(prices)+1)/2
        sma_obj = SimpleMovingAverage(prices=self.prices, period=self.period)
        tma = sma_obj()/down
        return tma


class DoubleExponentialMovingAverage(MovingAverage):
    def ma_in_point_p(self, prices) -> float:
        ema_obj = ExponentialMovingAverage(prices=self.prices, period=self.period)
        ema = ema_obj()
        dema = ema.multiply(2) - ema.multiply(ema)
        return dema

