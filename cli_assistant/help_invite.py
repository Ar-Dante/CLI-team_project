from .assistant import main
from .main_information import InfoHelper


def short_help():
    print(InfoHelper.get_info("info"))
    return main()
