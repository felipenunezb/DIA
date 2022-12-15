from collections import defaultdict
from extract import extract_all_data
from analyze import get_single_results, get_comparison, get_progress_comparison, get_report_rows
import pandas as pd
import streamlit as st

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
    #pruebas = [fl.name[23 + (fl.name[23:-4].find('_') + 1): 23 + (fl.name[23:-4].find('_') + 1) + (fl.name[23 + (fl.name[23:-4].find('_') + 1):-4].find('_'))] for fl in f]
    pruebas = ['LECTURA' if fl.name.find('LECTURA') > 0 else 'MATEMATICA' for fl in f]
    
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
    #etapa = container.selectbox(label = 'Etapa', options=ref_dict[curso][prueba].keys())
    etapas = sorted(list(ref_dict[curso][prueba].keys()))
    
    for etapa in etapas:
    
        #get file index, based on select boxes
        result_ix = ref_dict[curso][prueba][etapa]
        
        #pull dataframe
        results = get_single_results(df=results_list[result_ix], prueba=prueba, etapa=etapa)
        
        #plot density
        container.plotly_chart(results['box'],width=1100,height=300, use_container_width=True)
        #container.plotly_chart(results['hist'],width=1100,height=300, use_container_width=True)
        
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

def analyze_progress(container, ref_dict: dict, results_list: list, progress_ref_dict: dict):
    
    #update select boxes based on selection
    curso = container.selectbox(label = 'Curso', options=sorted(list(progress_ref_dict.keys())))
    prueba = container.selectbox(label = 'Prueba', options=progress_ref_dict[curso])
    
    extracted_list = []
    for etapa in sorted(list(ref_dict[curso][prueba].keys())):
        result_ix = ref_dict[curso][prueba][etapa]
        df = results_list[result_ix]
        melt_df = df.melt(id_vars=['curso', 'Nombre del Estudiante'])
        melt_df = melt_df.rename(columns={'value': 'Puntaje', 'variable': 'Ejes'})
        melt_df = melt_df[melt_df['Ejes'] != 'NIVEL DE LOGRO']
        melt_df['etapa'] = etapa
        extracted_list.append(melt_df)
    curso_df = pd.concat(extracted_list, axis=0)
    
    results = get_progress_comparison(curso_df, prueba, curso)
    
    #plot density
    for p in results['ind']:
        container.plotly_chart(p,width=640,height=480, use_container_width=True)
        
        
def get_progress_ref_dict(ref_dict):
    progress_ref_dict = defaultdict(lambda: [])
    for curso, prueba_etapa in ref_dict.items():
        for prueba, etapa in prueba_etapa.items():
            if len(etapa) > 1:
                progress_ref_dict[curso].append(prueba)
                
    return progress_ref_dict

def generate_report(container, ref_dict: dict, results_list: list, progress_ref_dict: dict):
    
    cambios = []
    for curso, pruebas in progress_ref_dict.items():
        for prueba in pruebas:
            extracted_list = []
            for etapa in sorted(list(ref_dict[curso][prueba].keys())):
                result_ix = ref_dict[curso][prueba][etapa]
                df = results_list[result_ix]
                melt_df = df.melt(id_vars=['curso', 'Nombre del Estudiante'])
                melt_df = melt_df.rename(columns={'value': 'Puntaje', 'variable': 'Ejes'})
                melt_df = melt_df[melt_df['Ejes'] != 'NIVEL DE LOGRO']
                melt_df['etapa'] = etapa
                extracted_list.append(melt_df)
            curso_df = pd.concat(extracted_list, axis=0)
    
            sub_results = get_report_rows(curso_df, prueba, curso)
            cambios.extend(sub_results)
            
    report_df = pd.DataFrame(cambios).sort_values(by=['Curso', 'Prueba', 'Cambio Pct. Prop.'], ascending=[True, True, False])
    cols = [col for col in report_df.columns if col != 'Cambio Pct. Prop.']
    
    csv = convert_df(report_df[cols])
    
    container.download_button(
        label="Descargar CSV",
        data=csv,
        file_name='cambios_significativos_dia_2022.csv',
        mime='text/csv',
    )
    
    container.dataframe(report_df[cols], height=800, use_container_width=True)
    
    
@st.cache
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')