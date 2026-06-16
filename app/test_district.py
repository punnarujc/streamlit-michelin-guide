import os
import sys

# Add project root to sys.path to allow importing from the 'app' package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.data import load_data, get_restaurants, get_unique_awards

load_data()
df = get_restaurants(awards=get_unique_awards())
location_split = df['Location'].str.split(', ', n=1, expand=True)
df['City'] = location_split[0]

def get_district(row):
    parts = [p.strip() for p in str(row['Address']).split(',')]
    try:
        idx = parts.index(row['City'])
        return parts[idx-1] if idx > 0 else 'Unknown'
    except ValueError:
        return 'Unknown'

df['District'] = df.apply(get_district, axis=1)
print(df[df['City'] == 'Bangkok']['District'].value_counts().head(20))
