from scipy.stats import ttest_ind
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# 1. Leer CSV
df = pd.read_csv('C:/EDA/matches.csv')
# Definir lista de columnas
cols = ['Date', 'Team', 'Opponent', 'Venue', 'Result', 'GF', 'GA', 'xG', 'xGA', 'Attendance', 'Referee', 'Formation', 'Round']

# Crear un nuevo DataFrame filtrado
df_sel = df[cols].copy()

# Extraer xGA por localía
home_xga = df_sel[df_sel['Venue']=='Home']['xGA']
away_xga = df_sel[df_sel['Venue']=='Away']['xGA']

# Calcular medias
mean_home_xga = home_xga.mean()
mean_away_xga = away_xga.mean()
print(f"xGA medio en casa:  {mean_home_xga:.2f}")
print(f"xGA medio fuera:    {mean_away_xga:.2f}")

#Test de diferencia (t-test) Si p-value < 0.05 entonnces la diferencia en xGA entre casa y fuera es significativa.
stat, pval = ttest_ind(home_xga, away_xga, equal_var=False)
print(f"t-stat: {stat:.2f}, p-value: {pval:.4f}")

# Bar plot de medias
xga_means = df.groupby('Venue')['xGA'].mean().reset_index()
plt.figure(figsize=(6,4))
sns.barplot(x='Venue', y='xGA', data=xga_means, palette=['skyblue','salmon'])
plt.title('xGA medio: Casa vs Fuera')
plt.ylabel('xGA medio')
plt.xlabel('')
plt.tight_layout()
plt.show()

# Distribución de xGA
plt.figure(figsize=(8,5))
sns.kdeplot(home_xga, label='Casa', shade=True)
sns.kdeplot(away_xga, label='Fuera', shade=True)
plt.title('Distribución de xGA por localía')
plt.xlabel('xGA')
plt.legend()
plt.tight_layout()
plt.show()