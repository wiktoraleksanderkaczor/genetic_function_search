from hashlib import md5


def hash_hamming_distance(str1, str2):
    str1 = md5(str1.encode()).hexdigest()
    str2 = md5(str2.encode()).hexdigest()
    return sum(c1 != c2 for c1, c2 in zip(str1, str2))
