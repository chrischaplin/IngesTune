import time
import sys
sys.path.append("../srcPostgres")

from db_classes import pyToPostgres


# Hard-coding some titles (belong in srcGridSearch)
table_name = 'producer_results_table'
config_name = '../../configs/db.config'


class Stats(object):

    def __init__(self, num_records):
        self.start = get_time_millis()
        self.window_start = get_time_millis()
        self.index = 0
        self.iteration = 0
        self.sampling = 1
        self.latencies = [0] * (int(num_records / self.sampling) + 1)
        self.max_latency = 0
        self.total_latency = 0
        self.window_count = 0
        self.window_max_latency = 0
        self.window_total_latency = 0
        self.window_bytes = 0
        self.count = 0
        self.bytes = 0

    def record(self, iter, latency, bytes, time):
        self.count += 1
        self.bytes += bytes
        self.total_latency += latency
        self.max_latency = max(self.max_latency, latency)
        self.window_count += 1
        self.window_bytes += bytes
        self.window_total_latency += latency
        self.window_max_latency = max(self.window_max_latency, latency)
        if iter % self.sampling == 0:
            self.latencies[self.index] = latency
            self.index += 1

    def next_completion(self, start, bytes, stats):
        cb = PerfCallback(self.iteration, start, bytes, stats).on_completion
        self.iteration += 1
        return cb


    def print_total(self,rec):
        elapsed = get_time_millis() - self.start
        recs_per_sec = 1000.0 * self.count / float(elapsed)
        mb_per_sec = 1000.0 * self.bytes / float(elapsed) / (1024.0 * 1024.0)
        percs = self.percentiles(
                self.latencies, self.index, [0.5, 0.95, 0.99, 0.999])


        # Add measurements to record
        rec['throughput'] = mb_per_sec
        rec['latency'] = percs[3]


        # Open database
        db={}
	dbWrapper = pyToPostgres(db)
	dbWrapper = dbWrapper.fromConfig(config_name)
	dbWrapper.openConnection()

        # Write record and close database
        dbWrapper.insertIntoTable(rec,table_name)
	dbWrapper.closeConnection()        



    @staticmethod
    def percentiles(latencies, count, percentiles):
        size = min(count, len(latencies))
        latencies = latencies[:size]
        latencies.sort()
        values = [1] * len(percentiles)
        for i in xrange(len(percentiles)):
            index = int(percentiles[i] * size)
            values[i] = latencies[index]

        return values



class PerfCallback(object):

    def __init__(self, iter, start, bytes, stats):
        self.start = start
        self.stats = stats
        self.iteration = iter
        self.bytes = bytes

    def on_completion(self, metadata):
        now = get_time_millis()
        latency = int(now - self.start)
        self.stats.record(self.iteration, latency, self.bytes, now)


def get_time_millis():
    return time.time() * 1000
