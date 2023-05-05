import argparse
import json
import pandas as pd
import numpy as np
from urllib.parse import urlparse
import os
import time

parser = argparse.ArgumentParser()

parser.add_argument("json_file_path", help = "put the json file path which you want to convert to csv")


parser.add_argument("-u", action="store_true", dest="to_unix_timestamp", default=False, help="show time in unix format")


args = parser.parse_args()

if args.to_unix_timestamp:
    
    start = time.time()
    data=pd.read_json(args.json_file_path,lines=True)
    bitly_data=pd.DataFrame(columns=['web_browser', 'operating_sys', 'from_url', 'to_url', 'city', 'longitude', 'latitude', 'time_zone', 'time_in', 'time_out'])
    bitly_data['operating_sys']= data['a'].str.extract(r'\((\w+)').fillna('unidentified')
    bitly_data['web_browser']= data['a'].str.extract(r'(^[MO]\S*)').fillna('unidentified')
    bitly_data['from_url'] = data['r'].apply(lambda url: urlparse(url).netloc).replace('','direct')
    bitly_data['to_url'] = data['u'].apply(lambda url: urlparse(url).netloc)
    bitly_data['city']=data['cy'].fillna('unidentified')
    bitly_data['longitude']=data['ll'].str[0].fillna('unidentified')
    bitly_data['latitude']=data['ll'].str[1].fillna('unidentified')
    bitly_data['time_zone']=data['tz'].replace('','unidentified')
    bitly_data['time_in'] = data['t']
    bitly_data['time_out'] = data['hc']
    
    input_path = args.json_file_path
    output_path = os.path.join(os.path.dirname(f'{input_path}'),'bitly_data_unix.csv' )
    bitly_data.to_csv(output_path)
    
    count_of_rows=bitly_data.count()[0]
    end=time.time()
    time_diff=end-start
    
    print('Number of rows:', count_of_rows,'rows')
    print('File Path:',output_path)
    print('Execution time:', time_diff, 'seconds')
    
else:
    start = time.time()
    data=pd.read_json(args.json_file_path,lines=True)
    bitly_data=pd.DataFrame(columns=['web_browser', 'operating_sys', 'from_url', 'to_url', 'city', 'longitude', 'latitude', 'time_zone', 'time_in', 'time_out'])
    bitly_data['operating_sys']= data['a'].str.extract(r'\((\w+)').fillna('unidentified')
    bitly_data['web_browser']= data['a'].str.extract(r'(^[MO]\S*)').fillna('unidentified')
    bitly_data['from_url'] = data['r'].apply(lambda url: urlparse(url).netloc).replace('','direct')
    bitly_data['to_url'] = data['u'].apply(lambda url: urlparse(url).netloc)
    bitly_data['city']=data['cy'].fillna('unidentified')
    bitly_data['longitude']=data['ll'].str[0].fillna('unidentified')
    bitly_data['latitude']=data['ll'].str[1].fillna('unidentified')
    bitly_data['time_zone']=data['tz'].replace('','unidentified')
    bitly_data['time_in'] = pd.to_datetime(data['t'], unit='s',errors='coerce').fillna('unidentified')
    bitly_data['time_out'] = pd.to_datetime(data['hc'], unit='s',errors='coerce').fillna('unidentified')
    
    input_path = args.json_file_path
    output_path = os.path.join(os.path.dirname(f'{input_path}'),'bitly_data.csv' )
    bitly_data.to_csv(output_path)
    
    count_of_rows=bitly_data.count()[0]
    end=time.time()
    time_diff=end-start
    
    print('Number of rows:', count_of_rows,'rows')
    print('File Path:',output_path)
    print('Execution time:', time_diff, 'seconds')