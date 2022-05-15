import pandas as pd
import os

def get_info(filepath: str) -> tuple:
    '''
    Nombre del establecimiento y curso.
    '''
    df = pd.read_excel(filepath, header=None, usecols="A:B", skiprows=lambda x: x not in [4,5,6])
    
    establecimiento = df.iloc[0,1]
    curso = df.iloc[1,1]
    
    return establecimiento, curso


def get_results(filepath: str) -> pd.DataFrame:
    '''
    Lista de alumnos y resultados por eje.
    '''
    df = pd.read_excel(filepath, header=0, skiprows=12,thousands = '.', decimal=',')
    df = df.drop(columns=['Número de Lista'])

    return df
    

def get_files_folder(folder_path: str) -> list:
    '''
    Lista de archivos (path), recorriendo los archivos en un directorio.
    '''
    files_list = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f)) and f.endswith('xls')]
    
    return files_list


def get_all_data(input_files) -> tuple:
    '''
    Itera sobre la lista de archivos y extrae la informacion de identificacion y resultados.
    Puede tomar una lista de paths o un folder con los archivos.
    '''
    info_list = []
    results_list = []
    
    if isinstance(input_files, str):
        files_list = get_files_folder(input_files)
    elif isinstance(input_files, list):
        files_list = input_files.copy()
    else:
        raise RuntimeError("Input should be a list of filepaths or the path to a folder of files.")
    
    for filepath in files_list:
        info_list.append(get_info(filepath))
        results_list.append(get_results(filepath))
        
    return info_list, results_list
    