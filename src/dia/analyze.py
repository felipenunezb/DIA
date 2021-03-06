import pandas as pd
from scipy.stats import ttest_ind
import seaborn as sns
from collections import defaultdict
import plotly.figure_factory as ff
import plotly.express as px


def get_single_results(df: pd.DataFrame, prueba) -> dict:
    
    #ejes
    cols = list(df.columns[2:])

    fig = ff.create_distplot([df[c] for c in cols], cols, show_hist=False, show_rug=False, curve_type='normal')
    
    melt_df = df.melt(id_vars=['curso', 'Nombre del Estudiante'])
    melt_df = melt_df.rename(columns={'value': 'Puntaje', 'variable': 'Ejes'})
    fig2 = px.box(melt_df, x="Puntaje", y=f"curso", color='Ejes', notched=False, orientation='h', title=f"{prueba}")
    
    fig.update_layout(width=1100,height=300,margin=dict(l=20, r=20, t=20, b=20))
    fig2.update_layout(width=1100,height=300,margin=dict(l=20, r=20, t=50, b=20))
      
    return {'kde': fig, 'box': fig2}

def get_comparison(df: pd.DataFrame):
    
    #ejes
    cols = list(df.columns[2:])
    
    #cursos
    cursos = list(df['curso'].unique())
    cursos_comb = []
    appended = []
    for c_0 in cursos:
        for c_1 in cursos:
            if c_0 != c_1 and c_1 not in appended:
                cursos_comb.append([c_0, c_1])
        appended.append(c_0)
        
    comb_dict = defaultdict(lambda: defaultdict())
    for col in cols:
        for comb in cursos_comb:
            df1 = df[df['curso'] == comb[0]]
            df2 = df[df['curso'] == comb[1]]
            p_val = ttest_ind(df1.loc[:, col], df2.loc[:,col]).pvalue
            comb_dict[col][f"{comb[0]} vs {comb[1]}"] =  "Significativo" if p_val < 0.05 else "No significativo"
        
        sub_df = df.loc[:, ['curso', col]].reset_index()
        sub_df = sub_df.set_index(['index', 'curso'])[col].unstack().reset_index(drop=True)
        sub_cols = sub_df.columns
        fig = ff.create_distplot([sub_df[c].dropna() for c in sub_cols], sub_cols, show_hist=False, show_rug=True)
        comb_dict[col]['kde'] = fig   
    
    return comb_dict

def get_2fold_comparison(df1: pd.DataFrame, df1_curso: str, df2: pd.DataFrame, df2_curso: str) -> dict:
    
    results = defaultdict(lambda x: defaultdict(lambda x: list))
    
    ncols = len(df1.columns)
    for ix in range(1,ncols):

        p_val = ttest_ind(df1.iloc[:, ix], df2.iloc[:,ix]).pvalue        
        
        tmp_01 = df1[[df1.columns[ix]]].copy(deep=True)
        tmp_02 = df2[[df2.columns[ix]]].copy(deep=True)
        tmp_01['curso'] = df1_curso
        tmp_02['curso'] = df2_curso
        tmp_df = pd.concat([tmp_01, tmp_02]).reset_index()
        kde_plot = sns.displot(tmp_df, x=df1.columns[ix], hue="curso", kind="kde")
        hist_plot = sns.displot(tmp_df, x=df1.columns[ix], hue="curso", element="step")
        
        results[ncols[ix]]['pvalue'] = p_val
        results[ncols[ix]]['kde'] = kde_plot
        results[ncols[ix]]['hist'] = hist_plot
        
        return results