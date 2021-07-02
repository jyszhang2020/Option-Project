# Option-Project

### Tiger Brokers
`cd Option`
Option dirtory will run the result that close to the Tiger.

#### How to Run
`python3 main.py`
main.py will give all the greeks, volatility, and option price. After changing stock symbol, evaluation date, expiration date, strike price, and option type new result will be returned.

#### Code Description
historical_volatility.py calculates the historical volatility of the stock and the close price of the stock.

data_types.py contains all the calcuation for greeks and volatility.

#

### Black Scholes Model

The Black-Scholes formula, for call:

![img](https://latex.codecogs.com/gif.latex?C%3DN%28d_1%29S_t-N%28d_2%29Ke%5E%7B-rt%7D)

and for put:

![img](https://latex.codecogs.com/gif.latex?P%3DKe%5E%7B-rt%7DN%28-d_2%29-S_tN%28-d_1%29)

where ![img](https://latex.codecogs.com/gif.latex?d_1%3D%5Cfrac%7B%5Cln%7B%5Cfrac%7BS_t%7D%7BK%7D%7D&plus;%28r&plus;%5Cfrac%7B%5Csigma%5E2%7D%7B2%7D%29t%7D%7B%5Csigma%5Csqrt%7Bt%7D%7D) and ![img](https://latex.codecogs.com/gif.latex?d_2%3Dd_1-%5Csigma%5Csqrt%7Bt%7D)

- C = call option price
- N = CDF of the normal distribution
- St= spot price of an asset
- K = strike price
- r = risk-free interest rate
- t = time to maturity
- σ = volatility of the asset

### Greek Letters

Option Greeks measure the exposure of option price or option delta to movement of different factors such as the underlying price, time and volatility.

**First Order Greeks:** Delta, Vega, Theta, Rho

**Second Order Greeks:** Gamma

###### Delta

Delta is the rate of change of the option price with respect to the **price of the underlying asset**. It measures the **first-order** sensitivity of the price to a movement in stock price S.

![img](https://latex.codecogs.com/gif.latex?%5CDelta%3D%5Cfrac%7B%5Cpartial%20C%7D%7B%5Cpartial%20S%7D)

For call:

![img](https://latex.codecogs.com/gif.latex?%5CDelta%3DN%28d_1%29)

for put:

![img](https://latex.codecogs.com/gif.latex?%5CDelta%3D-N%28-d_1%29)

###### Gamma

Gamma is the rate of change of the portfolio's delta with respect to the **underlying asset's price**. It represents the **second-order** sensitivity of the option to a movement in the underlying asset’s price.

![img](https://latex.codecogs.com/gif.latex?%5CGamma%3D%5Cfrac%7B%5Cpartial%5E2%7BC%7D%20%7D%7B%5Cpartial%20S%5E2%7D)

For call and put:

![img](https://latex.codecogs.com/gif.latex?%5CGamma%3D%5Cfrac%7B%7BN%7D%27%28d_1%29%7D%7BS%5Csigma%5Csqrt%7Bt%7D%7D)

###### Vega

The Vega is the rate of change in the value of the option with respect to the **volatility** of the underlying asset.

![img](https://latex.codecogs.com/gif.latex?V%3D%5Cfrac%7B%5Cpartial%20C%7D%7B%5Cpartial%20%5Csigma%7D)

For call and put:

![img](https://latex.codecogs.com/gif.latex?V%3DS%7BN%7D%27%28d_1%29%5Csqrt%7Bt%7D)

###### Theta

Theta is the rate of change of the value of the option with respect to the passage of time. It is also referred to as the **time** decay of the portfolio.

![img](https://latex.codecogs.com/gif.latex?%5CTheta%3D%5Cfrac%7B%5Cpartial%20C%7D%7B%5Cpartial%20t%7D)

For call:

![img](https://latex.codecogs.com/gif.latex?%5CTheta%3D-%5Cfrac%7BS%5Csigma%7BN%7D%27%28d_1%29%7D%7B2%5Csqrt%7Bt%7D%7D-rKe%5E%7B-rt%7DN%28d_2%29)

for put:

![img](https://latex.codecogs.com/gif.latex?%5CTheta%3D-%5Cfrac%7BS%5Csigma%7BN%7D%27%28d_1%29%7D%7B2%5Csqrt%7Bt%7D%7D&plus;rKe%5E%7B-rt%7DN%28d_2%29)

###### Rho

Rho is the rate of change of the value of a derivative with respect to the **interest rate**.

![img](https://latex.codecogs.com/gif.latex?%5Crho%3D%5Cfrac%7B%5Cpartial%20C%7D%7B%5Cpartial%20r%7D)

For call:

![img](https://latex.codecogs.com/gif.latex?%5Crho%3DKte%5E%7B-rt%7DN%28d_2%29)

for put:

![img](https://latex.codecogs.com/gif.latex?%5Crho%3D-Kte%5E%7B-rt%7DN%28-d_2%29)

###### Implied Volatility

It is defined as the expected future volatility of the stock over the life of the option. It is directly influenced by the supply and demand of the underlying option and the market’s expectation of the stock price’s direction.



### Option Data

```python
# Stock
stock = 'IBM'
# Expriation date
expiry = '11-28-2021'
# Strike price
K = 150
# time to maturity
t = (datetime.strptime(expiry, "%m-%d-%Y") - datetime.utcnow()).days / 365

today = datetime.now()
one_month_ago = today.replace(month=today.month-1)

df = web.DataReader(stock, 'yahoo', one_month_ago, today)
```

This could give us one month IBM stock data from yahoo finance.

![image-20210526010252382](/Users/joycefeifei/Library/Application Support/typora-user-images/image-20210526010252382.png)

###### Underlying price

Today's stock close price price

```python
S = df['Close'].iloc[-1]
```

###### Sigma

We are able to calculate the **sigma** value by multiplying the standard deviation of the stock returns over the past year by the square root of 252 (number of days the market is open over a year).

```python
# Previous day's price
df = df.assign(close_day_before=df.Close.shift(1))
# Stock Return
df['returns'] = ((df.Close - df.close_day_before)/df.close_day_before)

sigma = np.sqrt(252) * df['returns'].std()
```

###### Risk free rate

The 10-year U.S. treasury yield which you could get from ^TNX.

```python
r = web.DataReader("^TNX", 'yahoo', one_day_ago, today)['Close'].iloc[-1]
```



All in all, we could get the option price, implied volatility and greeks for this specific example.

```python
print('The Option Price for ' + stock + 'on ' + expiry + ' is: ', bs_call(S, K, t, r, sigma))
print("Implied Volatility: " + str(100 * call_implied_volatility(bs_call(S, K, t, r, sigma), S, K, t, r)) + " %")
print("Delta: " + str(delta('c', S, K, t, r, sigma)))
print("Gamma: " + str(gamma('c', S, K, t, r, sigma)))
```

![image-20210526011306265](/Users/joycefeifei/Library/Application Support/typora-user-images/image-20210526011306265.png)



### Resource

- https://financetrainingcourse.com/education/2012/09/option-greeks-delta-gamma-vega-theta-rho-a-quick-reference-guide/
- https://medium.com/swlh/calculating-option-premiums-using-the-black-scholes-model-in-python-e9ed227afbee
- https://quantchronicles.blogspot.com/2018/11/black-scholes-formula-and-greeks-full.html



