
import logging, os

'''Не использую logging в название файла во избежание путаницы'''
logging.basicConfig(
    level=logging.DEBUG,
    format=" %(asctime)s %(levelname)s %(message)s  ",
    handlers=[
        logging.FileHandler("py_log.log", mode="w"),  # в файл
        logging.StreamHandler()  # в консоль
    ]
)

class Log:
    _file_name = 'unknown'

    @classmethod
    def init(cls, file_name: str):
        ''' Specifying the file name.
            If not using then name file is unknown'''
        cls._file_name = os.path.relpath(file_name) 

    @classmethod
    def debug(cls, text: str = "", error = None):
        if text:
            logging.debug('text: %s, file: %s',text, cls._file_name, exc_info = True if error else False)
    
    @classmethod
    def info(cls, text: str = "", error = None):
        if text:
            logging.info('text: %s, file: %s',text, cls._file_name, exc_info = True if error else False)
    
    @classmethod
    def error(cls, text: str = "", error = None):
        if text:
            logging.error('text: %s, file: %s',text, cls._file_name, exc_info = True if error else False)
    
    @classmethod
    def warning(cls, text: str = "", error = None):
        if text:
            logging.warning('text: %s, file: %s',text, cls._file_name, exc_info = True if error else False)
    
    @classmethod
    def critical(cls, text: str = "", error = None):
        if text:
            logging.critical('text: %s, file: %s',text, cls._file_name, exc_info = True if error else False)
