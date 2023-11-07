import cProfile
import pstats
from time import perf_counter, process_time


def Profiler(
    target,
    args: list = (),
    kwargs=None,
    time_info: bool = False,
    output_file: bool = False,
    _return: str = "r",
) -> any:
    """
    The Profiler function is a wrapper for the cProfile module.
    It allows you to profile your code and get information about it's performance.
    The Profiler function takes in 5 arguments: target, args, time_info and output_file.
    target is the function that you want to profile (required).
    args are any arguments that need to be passed into target (optional).
    time_info will print out how long it took for the profiled code to run if set True (optional).
    output file will create a file named PROFILING.prof if set True (default False)
    Open this file with 'snakeviz PROFILING.prof' in CLI environment !!! Will overwrite if file exists
    _return: use 'r' to return response, 't' to return time or 'a' to return tuple of response and time

    :param target: Specify the function you want to profile
    :param args: tuple: Pass arguments to the target function
    :param time_info: bool: Print the time it spend to process
    :param output_file: bool: Dump the profiling data to a file
    :param _return: str: Determine what the function should return
    :return: A tuple: (response, time)
    """
    if kwargs is None:
        kwargs = {}
    with cProfile.Profile() as pr:
        _start = perf_counter()
        response = target(*args, **kwargs)
        _end = perf_counter()
    stats = pstats.Stats(pr)
    stats.sort_stats(pstats.SortKey.TIME)
    if output_file:
        stats.dump_stats(filename="PROFILING.prof")
        print("Use 'snakeviz PROFILING.prof' to open file")
    if time_info:
        print(f"Time it spend to process: {str(_end - _start)}s")
    if _return == "a":
        return (response, float(_end - _start))
    elif _return == "r":
        return response
    elif _return == "t":
        return float(_end - _start)
