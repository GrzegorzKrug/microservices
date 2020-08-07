import logging


def define_logger(name, mode='a'):
    custom_logger = logging.getLogger(name)
    file_path = name + '.log'

    fh = logging.FileHandler(file_path, mode=mode)
    ch = logging.StreamHandler()

    formatter = logging.Formatter(
            f'%(asctime)s - {name} - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    # custom_logger.addHandler(ch)
    custom_logger.addHandler(fh)

    return custom_logger
