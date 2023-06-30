# extract_routes.py
from hashlib import sha256
import psycopg2
from flask import Blueprint, jsonify, request
from iconfiguration import iconfiguration

import io
import json
import openai
import re
from services.DocumentExtractor import DocumentExtractor
from services.norm_key import norm_key, NORMALIZED_KEY
from services.DocumentGenerate import DocumentGenerate
from services.create_ner_statement import create_ner_statement
from services.create_ess_statement import *
extract_route = Blueprint('extract_route', __name__)

OPENAI_KEY = ''
openai.api_key = OPENAI_KEY


class FirstJSONObjectDecoder(json.JSONDecoder):
    def decode(self, s, _w=None):
        s = s.strip()
        obj, end = self.raw_decode(s)
        return obj


def extract_first_json_object(json_string):
    decoder = FirstJSONObjectDecoder()
    return decoder.decode(json_string)


def fix_unterminated_strings(s):
    stack = []
    result = ''
    in_string = False
    for c in s:
        if c == '"' and not (len(stack) > 0 and stack[-1] == '\\'):
            in_string = not in_string
            if not in_string:
                result += ''.join(stack) + c
                stack.clear()
            else:
                stack.append(c)
        elif not in_string and c in ('{', '}', '[', ']', ',', ':', '”', ' ”'):
            if len(stack) > 0 and stack[-1] not in ('{', '}', '[', ']', ',', ':', '”', ' ”'):
                result += stack.pop()
            result += c
            continue
        else:
            stack.append(c)

    # If the stack is not empty, join and add the remaining characters
    if stack:
        result += ''.join(stack)

    return result


@extract_route.route("/extract", methods=["POST"])
def extract():
    if "file" not in request.files:
        return jsonify({'status': 'failed', 'message': 'No file uploaded'}), 400

    uploaded_file = request.files['file']

    # Read the binary data from the file
    file_data = uploaded_file.read()

    # Create an in-memory binary stream from the file data
    file_stream = io.BytesIO(file_data)

    # Load the binary stream as a docx.Document object
    extracted_result = DocumentExtractor().extract(file_stream)

    name = uploaded_file.filename
    global hashed_name
    hashed_name = sha256(name.encode('utf-8')).hexdigest()

    response_data = {
        'status': 'success',
        'result': extracted_result,
        'message': "Document extraction successful."
    }

    return jsonify(response_data), 200


@extract_route.route("/generate", methods=["POST"])
def generate():
    if "file" not in request.files:
        return jsonify({'status': 'failed', 'message': 'No file uploaded'}), 400
    uploaded_file = request.files['file']
    name = uploaded_file.filename
    file_data = uploaded_file.read()
    file_stream = io.BytesIO(file_data)
    extracted_result = DocumentExtractor().extract(file_stream)
    data = norm_key(extracted_result)["ess"]
    if "พฤติการณ์ในการจับกุม" in norm_key(extracted_result)["out_of_scope"].keys():
        behavior_value = norm_key(extracted_result)[
            "out_of_scope"]["พฤติการณ์ในการจับกุม"]
    elif "พฤติการณ์ในการตรวจค้นและจับกุม" in norm_key(extracted_result)["out_of_scope"].keys():
        behavior_value = norm_key(extracted_result)[
            "out_of_scope"]["พฤติการณ์ในการตรวจค้นและจับกุม"]
    else:
        behavior_value = ""
    data.update({'พฤติการณ์ในการจับกุม': behavior_value})
    generated_document = DocumentGenerate(data).generate(name)
    response_data = {
        'status': 'success',
        'generated_document': generated_document,
        'message': "Document generation successful."
    }
    return jsonify(response_data), 200


@extract_route.route("/essential_extract", methods=["POST"])
def essential_extract():
    body = request.get_json()
    if ('data' not in body):
        return jsonify({"message": "Key 'data' is missing in the request's body."}), 400

    data = body['data']

    essential_data = norm_key(data)

    response_data = {
        'status': 'success',
        'result': essential_data,
        'message': "Essential extraction done."
    }

    return jsonify(response_data), 200


