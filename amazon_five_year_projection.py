import numpy as np
from pandas_datareader.data import DataReader
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
# date formatting : http://matplotlib.org/examples/api/date_demo.html

years = mdates.YearLocator()   # every year
months = mdates.MonthLocator()  # every month
yearsFmt = mdates.DateFormatter('%Y')

symbol = 'AMZN'
amzn = DataReader(symbol,  'yahoo', datetime(2012, 11, 18), datetime(2017, 11, 18))

dates = amzn['Adj Close'].keys().date
closing_prices = amzn['Adj Close'].values

fig, ax = plt.subplots()

# format ticks
ax.xaxis.set_major_locator(years)
ax.xaxis.set_major_formatter(yearsFmt)
ax.xaxis.set_minor_locator(months)

datemin = datetime(dates.min().year, 1, 1)
datemax = datetime(dates.max().year, 1, 1)
datemax = datetime(datemax.year + (datemax.year - datemin.year) + 1, 1, 1)
ax.set_xlim(datemin, datemax)

# rotates and right aligns the x labels, and moves the bottom of the
# axes up to make room for them
fig.autofmt_xdate()

# format the data labels
def price(x):
    return '$%1.2f' % x
ax.format_xdata = mdates.DateFormatter('%Y-%m-%d')
ax.format_ydata = price
ax.grid(True)

# Add labels
ax.set_title('Amazon Stock Price: 5-Year Trends')
ax.set_xlabel('Date')
ax.set_ylabel('Closing Price')

#Plot the data
ax.plot(dates, closing_prices, label='Historical Stock Data')

# Create polynomial fit
x = mdates.date2num(dates)
y = closing_prices
z2 = np.polyfit(x, y, 2) # Quadratic regression
p2 = np.poly1d(z2)

five_year_date_num = mdates.date2num(datetime(2022, 11, 18))

xx = np.linspace(x.min(), five_year_date_num, 100)
dd = mdates.num2date(xx)
ax.plot(dd, p2(xx), '-g', label='Quadratic Fit')

ax.annotate("Projected Stock Price\n{0:%b %d, %Y}\n${1:1.2f}/share".format(datetime(2022, 11, 18), p2(five_year_date_num)),
            xy=(five_year_date_num, p2(five_year_date_num)), xycoords='data',
            xytext=(-110, -170), textcoords='offset points',
            bbox=dict(boxstyle='round,pad=0.5', fc='white', alpha=0.5),
            arrowprops=dict(arrowstyle = '->', connectionstyle='arc3,rad=0')
            )

#add legend
ax.legend(loc='upper left')

# Display the plot
plt.show()