INSERT_STMT = "INSERT INTO transaction_ess (case_id, title_name, text, create_date, update_date) "

def create_ess_statement(data: list, case_id: str):
    statement = []

    for index in range(len(data)):
        # k, v = dict(data[index]).items()
        k_ess = ""
        v_ess = ""
        for k, v in data[index].items():
            k_ess = k
            v_ess = v
            break

        sql =  INSERT_STMT + "VALUES('{case_id}', '{title_name}', '{text}', now(), now()) \
        ".format(case_id=case_id, title_name=k_ess, text=v_ess)

        statement.append(sql)

    return statement

# data = [
#         {
#             "ของกลาง": "7 รายการ  1.ยาเสพติดให้โทษประเภท 1 (ยาบ้า) ลักษณะเ…้องหา -ของกลางรายการที่ 7 ตรวจยึดได้จาก ผู้ต้องหา"
#         },
#         {
#             "ข้อหา": "จำหน่ายยาเสพติดให้โทษประเภท 1 (เมทแอมเฟตามีนหรือยา…ความมั่นคงของรัฐหรือความปลอดภัยของประชาชนทั่วไป"
#         }
#     ]

# print(create_ess_statement(data, 123))