@extract_route.route("/ner_openai", methods=["POST"])
def ner_openai():
    body = request.get_json()
    if 'data' not in body:
        return jsonify({"message": "Key 'data' is missing in the request's body."}), 400

    data = body['data']

    premise = '''Find NER from the message below and reply me as a dictionary in python\
                the dict's key is string, while the value is list of string for example\
                {
                    "ชื่อคน": [
                        "ชัยวัด นามสกุล"
                    ],
                    "ที่อยู่": [
                        "188 หมู่ 70 ตำบลสะเนียน อำเภอเมือง จังหวัดน่าน"
                    ],
                    "ยาเสพติด": [
                        "ยาบ้า 160,000 เม็ด"
                        "กัญชา 1 ห่อ"
                    ],
                    "รถยนต์": [
                        "โตโยต้า รุ่น รีโว่ สีขาว หมายเลขทะเบียน 9xx 8888 กรุงเทพมหานคร"
                    ],
                    "เลขบัตรประจำตัวประชาชน": [
                        "555xxxxxxx562 "
                    ],
                    "เบอร์โทรศัพท์": [
                        "09xxxxxx62"
                        "09xxxxxx97"
                    ]
                    "รุ่นโทรศัพท์": [
                        "SAMSUNG สีดำ"
                    ]
                    "IMEI":[
                        "IMEI1 : 359021821741090/01, IMEI2 : 359763691741094/01"
                        "IMEI 35899507995693/01 "
                        ]
                    "หมายเลขซิม":[
                        "AIS วัน-ทู-คอล หมายเลขซิม 89xx03 2121 PRERAID 0435_2190 5"
                        "unitel SIM Net หมายเลขซิม 4 4530123571 3 : 89700298 80 57"
                        ]
                }
                There must not be a key named "มีของกลาง" or "ของกลาง"
                Required NER are: วันที่, ยาเสพติด, เบอร์โทรศัพท์, ชื่อคน, ที่อยู่, เลขบัตรประจำตัวประชาชน, การกระทำความผิด
                หากไม่สามารถระบุ entity ได้ให้ปล่อยเป็นค่า list ว่าง []
                '''
    # "SAMSUNG สีดำ หมายเลขเบอร์โทร 09xxxxxx97 ระบบ AIS วัน-ทู-คอล IMEI 35899507995693/01",
    # Example for ยาเสพติด: are กัญชา, แป้ง, ไอซ์, ยาแก้ไอ
    # Example on how to mark NER on ภาหนะ: โตโยต้า วีออส สีดำ ทะเบียน 7xx xxxx ตรัง
    # Example on how to mark NER on เบอร์โทรศัพท์: แอปเปิ้ล 0950105141
    # Example on how to mark NER on การกระทำความผิด: เสพ ขาย ใช้เอง มีไว้ครอบครอง
    # แม้ว่าบาง entity จะมีเพียง 1 อย่าง ให้ระบุไว้เป็น list เช่นกัน

    NER_KEY = ["สถานที่จับกุม", "ผู้ต้องหา",
               "สถานที่เกิดเหตุ", "ของกลาง", "ข้อหา"]
    group = []
    for i in range(0, len(NER_KEY), 3):
        text = ''
        for j in range(3):
            if i + j < len(NER_KEY):
                try:
                    text += f"{NER_KEY[i+j]} {data[NER_KEY[i+j]]} "
                except Exception:
                    continue
        group.append(text)

    final_result = {}

    for k in group:
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=[
                {"role": "assistant", "content": premise},
                {"role": "user", "content": k}
            ],
            temperature=0
        )
        # print("\n----------------------")
        # print(response['choices'][0]['message']['content'].strip())
        partial_result = {}
        response_string = response['choices'][0]['message']['content'].strip()
        fixed_response_string = fix_unterminated_strings(response_string)
        try:
            partial_result = extract_first_json_object(fixed_response_string)
        except:
            for count, letter in enumerate(reversed(fixed_response_string)):
                if (letter == "}" or letter == " " or letter == "\n"):
                    continue
                elif (letter == ","):
                    new_str = fixed_response_string[:-(count) - 1] + \
                        "" + fixed_response_string[-(count):]
                    break
                else:
                    break
            try:
                partial_result = extract_first_json_object(new_str)
            except:
                pass
        for key in partial_result.keys():
            if key in final_result.keys() and partial_result[key] != []:
                for value in partial_result[key]:
                    if value not in final_result[key] and value != "ไม่ระบุ":
                        final_result[key].append(value)  # Append value first
                    else:
                        pass
                # Remove duplicates after appending
                final_result[key] = list(set(final_result[key]))
            elif key in final_result.keys() and partial_result[key] == []:
                pass
            elif key not in final_result.keys():
                final_result[key] = partial_result[key]

    for key in final_result.keys():
        if final_result[key] == []:
            final_result[key] = ["ไม่มีข้อมูล"]
        elif 'ไม่ระบุ' in final_result[key]:
            final_result[key].remove('ไม่ระบุ')
            if final_result[key] == []:
                final_result[key] = ["ไม่มีข้อมูล"]
        else:
            pass
    # print(final_result)
    return jsonify({'status': 'success', 'result': final_result, 'usage': response['usage'], 'message': "NER processing successful."}), 200


@extract_route.route("/add_ess_data", methods=["POST"])
def add_ess_data():
    data = request.get_json()['dataExtraction']

    try:
        case_id = hashed_name
    except:
        for val in data[0].values():
            case_id = hash(val)
            break
    ###

    insert_stmt = create_ess_statement(data, case_id)
    for sql in insert_stmt:
        try:
            # Establish a connection
            conn = psycopg2.connect(database="NSB-POC",
                                    host="localhost",
                                    user="postgres",
                                    password="P@ssw0rd",
                                    port="5432")

            cur = conn.cursor()

            # Execute an INSERT statement
            cur.execute(sql)

            # Commit the transaction
            conn.commit()

        except Exception as e:
            print("Error: ", e)
            status = 400

        finally:
            # Close cursor and connection
            cur.close()
            conn.close()

    status = 200

    return jsonify({"msg": "SUCCESS"}), status


@extract_route.route("/add_ner_data", methods=["POST"])
def add_ner_data():
    data = request.get_json()['dataExtraction']
    try:
        case_id = hashed_name
    except:
        for val in data[0].values():
            case_id = hash(val)
            break

    new_dict = {}
    for val in data:
        new_dict.update(val)
    ###

    insert_stmt = create_ner_statement(new_dict, case_id)
    for sql in insert_stmt:
        try:
            # Establish a connection
            conn = psycopg2.connect(database="NSB-POC",
                                    host="localhost",
                                    user="postgres",
                                    password="P@ssw0rd",
                                    port="5432")
            cur = conn.cursor()
            # Execute an INSERT statement
            cur.execute(sql)
            # Commit the transaction
            conn.commit()
        except Exception as e:
            print("Error: ", e)
            status = 400
        finally:
            # Close cursor and connection
            cur.close()
            conn.close()
    status = 200
    return jsonify({"msg": "SUCCESS"}), status
