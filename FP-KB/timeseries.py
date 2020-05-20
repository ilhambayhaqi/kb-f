import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler

from tensorflow import keras
from tensorflow.keras.preprocessing.sequence import TimeseriesGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, Dropout, Activation
from tensorflow.keras.callbacks import EarlyStopping
from datetime import datetime

#%matplotlib inline

url_confirmed = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"
url_dead = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv"
url_recovered = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv"

country = "Indonesia"

df_confirmed = pd.read_csv(url_confirmed)
df_dead = pd.read_csv(url_dead)
df_recovered = pd.read_csv(url_recovered)

#print(df_confirmed)
#print(df_dead)
#print(df_recovered)

df_confirmed1 = df_confirmed[df_confirmed["Country/Region"] == country]

## Timeseries Entry
df_confirmed2 = pd.DataFrame(df_confirmed1[df_confirmed1.columns[4:]].sum(), columns=["confirmed"])
df_confirmed2.index = pd.to_datetime(df_confirmed2.index,format='%m/%d/%y')

df_dead1 = df_dead[df_dead["Country/Region"] == country]
df_dead2 = pd.DataFrame(df_dead1[df_dead1.columns[4:]].sum(), columns=["dead"])
df_dead2.index = pd.to_datetime(df_dead2.index, format='%m/%d/%y')


df_recovered1 = df_recovered[df_recovered["Country/Region"] == country]
df_recovered2 = pd.DataFrame(df_recovered1[df_recovered1.columns[4:]].sum(), columns=["recovered"])
df_recovered2.index = pd.to_datetime(df_recovered2.index, format='%m/%d/%y')

# Join Table
df_conf_dead = df_confirmed2.join(df_dead2, how = "inner")
df_all = df_conf_dead.join(df_recovered2, how = "inner")

#print(df_conf_dead)
#print(df_all)

# Plottiong Table
#plt.figure(figsize=(5,5))
#df_all.plot(figsize=(10,5), title=country)
#plt.show()

df_new = df_confirmed2[["confirmed"]]

test_num = 10;
x = len(df_new) - test_num;
train = df_new.iloc[:x]
test = df_new.iloc[x:]

# Normalisasi data
scaler = MinMaxScaler()
scaler.fit(train)

scaled_train = scaler.transform(train)
scaled_test = scaler.transform(test)
#print(scaled_test)


# Preparation for Model
n_input = 5
n_features = 1
far_predict = 7;

generator = TimeseriesGenerator(scaled_train, scaled_train, length = n_input, batch_size = 1)
#x, y = generator[50]
#print(x,y)

model = Sequential()
model.add(LSTM(150, activation="relu", input_shape=(n_input, n_features)))
#model.add(Dropout(0.2))
model.add(Dense(75, activation='relu'))
model.add(Dense(units=1))
#model.add(Activation('softmax'))
#model.add(Dense(1))
model.compile(optimizer="adam",loss="mse")
#print(model.summary())

validation_set = np.append(scaled_train[55],scaled_test)
validation_set=validation_set.reshape(11,1)
validation_gen = TimeseriesGenerator(validation_set,validation_set,length= n_input, batch_size=1)
#print(validation_set)

#Early Stopping
patience_value = 50
early_stop = EarlyStopping(monitor='val_loss',patience= patience_value, restore_best_weights=True)

model.fit_generator(generator,validation_data=validation_gen,epochs=200,callbacks=[early_stop],steps_per_epoch=10)
'''
pd.DataFrame(model.history.history).plot(title="loss vs epochs curve")
myloss = model.history.history["val_loss"]
plt.title("validation loss vs epochs")
plt.plot(range(len(myloss)),myloss)
plt.show()
'''
# Forcasting
test_prediction = []
first_eval_batch = scaled_train[-n_input:]
current_batch = first_eval_batch.reshape(1, n_input, n_features)
#current_batch.shape

for i in range(len(test) + far_predict):
	current_pred = model.predict(current_batch)[0]
	test_prediction.append(current_pred)
	current_batch = np.append(current_batch[:,1:,:], [[current_pred]], axis = 1)
#print(test_prediction)

true_prediction = scaler.inverse_transform(test_prediction)
#print(true_prediction[:,0])

time_series_array = test.index
for k in range(0, far_predict):
	time_series_array = time_series_array.append(time_series_array[-1:] + pd.DateOffset(1))

