import sys
import re
import json
from operator import itemgetter
import helpers

def format_json(data):
    """Converts data into json format.

    Takes a list of user data information and converts into
    JSON format with an errors list and an entries list.

    Args:
        data: a list of either succesfully parsed dictionaries or 'error' 
        strings.

    Returns:
        A dict mapping keys to the corresponding table row data
        fetched. Each row is represented as a tuple of strings. For
        example:

        {
          entries[{'first': 'josh', 'last': 'newman', 'color': 'red', 
                  'zip': 01234'}],
         'errors: [1, 4, 5]'
        }

    Raises:
        IOError: An error occurred accessing the bigtable.Table object.
    """

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

def sort_json(json_data, keys_to_sort_by):
    """Sorts entries data by specified keys.

    Takes a JSON object of data and sorts the entries by specified keys.

    Args:
        json_data: a JSON object containing a list of error line numbers and a 
        list of successfully parsed user data
        keys_to_sort_by: a list of keys to sort by

    Returns:
        The original JSON object with its entries in sorted order

    Raises:
        IOError: An error occurred accessing the bigtable.Table object.
    """

    json_data['entries'] = sorted(json_data['entries'], key=itemgetter('last', 
                                                                       'first'))
    return json_data

def format_user_data(user_data):
    """Formats user data.

    Takes a dictionary of user data and changes format of phone number.

    Args:
        user_data: a dictionary of user data 

    Returns:
        The user data with phone number in format: 111-222-33333
    """

    SEPERATOR = '-'
    phone = user_data['phone']
    #Phone number should be in format 999-999-9999
    user_data['phone'] = SEPERATOR.join([phone[i:i+3] 
                       for i in range(0, len(phone)-1, 3)]) + phone[-1]


def parse_names(user_data, names):
    """Attaches first and last name to user data dictionary.

    Takes a user data dictionary and names list. Attaches these fields to
    the user data dictionary.

    Args:
        user_data: a dictionary of user data
        names: a list containing user's first and last name

    Returns:
        The user data dictonary extended with the first and last name
    """
    user_data['first'] = names[0]
    user_data['last'] = names[1]
    return user_data


def parse_info(user_data, info):
    """Sorts entries data by specified keys.

    Takes a JSON object of data and sorts the entries by specified keys.

    Args:
        json_data: a JSON object containing a list of error line numbers and a 
        list of successfully parsed user data
        keys_to_sort_by: a list of keys to sort by

    Returns:
        The original JSON object with its entries in sorted order

    Raises:
        IOError: An error occurred accessing the bigtable.Table object.
    """
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
    """Checks if user information is in first name, last name order.

    Takes a list of user information and returns a Boolean based on ordering.
    Last, First ordering is present if the last item in the list is a zip 
    code.

    Args:
        user_info: a list of user data.

    Returns:
        A Boolean that is True if data is in first name, last name order.
    """
    #(Last, First) order if last entry field is zip code
    if (re.match(r'^\d{5}$', user_info[-1])):
        return False
    return True


def parse_user_data(user_info, user_data={}, NUM_NAME_FIELDS=2):
    """Handles parsing of user name data and (zip, phone, color) data.

      Takes a list of user information extends an empty user data dictionary
      with first name, last name, zip code, phone number, color data.

      Args:
          user_info: a list of user data.
          user_data: an empty dictionary of user data
          NUM_NAME_FIELDS: a constant specifying how many name fields there are
          (3 would denote a middle name field as well)

      Returns:
          An extended user data dictionary with the data in user_info.
      """
    #Can easily extend if data will later include a middle-name
    names = user_info[0:NUM_NAME_FIELDS]
    info = user_info[NUM_NAME_FIELDS:]

    parse_names(user_data, names)
    parse_info(user_data, info)
    return user_data


def standardize_names(entry):
    """Checks if user information is in first name, last name order.

    Takes a list of user information and returns a Boolean based on ordering.
    Last, First ordering is present if the last item in the list is a zip 
    code.

    Args:
        user_info: a list of user data.

    Returns:
        A Boolean that is True if data is in first name, last name order.
    """
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
    """Standarizes the multiple possible entry formats into unified format.

    Takes an list of user data and standardizes the format by removing
    removing characters, splitting text into a list and standarizign names 
    format.

    Args:
        entry: a list of user data.
        NUM_FIELDS: a constant specifying how many data fields an entry should
        have.

    Returns:
        A list of standarized user information. For example:

        ['Josh', 'Newman', 'blue', '08321', '1112223333']
    """

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
      helpers.swap(0, 1, entry)
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
    helpers.output_json(user_json, output_filename)

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
