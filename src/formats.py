'''
    File name: formats.py
    Author: Simonas Laurinavicius
    Email: simonas.laurinavicius@mif.stud.vu.lt
    Python Version: 3.7.6

    Purpose: 
        Formats module defines DNS communication formats.
'''

# Standard library
from dataclasses import dataclass, astuple
from typing import List

# Local modules
import utilities 


# Mapping types to byte values, more on type values can be found in RFC 1035 Section 3.2.2. and 3.2.3. [https://tools.ietf.org/html/rfc1035]
Type = {
    'A': b"\x00\x01",
    "NS": b"\x00\x02",
    "SOA": b"\x00\x06",
    "MX": b"\x00\x0F",
    '*': b"\x00\xFF"
}

# Mapping class to byte values, more on class values can be found in RFC 1035 Section 3.2.4. [https://tools.ietf.org/html/rfc1035]
Class = {
    "IN": b"\x00\x01",
    "CH": b"\x00\x03",
    "HS": b"\x00\x04"
}

# Header Format is defined in RFC 1035 Section 4.1.1. [https://tools.ietf.org/html/rfc1035]
@dataclass
class Header:
    id_: bytes
    flags: bytes
    qd_count: bytes
    an_count: bytes
    ns_count: bytes
    ar_count: bytes

    def __bytes__(self):
        return dataclass_to_bytes(self)

# Question Format is defined in RFC 1035 Section 4.1.2. [https://tools.ietf.org/html/rfc1035]
@dataclass
class Question:
    q_name: str
    q_type: bytes
    q_class: bytes

    def __bytes__(self):
        bytes_ = utilities.encode_domain_name(self.q_name)
        bytes_ += (self.q_type + self.q_class)

        return bytes_
# RR Format is defined in RFC 1035 Section 4.1.3. [https://tools.ietf.org/html/rfc1035]
@dataclass
class RR:
    name: bytes
    type_: bytes
    class_: bytes
    ttl: bytes
    rd_length: bytes
    r_data: bytes

    def __bytes__(self):
        return dataclass_to_bytes(self)

# Message Format is defined in RFC 1035 Section 4.1. [https://tools.ietf.org/html/rfc1035]
@dataclass
class Message:
    header: Header
    question: Question
    answer_rr: List[RR]
    authority_rr: List[RR]
    additional_rr: List[RR]

    def __bytes__(self):
        bytes_ = self.header.__bytes__()
        bytes_ += self.question.__bytes__()
        bytes_ += Message.rr_list_to_bytes(self.answer_rr)
        bytes_ += Message.rr_list_to_bytes(self.authority_rr)
        bytes_ += Message.rr_list_to_bytes(self.additional_rr)

        return bytes_

    @staticmethod
    def rr_list_to_bytes(rr_list):
        bytes_ = b''
        for rr in rr_list:
            bytes_ += rr.__bytes__()
        return bytes_


def dataclass_to_bytes(dataclass_):
    bytes_ = b''
    for field in astuple(dataclass_):
        bytes_ += field
    return bytes_