# Serving prediction
df_forecast = pd.DataFrame(columns=["confirmed","confirmed_predicted"],index=time_series_array)
df_forecast.loc[:,"confirmed_predicted"] = true_prediction[:,0]
df_forecast.loc[:,"confirmed"] = test["confirmed"]

print(df_forecast)
#df_forecast.plot(title=country + " Predictions for next " + str(far_predict) + " days")

MAPE = np.mean(np.abs(np.array(df_forecast["confirmed"][:5]) - np.array(df_forecast["confirmed_predicted"][:5]))/np.array(df_forecast["confirmed"][:5]))
sum_errs = np.sum((np.array(df_forecast["confirmed"][:5]) - np.array(df_forecast["confirmed_predicted"][:5]))**2)
stdev = np.sqrt(1/(5-2) * sum_errs)
interval = 1.96 * stdev

print("\nConfidence Level : " + str(1-MAPE) + "%")

df_forecast["confirm_min"] = df_forecast["confirmed_predicted"] - interval
df_forecast["confirm_max"] = df_forecast["confirmed_predicted"] + interval
df_forecast["Model Accuracy"] = round((1-MAPE),2)

df_forecast["Country"] = country
df_forecast["Execution date"] = str(datetime.now()).split()[0]
#df_forecast.to_excel("Indonesia_confirmed.xlsx")

#df_forecast.iloc[:,:4].plot()

df_train = df_confirmed2[:-5]

## Plot 1 Summary Full
fig= plt.figure(figsize=(10,5))
plt.title("{} - Results".format(country))
plt.xticks(rotation=20, horizontalalignment='right')

plt.axvline(x = df_train.index[-5], color='black', linestyle='--', alpha=.3)
#plt.plot(df_forecast.index,df_forecast["confirmed"],label="confirmed")
plt.plot(df_train.index,df_train["confirmed"], label="Train Confirmed", color='orange')
plt.plot(df_forecast.index,df_forecast["confirmed"],label="Validation Confirmed", color='g')
plt.plot(df_forecast.index,df_forecast["confirmed_predicted"],label="Prediction Confirmed", color='r')
#ax.fill_between(x, (y-ci), (y+ci), color='b', alpha=.1)
plt.fill_between(df_forecast.index,df_forecast["confirm_min"],df_forecast["confirm_max"],color="indigo",alpha=0.09,label="Confidence Interval")
plt.legend()

plt.savefig('img/summaryFull.png', dpi=300, bbox_inches='tight')
#plt.show()
plt.close()

## Plot 2 Summary Confirmed
fig= plt.figure(figsize=(10,5))
plt.title("{} - Results".format(country))
plt.xticks(rotation=20, horizontalalignment='right')


plt.axvline(x = df_train.index[-5], color='black', linestyle='--', alpha=.3)
plt.plot(df_train.index,df_train["confirmed"], label="Train Confirmed", color='orange')
plt.plot(df_forecast.index,df_forecast["confirmed"],label="Validation Confirmed", color = 'g')
#plt.plot(df_forecast.index,df_forecast["confirmed"],label="Validation Confirmed")
#ax.fill_between(x, (y-ci), (y+ci), color='b', alpha=.1)
plt.fill_between(df_forecast.index,df_forecast["confirm_min"],df_forecast["confirm_max"],color="indigo",alpha=0.09,label="Confidence Interval")
plt.legend()

plt.savefig('img/summaryConfirmed.png', dpi=300, bbox_inches='tight')
#plt.show()
plt.close()


## Plot 3 Summary Prediction

fig= plt.figure(figsize=(10,5))
plt.title("{} - Results".format(country))

#plt.axvline(x = df_train.index[-5], color='b', linestyle='--')
#plt.plot(df_train.index,df_train["confirmed"], label="Train Confirmed")
plt.plot(df_forecast.index,df_forecast["confirmed"],label="Validation Confirmed")
plt.plot(df_forecast.index,df_forecast["confirmed_predicted"],label="confirmed_predicted")
#ax.fill_between(x, (y-ci), (y+ci), color='b', alpha=.1)
plt.fill_between(df_forecast.index,df_forecast["confirm_min"],df_forecast["confirm_max"],color="indigo",alpha=0.09,label="Confidence Interval")
plt.legend()
plt.savefig('img/summaryPrediction.png', dpi=300, bbox_inches='tight')