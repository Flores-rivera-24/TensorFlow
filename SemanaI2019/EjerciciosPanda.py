import streamlit as st
import pandas as pd
import numpy as np
import time
import uber_display

"- **assign name**"

ser = pd.Series(list('abcedfghijklmnopqrstuvwxyz'))
ser

# answer
ser.name = 'alphabets'
ser.head()



"- **Find the numbers that are not common on the series**"
#problem 2
ser1 = pd.Series([1, 2, 3, 4, 5])
ser2 = pd.Series([4, 5, 6, 7, 8])

# answer
ser1[~ser1.isin(ser2)]

"- **change to uppercase a dataframe of strings**"


#problem 3
ser = pd.Series(['how', 'to', 'kick', 'ass?'])
ser

# answer
ans = ser.map(lambda i: i.title())
ans

"- **Turn numpy array to a specific dataframe**"

ser = np.random.randint(1,10,35)
ser

result = pd.DataFrame(ser.reshape(7,-1))
result

"- **Compute euclidian distance between A and B **"
"A"
a = pd.Series([1,2,3,4,5,6,7,8,9,10])
a

"B"
b = pd.Series([10,9,8,7,6,5,4,3,2,1])
b

# Answers

result = pd.Series(np.linalg.norm(a-b))
result
