import "math"

maxDataPoints = 100

from(bucket: "Frigo1")
|>range(start: v.timeRangeStart, stop: v.timeRangeStop)
|>filter(fn: (r) => r._measurement == "ens")
|>filter(fn: (r) => r._field == "temp1")
|>aggregateWindow(fn: mean, every: duration(v: (int(v: v.timeRangeStop) - int(v: v.timeRangeStart))/maxDataPoints))