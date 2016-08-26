Age Graded Performance
======================

This calculates age-graded performance for running races. Age-graded
performance levels the playing field when calculating finish times for races.
For more information see the
[USATF Masters Article](http://www.usatfmasters.org/fa_agegrading.htm).

This project was developed as part of a race results project for my local
running club, the [Dolphin South End Runners](http://www.dserunners.com), San
Francisco's oldest running club.

## Installation

```
> ./setup.py install
```

## Usage:

### Command Line:

```
> agegrader age gender distance_in_km finish_time_in_seconds

> agegrader 15 m 5 1234
> Age Graded Performance: 65.4% 20:51, 6:23/mile
```

### As a Module:

```
from agegrader import AgeGrader

age_grader = AgeGrader()

age_grader.age_graded_performance_factor(age, gender, distance, seconds)
=> the age graded performance factor as a decimal (.83 = 83%)

age_grader.age_graded_finish_time(age, gender, distance, seconds)
=> the age graded finish time in seconds

age_grader.age_graded_seconds_per_mile(age, gender, distance, seconds)
=> the age graded pace in seconds per mile

age_grader.age_gender_distance_record(age, gender, distance)
=> returns the adjusted record for the given age, gender, and distance

age_grader.gender_distance_record(gender, distance)
=> this is the "world record" for the distance
=> returns the adjusted record for the given gender and distance
```

### Advanced Usage:

#### Custom data file:

```
with open('path/to/custom_data.json') as dat:
    a = AgeGrader(dat)
    a.age_graded_performance_factor(age, gender, distance, seconds)
```

### Calculation Notes

This uses an estimation method to adjust for missing data points. For
example, there is no data for 4.5-mile distances. There are 4 and 5-mile
tables, though, and we use them to estimate the world record for the given
distance.
