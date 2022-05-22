from collections import defaultdict
from dia.extract import extract_all_data
from dia.analyze import get_single_results, get_comparison
import pandas as pd

def get_dict_references(info_list, pruebas):
    '''
    parameters:
    info_list: list of dictionaries [{establecimiento, curso}]
    pruebas: list of pruebas [pruebas]
    
    returns
    ref_dict: {curso: {prueba: ix}}
    '''
    ref_dict = defaultdict(lambda: defaultdict())
    for ix, (info, prueba) in enumerate(zip(info_list, pruebas)):
        ref_dict[info['curso']][prueba] = ix
        
    return ref_dict

        
def get_data(f: list) -> tuple:
    
    #get data from excel files
    info_list, results_list_ = extract_all_data(f)
    
    #get pruebas from name of files
    pruebas = [fl.name[23 + (fl.name[23:-4].find('_') + 1): 23 + (fl.name[23:-4].find('_') + 1) + (fl.name[23 + (fl.name[23:-4].find('_') + 1):-4].find('_'))] for fl in f]
    
    #append curso to dataframes
    results_list = []
    for df, info in zip(results_list_, info_list):
        df_ = df.copy(deep=True)
        df_.insert(loc=0, column='curso', value=info['curso'])
        #df_['curso'] = info['curso']
        results_list.append(df_)
    
    #get reference dictionary ([curso][prueba] -> index)
    ref_dict = get_dict_references(info_list, pruebas)
    
    return results_list, ref_dict


def analyze_single(container, ref_dict: dict, results_list: list):
    
    #update select boxes based on selection
    curso = container.selectbox(label = 'Curso', options=sorted(list(ref_dict.keys())))
    prueba = container.selectbox(label = 'Prueba', options=ref_dict[curso].keys())
    
    #get file index, based on select boxes
    result_ix = ref_dict[curso][prueba]
    
    #pull dataframe
    results = get_single_results(df=results_list[result_ix])
    
    #plot density
    container.plotly_chart(results['kde'])
    
    #TODO: scatter plot? clusters?
    
def analyze_compare(container, ref_dict: dict, results_list: list):
    
    #get list of cursos, without letters
    curso_ref_dict = defaultdict(lambda: list())
    _ = [curso_ref_dict[c.split()[0]].append(c) for c in list(ref_dict.keys())]

    #update select boxes based on selection
    curso = container.selectbox(label = 'Nivel', options=sorted(list(curso_ref_dict.keys())))
    prueba = container.selectbox(label = 'Prueba', options=ref_dict[curso_ref_dict[curso][0]])
    
    #get dataframes
    cursos_list = curso_ref_dict[curso]
    df_indexes = [ref_dict[c][prueba] for c in cursos_list]
    dataframes = [results_list[ix] for ix in df_indexes]
    df = pd.concat(dataframes)
    
    #analyze
    comb_dict = get_comparison(df)
    
    for eje, vals in comb_dict.items():
        container.write(eje)
        col1, col2 = container.columns([3, 1])
        col1.plotly_chart(vals['kde'])
        comparisons = [c for c in list(vals.keys()) if c != 'kde']
        for c in comparisons:
            col2.write(f"{c}: {vals[c]}")
    
    
    return