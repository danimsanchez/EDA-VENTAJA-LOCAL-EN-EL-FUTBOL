import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Leer CSV
df = pd.read_csv('C:/EDA/matches.csv')
# Definir lista de columnas
cols = ['Date', 'Team', 'Opponent', 'Venue', 'Result', 'GF', 'GA', 'xG', 'xGA', 'Attendance', 'Referee', 'Formation', 'Round']

# Crear un nuevo DataFrame filtrado
df_sel = df[cols].copy()

# Filtrar solo partidos en casa
df_home = df_sel[df_sel['Venue']=='Home'].copy()

# Crear indicador de victoria local
df_home['home_win'] = np.where(df_home['Result']=='W', 1, 0)

# Correlación entre Attendance y home_win por equipo
corr_by_team = (
    df_home
      .groupby('Team')
      .apply(lambda g: g['Attendance'].corr(g['home_win']))
      .sort_values(ascending=False)
)

# Mostrar en consola
pd.set_option('display.float_format', '{:.3f}'.format)
print("\nCorrelación Asistencia vs. Victoria Local por Equipo:\n")
print(corr_by_team)

# Gráfico de barras horizontal
plt.figure(figsize=(10, 8))
sns.barplot(
    x=corr_by_team.values,
    y=corr_by_team.index,
    palette='coolwarm'
)
plt.axvline(0, color='black', linewidth=1)
plt.title('Correlación Asistencia ↔ Victoria Local (por Equipo)')
plt.xlabel('Coeficiente de correlación de Pearson')
plt.ylabel('Equipo')
plt.tight_layout()
plt.show()