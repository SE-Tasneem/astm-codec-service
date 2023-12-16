# PS code
def getMessage(message='Q|1|^342244||||||||||O'):
    query_item = {
      'type': None,
      'seq': None,
      'patient_info': {
          'patient_id': None,
          'specimen_id': None
      },
      'ending_range_id': None,
      'universal_test_id': None,
      'request_time_limits': None,
      'start_request_results': None,
      'end_request_results': None,
      'physician_name': None,
      'physician_telephone': None,
      'user_field_1': None,
      'user_field_2': None,
      'request_info': None
    }
    key_order = [
    'type', 'seq', 'patient_info',
    'ending_range_id', 'universal_test_id', 'request_time_limits',
    'start_request_results', 'end_request_results', 'physician_name',
    'physician_telephone', 'user_field_1', 'user_field_2', 'request_info'
    ]
    elements = message.split('|')
    for key, value in enumerate(key_order):
      query_item[value] = elements[key]
    if 'patient_info' in query_item and query_item['patient_info'] is not None:
      patient_info = query_item['patient_info'].split('^')
      if len(patient_info) == 2:
        query_item['patient_id'] = patient_info[0] if patient_info[0] is not None else ''
        query_item['specimen_id'] = patient_info[1] if patient_info[1] is not None else ''

    return query_item
  
def setMessage(query_item):
    key_order = [
        'type', 'seq', 'patient_info',
        'ending_range_id', 'universal_test_id', 'request_time_limits',
        'start_request_results', 'end_request_results', 'physician_name',
        'physician_telephone', 'user_field_1', 'user_field_2', 'request_info'
    ]
    elements = []
    for key in key_order:
        value = query_item[key]
        if key == 'patient_info':
            # Combine patient_id and specimen_id with '^'
            patient_info_value = '^'.join([value['patient_id'], value['specimen_id']])
            elements.append(patient_info_value)
        else:
            elements.append(str(value) if value is not None else '')

    message = '|'.join(elements)
    return message

# Example usage:
query_item = {
    'type': 'Q',
    'seq': '1',
    'patient_info': {
        'patient_id': '123',
        'specimen_id': '456'
    },
    'ending_range_id': None,
    'universal_test_id': None,
    'request_time_limits': None,
    'start_request_results': None,
    'end_request_results': None,
    'physician_name': None,
    'physician_telephone': None,
    'user_field_1': None,
    'user_field_2': None,
    'request_info': 'O'
}

result = setMessage(query_item)
print(result)

# Example usage:
result = getMessage()
print(result)
