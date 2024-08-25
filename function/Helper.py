import io
import time
import random


def CheckScore(value):
    try:
        if value['score'] < 0.001:
            return ''
        else:
            return value['answer']
    except:
        return ''


def CheckCoordinate(data_coordinate):
    if (data_coordinate['north'] > data_coordinate['south']) and (data_coordinate['west'] < data_coordinate['east']):
        return True
    else:
        return False


def GeneratorMessage(response):
    for word in response.split():
        yield word + " "
        time.sleep(0.05)


def CheckCache(cache, target):
    for key, val in target.items():
        if not (cache[key] != '' and val == ''):
            cache[key] = val
        else:
            target[key] = cache[key]

    return cache, target


def CheckParamMessage(**kwargs):
    params_none = [key for key, val in kwargs.items() if val is None or val == '']

    if len(params_none) != 0:
        list_param = ', '.join(params_none)
        message = f'Please provide the data information about {list_param}'
    else:
        message = ''

    return params_none, message


def ConvertDataDownload(data):
    # Convert DataFrame to CSV
    csv_buffer = io.StringIO()
    data.to_csv(csv_buffer, index=False)
    csv_data = csv_buffer.getvalue()

    return csv_data


def GetNumberUnique(lst):
    """Generate a random number within a range that is not in the given list."""
    if not lst:
        # If the list is empty, any number within the range is valid
        return random.randint(1, 1000000)

    while True:
        rand_num = random.randint(1, 1000000)

        if rand_num not in lst:
            return rand_num
