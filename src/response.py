'''
    File name: response.py
    Author: Simonas Laurinavicius
    Email: simonas.laurinavicius@mif.stud.vu.lt
    Python Version: 3.7.6

    Purpose: 
        Response module defines various functions related to response proccesing
'''

# Local modules
import zone
import question
import formats
import utilities

# Server Response Algorithm is described in RFC 1034 Section 4.3.2. [https://tools.ietf.org/html/rfc1034]
def build_response(query):

    question_ = question.get_question(query[12:]) 
    (records, class_) = zone.search_zones(question_)

    print("Question: ", question_.__bytes__())

    answer_rr = []
    authority_rr = []
    additional_rr = []

    for record in records:
        encoded_record = utilities.record_to_bytes(record, class_)
        answer_rr.append(encoded_record)

    name_err = utilities.check_for_name_error(answer_rr)
    an_count = len(answer_rr).to_bytes(2, byteorder="big")

    response_header = build_response_header(query[:12], an_count, name_err)

    response = formats.Message(response_header, question_, 
                        answer_rr, authority_rr, 
                        additional_rr).__bytes__() 

    print("Response: ", response)  
    
    return response

def build_response_header(query_header, an_count, name_err):

    response_id = query_header[:2]

    response_qd_count = b"\x00\x01" # We stick to 1 Question per Query [https://stackoverflow.com/questions/32031349/what-does-qd-stand-for-in-dns-rfc1035]
    response_an_count = an_count
    response_ns_count = b"\x00\x00"
    response_ar_count = b"\x00\x00"

    response_flags = build_response_flags(query_header[2:4], name_err)

    response_header = formats.Header(response_id, response_flags, 
                        response_qd_count, response_an_count, 
                        response_ns_count, response_ar_count)

    return response_header

# More on Response Flags can be found in RFC 1035 Section 4.1.1. [https://tools.ietf.org/html/rfc1035]
def build_response_flags(query, name_err):

    response_byte_1 = 0b0
    query_byte_1 = int.from_bytes(query[:1], byteorder="big") 

    response_byte_1 = utilities.set_bit(response_byte_1, 1, 7)   # Set Response QR to 1

    opcode_mask = 0b01111000
    query_opcode = opcode_mask & query_byte_1   # Read Query OPCODE

    response_byte_1 |= query_opcode   # Set Response OPCODE

    response_byte_1 = utilities.set_bit(response_byte_1, 1, 2)   # Set Response AA to 1

    response_byte_1 = utilities.set_bit(response_byte_1, 0, 1)  # Set Response TC to 0

    rd_mask = 0b00000001
    request_rd = rd_mask & query_byte_1   # Read Query RD

    response_byte_1 |= request_rd   # Set Response RD

    response_byte_2 = 0b0   # Set Response RA, Z, RCODE to 0

    # If we have a Name Error, set RCODE to 3, more on Errors can be found in RFC 1035 Section 4.1 [https://tools.ietf.org/html/rfc1034]
    if name_err:
        response_byte_2 += 0b00000011

    response_flags = response_byte_1.to_bytes(1, byteorder="big") + response_byte_2.to_bytes(1, byteorder="big")

    return response_flags