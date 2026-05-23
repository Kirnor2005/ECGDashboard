"""
In dit script word er een nieuw csv bestand gemaakt met een paar nieuwe variabelen die goed zijn voor analyses 
zoals: HRV (sdnn, rmssd en pnn50), Gem Hartslag, Minimale Hartslag, Maximale Hartslag, STD 
en nog een paar oude waarden zoals cholesterol en bloedsuiker
"""

import numpy as np
import pandas as pd

data = pd.read_csv(r"C:\Users\Kirno\Streamlit\Data metingen Amsterdam.csv", sep=';', decimal=',', engine='python', on_bad_lines='skip')
data['Wijk'] = data['Wijk'].ffill()

data_verwerkt = pd.DataFrame()

#ik had problemen met excel waardoor ik alles 3x na ben gelopen en voor de zekerheid overal dropna() heb toegevoegd.

df_hrv = data.groupby('Wijk', as_index=False).agg(
    sdnn_1=('rrData 1', lambda x: x.dropna().std(ddof=1)),
    rmssd_1=('rrData 1', lambda x: np.sqrt(np.mean(np.diff(x.dropna())**2)) if len(x.dropna()) > 1 else np.nan),
    nn50_1=('rrData 1', lambda x: np.sum(np.abs(np.diff(x.dropna())) > 50)),
    pnn50_1=('rrData 1', lambda x: np.sum(np.abs(np.diff(x.dropna())) > 50) / (len(x.dropna()) - 1) * 100 if len(x.dropna()) > 1 else np.nan),
    sdnn_2=('rrData 2', lambda x: x.dropna().std(ddof=1)),
    rmssd_2=('rrData 2', lambda x: np.sqrt(np.mean(np.diff(x.dropna())**2)) if len(x.dropna()) > 1 else np.nan),
    nn50_2=('rrData 2', lambda x: np.sum(np.abs(np.diff(x.dropna())) > 50)),
    pnn50_2=('rrData 2', lambda x: np.sum(np.abs(np.diff(x.dropna())) > 50) / (len(x.dropna()) - 1) * 100 if len(x.dropna()) > 1 else np.nan)
)

stats = data.groupby('Wijk').agg(
    HR1=('Gem HR 1', lambda x: x.dropna().mean()),
    HR2=('Gem HR 2', lambda x: x.dropna().mean()),
    MinHR1=('Gem HR 1', lambda x: x.dropna().min()),
    MinHR2=('Gem HR 2', lambda x: x.dropna().min()),
    MaxHR1=('Gem HR 1', lambda x: x.dropna().max()),
    MaxHR2=('Gem HR 2', lambda x: x.dropna().max()),
    STDHR1=('Gem HR 1', lambda x: x.dropna().std()),
    STDHR2=('Gem HR 2', lambda x: x.dropna().std())
)

stats['HR Diff'] = stats['HR2'] - stats['HR1']

data_verwerkt['Bloeddruk (Bovendruk) 1'] = data.groupby('Wijk')['Bloeddruk (Bovendruk) 1'].first()
data_verwerkt['Bloeddruk (Bovendruk) 2'] = data.groupby('Wijk')['Bloeddruk (Bovendruk) 2'].first()
data_verwerkt['Cholesterol 1'] = data.groupby('Wijk')['Cholesterol 1'].first()
data_verwerkt['Cholesterol 2'] = data.groupby('Wijk')['Cholesterol 2'].first()
data_verwerkt['Non-HDL 1'] = data.groupby('Wijk')['Non-HDL 1'].first()
data_verwerkt['Non-HDL 2'] = data.groupby('Wijk')['Non-HDL 2'].first()
data_verwerkt['Bloedsuiker 1'] = data.groupby('Wijk')['Bloedsuiker 1'].first()
data_verwerkt['Bloedsuiker 2'] = data.groupby('Wijk')['Bloedsuiker 2'].first()
data_verwerkt['BMI 1'] = data.groupby('Wijk')['BMI 1'].first()
data_verwerkt['BMI 2'] = data.groupby('Wijk')['BMI 2'].first()


data_verwerkt = data_verwerkt.merge(df_hrv, on='Wijk', how='left')
data_verwerkt = data_verwerkt.merge(stats, on='Wijk', how='left')
display(data_verwerkt)


data_verwerkt.to_csv(r"C:\Users\Kirno\Streamlit\data_verwerkt_goedeversie.csv", index=False)

"""
Inspiratie:
https://medium.com/orikami-blog/exploring-heart-rate-variability-using-python-483a7037c64d
https://www.kubios.com/blog/hrv-analysis-methods/
"""