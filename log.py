import logging

def get_logger(name,filename,level):
    logger=logging.getLogger(name)

    c_handler = logging.StreamHandler()
    f_handler = logging.FileHandler('./log/'+filename)
    if level=="info":
        c_handler.setLevel(logging.INFO)
        f_handler.setLevel(logging.INFO)
    elif level=='debug':
        c_handler.setLevel(logging.DEBUG)
        f_handler.setLevel(logging.DEBUG)
    elif level == "error":
        c_handler.setLevel(logging.ERROR)
        f_handler.setLevel(logging.ERROR)
    else:
        c_handler.setLevel(logging.DEBUG)
        f_handler.setLevel(logging.DEBUG)

    # Create formatters and add it to handlers
    c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
    f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    c_handler.setFormatter(c_format)
    f_handler.setFormatter(f_format)

    # Add handlers to the logger
    logger.addHandler(c_handler)
    logger.addHandler(f_handler)

    return logger