import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns

# Leer CSV
df = pd.read_csv('C:/EDA/matches.csv')

# Definir lista de columnas
cols = ['Date', 'Team', 'Opponent', 'Venue', 'Result', 'GF', 'GA', 'xG', 'xGA', 'Attendance', 'Referee', 'Formation', 'Round']

# Crear un nuevo DataFrame filtrado
df_sel = df[cols].copy()

# Filtrar solo partidos en casa
df_home = df_sel[df_sel['Venue'] == 'Home'].copy()

# Crear indicador de victoria local
df_home['home_win'] = np.where(df_home['Result'] == 'W', 1, 0)

#Calculamos la correlación de Pearson entre asistencia y probabilidad de ganar
corr = df_home['Attendance'].corr(df_home['home_win'])
print(f"Correlación Attendance vs. home_win: {corr:.2f}")

# Generar bins y calcular tasa de victorias
df_home['att_quantile'] = pd.qcut(df_home['Attendance'], 5)
win_rate_by_bin = (
    df_home.groupby('att_quantile')['home_win']
           .mean()
           .mul(100)
           .reset_index(name='win_pct')
)

print(win_rate_by_bin)

# Scatter + curva logística
plt.figure(figsize=(8, 5))
sns.regplot(x='Attendance',
            y='home_win',
            data=df_home,
            logistic=True,
            ci=None,
            scatter_kws={'s':20, 'alpha':0.3})
plt.title('Probabilidad de victoria local vs Asistencia')
plt.xlabel('Asistencia')
plt.ylabel('Probabilidad de victoria local')
plt.ylim(-0.05,1.05)
plt.tight_layout()
plt.show()