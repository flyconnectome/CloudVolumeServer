import os

# Keyword arguments for initializing cloudvolume.CloudVolume
CloudVolumeKwargs = dict(
                         cloudpath="",
                         parallel=True,
                         cache=True,
                         fill_missing=True,
                         progress=False
                       )

# Number of cores used to parallel fetching of locations
MaxWorkers = os.cpu_count() - 5

# Max number of locations per query
MaxLocations = 10e3
