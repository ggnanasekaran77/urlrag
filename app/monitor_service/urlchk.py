"""
Process CSV file get the HTTP response code and insert them into influxdb
"""
import concurrent.futures
import io
import multiprocessing
from collections import OrderedDict
from csv import DictReader
from datetime import datetime
from multiprocessing import Value
from urllib.request import urlopen
import requests

import rx
from rx import operators as ops

from influxdb_client import Point, InfluxDBClient, WriteOptions, WritePrecision
from influxdb_client.client.write_api import WriteType


class ProgressTextIOWrapper(io.TextIOWrapper):
    """
    TextIOWrapper that store progress of read.
    """
    def __init__(self, *args, **kwargs):
        io.TextIOWrapper.__init__(self, *args, **kwargs)
        self.progress = None
        pass

    def readline(self, *args, **kwarg) -> str:
        readline = super().readline(*args, **kwarg)
        self.progress.value += len(readline)
        return readline


class InfluxDBWriter(multiprocessing.Process):
    """
    Writer that writes data in batches with 50_000 items.
    """
    def __init__(self, queue):
        multiprocessing.Process.__init__(self)
        self.queue = queue
        self.client = InfluxDBClient.from_config_file("config.ini")
        self.write_api = self.client.write_api(
            write_options=WriteOptions(write_type=WriteType.batching, batch_size=5_000, flush_interval=1_000))

    def run(self):
        while True:
            next_task = self.queue.get()
            if next_task is None:
                # Poison pill means terminate
                self.terminate()
                self.queue.task_done()
                break
            self.write_api.write(bucket="monitor_service", record=next_task)
            self.queue.task_done()

    def terminate(self) -> None:
        proc_name = self.name
        print()
        print('Writer: flushing data...')
        self.write_api.close()
        self.client.close()
        print('Writer: closed'.format(proc_name))


def parse_row(row: OrderedDict):

    return Point("http_response_code") \
        .tag("monitor_type", "http_response_code") \
        .field("name", row['name']) \
        .field("url", row['url']) \
        .field("http_response_code", requests.head(row['url'], timeout=2, allow_redirects=True).status_code) \
        .time(datetime.utcnow(), WritePrecision.NS)


def parse_rows(rows, total_size):
    """
    Parse bunch of CSV rows into LineProtocol

    :param total_size: Total size of file
    :param rows: CSV rows
    :return: List of line protocols
    """
    _parsed_rows = list(map(parse_row, rows))

    counter_.value += len(_parsed_rows)
    if counter_.value % 1_000 == 0:
        print('{0:8}{1}'.format(counter_.value, ' - {0:.2f} %'
                                .format(100 * float(progress_.value) / float(int(total_size))) if total_size else ""))
        pass

    queue_.put(_parsed_rows)
    return None


def init_counter(counter, progress, queue):
    """
    Initialize shared counter for display progress
    """
    global counter_
    counter_ = counter
    global progress_
    progress_ = progress
    global queue_
    queue_ = queue


def process_urls():
    """
    Create multiprocess shared environment
    """
    queue_ = multiprocessing.Manager().Queue()
    counter_ = Value('i', 0)
    progress_ = Value('i', 0)
    startTime = datetime.now()

    url = "file://urls.csv"

    """
    Open URL and for stream data 
    """
    response = urlopen(url)
    if response.headers:
        content_length = response.headers['Content-length']
    io_wrapper = ProgressTextIOWrapper(response)
    io_wrapper.progress = progress_

    """
    Start writer as a new process
    """
    writer = InfluxDBWriter(queue_)
    writer.start()

    """
    Create process pool for parallel encoding into LineProtocol
    """
    cpu_count = multiprocessing.cpu_count()
    with concurrent.futures.ProcessPoolExecutor(cpu_count, initializer=init_counter,
                                                initargs=(counter_, progress_, queue_)) as executor:
        """
        Converts incoming HTTP stream into sequence of LineProtocol
        """
        data = rx \
            .from_iterable(DictReader(io_wrapper)) \
            .pipe(ops.buffer_with_count(1_000),
                  # Parse 1_000 rows into LineProtocol on subprocess
                  ops.flat_map(lambda rows: executor.submit(parse_rows, rows, content_length)))

        """
        Write data into InfluxDB
        """
        data.subscribe(on_next=lambda x: None, on_error=lambda ex: print(f'Unexpected error: {ex}'))

    """
    Terminate Writer
    """
    queue_.put(None)
    queue_.join()

    print()
    print(f'Import finished in: {datetime.now() - startTime}')
    print()


def main():
    process_urls()