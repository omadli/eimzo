import re
import logging
import subprocess
from datetime import datetime
from django.conf import settings

class InvalidPassword(Exception):
    pass

class InvalidKey(Exception):
    pass


LIST_BYTES = [
    (b"\x18", bytes("ʻ".encode("utf-8"))),
    (b"\xbc", bytes("'".encode("utf-8")))
    
]

def replace_all_bytes(b: bytes) -> str:
    for i, j in LIST_BYTES:
        b = b.replace(i, j)
    return b


def check_pfx_file(filename, password=settings.DEFAULT_PASSWORD):
    COMMAND = ["openssl", "pkcs12", "-info", "-in", f"{filename}", "-passin", f"pass:{password}"]  # noqa: E501

    result = subprocess.Popen(COMMAND, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    stderr_binary = result.stderr.read()
    logging.debug(stderr_binary)
    
    if b"invalid password" in stderr_binary:
        raise InvalidPassword()
    
    result_binary = result.stdout.read()
    result_unicode = replace_all_bytes(result_binary).decode()
    logging.debug(result_binary)
    logging.debug(result_unicode)
    
    result1 = parse_args1(result_unicode)
    return result1

def decode_str(s: str) -> str:
    res = ""
    for letter in list(s):
        o = ord(letter)
        if 47 < o < 95:
            i = chr(o + 1024)
        else:
            i = letter
        res += i
    return res

def parse_date(date_str: str) -> datetime:
    # 2023.08.03 11:41:51
    return datetime.strptime(date_str, "%Y.%m.%d %H:%M:%S")

def parse_args1(res: str) -> dict:
    lines = res.split("\n")
    args_line = lines[1]
    result1 = {}
    args = args_line.replace("    friendlyName: ", "")
    if len(args) < 20:
        raise InvalidKey()
    args = args.split(",")
    for arg in args:
        key, value = arg.split("=", maxsplit=1)
        result1[key] = value
    
    result2 = {}
    result2["serialnumber"] = result1.pop("serialnumber")
    result2["full_name"] = decode_str(result1.pop('cn'))
    result2["name"] = decode_str(result1.pop('name'))
    result2["surname"] = decode_str(result1.pop('surname'))
    result2["jshshir"] = int(result1.pop("1.2.860.3.16.1.2"))
    result2["validfrom"] = parse_date(result1.pop("validfrom"))
    result2["validto"] = parse_date(result1.pop("validto"))
    result2["location"] = decode_str(result1.pop("l"))
    result2["city"] = decode_str(result1.pop("st"))
    result2["country"] = result1.pop("c")
    
    result2.update({
        "organization": None,
        "t": None,
        "ou": None,
        "uid": None,
        "businesscategory": None
    })
    
    if result1.get("o") is not None:
        result2["organization"] = decode_str(result1.pop("o"))
    if result1.get("t") is not None:
        result2["t"] = decode_str(result1.pop("t"))
    if result1.get("ou") is not None:
        result2["ou"] = decode_str(result1.pop("ou"))
    if result1.get("uid", None) is not None:
        result2["uid"] = int(result1.pop("uid"))
        
    if result1.get("businesscategory", None) is None:
        result2["stir"] = result2["uid"]
        result2["type"] = "jismoniy"
        
    else:
        result2["type"] = "yuridik"
        result2["stir"] = int(result1.pop("1.2.860.3.16.1.1"))
        
        result2["businesscategory"] = decode_str(result1.pop("businesscategory"))
        
    if len(result1.keys()):
        result2["other"] = result1
    return result2
    

def remove_all(s: str, chars: str) -> str:
    for ch in chars:
        s = s.replace(ch, "")
    return s
    
def check_pass(file_name: str):
    file_name = file_name.replace(".pfx", "")
    file_name = re.sub(r"DS[0-9]{9}000[0-9]", "", file_name, 1)
    file_name = re.sub(r"[A-Za-zА-Яа-я]+", "", file_name)
    file_name = re.sub(r"\([2-9]\)", "", file_name)
    file_name = remove_all(file_name, " -_().'")
    m = re.match(r"[0-9]{7,9}", file_name)
    if m:
        passwd = m.group(0)
        return passwd
    else:
        return None
    