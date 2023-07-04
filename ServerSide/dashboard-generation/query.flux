import "math"

calculateWindowFactor = (timeStart, timeStop) => math.exp(x: -1./float(v: uint(v: duration(v: uint(v: timeStart) - uint(v: timeStop)))))

from(bucket: "Frigo1")
|>range(start: v.timeRangeStart, stop: v.timeRangeStop)
|>filter(fn: (r) => r._measurement == "ens")
|>filter(fn: (r) => r._field == "temp1")
|>aggregateWindow(fn: mean, every: duration(v: uint(v: float(v: float(v: uint(v: 1d)))*calculateWindowFactor(timeStart: v.timeRangeStart, timeStop: v.timeRangeStop))))