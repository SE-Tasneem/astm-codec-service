from astm import codec
from astm import omnilab
from astm.constants import ENCODING
import json

decode_record = lambda r: codec.decode_record(r.encode(), 'ascii')
encode_record = lambda r: codec.encode_record(r, 'ascii')

# Decode record according to the start char 
def handle_header_record(data):
    header = omnilab.client.Header(*decode_record(data))
    result = {
        'type': header.type,
        'sender_name':  header.sender.name,
        'sender_version': header.sender.version,
        'version': header.version,
        'timestamp': header.timestamp.strftime('%Y-%m-%d %H:%M:%S')
    }
    return result

def handle_patient_record(data):
    patient = omnilab.client.Header(*decode_record(data))
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
        'special_1_value': patient.special_1.value,
        'special_1_unit': patient.special_1.unit,
        'special_2_value': patient.special_2.value,
        'special_2_unit': patient.special_2.unit,
        'location': patient.location
    }
    return result

def handle_test_order_record(data):
    order = omnilab.client.Header(*decode_record(data))
    testArray = {}
    for test in order.test:
      case = {'assay_code': test.assay_code, 'assay_name': test.assay_name}
      testArray.append(case)
    result = {
        'type': order.type,
        'seq':  order.seq,
        'sample_id': order.sample_id,
        'tests': testArray,
        'priority': order.priority,
        'created_at': order.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        'sampled_at': order.sampled_at.strftime('%Y-%m-%d %H:%M:%S'),
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
    print("Result Record")
    return omnilab.client.Result(*decode_record(data))

def handle_comment_record(data):
    print("Comment Record")
    return omnilab.client.Comment(*decode_record(data))

def handle_scientific_record(data):
    print("Scientific Record")
    return 'Scientific Record'

def handle_manufacturer_record(data):
    print("Manufacturer Record")
    return 'Manufacturer Record'

def handle_request_information(data):
    print("Request Information")
    return 'Request Information'

def handle_final_record(data):
    print("Final Record")
    return 'Final Record'

def decode_message(data):
  data = 'H|\^&|||HOST^1.0.0|||||||P|E 1394-97|20091116104731'

  switcher = {
      'H': lambda: handle_header_record(data),
      'P': lambda: handle_patient_record(data),
      'O': lambda: handle_test_order_record(data),
      'R': lambda: handle_result_record(data),
      'C': lambda: handle_comment_record(data),
      'S': lambda: handle_scientific_record(data),
      'M': lambda: handle_manufacturer_record(data),
      'Q': lambda: handle_request_information(data),
      'L': lambda: handle_final_record(data)
  }
  # Handling the data based on the starting letter
  letter = data[0]
  result = switcher.get(letter, lambda: "Record not recognized")()
  print(result)
  print(json.dumps(result))

