'''
    File name: question.py
    Author: Simonas Laurinavicius
    Email: simonas.laurinavicius@mif.stud.vu.lt
    Python Version: 3.7.6

    Purpose: 
        Question modules defines various functions related to question section proccesing
'''

# Local modules
import formats
import utilities

# More on Question section formatting can be found in RFC 1035 Section 4.1.2. [https://tools.ietf.org/html/rfc1035]
def get_question(query):
    (q_name, start_idx) = get_q_name(query)   # start_idx denotes end of q_name part of the question, so we can read q_type and q_class afterwards
    q_type = query[start_idx:start_idx + 2]   # q_type takes 2 bytes
    q_class = query[start_idx + 2: start_idx + 4]   # q_class takes 2 bytes

    question = formats.Question(q_name, q_type, q_class)

    return question

def get_q_name(question):
    labels = []
    separator = '.'   # DNS uses '.' to seperate labels of Domain Name

    domain_length = question[0]   # question[0] gives length of the first domain
    start_idx = 1
    end_idx = domain_length + start_idx

    while domain_length > 0:
        # Add a label
        label = read_label(question, start_idx, end_idx)
        labels.append(label)

        # Renew indexes
        domain_length = question[end_idx]
        start_idx = end_idx + 1
        end_idx = domain_length + start_idx

    q_name = separator.join(labels)
    q_name += '.'   # Add root domain

    return (q_name, end_idx)


def read_label(query, start_idx, end_idx):
    label = ""

    for byte in query[start_idx:end_idx]:
        label += chr(byte)

    return label