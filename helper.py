import time


def timer(func):
    def wrapper_timer(*args, **kwargs):
        start_time = time.perf_counter()
        value = func(*args, **kwargs)
        print(f"{func.__name__}() time taken: {time.perf_counter() - start_time:.4f} secs")
        return value
    return wrapper_timer

