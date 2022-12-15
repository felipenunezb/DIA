from collections import defaultdict
import streamlit as st
import pandas as pd
import json

from aux_fx import get_data, analyze_single, analyze_compare, analyze_progress, get_progress_ref_dict, generate_report

st.set_page_config(page_icon="👩‍🏫", page_title="DIA", layout="wide")

OPTION_EXAMPLE = "Revisar 2022"
OPTION_UPLOAD = "Subir archivos"
SIDEBAR_OPTIONS = [OPTION_EXAMPLE, OPTION_UPLOAD]

ANALYSIS_SINGLE = 'Analizar curso'
ANALYSIS_COMPARISON = 'Comparar cursos'
ANALYSIS_EVOLUTION = 'Comparar progresion'
ANALYSIS_OVERALL = 'Reporte Cambios Significativos'
ANALYSIS_OPTIONS = [ANALYSIS_SINGLE, ANALYSIS_EVOLUTION, ANALYSIS_OVERALL]

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

    elif app_mode == OPTION_EXAMPLE:
        
        with open('./sample_data/ref_dict.json', 'r') as infile:
            ref_dict = json.load(infile)
            
        with open('./sample_data/results_list_dict.json', 'r') as infile:
            results_list_dict = json.load(infile)
            
        results_list = [pd.DataFrame(d) for d in results_list_dict]
        
        progress_ref_dict = get_progress_ref_dict(ref_dict)

        analysis = st.sidebar.selectbox("Analisis", ANALYSIS_OPTIONS)
            
        if analysis == ANALYSIS_SINGLE:
        
            analyze_single(sc, ref_dict, results_list)
        
        elif analysis == ANALYSIS_EVOLUTION:
            
            analyze_progress(sc, ref_dict, results_list, progress_ref_dict)
            
        elif analysis == ANALYSIS_OVERALL:
            
            generate_report(sc, ref_dict, results_list, progress_ref_dict)
            
        else:
            
            sc.write("WIP")
        
main()