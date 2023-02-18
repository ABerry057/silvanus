import pandas as pd
from pathlib import Path

csv_rel_paths = Path('./data/raw_data').glob('*.csv')
desired_cols = [
    'Spill Number', 'Date Spill Reported', 'Spill Name', 
    'County', 'City/Town', 'Address'
]

csv_contents = []
for p in csv_rel_paths:
    data = pd.read_csv(
        filepath_or_buffer='./' + str(p), 
        usecols=desired_cols,
        parse_dates=['Date Spill Reported']
    )
    csv_contents.append(data)

data_set = pd.concat(csv_contents)
# transform some string cols to title case
cols_to_normalize = ['Spill Name', 'City/Town', 'Address']
data_set[cols_to_normalize] = data_set[cols_to_normalize].apply(lambda x: x.str.title())
data_set.columns = [c.replace(' ', '_').lower() for c in data_set.columns]

data_set.to_parquet('./data/spill_data.parquet')