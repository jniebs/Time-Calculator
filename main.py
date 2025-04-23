def add_time(start, duration, day = ''):
    #Desctructuring Time
    start_temp = start.split()
    time_temp, am_pm = start_temp
    start_hour, start_min = map(int, time_temp.split(':'))

    # Convert start time to 24-hour format for easier calculation
    if am_pm == 'PM' and start_hour != 12:
        start_hour += 12
    if am_pm == 'AM' and start_hour == 12:
        start_hour = 0

    #Desctructuring Duration
    duration_temp = map(int, duration.split(':'))
    duration_hour, duration_min = duration_temp

    # Add time
    total_min = start_min + duration_min
    extra_hour = total_min // 60
    new_min = total_min % 60

    total_hour = start_hour + duration_hour + extra_hour
    add_days = total_hour // 24
    final_hour_24 = total_hour % 24

    # Convert back to 12-hour format
    if final_hour_24 == 0:
        display_hour = 12
        am_pm = 'AM'
    elif final_hour_24 < 12:
        display_hour = final_hour_24
        am_pm = 'AM'
    elif final_hour_24 == 12:
        display_hour = 12
        am_pm = 'PM'
    else:
        display_hour = final_hour_24 - 12
        am_pm = 'PM'

    # Format minutes
    display_min = f'{new_min:02}'

    #Evaluate Day of Week
    if day:
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        day_index = (days.index(day.capitalize()) + add_days) % 7
        new_day = days[day_index]
    else:
        new_day = ''

    # Compose final result
    new_time = f'{display_hour}:{display_min} {am_pm}'
    if new_day:
        new_time += f', {new_day}'

    if add_days == 1:
        new_time += ' (next day)'
    elif add_days > 1:
        new_time += f' ({add_days} days later)'

    return new_time


print(add_time('11:59 PM', '24:05'))