def isEmpty(value):
    if value == "":
        return True
    else:
        return False

def isNegative(value):
    if value  == "-" or float(value) < 0:
        return True
    else:
        return False
    