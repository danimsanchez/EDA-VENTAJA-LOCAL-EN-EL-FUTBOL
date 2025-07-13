import matplotlib.pyplot as plt
import pandas as pd

# Leer CSV
df = pd.read_csv('C:/EDA/matches.csv')
# Definir lista de columnas
cols = ['Date', 'Team', 'Opponent', 'Venue', 'Result', 'GF', 'GA', 'xG', 'xGA', 'Attendance', 'Referee', 'Formation', 'Round']

# Crear un nuevo DataFrame filtrado
df_sel = df[cols].copy()

# Filtrar partidos en casa y fuera
home = df_sel[df_sel['Venue'] == 'Home']
away = df_sel[df_sel['Venue'] == 'Away']

# Contar victorias
home_wins = (home['Result'] == 'W').sum()
away_wins = (away['Result'] == 'W').sum()

# Totales
n_home = len(home)
n_away = len(away)

# Porcentajes
pct_home_win = home_wins / n_home * 100
pct_away_win = away_wins / n_away * 100

# Visualizar resultados
print(f"Partidos en casa: {n_home}, victorias: {home_wins} ({pct_home_win:.1f}%)")
print(f"Partidos fuera: {n_away}, victorias: {away_wins} ({pct_away_win:.1f}%)")

# Plot
plt.bar(['Home win %','Away win %'], [pct_home_win, pct_away_win], color=['skyblue','salmon'])
plt.ylabel('Porcentaje de victorias')
plt.title('Comparativa victorias casa vs fuera')
plt.ylim(0,100)
plt.show()
