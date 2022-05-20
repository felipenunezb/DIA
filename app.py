from collections import defaultdict
import streamlit as st
import pandas as pd

from dia.extract import get_all_data
from dia.analyze import get_single_results

from aux_fx import get_dict_references

st.set_page_config(page_icon="👩‍🏫", page_title="DIA", layout="wide")

OPTION_EXAMPLE = "Revisar ejemplo"
OPTION_UPLOAD = "Subir archivos"
SIDEBAR_OPTIONS = [OPTION_UPLOAD, OPTION_EXAMPLE]

def main():
    
    st.sidebar.title("Seleccione archivo:")
    
    app_mode = st.sidebar.selectbox("Fuente", SIDEBAR_OPTIONS)
    
    if app_mode == OPTION_UPLOAD:
        
        f = st.sidebar.file_uploader("Seleccione los documentos a subir", type=['xls'], accept_multiple_files=True)
        
        if f:
            
            info_list, results_list = get_all_data(f)
            pruebas = [fl.name[23 + (fl.name[23:-4].find('_') + 1): 23 + (fl.name[23:-4].find('_') + 1) + (fl.name[23 + (fl.name[23:-4].find('_') + 1):-4].find('_'))] for fl in f]
                
            ref_dict = get_dict_references(info_list, pruebas)
            
            view_results(ref_dict, results_list)
        
        
def view_results(ref_dict, results_list):
    
    curso = st.selectbox(label = 'Curso', options=sorted(list(ref_dict.keys())))
    prueba = st.selectbox(label = 'Prueba', options=ref_dict[curso].keys())
    
    result_ix = ref_dict[curso][prueba]
    
    results = get_single_results(df=results_list[result_ix], df_nm=curso)
    
    st.plotly_chart(results['kde'])
    
        
main()