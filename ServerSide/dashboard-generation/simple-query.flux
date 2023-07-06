
maxDataPoints = 100

from(bucket: "ensParis")
|>range(start: v.timeRangeStart, stop: v.timeRangeStop)
|>filter(fn: (r) => r._field == "P")
|>aggregateWindow(fn: mean, every: duration(v: (int(v: v.timeRangeStop) - int(v: v.timeRangeStart))/maxDataPoints))