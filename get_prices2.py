from pandas_datareader import data
import pandas as pd
import datetime
# import pandas_datareader 

sym = ['NOK', 'SESG SA', 'CNA.L', 'BT']
# Define which online source one should use
data_source = 'google'

#  Set start and end dates
start_date = '2006-01-01'
today = datetime.datetime.now() 
end_date = today.strftime("%Y-%m-%d")
# Pull the data
panel_data = data.DataReader(sym, data_source, start_date, end_date)
all_weekdays = pd.date_range(start=start_date, end=end_date, freq= 'B')

# Getting just the adjusted closing prices. This will return a Pandas DataFrame
# The index in this DataFrame is the major index of the panel_data.
close = panel_data.ix['Close']

# Getting just the weekdays 
all_weekdays = pd.date_range(start=start_date, end=end_date, freq='B')
# Reindex to weekdays
close = close.reindex(all_weekdays)
close.describe()

close.head(5)
close.tail(5)

