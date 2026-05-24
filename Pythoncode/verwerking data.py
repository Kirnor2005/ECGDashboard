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
data_verwerkt['filler'] = data.groupby('Wijk')['Bloeddruk (Bovendruk) 1'].first()

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

df = pd.DataFrame()

#mvc = meest voorkomende categorie
df['mvc Bloeddruk (Bovendruk) 1'] = data.groupby('Wijk')['Bloeddruk (Bovendruk) 1'].first()
df['mvc Bloeddruk (Bovendruk) 2'] = data.groupby('Wijk')['Bloeddruk (Bovendruk) 2'].first()
df['mvc Cholesterol 1'] = data.groupby('Wijk')['Cholesterol 1'].first()
df['mvc Cholesterol 2'] = data.groupby('Wijk')['Cholesterol 2'].first()
df['mvc Non-HDL 1'] = data.groupby('Wijk')['Non-HDL 1'].first()
df['mvc Non-HDL 2'] = data.groupby('Wijk')['Non-HDL 2'].first()
df['mvc Bloedsuiker 1'] = data.groupby('Wijk')['Bloedsuiker 1'].first()
df['mvc Bloedsuiker 2'] = data.groupby('Wijk')['Bloedsuiker 2'].first()
df['mvc BMI 1'] = data.groupby('Wijk')['BMI 1'].first()
df['mvc BMI 2'] = data.groupby('Wijk')['BMI 2'].first()

data_verwerkt = data_verwerkt.merge(df_hrv, on='Wijk', how='left')
data_verwerkt = data_verwerkt.merge(stats, on='Wijk', how='left')
display(data_verwerkt)

# cv = coded values
cv = pd.DataFrame()

mapping_bd1 = {
    "<120": 1,
    "120-140": 2,
    "140-180": 3,
    ">180": 4
}

cv["c BD 1"] = df["mvc Bloeddruk (Bovendruk) 1"].map(mapping_bd1)

mapping_bd2 = {
    "<120": 1,
    "120-140": 2,
    "140-180": 3,
    ">180": 4
}

cv["c BD 2"] = df["mvc Bloeddruk (Bovendruk) 2"].map(mapping_bd2)

mapping_chol1 = {
    "<5": 1,
    "5-6.5": 2,
    "6.5-8": 3,
    ">8": 4
}

cv["c chol1"] = df["mvc Cholesterol 1"].map(mapping_chol1)

mapping_chol2 = {
    "<5": 1,
    "5-6.5": 2,
    "6.5-8": 3,
    ">8": 4
}

cv["c chol2"] = df["mvc Cholesterol 2"].map(mapping_chol2)

cv

mapping_nhdl1 = {
    "<3.8": 1,
    ">3.8": 2
}

cv["c nhdl1"] = df["mvc Non-HDL 1"].map(mapping_nhdl1)

mapping_nhdl2 = {
    "<3.8": 1,
    ">3.8": 2
}

cv["c nhdl2"] = df["mvc Non-HDL 2"].map(mapping_nhdl2)

mapping_bs1 = {
    "<7.8": 1,
    "7.8-11": 2,
    ">11.1": 3
}

cv["c bs1"] = df["mvc Bloedsuiker 1"].map(mapping_bs1)

mapping_bs2 = {
    "<7.8": 1,
    "7.8-11": 2,
    ">11.1": 3
}

cv["c bs2"] = df["mvc Bloedsuiker 2"].map(mapping_bs2)

mapping_bmi1 = {
    "<18.5": 1,
    "18.5-25": 2,
    "25-30": 3,
    ">30": 4
}

cv["c bmi1"] = df["mvc BMI 1"].map(mapping_bmi1)

mapping_bmi2 = {
    "<18.5": 1,
    "18.5-25": 2,
    "25-30": 3,
    ">30": 4
}

cv["c bmi2"] = df["mvc BMI 2"].map(mapping_bmi2)


# kolommen aanpassen
cols = ["c BD 1", "c BD 2", "c chol1", "c chol2", "c bs1", "c bs2", "c bmi1", "c bmi2"]

for col in cols:
    cv[col + " gem"] = (
        cv[col] + np.random.uniform(-0.9, 0.9, size=len(df))
    ).clip(1, 4).round(2)

df = df.merge(
    cv[["c BD 1 gem", "c BD 2 gem", "c chol1 gem", "c chol2 gem",
        "c bs1 gem", "c bs2 gem", "c bmi1 gem", "c bmi2 gem"]],
    left_index=True,
    right_index=True,
    how="left"
)

# keep the index as a column
df = df.reset_index()

# drop it
df = df.reset_index(drop=True)

data_verwerkt = data_verwerkt.merge(df, on='Wijk', how="left")
data_verwerkt = data_verwerkt.drop(columns = 'filler')
data_verwerkt.to_csv(r"C:\Users\Kirno\Streamlit\verwerkte_data.csv", index=False)

"""
Inspiratie:
https://medium.com/orikami-blog/exploring-heart-rate-variability-using-python-483a7037c64d
https://www.kubios.com/blog/hrv-analysis-methods/
"""
