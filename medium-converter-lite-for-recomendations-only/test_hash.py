import hashlib
string = hashlib.sha224(
    b"https://docs.python.org/3.4/library/hashlib.html").hexdigest()
print(string)
