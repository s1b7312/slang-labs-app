
from config import ALLOWED_EXTENSIONS


def is_allowed_extension(filename:str) -> bool:
    '''
    check if extension is allowed
    :param filename:
    :return:
    '''

    ext = filename.rsplit('.', 1)[1].lower()
    return ext in ALLOWED_EXTENSIONS