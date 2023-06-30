INSERT_STMT = "INSERT INTO transaction_ner (case_id, grp_entity, entity_name, entity_value, create_date, update_date) "

def create_ner_statement(data: dict, case_id: str):
    statement = []

    for entity_name, entity_value in data.items():
        if len(entity_value) == 0:
            continue

        for count, value in enumerate(entity_value):
            # ยาเสพติด_1
            entity_group = entity_name + "_" + str(count + 1)

            # TODO - low priority - adjust DRY
            if (entity_name == 'ยาเสพติด'):

                n_stmt = nacrotics_statement(value, case_id, entity_group)
                statement.extend(n_stmt)

            else:
                sql =  INSERT_STMT + "VALUES('{case_id}', '{entity_group}', '{entity_name}', '{entity_value}', now(), now()) \
                ".format(case_id=case_id, entity_group=entity_group, entity_name=entity_name, entity_value=value).strip()

                statement.append(sql)

    return statement


def nacrotics_statement(val: str, case_id: str, entity_group: str) -> list:
    '''
    input as a list of nacrotic type, quantity and unit
    '''
    result = []
    nacrotics_lst = val.split()

    unit_index = -1
    result.append( 
            INSERT_STMT + "VALUES('{case_id}', '{entity_group}', '{entity_name}', '{entity_value}', now(), now())\
                    ".format(case_id=case_id, entity_group=entity_group, entity_name="drug_name", entity_value=nacrotics_lst[0]).strip()
    )
    for count, elem in enumerate(nacrotics_lst):
        if elem.isdigit():
            result.append(
                    INSERT_STMT + "VALUES('{case_id}', '{entity_group}', '{entity_name}', '{entity_value}', now(), now())\
                                ".format(case_id=case_id, entity_group=entity_group, entity_name="qty", entity_value=str(elem)).strip()
            )
            unit_index = count + 1
            try:
                unit = nacrotics_lst[unit_index]
            except:
                unit = "ไม่ทราบหน่วย"

            result.append(
                    INSERT_STMT + "VALUES('{case_id}', '{entity_group}', '{entity_name}', '{entity_value}', now(), now())\
                        ".format(case_id=case_id, entity_group=entity_group, entity_name="unit", entity_value=str(unit)).strip()
                )
            break
    return result

################################# For batch test #################################
# d = {
#         "การกระทำความผิด": [
#             "จับกุม"
#         ],
#         "ชื่อคน": [
#             "นางสาวพรทิวา ทองใบ"
#         ],
#         "ที่อยู่": [
#             "204 หมู่ที่ 3 ตำบลหนองหลัก อำเภอไชยวาน  จังหวัดอุดรธานี",
#             "827/51 (พันดาวเพลส คอนโดมิเนียม ห้องเลขที่ 7A1 ชั้น 7) ซอยสุขุมวิท 50 ถนนสุขุมวิท แขวงพระโขนง เขตคลองเตย กรุงเทพมหานคร"
#         ],
#         "ภาหนะ": [],
#         "ยาเสพติด": [
#             "กัญชา จำนวน 2 มวน",
#             "กัญชา จำนวน 1 ห่อ",
#             "กัญชา จำนวน 1 ห่อ"
#         ],
#         "วันที่": [],
#         "เบอร์โทรศัพท์": [],
#         "เลขบัตรประจำตัวประชาชน": [
#             "3 4108 00241 99 2"
#         ]
#     }

# stmt = create_statement(d, '1113')
# print(stmt[0])