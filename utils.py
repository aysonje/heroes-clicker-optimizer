def hum2int(s):
    mapper = {
        'K': 3,
        'M': 6,
        'B': 9,
        'T': 12,
        'q': 15,
        'Q': 18,
        's': 21,
        'S': 24,
        'O': 27,
        'N': 30,
    }
    for key, exp in mapper.iteritems():
        if s.endswith(key):
            multiplier = 10**exp
            digits = s[:-1]
            break
    else:
        multiplier = 1
        digits = s
    parts = digits.split('.')
    if len(parts) == 1:
        return int(digits) * multiplier
    else:
        whole = parts[0]
        decimal = parts[1]
        decimal = decimal + '0'*(3-len(decimal))
        return int(whole) * multiplier + int(decimal) * multiplier/1000
