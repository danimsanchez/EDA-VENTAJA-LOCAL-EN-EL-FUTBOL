import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Leer CSV
df = pd.read_csv('C:/EDA/matches.csv')
# Definir lista de columnas
cols = ['Date', 'Team', 'Opponent', 'Venue', 'Result', 'GF', 'GA', 'xG', 'xGA', 'Attendance', 'Referee', 'Formation', 'Round']

# Crear un nuevo DataFrame filtrado
df_sel = df[cols].copy()

# Calcular pct victorias casa y fuera por equipo
team_stats = df_sel.groupby(['Team','Venue'])['Result'] \
               .apply(lambda s: (s=='W').mean()*100) \
               .unstack()

# Añadir columna Diff = %Home − %Away
team_stats['Diff'] = team_stats['Home'] - team_stats['Away']

# Formatear y mostrar resultados por consola
pd.set_option('display.float_format', '{:.1f}%'.format)
print("\n-- Estadísticas de Victorias por Equipo --")
print(team_stats.sort_values('Diff', ascending=False))

# Ordenar de mayor a menor brecha
team_stats = team_stats.sort_values('Diff', ascending=False)

# Plot
plt.figure(figsize=(10, 8))
sns.barplot(
    x='Diff',
    y=team_stats.index,
    data=team_stats.reset_index(),
    palette='coolwarm'
)
plt.axvline(0, color='k', linewidth=1)
plt.title('Ventaja de Local: % Victorias Casa − % Victorias Fuera (Premier 23/24)')
plt.xlabel('Diferencia de % de Victorias')
plt.ylabel('Equipo')
plt.tight_layout()
plt.show()