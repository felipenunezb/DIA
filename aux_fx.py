from collections import defaultdict

def get_dict_references(info_list, pruebas):
    
    ref_dict = defaultdict(lambda: defaultdict())
    for ix, (info, prueba) in enumerate(zip(info_list, pruebas)):
        ref_dict[info['curso']][prueba] = ix
        
    return ref_dict