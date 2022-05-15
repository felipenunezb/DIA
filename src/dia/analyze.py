import pandas as pd
from scipy.stats import ttest_ind
import seaborn as sns
from collections import defaultdict

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