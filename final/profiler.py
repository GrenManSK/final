import cProfile
import pstats


def Profiler(target, args=()):
    if args == ():
        with cProfile.Profile() as pr:
            response = target
    else:
        with cProfile.Profile() as pr:
            response = target(*args)
    stats = pstats.Stats(pr)
    stats.sort_stats(pstats.SortKey.TIME)
    stats.dump_stats(filename='PROFILING.prof')
    return response
