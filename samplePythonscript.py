import json
import pandas as pd
import sys
my_input_param = sys.argv[1]
df = pd.read_csv("data/train.csv",encoding='ISO-8859-1',usecols = ['product_uid','product_title'])
df = df[1:5]
r = df.to_json(orient = "records") 
print(r)
# for entry in r:
# 	print(entry)