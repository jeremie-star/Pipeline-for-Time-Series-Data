# Task 2 - MongoDB query results

Collection `energy_ts.readings` (19,735 documents)

## Q1. Latest record
```js
db.readings.find().sort({timestamp:-1}).limit(1)
```
Result: `{'reading_id': 19735, 'timestamp': datetime.datetime(2016, 5, 27, 18, 0), 'appliances_wh': 430, 'lights_wh': 10, 'weather': {'t_out': 22.2, 'press_mm_hg': 755.2, 'rh_out': 57.0, 'windspeed': 4.0, 'visibility': 27.0, 'tdewpoint': 13.2}}`

## Q2. Records in a date range (2016-01-11)
```js
db.readings.find({timestamp:{$gte:ISODate('2016-01-11'),$lt:ISODate('2016-01-12')}})
```
Matched 42 readings. First 3: `[{'timestamp': datetime.datetime(2016, 1, 11, 23, 50), 'appliances_wh': 40}, {'timestamp': datetime.datetime(2016, 1, 11, 23, 40), 'appliances_wh': 60}, {'timestamp': datetime.datetime(2016, 1, 11, 23, 30), 'appliances_wh': 70}]`

## Q3. Average appliance usage by hour of day (aggregation)
```js
db.readings.aggregate([{$group:{_id:{$hour:'$timestamp'},avg:{$avg:'$appliances_wh'}}},{$sort:{_id:1}}])
```
| hour | avg_appliances_wh |
|---:|---:|
| 0 | 52.8 |
| 1 | 51.3 |
| 2 | 49.1 |
| 3 | 48.2 |
| 4 | 49.4 |
| 5 | 52.7 |
| 6 | 57.7 |
| 7 | 78.6 |
| 8 | 106.1 |
| 9 | 112.8 |
| 10 | 125.4 |
| 11 | 133.1 |
| 12 | 123.6 |
| 13 | 124.7 |
| 14 | 108.3 |
| 15 | 105.8 |
| 16 | 119.9 |
| 17 | 161.4 |
| 18 | 190.4 |
| 19 | 143.1 |
| 20 | 127.0 |
| 21 | 96.5 |
| 22 | 69.1 |
| 23 | 57.0 |

## Q4. High-usage events (> 600 Wh)
```js
db.readings.find({appliances_wh:{$gt:600}}).sort({appliances_wh:-1}).limit(5)
```
Top 5: `[{'timestamp': datetime.datetime(2016, 1, 16, 18, 50), 'appliances_wh': 1080}, {'timestamp': datetime.datetime(2016, 1, 21, 18, 50), 'appliances_wh': 1070}, {'timestamp': datetime.datetime(2016, 1, 14, 17, 0), 'appliances_wh': 910}, {'timestamp': datetime.datetime(2016, 4, 4, 15, 40), 'appliances_wh': 900}, {'timestamp': datetime.datetime(2016, 1, 21, 19, 0), 'appliances_wh': 890}]`
