def seconds_to_duration(seconds):
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return '%d:%02d:%02d' % (hours, minutes, seconds)


def miles_to_kilometers(miles):
    return miles / 0.621371


def kilometers_to_miles(km):
    return km * 0.621371


def next_highest_in_list(number_list, target):
    number_list.sort()
    for number in number_list:
        if number >= target:
            return number
    return number_list[-1]


def next_lowest_in_list(number_list, target):
    number_list.sort(reverse=True)
    for number in number_list:
        if number <= target:
            return number
    return number_list[-1]
