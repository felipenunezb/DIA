from collections import defaultdict
import streamlit as st
import pandas as pd

from aux_fx import get_data, analyze_single, analyze_compare

st.set_page_config(page_icon="👩‍🏫", page_title="DIA", layout="wide")

OPTION_EXAMPLE = "Revisar ejemplo"
OPTION_UPLOAD = "Subir archivos"
SIDEBAR_OPTIONS = [OPTION_UPLOAD, OPTION_EXAMPLE]

ANALYSIS_SINGLE = 'Analizar curso'
ANALYSIS_COMPARISON = 'Comparar cursos'
ANALYSIS_EVOLUTION = 'Comparar progresion'
ANALYSIS_OPTIONS = [ANALYSIS_SINGLE, ANALYSIS_COMPARISON, ANALYSIS_EVOLUTION]

def main():
    
    st.sidebar.title("Seleccione archivo:")
    app_mode = st.sidebar.selectbox("Fuente", SIDEBAR_OPTIONS)
    
    #set child multi-element container, for easy cleaning
    c = st.empty()
    sc = c.container()
    
    if app_mode == OPTION_UPLOAD:
        
        f = st.sidebar.file_uploader("Seleccione los documentos a subir", type=['xls'], accept_multiple_files=True)
        
        if f:
            
            results_list, ref_dict = get_data(f)
            
            analysis = st.sidebar.selectbox("Analisis", ANALYSIS_OPTIONS)
            
            if analysis == ANALYSIS_SINGLE:
            
                analyze_single(sc, ref_dict, results_list)
            
            elif analysis == ANALYSIS_COMPARISON:
                
                analyze_compare(sc, ref_dict, results_list)
                
            else:
                
                sc.write("WIP")


    
        
main()