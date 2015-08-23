import sys
import re
import json
from operator import itemgetter

def format_json(data):
    entries = []
    errors = []
    for idx, entry in enumerate(data):
        if(entry == 'error'):
            #Input lines are one, not zero indexed
            errors.append(idx + 1)
        else:
            entries.append(entry)

    return {
        'entries': entries,
        'errors': errors
    }

def sort_json(json_data):
    json_data['entries'] = sorted(json_data['entries'], key=itemgetter('last', 
                                                                       'first'))
    return json_data

def format_user_data(user_data):
    SEPERATOR = '-'
    phone = user_data['phone']
    #Phone number should be in format 999-999-9999
    user_data['phone'] = SEPERATOR.join([phone[i:i+3] 
                       for i in range(0, len(phone)-1, 3)]) + phone[-1]


def output_results(json_data, file_name):
    with open(file_name, "w") as outfile:
        json.dump(json_data, outfile, indent=2)


def parse_names(user_data, names):
    user_data['first'] = names[0]
    user_data['last'] = names[1]
    return user_data


def parse_info(user_data, info):
    regexes = {
        'phone': r'^\d{10}$',
        'zip': r'^\d{5}$',
        'color': r'[a-zA-Z]+'
    }

    #Test all regexes against all fields
    for entry in info:
        for key, regex in regexes.iteritems():
            match = re.match(regex, entry)
            if match:
                user_data[key] = match.group()

    if (all(x in user_data for x in ['phone', 'zip', 'color'])):
        return user_data
    else:
      raise Exception('Invalid Entry')


def in_first_last_name_order(user_info):
    #(Last, First) order if last entry field is zip code
    if (re.match(r'^\d{5}$', user_info[-1])):
        return False
    return True


def parse_user_data(user_info, user_data={}, NUM_NAME_FIELDS=2):
    #Can easily extend if data will later include a middle-name
    names = user_info[0:NUM_NAME_FIELDS]
    info = user_info[NUM_NAME_FIELDS:]

    parse_names(user_data, names)
    parse_info(user_data, info)
    return user_data


def swap(i, j, arr):
    temp = arr[i]
    arr[i] = arr[j]
    arr[j] = temp

def standardize_names(entry):
    output = []
    names = entry[0]
    #Split by occurences of UpperCase to LowerCase
    names = [piece for piece in re.split(r'([A-Z][a-z]+)', names) if piece]
    #Handling for names with capitals e.g. McGreggor
    if (len(names) > 2):
      return names[0:2] + names[2:3] + entry[1:]
    else:
      entry = names[0:1] + names[1:2] + entry[1:]

    return entry


def standardize_entry(entry, NUM_FIELDS=5):
    SPECIAL_CHARS = '()-\n '
    #Removes chars from phone numbers and names
    entry = entry.translate(None, SPECIAL_CHARS)
    entry = entry.split(',')
    #Firstname, Lastname weren't comma seperated
    if(len(entry) < NUM_FIELDS):
        entry = standardize_names(entry)

    #Check if format is in (First, Last) order
    name_flag = in_first_last_name_order(entry)
    print(name_flag)
    if (name_flag == False):
      print(entry, name_flag)
      swap(0, 1, entry)
    return entry


def main(input_filename, output_filename):
    NUM_FIELDS = 5
    NUM_NAME_FIELDS = 2

    target_file = open(input_filename, 'r')
    data = []

    for line in target_file:
        try:
            user_information = {}
            line = standardize_entry(line, NUM_FIELDS)
            parse_user_data(line, user_information, NUM_NAME_FIELDS)
            format_user_data(user_information)
            data.append(user_information)
        except:
            data.append('error')

    user_json = format_json(data)
    user_json = sort_json(user_json)
    output_results(user_json, output_filename)

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
