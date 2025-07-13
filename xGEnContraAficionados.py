import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# 1. Leer CSV
df = pd.read_csv('C:/EDA/matches.csv')
# Definir lista de columnas
cols = ['Date', 'Team', 'Opponent', 'Venue', 'Result', 'GF', 'GA', 'xG', 'xGA', 'Attendance', 'Referee', 'Formation', 'Round']

# Crear un nuevo DataFrame filtrado
df_sel = df[cols].copy()

# Filtrar solo partidos en casa
df_home = df_sel[df_sel['Venue']=='Home'].copy()

# Correlación Attendance vs xGA
corr = df_home['Attendance'].corr(df_home['xGA'])
print(f"Correlación Attendance vs xGA: {corr:.3f}")

# Crear cuantiles basados en Attendance
df_home['att_q'] = pd.qcut(df_home['Attendance'], 5)

# Calcular xGA medio por cuantil
xga_by_q = (
    df_home
      .groupby('att_q')['xGA']
      .mean()
      .reset_index(name='mean_xGA')
)

print(xga_by_q)


#La pendiente de la línea indicará visualmente si existe efecto reductor de xGA a medida que crece la asistencia.
plt.figure(figsize=(8,5))
sns.regplot(
    x='Attendance',
    y='xGA',
    data=df_home,
    scatter_kws={'alpha':0.3, 's':20},
    line_kws={'color':'red'}
)
plt.title('xGA vs Asistencia (partidos en casa)')
plt.xlabel('Asistencia')
plt.ylabel('xGA concedido')
plt.tight_layout()
plt.show()