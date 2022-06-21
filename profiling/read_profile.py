import pstats
from pstats import SortKey
p = pstats.Stats('./profiling/profile.stat')
p.strip_dirs().sort_stats(SortKey.TIME).print_stats('models')
p.strip_dirs().sort_stats(SortKey.TIME).print_stats('helpers')
p.strip_dirs().sort_stats(SortKey.TIME).print_stats('main')