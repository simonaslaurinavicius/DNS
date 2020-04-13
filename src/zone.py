'''
    File name: zone.py
    Author: Simonas Laurinavicius
    Email: simonas.laurinavicius@mif.stud.vu.lt
    Python Version: 3.7.6

    Purpose: 
        Zone module defines various functions related to zone loading and searching 
'''

# Standard library
import glob
import json

# Local modules
import utilities

def load_zones():
    zones = []
    zone_files = glob.glob("../zones/*.json")

    for zone_file in zone_files:
        zone = json.load(open(zone_file))
        zones.append(zone)

    return zones

# More on zone files can be found in RFC 1035 Section 5. [https://tools.ietf.org/html/rfc1035]
def search_zones(question):

    most_matched = 0
    matched = 0
    nearest = None

    zones = load_zones()

    for zone in zones:
        matched = find_nearest_ancestor(question.q_name, zone)

        if matched > most_matched:
            nearest = zone
            most_matched = matched

    (records, class_) = search_zone(question, nearest)
    return (records, class_)

def search_zone(question, zone):
    origin = zone["origin"]
    class_ = zone["class"]
    records = []

    for record in zone["RR"]:
        # Replace @ symbol in record
        if record["name"] == '@': 
            record["name"] = origin

        if utilities.match(question, record):
            records.append(record)

    return (records, class_)

def find_nearest_ancestor(q_name, zone):
    matched = 0
    origin = zone["origin"]
    length = len(utilities.return_shorter_str(q_name, origin))

    # Reverse Strings as TLD are at the end of the strings
    q_name = q_name[::-1]
    origin = origin[::-1]

    for i in range(length):
        if q_name[i] == origin[i]:
            matched += 1

    return matched