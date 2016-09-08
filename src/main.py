from preprocessing import *
from classifier import *
import os

SOURCE_PMB = "PMB"
SOURCE_SAMMED = "SAMMED"


if __name__ == '__main__':
    print("Start...")

    # load_dcb_table_into_memory()
    # pre_processing_table("FAT_QTD_PMB_PPP_0310_0215_999_FORMATADA.XLS","PMB", 1,2,3,4)
    # all_filenames = os.listdir("raw")
    # all_filenames = [filename for filename in all_filenames if filename.startswith("rel_LISTA_REVISTA_SAMMED")]
    # for fname in all_filenames:
    #    pre_processing_table(fname,"SAMMED",8,7,6,3)

    #product_matches(SOURCE_PMB, SOURCE_SAMMED)

    check_digits_pattern("750 MG PÓ SOL INJ CT FA VD INC + 1 AMP DIL VD INC X 6 ML")

    print("Finished.")
