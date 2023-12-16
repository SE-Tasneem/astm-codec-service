from astm import codec
from astm import omnilab
from astm.constants import ENCODING
import json
import datetime
from query_message import setMessage

decode_record = lambda r: codec.decode_record(r.decode(), ENCODING)
encode_record = lambda r: codec.encode_record(r, ENCODING)

# encode record according to the start char 
def create_header_record(header):
  try:
    message = ''
    message += '{}|{}|{}|{}|{}'.format(
      header['type'],
      header['sender_name'],
      header['sender_version'],
      header['version'],
      header['timestamp']
    )
  except Exception as e:
    print("The error is: ",e)
    return "something went wrong!"
  return message

def create_patient_record(patient):
  message = ''
  message += '{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}'.format(
    patient['type'],
    patient['seq'],
    patient['practice_id'],
    patient['laboratory_id'],
    patient['first_name'],
    patient['last_name'],
    patient['birthdate'].strftime('%Y-%m-%d %H:%M:%S'),
    patient['sex'],
    patient['physician_id'],
    patient['special_1'],
    patient['special_2'],
    ''
  )
  return message

def create_test_order_record(order):
    tests = ""
    message = ""
    message += '{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}'.format(
      order['type'],
      order['seq'],
      order['sample_id'],
      order['test'],
      order['priority'],
      order['created_at'],
      order['sampled_at'],
      order['collected_at'],
      order['volume'],
      order['collector'],
      order['action_code'],
      order['danger_code'],
      order['clinical_info'],
      order['delivered_at'],
      order['biomaterial'],
      order['physician'],
      order['physician_phone'],
      order['user_field_1'],
      order['user_field_2'],
      order['laboratory_field_1'],
      order['laboratory_field_2'],
      order['modified_at'],
      order['instrument_charge'],
      order['instrument_section'],
      order['report_type'],
      order['reserved'],
      order['location_ward'],
      order['infection_flag'],
      order['specimen_service'],
      order['laboratory']
    )
    return message

def create_result_record(data):
    result = omnilab.client.Result(*encode_record(data))
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

def create_comment_record(data):
    comment  = omnilab.client.Comment(*encode_record(data))
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

def create_query_record(data):
    result = setMessage(data)
    return result

def create_scientific_record(data):
    print("Scientific Record")
    return 'Scientific Record'

def create_manufacturer_record(data):
    print("Manufacturer Record")
    return 'Manufacturer Record'

def create_final_record(data):
    term = omnilab.client.Terminator(*encode_record(data))
    result = {
        'type': term.type,
        'seq': term.seq,
        'code': term.code
    }
    return result

def encode_message(data):
  switcher = {
      'H': lambda: create_header_record(data),
      'P': lambda: create_patient_record(data),
      'O': lambda: create_test_order_record(data),
      'R': lambda: create_result_record(data),
      'C': lambda: create_comment_record(data),
      'S': lambda: create_scientific_record(data),
      'M': lambda: create_manufacturer_record(data),
      'Q': lambda: create_query_record(data),
      'L': lambda: create_final_record(data)
  }
  # Handling the data based on the starting letter
  if len(data) > 0:
    print(data)
    letter = data['type']
    print(letter)
    result = switcher.get(letter, lambda: "Array not recognized")()
  else:
    result = 'Message is empty'
  return json.dumps(result)
# for test:
patient = {
    'type': 'P',
    'seq': 1,
    'practice_id': '1234567890',
    'laboratory_id': 'ABCDEFGHIJ',
    'first_name': 'John',
    'last_name': 'Doe',
    'birthdate': datetime.datetime(1980, 1, 1),
    'sex': 'M',
    'physician_id': '123456',
    'special_1': 'SPECIAL1',
    'special_2': 'SPECIAL2'
}
# data = 'O|1|12120001||^^^NA^Sodium\^^^Cl^Clorum|R|20011023105715|20011023105715||||N||||S|||CHIM|AXM|Lab1|12120||||O|||||LAB2'
order = {
  'type': 'O',
  'seq': 1,
  'sample_id': '12120001',
  'instrument': '',
  'test': '^^^NA^Sodium\^^^Cl^Clorum',
  'priority': 'R',
  'created_at': '20011023105715',
  'sampled_at': '20011023105715',
  'collected_at': '',
  'volume': '',
  'collector': '',
  'action_code': 'N',
  'danger_code': '',
  'clinical_info': '',
  'delivered_at': '',
  'biomaterial': 'S',
  'physician': '',
  'physician_phone': '',
  'user_field_1': 'CHIM',
  'user_field_2': 'AXM',
  'laboratory_field_1': 'Lab1',
  'laboratory_field_2': '12120',
  'modified_at': '',
  'instrument_charge': '',
  'instrument_section': '',
  'report_type': 'O',
  'reserved': '',
  'location_ward': '',
  'infection_flag': '',
  'specimen_service': '',
  'laboratory': 'LAB2'
}
# data = 'R|1|^^^NA^Sodium|7.273|mmol/l|10-120|0|N|F||Val.Autom.^Smith |201009261006|201009261034^201009261033|Architect'
result = {
  'type': 'R',
  'seq': 1,
  'test': 'instrument',
  'units': 'mmol/l',
  'references': '10-120',
  'abnormal_flag': 0,
  'abnormality_nature': 'N',
  'status': 'F',
  'operator_code_on_labonline': 'Val.Autom.',
  'operator_code_on_analyzer': 'Smith',
  'started_at': datetime.datetime(2010, 9, 26, 10, 0, 6),
  'completed_at_labonline': datetime.datetime(2010, 9, 26, 10, 0, 6),
  'completed_at_analyzer': datetime.datetime(2010, 9, 26, 10, 0, 6),
  'instrument': 'Architect'
}
print(encode_message(order))