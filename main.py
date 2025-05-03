import string
import re

# Removes non-printable characters, including backspace
def clean_input(text):
    cleaned_text = ''.join(ch for ch in text if ch in string.printable and ch != '\x7f')
    cleaned_text = re.sub(r'\s*(AM|PM)\s*$', r' \1', cleaned_text.strip(), flags=re.IGNORECASE)
    cleaned_text = re.sub(r' 1$', '', cleaned_text)
    
    return cleaned_text.strip()

# Main Function
def add_time(start, duration, day = ''):
    # Destructuring start time
    cleaned_start = clean_input(start)

    match = re.fullmatch(r'(\d{1,2})(?::(\d{2}))?\s*([AaPp][Mm])$', cleaned_start)
    if not match:
        raise ValueError("Invalid start time format. Use 'H:MM AM/PM' or 'H AM/PM'.")

    start_hour = int(match.group(1))
    start_min = int(match.group(2)) if match.group(2) else 0
    am_pm = match.group(3).upper()

    # Convert start time to 24-hour format for easier calculation
    if am_pm == 'PM' and start_hour != 12:
        start_hour += 12
    if am_pm == 'AM' and start_hour == 12:
        start_hour = 0

    # Destructuring duration
    duration_parts = duration.split(':')
    if len(duration_parts) == 2:
        duration_hour, duration_min = map(int, duration_parts)
    elif len(duration_parts) == 1:
        duration_hour = int(duration_parts[0])
        duration_min = 0
    else:
        raise ValueError("Invalid duration format. Use 'H' or 'H:MM'.")

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

    # Evaluate day of week
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

# Prompt user function
def prompt_user():
    valid_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    while True:
        try:
            start = clean_input(input("Enter the start time (e.g., '11:59 PM'): "))
            duration = clean_input(input("Enter the duration time (e.g., '24:05'): "))
            day = clean_input(input("Enter the day of the week (optional, e.g., 'Monday'): "))

            if day:
                normalized_day = day.capitalize()
                if normalized_day not in valid_days:
                    print(f"Error: '{day}' is not a valid day of the week.")
                    continue
                print(f"\nDay of week entered. Result:\n{add_time(start, duration, normalized_day)}")
            else:
                print(f"\nResult:\n{add_time(start, duration)}")

        except ValueError as ve:
            print(f"Error: {ve}")

        again = input("\nWould you like to try again? (y/n): ").strip().lower()
        if again != 'y':
            print("Goodbye!")
            break

if __name__ == "__main__":
    prompt_user()
