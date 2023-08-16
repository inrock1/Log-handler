def read_log_file(filename):
    with open(filename, "r") as log_file:
        for line in log_file:
            yield line


def get_name_error(s_p_1: str, s_p_2: str):
    step1 = s_p_1[:-1] + s_p_2
    step2 = [
        bin(int(step1[0:2]))[2:].zfill(8),
        bin(int(step1[2:4]))[2:].zfill(8),
        bin(int(step1[4:6]))[2:].zfill(8),
    ]
    step3 = [int(step2[0][4]), int(step2[1][4]), int(step2[2][4])]

    if step3[0] == 1:
        return f"{step3} Battery device error"
    elif step3[1] == 1:
        return f"{step3} Temperature device error"
    elif step3[2] == 1:
        return f"{step3} Threshold central error"
    return f"{step3} Unknown device error"


def print_results(sensor_success_count, total_success_count, total_fail_count, errors):
    print("All big messages:", total_success_count + total_fail_count)
    print("Successful big messages:", total_success_count)
    print("Failed big messages:", total_fail_count)
    print()

    for sensor_id, error in errors.items():
        print(f"{sensor_id}: {error}")
    print()

    print(f"Success messages count:")
    for sensor_id, success_count in sensor_success_count.items():
        print(f"{sensor_id}: {success_count}")


def calculate_results(log_file_path):
    sensor_success_count = {}
    sensor_fail = set()
    errors = {}

    for line in read_log_file(log_file_path):
        if "BIG" in line:
            log_string = line.strip().split("'")[1]
            parts = log_string.split(";")
            sensor_id = parts[2]
            s_p_1 = parts[6]
            s_p_2 = parts[13]
            state = parts[-2]

            if state == "02" and sensor_id not in sensor_fail:
                count = sensor_success_count.get(sensor_id, 0)
                count += 1
                sensor_success_count[sensor_id] = count

            elif state == "DD":
                sensor_fail.add(sensor_id)
                sensor_success_count.pop(sensor_id, None)
                errors[sensor_id] = get_name_error(s_p_1, s_p_2)

            elif state != "DD" and state != "02":
                print("Unknown state")

    total_success_count = len(sensor_success_count)
    total_fail_count = len(sensor_fail)
    print_results(sensor_success_count, total_success_count, total_fail_count, errors)


calculate_results("app_2.log")


"""
Примітка. 
по ТЗ не зрозуміло як трактувати коли у бітових флажках присутня більш ніж одна "1".
[1, 1, 1] - це 3 помилки одночасно, чи тут потрібно сумувати їх і це помилка №3?
Тому при присвоєнні назви помилки зроблено припущення, 
що в списку помилок для відображення номер помилки - 
це порядковий номер масиву помилок, і виводиться перша знайдена помилка.
"""

