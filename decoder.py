from astm import codec
from astm import omnilab
from astm.constants import ENCODING
import json

from query_message import getMessage

decode_record = lambda r: codec.decode_record(r.encode(), ENCODING)
encode_record = lambda r: codec.encode_record(r, ENCODING)

# Decode record according to the start char 
def handle_header_record(data):
  try:
    header = omnilab.client.Header(*decode_record(data))
  except Exception as e:
    print("The error is: ",e)
    return "something went wrong!"
  result = {
      'type': header.type,
      'sender_name':  header.sender.name,
      'sender_version': header.sender.version,
      'version': header.version,
      'timestamp': header.timestamp.strftime('%Y-%m-%d %H:%M:%S')
  }
  return result

def handle_patient_record(data):
    patient = omnilab.client.Patient(*decode_record(data))
    special_1 = ''
    special_2 = ''
    if 'special_1' in patient:
      special_1 = patient.special_1
    if 'special_2' in patient:
      special_2 = patient.special_2

    result = {
        'type': patient.type,
        'seq':  patient.seq,
        'practice_id': patient.practice_id,
        'laboratory_id': patient.laboratory_id,
        'first_name': patient.name.first,
        'last_name': patient.name.first,
        'birthdate': patient.birthdate.strftime('%Y-%m-%d %H:%M:%S'),
        'sex': patient.sex,
        'physician_id': patient.physician_id,
        'special_1': special_1,
        'special_2': special_2
    }
    return result

def handle_test_order_record(data):
    order = omnilab.client.Order(*decode_record(data))
    testArray = []
    for test in order.test:
      case = {'assay_code': test.assay_code, 'assay_name': test.assay_name}
      testArray.append(case)
    result = {
        'type': order.type,
        'seq':  order.seq,
        'sample_id': order.sample_id,
        'tests': testArray,
        'priority': order.priority,
        'created_at': order.created_at.strftime('%Y-%m-%d %H:%M:%S') if order.created_at else '',
        'sampled_at': order.sampled_at.strftime('%Y-%m-%d %H:%M:%S') if order.sampled_at else '',
        'action_code': order.action_code,
        'biomaterial': order.biomaterial,
        'user_field_1': order.user_field_1,
        'user_field_2': order.user_field_2,
        'laboratory_field_1': order.laboratory_field_1,
        'laboratory_field_2': order.laboratory_field_2,
        'report_type': order.report_type,
        'laboratory': order.laboratory
    }
    return result

def handle_result_record(data):
    result = omnilab.client.Result(*decode_record(data))
    testArray = {}
    for test in result.test:
      case = {'assay_code': test.assay_code, 'assay_name': test.assay_name}
      testArray.append(case)
    result = {
        'type': result.type,
        'seq':  result.seq,
        'test': testArray,
        'practice_id': result.value,
        'birthdate': result.completed_at.strftime('%Y-%m-%d %H:%M:%S')
    }
    return result

def handle_comment_record(data):
    comment  = omnilab.client.Comment(*decode_record(data))
    dataArray = {}
    for data in comment .test:
      case = {'code': data.code, 'assay_name': data.value}
      dataArray.append(case)
    result = {
        'source': comment.source,
        'data': dataArray,
        'ctype': comment.ctype,
        'birthdate': comment.completed_at.strftime('%Y-%m-%d %H:%M:%S')
    }
    return result

def handle_query_record(data):
    result = getMessage(data)
    return result

def handle_scientific_record(data):
    print("Scientific Record")
    return 'Scientific Record'

def handle_manufacturer_record(data):
    print("Manufacturer Record")
    return 'Manufacturer Record'


def handle_final_record(data):
    term = omnilab.client.Terminator(*decode_record(data))
    result = {
        'type': term.type,
        'seq': term.seq,
        'code': term.code
    }
    return result

def decode_message(data):
  switcher = {
      'H': lambda: handle_header_record(data),
      'P': lambda: handle_patient_record(data),
      'O': lambda: handle_test_order_record(data),
      'R': lambda: handle_result_record(data),
      'C': lambda: handle_comment_record(data),
      'S': lambda: handle_scientific_record(data),
      'M': lambda: handle_manufacturer_record(data),
      'Q': lambda: handle_query_record(data),
      'L': lambda: handle_final_record(data)
  }
  # Handling the data based on the starting letter
  if len(data) > 0:
    print(data)
    letter = data[0]
    print(letter)
    result = switcher.get(letter, lambda: "Record not recognized")()
  else:
    result = 'Message is empty'
  return json.dumps(result)