import pandas as pd
import statsmodels.formula.api as smf
import numpy as np
import matplotlib.pyplot as plt

# Leer CSV
df = pd.read_csv('C:/EDA/matches.csv')
# Definir lista de columnas
cols = ['Date', 'Team', 'Opponent', 'Venue', 'Result', 'GF', 'GA', 'xG', 'xGA', 'Attendance', 'Referee', 'Formation', 'Round']

# Crear un nuevo DataFrame filtrado
df_sel = df[cols].copy()

# Crear un nuevo DataFrame filtrado
df_home = df_sel[df_sel['Venue']=='Home'].copy()

# Crear indicador de victoria local
df_home['home_win'] = np.where(df_home['Result']=='W', 1, 0)

# Definir lista de rivales Top 6 (ajusta nombres exactos según tu df)
top6 = [
    'Arsenal', 'TottenhamHotspur', 'Chelsea',
    'Liverpool', 'ManchesterCity', 'ManchesterUnited'
]

# Crear indicador de rival Top 6
df_home['top6_opponent'] = np.where(
    df_home['Opponent'].isin(top6), 1, 0
)

# Modelo con interacción
model = smf.logit(
    formula='home_win ~ Attendance + top6_opponent + Attendance:top6_opponent',
    data=df_home
).fit(disp=False)

# Rango de asistencia
att_range = np.linspace(
    df_home['Attendance'].min(),
    df_home['Attendance'].max(), 100
)

# DataFrame para predicción
pred_df = pd.DataFrame({
    'Attendance': np.concatenate([att_range, att_range]),
    'top6_opponent': [0]*100 + [1]*100
})

# Predicción de probabilidades
pred_df['pred_prob'] = model.predict(pred_df)

# Separar para graficar
pred_no6 = pred_df[pred_df['top6_opponent']==0]
pred_6   = pred_df[pred_df['top6_opponent']==1]

# Plot
plt.figure(figsize=(8,5))
plt.plot(
    pred_no6['Attendance'], pred_no6['pred_prob'],
    label='Rival no Top 6', color='green', lw=2
)
plt.plot(
    pred_6['Attendance'], pred_6['pred_prob'],
    label='Rival Top 6', color='red',   lw=2
)
plt.scatter(
    df_home['Attendance'], df_home['home_win'],
    alpha=0.2, s=20, color='gray'
)
plt.title('Probabilidad de victoria local vs Asistencia\n(rival Top 6 vs resto)')
plt.xlabel('Asistencia')
plt.ylabel('Probabilidad de victoria local')
plt.legend()
plt.ylim(0,1)
plt.tight_layout()
plt.show()

# Coeficientes del modelo
coef_df = pd.DataFrame({
    'coef': model.params,
    'std_err': model.bse,
    'p_value': model.pvalues
})
print("\nCoeficientes y significancia:\n", coef_df)