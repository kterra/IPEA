from preprocessing import *
from classifier import *
import os

SOURCE_PMB_2015 = "PMB_2015"
SOURCE_SAMMED_2015 = "SAMMED_2015"
SOURCE_SAMMED_2014 = "SAMMED_2014"
SOURCE_CATMAT_2014 = "CATMAT_2014"


if __name__ == '__main__':
    """ Starts the programs.
    Pre-processing and Classifier are called here.
    Log and results will be stored on files.
    """

    print("Start...")

    #Processing DCB table to get complete products names
    #load_dcb_table_into_memory()

    #Pre processing of labs tables
    #enter columns: apresentaccao, produto, lab, codigo
    # pre_processing_table("FAT_QTD_PMB_PPP_0310_0215_999_FORMATADA.XLS","PMB", 1,2,3,4)
    # all_filenames = os.listdir("raw")
    # all_filenames = [filename for filename in all_filenames if filename.startswith("rel_LISTA_REVISTA_SAMMED")]
    # for fname in all_filenames:
    #    pre_processing_table(fname,"SAMMED",8,7,6,3)

    #pre_processing_table("PMB_2015_02_FORMATADA.XLS",SOURCE_PMB_2015, 5,3,2,20)
    #pre_processing_table("xls_conformidade_gov_site_2015_02_20_FORMATADA.xls",SOURCE_SAMMED_2015, 9,8,5,6)
    #pre_processing_table("dados_cadastrais_sammed.xlsx","CAD_SAMMED", 6,5,4,8)

    #pre_processing_table("xls_conformidade_gov_site_2014_12_22_FORMATADA.xls",SOURCE_SAMMED_2014, 8,7,4,5)

    #enter columns: apresentaccao, produto, unit, vol, codigo
    #pre_processing_CATMAT_table("LISTA DE CATMATS MEDICAMENTOS 2014_FORMATADA.xlsx",SOURCE_CATMAT_2014, 2,3,4,5,1)


    #Search drug macthes by drugs' names

    #search_drugs_names_matches(SOURCE_CATMAT_2014, SOURCE_SAMMED_2014)

    #Search drug macthes by presentation description
    search_drugs_presentation_matches(SOURCE_CATMAT_2014, SOURCE_SAMMED_2014)


    print("Finished.")
