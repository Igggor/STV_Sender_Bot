def check_name(s: str):
    if s.count(".") == 2:
        s = s.replace(".", ". ").split()
        return s[0], s[1]
    if len(s.split()) == 2:
        return s.split()[0], s.split()[1]
    else:
        return s, ""