import usaddress
import pandas as pd
import pandas_usaddress

df = pd.read_csv('NBPDFebthruMay2019.csv')
df.replace('NEWBRUNSWICK', 'NEW BRUNSWICK')
df = df.replace(to_replace= r'\\', value= '', regex=True)
result = pandas_usaddress.tag(df, ['Incident Location'], granularity='high', standardize=False)
final = result[['Dispatch Number', 'Call Date', 'Call Type', 'AddressNumber', 'StreetName','StateName' ]]
final.to_csv('parsed_output3.csv')