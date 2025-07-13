import pandas as pd
from scipy.stats import ttest_ind
import seaborn as sns
import matplotlib.pyplot as plt

# 1. Leer CSV
df = pd.read_csv('C:/EDA/matches.csv')
# Definir lista de columnas
cols = ['Date', 'Team', 'Opponent', 'Venue', 'Result', 'GF', 'GA', 'xG', 'xGA', 'Attendance', 'Referee', 'Formation', 'Round']

# Crear un nuevo DataFrame filtrado
df_sel = df[cols].copy()

# Separar xG por local y visitante
home_xg = df_sel[df_sel['Venue']=='Home']['xG']
away_xg = df_sel[df_sel['Venue']=='Away']['xG']

# Calcular medias
mean_home = home_xg.mean()
mean_away = away_xg.mean()
print(f"xG medio en casa:  {mean_home:.2f}")
print(f"xG medio fuera:  {mean_away:.2f}")

#Test de diferencia (t-test) Si p-value < 0.05 entonnces la diferencia en xG entre casa y fuera es significativa.
stat, pval = ttest_ind(home_xg, away_xg, equal_var=False)
print(f"t-stat: {stat:.2f}, p-value: {pval:.4f}")

# Media por Venue
xg_means = df.groupby('Venue')['xG'].mean().reset_index()

#Visualización de la brecha de xG
plt.figure(figsize=(6,4))
sns.barplot(x='Venue', y='xG', data=xg_means, palette=['skyblue','salmon'])
plt.title('xG medio: Casa vs Fuera')
plt.ylabel('xG medio')
plt.xlabel('')
plt.tight_layout()
plt.show()

#Distribución de xG
plt.figure(figsize=(8,5))
sns.kdeplot(home_xg, label='Casa', shade=True)
sns.kdeplot(away_xg, label='Fuera', shade=True)
plt.title('Distribución de xG por localía')
plt.xlabel('xG')
plt.legend()
plt.tight_layout()
plt.show()
