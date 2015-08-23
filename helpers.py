def swap(i, j, arr):
    temp = arr[i]
    arr[i] = arr[j]
    arr[j] = temp


def output_json(json_data, file_name):
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

    with open(file_name, "w") as outfile:
        json.dump(json_data, outfile, indent=2)