import matplotlib.pyplot as plt
import pandas as pd
from statsmodels.stats.proportion import proportions_ztest
import statsmodels.formula.api as smf
import seaborn as sns


# 1. Leer CSV
df = pd.read_csv('C:/EDA/matches.csv')
# Definir lista de columnas
cols = ['Date', 'Team', 'Opponent', 'Venue', 'Result', 'GF', 'GA', 'xG', 'xGA', 'Attendance', 'Referee', 'Formation', 'Round']

# Crear un nuevo DataFrame filtrado
df_sel = df[cols].copy()

# Copiar DataFrame
df2 = df_sel.copy()
df2['home_win'] = (df2['Result'] == 'W').astype(int)

# Agrupar por árbitro
ref_stats = (
    df2
      .groupby('Referee')['home_win']
      .agg(['mean','count'])
      .rename(columns={'mean':'home_win_pct','count':'n_matches'})
      .reset_index()
)

# Convertir a % y filtrar árbitros con al menos 20 partidos
ref_stats['home_win_pct'] = ref_stats['home_win_pct'] * 100
ref_stats = ref_stats[ref_stats['n_matches'] >= 20]  # umbral arbitral

# Ordenar de mayor a menor
ref_stats = ref_stats.sort_values('home_win_pct', ascending=False)
print(ref_stats.head(10))

#Test de proporciones (binomial). Comprobamos si el porcentaje de cada árbitro difiere del % global de victorias locales.
global_p = df2['home_win'].mean()  # proporción global

significant_refs = []
for _, row in ref_stats.iterrows():
    count = int(row['home_win_pct'] * row['n_matches'] / 100)
    nobs  = int(row['n_matches'])
    stat, pval = proportions_ztest(count, nobs, value=global_p)
    if pval < 0.05:
        significant_refs.append({
            'Referee': row['Referee'],
            'home_win_pct': row['home_win_pct'],
            'n_matches': nobs,
            'p_value': pval
        })

if not significant_refs:
    print("No hay árbitros con tasa de victorias local significativamente distinta de la global (p<0.05).")
else:
    sig_df = (
        pd.DataFrame(significant_refs)
          .sort_values('home_win_pct', ascending=False)
          .reset_index(drop=True)
    )
    print("\nÁrbitros con % local significativamente distinto:\n", sig_df)

#Modelo logístico multinivel. Para aislar el efecto del árbitro controlando asistencia, rivalidad y xG. Los coeficientes de C(Referee)[T.XXX] medirán el cambio en log-odds de victoria local asociado a cada árbitro, tras ajustar por variables de partido.
# Crear indicador Top6 si no existe
top6 = ['Arsenal','Chelsea','Liverpool','ManCity','ManUtd','Tottenham']
df2['top6_opp'] = df2['Opponent'].isin(top6).astype(int)

# Ajustar el modelo logístico con árbitro como covariable categórica
model = smf.logit(
    'home_win ~ Attendance + xG + xGA + top6_opp + C(Referee)',
    data=df2
).fit(disp=False)

# Extraer coeficientes y p-values para las dummies de árbitro
ref_coefs = model.params.filter(like='Referee')
ref_pvals  = model.pvalues.filter(like='Referee')

# Construir DataFrame de resultados arbitrales
df_referees = pd.DataFrame({
    'coef':    ref_coefs,
    'p_value': ref_pvals
}).sort_values('coef', ascending=False)

print("\nSesgo arbitral (cambio en log-odds de victoria local):\n")
print(df_referees)

#resultados
plt.figure(figsize=(10,6))
sns.histplot(ref_stats['home_win_pct'], bins=20, kde=True, color='skyblue')
plt.axvline(global_p*100, color='red', linestyle='--',
            label=f'Global {global_p*100:.1f}%')
plt.title('% Victorias Locales por Árbitro')
plt.xlabel('% Victorias Locales')
plt.ylabel('Frecuencia de Árbitros')
plt.legend()
plt.tight_layout()
plt.show()