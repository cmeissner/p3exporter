"""Module that defines all needed classes and functions for example collector."""
import asyncio
import random
import time

from p3exporter.collector import CollectorBase, CollectorConfig
from p3exporter.cache import timed_lru_cache, async_cache
from prometheus_client.core import GaugeMetricFamily, InfoMetricFamily
from random import randint


class ExampleCollector(CollectorBase):
    """A sample collector.

    It does not really do much. It only runs a method and return the time it runs as a gauge metric.
    """

    def __init__(self, config: CollectorConfig):
        """Instanciate a MyCollector object."""
        super(ExampleCollector, self).__init__(config)

    def collect(self):
        """Collect the metrics."""
        runtime, result = _run_process()
        yield GaugeMetricFamily('example_process_cached_runtime', 'Time a process runs in seconds', value=runtime)
        yield InfoMetricFamily('example_process_cached_status', 'Status of example process', value={'status': result})
        runtime, result = _run_async_process()
        yield GaugeMetricFamily('example_process_async_cached_runtime', 'Time a process runs in seconds', value=runtime)
        yield InfoMetricFamily('example_process_async_cached_status', 'Status of example process', value={'status': result})


@timed_lru_cache(10)
def _run_process():
    """Sample function to ran a command for metrics."""
    timer = time.perf_counter()
    time.sleep(random.random())  # nosec
    runtime = time.perf_counter() - timer
    return runtime, "sucess"


@async_cache('example_funtion')
async def _run_async_process():
    """Sample funtion to run a command asynchornously for metrics."""
    timer = time.perf_counter()
    await asyncio.sleep(10)  # Simulate some work
    runtime = time.perf_counter() - timer
    value = randint(runtime, 100)
    return value
