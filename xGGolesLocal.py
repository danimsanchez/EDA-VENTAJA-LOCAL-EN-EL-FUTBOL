import pandas as pd
from scipy.stats import ttest_ind
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Leer CSV
df = pd.read_csv('C:/EDA/matches.csv')
# Definir lista de columnas
cols = ['Date', 'Team', 'Opponent', 'Venue', 'Result', 'GF', 'GA', 'xG', 'xGA', 'Attendance', 'Referee', 'Formation', 'Round']

# Crear un nuevo DataFrame filtrado
df_sel = df[cols].copy()

# Evitar divisiones por cero
df_conv = df_sel[df_sel['xG'] > 0].copy()

# Tasa de conversión: goles marcados / xG
df_conv['conv_rate'] = df_conv['GF'] / df_conv['xG']

# Subconjuntos casa y fuera
home_conv = df_conv[df_conv['Venue']=='Home']['conv_rate']
away_conv = df_conv[df_conv['Venue']=='Away']['conv_rate']

# Media de conversión
mean_home_conv = home_conv.mean()
mean_away_conv = away_conv.mean()

print(f"Tasa media de conversión en casa: {mean_home_conv:.2f}")
print(f"Tasa media de conversión fuera:    {mean_away_conv:.2f}")

#Test de diferencia de medias, Un p-value < 0.05 indicaría que la diferencia en la tasa de conversión es significativa.
stat, pval = ttest_ind(home_conv, away_conv, equal_var=False)
print(f"t-stat: {stat:.2f}, p-value: {pval:.4f}")

# Preparar DataFrame de medias
conv_means = df_conv.groupby('Venue')['conv_rate'].mean().reset_index()

plt.figure(figsize=(6,4))
sns.barplot(x='Venue', y='conv_rate', data=conv_means, palette=['skyblue','salmon'])
plt.title('Tasa media de conversión xG→G: Casa vs Fuera')
plt.ylabel('Goles marcados / xG')
plt.xlabel('')
plt.tight_layout()
plt.show()

# Distribución de la tasa de conversión
plt.figure(figsize=(8,5))
sns.kdeplot(home_conv, label='Casa', shade=True)
sns.kdeplot(away_conv, label='Fuera', shade=True)
plt.title('Distribución de la tasa de conversión por localía')
plt.xlabel('Conv_rate')
plt.legend()
plt.tight_layout()
plt.show()