import traceback


def readable_exception(e: Exception, verbose=False):
    message = None
    if verbose is True:
        message = traceback.format_exc()
    if message is None:
        message = str(e)
    return f"{message}| Handled"
