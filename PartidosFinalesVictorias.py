import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from statsmodels.stats.proportion import proportions_ztest
import seaborn as sns

# Leer CSV
df = pd.read_csv('C:/EDA/matches.csv')
# Definir lista de columnas
cols = ['Date', 'Team', 'Opponent', 'Venue', 'Result', 'GF', 'GA', 'xG', 'xGA', 'Attendance', 'Referee', 'Formation', 'Round']

# Crear un nuevo DataFrame filtrado
df_sel = df[cols].copy()

# Copiar DataFrame
df2 = df_sel.copy()

# Extraer número de jornada (Round = 'Matchweek X')
df2['Matchweek'] = df2['Round'].str.extract('(\d+)').astype(int)

# Número máximo de jornada
max_md = df2['Matchweek'].max()

# Definir últimas 6 jornadas
df2['LateSeason'] = np.where(df2['Matchweek'] > max_md - 6, 1, 0)

# Filtrar solo partidos en casa
df_home2 = df2[df2['Venue']=='Home'].copy()
df_home2['home_win'] = (df_home2['Result']=='W').astype(int)

# Tasa de victorias en casa por fase
win_rates = (
    df_home2
      .groupby('LateSeason')['home_win']
      .mean()
      .mul(100)
      .reset_index()
      .replace({0:'Early', 1:'Late'})
      .rename(columns={'LateSeason':'Phase','home_win':'WinPct'})
)

print(win_rates)

# Conteos y totales
counts = df_home2.groupby('LateSeason')['home_win'].sum().values
nobs   = df_home2.groupby('LateSeason')['home_win'].count().values

#Test de proporciones, Un p-value < 0.05 confirmaría que la diferencia Early vs. Late es significativa.
stat, pval = proportions_ztest(counts, nobs)
print(f"z-stat: {stat:.2f}, p-value: {pval:.4f}")


# resultados
plt.figure(figsize=(6,4))
sns.barplot(x='Phase', y='WinPct', data=win_rates, palette=['skyblue','salmon'])
plt.title('Victorias en Casa: Early vs Late Season')
plt.ylabel('% victorias locales')
plt.xlabel('')
plt.tight_layout()
plt.show()