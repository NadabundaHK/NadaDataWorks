# -*- coding: utf-8 -*-
"""CP 3.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1ROaG1VYpMUjxd89Y79lZTN8XZ3Y95dzp
"""

import pandas as pd
import numpy as np
import tensorflow as tf
import seaborn as sns

df = pd.read_csv('/content/Churn_Modelling.csv')
df.head()

df.info()

df['Geography'].unique()

visual = df.groupby(['Geography'])['Age'].agg(['mean', 'std']).reset_index().sort_values(by='mean', ascending=False)
ax = sns.barplot(x="Geography", y="mean", data=visual)

visual = df.groupby(['Geography'])['CreditScore'].agg(['mean', 'std']).reset_index().sort_values(by='mean', ascending=False)
ax = sns.barplot(x="Geography", y="mean", data=visual)

visual = df.groupby(['Geography'])['EstimatedSalary'].agg(['mean', 'std']).reset_index().sort_values(by='mean', ascending=False)
ax = sns.barplot(x="Geography", y="mean", data=visual)

ax = sns.countplot(x="Exited", hue="Gender", data=df)

df['Exited'].value_counts()

ax = sns.countplot(x="Exited", hue="IsActiveMember", data=df)

ax = sns.countplot(x="Exited", hue="Geography", data=df)

ax = sns.countplot(x="Exited", hue="HasCrCard", data=df)

ax = sns.countplot(x="Exited", hue="NumOfProducts", data=df)

g = sns.catplot(x="Exited", y="Balance", data=df)

g = sns.catplot(x="Exited", y="Age", data=df)

g = sns.catplot(x="Exited", y="CreditScore", data=df)

import matplotlib.pyplot as plt
# Select only numeric columns
numeric_df = df.select_dtypes(include=np.number)
# Calculate the correlation matrix
correlation_matrix = numeric_df.corr()
#Create the heatmap
plt.figure(figsize=(12, 10))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f")
plt.title('Correlation Matrix of Numeric Features')
plt.show()

g = sns.pairplot(df, hue="Exited")

"""Encoding"""

df

df_cp = df.drop(['RowNumber', 'CustomerId', 'Surname'], axis = 1)
df_cp

from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()
df_cp['Gender'] = le.fit_transform(df_cp['Gender'])

df_cp = pd.get_dummies(df_cp, drop_first=True)
df_cp.head()

X = df_cp.drop(columns=['Exited'])
y = df_cp['Exited']

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0)

from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)

X_train

"""Bangun Model ANN"""

ann = tf.keras.models.Sequential() #instansiasi objek ANN yang masih kosong

ann.add(tf.keras.layers.Dense(units=6, activation='relu'))

ann.add(tf.keras.layers.Dense(units=6, activation='relu'))

ann.add(tf.keras.layers.Dense(units=1, activation='sigmoid'))

ann.compile(optimizer = 'adam', loss = 'binary_crossentropy', metrics = ['accuracy'])

import keras
from datetime import datetime

#Define the Keras TensorBoard callback.
logdir="logs/fit/" + datetime.now().strftime("%Y%m%d-%H%M%S")
tensorboard_callback = keras.callbacks.TensorBoard(log_dir=logdir)

ann.fit(X_train, y_train, batch_size = 32, epochs = 100, callbacks=[tensorboard_callback])

y_pred = ann.predict(X_test)
y_pred

# Tentukan binary output berdasarkan threshold 0.5
y_pred_binary= (y_pred >= 0.5)

# Cetak hasil binary output
print("y_pred_binary:", y_pred_binary)

from sklearn.metrics import confusion_matrix, accuracy_score
# Hitung confusion matrix
cm = confusion_matrix(y_test, y_pred_binary)
print(cm)

# Hitung accuracy
accuracy_score(y_test, y_pred_binary)

!jupyter nbconvert --to html /content/CP_3.ipynb