'''
    File name: utilities.py
    Author: Simonas Laurinavicius
    Email: simonas.laurinavicius@mif.stud.vu.lt
    Python Version: 3.7.6

    Purpose: 
        Formats module defines various helper functions used by different modules
'''

# Local modules
import formats

def return_shorter_str(str1, str2):
    if len(str1) < len(str2):
        return str1
    elif len(str1) > len(str2):
        return str2
    else:
        return str1

# Reference: [https://stackoverflow.com/questions/12173774/how-to-modify-bits-in-an-integer]
def set_bit(byte, value, idx):
    mask = 1 << idx
    byte &= ~mask
    if value:
        byte |= mask
    return byte

def match(question, record):
    all_types = False

    if question.q_type == formats.Type['*']:    # If user wants all records with a certain name, type is not important
        all_types = True

    if question.q_name == record["name"] and (question.q_type == formats.Type[record["type"]] or all_types):
        return True
    else:
        return False

def check_for_name_error(answer_rr):
    name_err = False

    if len(answer_rr) == 0:
        name_err = True

    return name_err
    
def encode_domain_name(name):
    domain_parts = name.split('.')
    name = b''

    for domain in domain_parts:
        name += len(domain).to_bytes(1, byteorder="big")
        name += str.encode(domain)

    return name

def encode_record_addr(addr):
    addr_parts = addr.split('.')
    addr = b''

    for octet in addr_parts:
        addr += int(octet).to_bytes(1, byteorder="big")

    return addr

def record_to_bytes(record, class_):
    name = encode_domain_name(record["name"])
    type_ = formats.Type[record["type"]]
    class_ = formats.Class[class_]
    if record["type"] != "SOA":
        ttl = record["ttl"].to_bytes(4, byteorder="big")
    else:
        ttl = (0).to_bytes(4, byteorder="big") # SOA records are always distributed with zero TTL to prohibit caching
    r_data = get_rdata(record, class_)
    rd_length = len(r_data).to_bytes(2, byteorder="big")

    resource_record = formats.RR(name, type_, class_, ttl, rd_length, r_data)
    return resource_record

def get_soa_rdata(record):
    r_data = b''
    domain_entries = ["name_server", "maintainer"]
    time_fields = ["serial", "refresh", "retry", "expire", "minimum"]

    for entry in domain_entries:
        r_data += encode_domain_name(record[entry])
    for field in time_fields:
        r_data += record[field].to_bytes(4, byteorder="big")

    return r_data

def get_ns_rdata(record):
    r_data = encode_domain_name(record["host_name"])

    return r_data

def get_mx_rdata(record):
    r_data = record["preference"].to_bytes(2, byteorder="big")
    r_data += encode_domain_name(record["exchange"])

    return r_data

def get_a_rdata(record):
    r_data = encode_record_addr(record["address"])
    return r_data

def get_rdata(record, class_):
    r_data = b''

    if class_ == formats.Class["IN"]:
        if record["type"] == "SOA":
            r_data = get_soa_rdata(record)
        elif record["type"] == "NS":
            r_data = get_ns_rdata(record)
        elif record["type"] == "MX":
            r_data = get_mx_rdata(record)
        else:
            r_data = get_a_rdata(record)        # We set default to be type A RR
    
    return r_data
        