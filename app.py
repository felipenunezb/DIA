import streamlit as st
import pandas as pd

from dia.extract import get_all_data

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
            st.write(f)
            
            info_list, results_list = get_all_data(f)
            pruebas = [fl.name[23 + (fl.name[23:-4].find('_') + 1): 23 + (fl.name[23:-4].find('_') + 1) + (fl.name[23 + (fl.name[23:-4].find('_') + 1):-4].find('_'))] for fl in f]
                
            
            st.write(info_list)
            st.write(pruebas)
            
            st.write(results_list[0])
            
        
        
main()