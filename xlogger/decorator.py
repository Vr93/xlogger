import functools
import time
from xlogger.logger import logger

def log(**kwargs):
    log_level = kwargs['level']
    def decorator_log(func):
        @functools.wraps(func)
        def wrapper_log(*args, **kwargs):
            args_repr = [repr(a) for a in args]
            time_start = time.perf_counter()
            kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
            signature = ", ".join(args_repr + kwargs_repr)
            logger.log(_convert_str_to_int_log_level(log_level), f"Calling {func.__name__}({signature})")
            value = func(*args, **kwargs)
            run_time = time.perf_counter() - time_start
            logger.log(_convert_str_to_int_log_level(log_level), f"{func.__name__!r} returned {value!r}, finished in {run_time:.4f}s")
            return value
        return wrapper_log
    return decorator_log

def _convert_str_to_int_log_level(log_level):
    """ Returns log level as int
    Parameters
    ------
    log_level : str or int
    Returns
    ------
    log_level: int
        Converts log level from str to int """
    if isinstance(log_level, str):
        log_levels = {
            'NOTSET' : 0,
            'NOT SET' : 0,
            'DEBUG' : 10,
            'INFO' : 20,
            'WARNING' : 30,
            'ERROR' : 40,
            'CRITICAL' : 50
        }
        return log_levels[log_level.upper()]
    else:
        return log_level
