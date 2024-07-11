from datetime import datetime


def check_date(date: str) -> str:
    try:
        date = date.replace(".", " ").strip().split()
        if (len(date[0]) == 4 and 2 <= len(date[1]) + len(date[-1]) <= 4
                and 0 < int(date[1]) < 13 and 0 < int(date[-1]) < 32):
            return '.'.join(date[::-1])
        elif (len(date[-1]) == 4 and 2 <= len(date[1]) + len(date[0]) <= 4
              and 0 < int(date[1]) < 13 and 0 < int(date[0]) < 32):
            return '.'.join(date)
        else:
            # logger.warning(f"Error input time {'.'.join(date)}. Current time set")
            return datetime.now().strftime('%d.%m.%Y')
    except Exception as ex:
        return datetime.now().strftime('%d.%m.%Y')


def check_name(s: str):
    if s.count(".") == 2:
        s = s.replace(".", ". ").split()
        return s[0], s[1]
    if len(s.split()) == 2:
        return s.split()[0], s.split()[1]
    else:
        return s, ""
