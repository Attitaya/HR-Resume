# app.py
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from services.DocumentReader import DocumentReader
from services.DocumentGenerate import DocumentGenerate
from services.norm_key import norm_key
from services.create_statement import create_statement
from collections import OrderedDict
import os
import openai
import json
import re
import psycopg2

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "uploads"
CORS(app)

OPENAI_KEY = ''
openai.api_key = OPENAI_KEY


@app.route("/extract", methods=["POST"])
def extract():
    file_name = request.get_json()['file_name']
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], file_name)

    dcr = DocumentReader(file_path)
    ner = dcr.get_ner()
    ess = dcr.get_ess()

    global result_extracted
    result_extracted = {}
    result_extracted = {"ner": ner, "ess": ess}
    return jsonify({"data": ner})


@app.route("/notice_extract", methods=["POST"])
def notice_extract():
    if (result_extracted == {}):
        return jsonify({"message": "Need to extract document first!"}), 400

    noticed_fields = ['สถานที่บันทึก', 'วัน เดือน ปี เวลาที่บันทึก', "วัน เดือน ปี เวลา จับกุม", "ได้ร่วมกันทำการจับกุม", "ได้ร่วมกันจับกุมตัว",
                      "พร้อมของกลาง", "โดยกล่าวหาว่า", "วัน/เดือน/ปี ที่จับกุม", "วัน/เดือน/ปี ที่บันทึก", "สถานที่ทำการบันทึก"]

    global notice_extracted
    notice_extracted = OrderedDict()

    for field in noticed_fields:
        for region, value in result_extracted.items():
            if field not in value.keys():
                continue
            notice_extracted[field] = result_extracted[region][field]

    return jsonify({'data': notice_extracted})


@app.route("/ner_openai", methods=["POST"])
def ner_openai():
    body = request.get_json()
    if ('data' not in body):
        return jsonify({"message": "Missing 'data' in request's body"}), 400

    data = request.get_json()['data']

    norm_data = norm_key(data)

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
                        "โตโยต้า รุ่น รีโว่ สีขาว หมายเลขทะเบียน 9xx 8888 กรุงเทพมหานคร",
                    ],
                    "เลขบัตรประจำตัวประชาชน": [
                        "555xxxxxx561"
                    ],
                    "โทรศัพท์มือถือ": [
                        "SAMSUNG สีดำ หมายเลขเบอร์โทร 09xxxxxx97 ระบบ AIS วัน-ทู-คอล IMEI 35899507995693/01",
                        "AIS วัน-ทู-คอล หมายเลขซิม 89xx03 2121 PRERAID 0435_2190 5",
                    ]
                }
                Required NER are: ภาหนะ, วันที่, ยาเสพติด, เบอร์โทรศัพท์, ชื่อคน, ที่อยู่, id no (เลขบัตรประจำตัวประชาชน), การกระทำความผิด 
                หากไม่สามารถระบุ entity ได้ให้ปล่อยเป็นค่า list ว่าง []
                '''

    # premise = '''Find NER from the message below and reply me as a dictionary in python\
    #             the dict's key is string, while the value is list of string for example\
    #             {
    #                 "ชื่อคน": [
    #                     "ชัยวัด นามสกุล"
    #                 ],
    #                 "ที่อยู่": [
    #                     "188 หมู่ 70 ตำบลสะเนียน อำเภอเมือง จังหวัดน่าน"
    #                 ],
    #                 "ยาเสพติด": [
    #                     "ยาบ้า 160,000 เม็ด"
    #                     "กัญชา 1 ห่อ"
    #                 ],
    #                 "รถยนต์": [
    #                     "โตโยต้า รุ่น รีโว่ สีขาว หมายเลขทะเบียน 9xx 8888 กรุงเทพมหานคร",
    #                 ],
    #                 "เลขบัตรประจำตัวประชาชน": [
    #                     "555xxxxxx561"
    #                 ],
    #                 "โทรศัพท์มือถือ": [
    #                     "SAMSUNG สีดำ หมายเลขเบอร์โทร 09xxxxxx62 ระบบทรูมูฟ เอซ IMEI1 359021821741090/01 IMEI2 : 359763691741094/01 : SN R58R521MEQB ",
    #                     "SAMSUNG สีดำ หมายเลขเบอร์โทร 09xxxxxx97 ระบบ AIS วัน-ทู-คอล IMEI 35899507995693/01",
    #                     "AIS วัน-ทู-คอล หมายเลขซิม 89xx03 2121 PRERAID 0435_2190 5",
    #                 ]
    #             }
    #             There must not be a key named "มีของกลาง" or "ของกลาง"
    #             Required NER are: ภาหนะ, วันที่, ยาเสพติด, เบอร์โทรศัพท์, ชื่อคน, ที่อยู่, id no (เลขบัตรประจำตัวประชาชน), การกระทำความผิด 
    #             Example for ยาเสพติด: are กัญชา, แป้ง, ไอซ์, ยาแก้ไอ
    #             Example on how to mark NER on ภาหนะ: โตโยต้า วีออส สีดำ ทะเบียน 7xx xxxx ตรัง
    #             Example on how to mark NER on เบอร์โทรศัพท์: แอปเปิ้ล 0950105141
    #             Example on how to mark NER on การกระทำความผิด: เสพ ขาย ใช้เอง มีไว้ครอบครอง
    #             แม้ว่าบาง entity จะมีเพียง 1 อย่าง ให้ระบุไว้เป็น list เช่นกัน
    #             หากไม่สามารถระบุ entity ได้ให้ปล่อยเป็นค่า list ว่าง []
    #             '''

    # NACROTICS
    text = norm_data['พร้อมของกลาง']
    # PLACE
    try:
        text += " สถานที่จับกุม" + data['สถานที่จับกุม'] + " "
    except:
        try:
            text += " สถานที่จับกุม" + data['สถานที่เกิดเหตุ / จับกุม'] + " "
        except:
            pass
    # NAME VICTIM
    try:
        text += " ได้ร่วมกันทำการจับกุม" + data['ได้ร่วมกันทำการจับกุม']
    except:
        text += " ได้ร่วมกันทำการจับกุม" + \
            data['ได้ร่วมกันจับกุมตัวผู้กระทำความผิดเกี่ยวกับยาเสพติดให้โทษ 1 ราย']
    print(text)

    response = openai.ChatCompletion.create(model='gpt-3.5-turbo', messages=[{"role": "assistant", "content": premise}                                                                                 # ,{"role" : "user", "content": f"related-context:{formatted_ctx}"}
                                                                             , {"role": "user", "content": f" {text}"}], temperature=0
                                            )

    ans = str(response['choices'][0]['message']['content']).strip()
    json_dict = json.loads(ans)

    return jsonify({'data': json_dict, 'usage': response['usage']})


@app.route("/generate", methods=["POST"])
def generate():
    file_name = request.get_json()['file_name']
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], file_name)
    dcr = DocumentReader(file_path)
    ess = dcr.get_ess()
    dg = DocumentGenerate(ess)
    dg.generate()

    return send_from_directory(".", "เอกสารเร่งด่วน.docx", as_attachment=True)


@app.route("/add_data", methods=["POST"])
def add_data():
    data = request.get_json()['data']

    # TODO- delete this and create case_id
    case_id = ""
    for val in data.keys():
        case_id = hash(val)
        break
    ###

    insert_stmt = create_statement(data, case_id)
    status = 200
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

    return jsonify({"msg": "SUCCESS"}, status)


if __name__ == "__main__":
    app.run(debug=True, port=8899)
