#norm_key.py
import re
from pprint import pprint

# The value in both list must be arranged in this order to normalize key according to found pattern
NORMALIZED_KEY = ["สถานที่บันทึก", "วัน เดือน ปี ที่บันทึก", "วัน เดือน ปี ที่จับกุม", \
                  "สถานที่จับกุม", "สถานที่เกิดเหตุ","ผู้ต้องหา", "ของกลาง", "ข้อหา", \
                    #"พฤติการณ์ในการจับกุม"
                ]
HEADER_PATTERNS = [
        r"(?:สถานที่บันทึก|สถานที่ทำการบันทึก)",
        r"(?:วัน[/ ]เดือน[/ ]ปี ?เวลา?ที่?บันทึก|วัน[/ ]เดือน[/ ]ปี ที่บันทึก|วัน[/ ]เดือน[/ ]ปี ?เวลา? บันทึก)",
        r"(?:วัน[/ ]เดือน[/ ]ปี ?เวลา?ที่?จับกุม|วัน[/ ]เดือน[/ ]ปี ที่จับกุม|วัน[/ ]เดือน[/ ]ปี ?เวลา? จับกุม|วัน[/ ]เดือน[/ ]ปี ตรวจค้น[/ ]จับกุม)",
        r"สถานที่(?:จับกุม / เกิดเหตุ|เกิดเหตุ / จับกุม|จับกุม)",
        r"สถานที่(?:จับกุม / เกิดเหตุ|เกิดเหตุ / จับกุม|เกิดเหตุ)",
        r"ได้ร่วมกัน(?:จับกุมตัว|ทำการจับกุม)",
        r"พร้อม(?:ด้วย)?ของกลาง",
        r"(?:โดยกล่าวหาว่า)",
        #r"(?:พฤติการณ์ในการจับกุม|พฤติการณ์ในการตรวจค้นและจับกุม)"
    ]

def norm_key(data):
    result_dict = {}
    result_dict["ess"] = {}
    result_dict["out_of_scope"] = {}

    # initalize ess key to check extraction error
    for key in NORMALIZED_KEY:
        result_dict["ess"][key] = ''
    # separate ess and oos
    for k, v in data.items():
        mutate = False
        for index, pattern in enumerate(HEADER_PATTERNS):
            match = re.search(pattern, k)
            # If key is normalized, iterate through the next key
            if match and match.group(0) != '':
                if index == 3 or index == 4:  # The case where a single pattern corresponds to multiple normalized keys
                    result_dict["ess"][NORMALIZED_KEY[3]] = v
                    result_dict["ess"][NORMALIZED_KEY[4]] = v
                else:
                    result_dict["ess"][NORMALIZED_KEY[index]] = v
                mutate = True
                break
        if not mutate:
            result_dict["out_of_scope"][k] = v

    return result_dict

################################# For batch test #################################
# d = {
#         "กรมศุลกากร อำนวยการโดย": "นายชูชัย อุดมโภชน์ ที่ปรึกษาด้านพัฒนา ระบบสิทธิประโยชน์ทางศุลกากร นายพงศ์เทพ บัวทรัพย์ รองอธิบดีกรมศุลกากร",
#         "กองสืบสวนและปราบปราม กรมศุลกากร": "นายถวัลย์ รอดจิตต์ ผู้อำนวยการกองสืบสวนและปราบปราม , นายประทีป สมมัง , นายธนดล เกศา นายไมตรี แสงทอง , นายนครินทร์ พานิชย์ , นายอมรเทพ มะโนวรรณ์",
#         "ด่านศุลกากรแม่สอด": "นายเชาวน์ ตะกรุดเงิน นายด่านศุลกากรแม่สอด , นายไพยง สังข์ทอง , นายพิชยา เจริญสันต์ , นายกวินทร์         เขมกุลวานิช , ร.ต.ศักดิ์สยาม จำนงค์ , นายระบอบ เรืองเกษม , นายสมชาย บุญญะบุญญา  , นายสมสกุล สิทธิโชค , นายสรวิทย์ มีแสงนิล , จ.อ.วิรุฬห์วิชญ์ วรโชติโภคิน , นายอรรถกร อ่อนชูศรี",
#         "บันทึกการจับกุม": "",
#         "พร้อมของกลาง จำนวน": "7 รายการ  1.ยาเสพติดให้โทษประเภท 1 (ยาบ้า) ลักษณะเป็นเม็ดกลมแบน สีส้มและมีเม็ดสีเขียวปะปนเล็กน้อย มีตราสัญลักษณ์ WY ด้านหนึ่ง อีกด้านหนึ่งเรียบ บรรจุอยู่ในซองพลาสติกทึบแสงสีฟ้าเข้มและสีชมพูประทับตราอักษรภาษาอังกฤษ A สีเงิน  มีที่รูดปิดเปิดบริเวณปากซองๆ ละประมาณ 200 เม็ด ทำเป็นมัดๆ ละ 10 ซอง ห่อหุ้มด้วยกระดาษสาสีขาว ประทับตราอักษรภาษาอังกฤษ A สีเขียว ห่อด้วยถุงพลาสติกใส พันด้วยเทปกาวแล้วห่อหุ้มด้วยฟอยล์อลูปิเนียมสีเงิน ห่อหุ้มด้วยถุงพลาสติดสีขาวขุ่น แล้วพันรัดไว้ด้วยเทปกาวสีดำ จำนวน 80 มัด หรือจำนวนยาบ้าทั้งสิ้นประมาณ 160,000 เม็ด  ได้จากการตรวจค้น 2.รถยนต์นั่งส่วนบุคคล ยี่ห้อ โตโยต้า รุ่น รีโว่   สีขาว หมายเลขทะเบียน  3ขก 8984 กรุงเทพมหานคร จำนวน 1 คัน ใช้เป็นยานพาหนะในการลำเลียงยาเสพติดของกลาง ซึ่งผู้ต้องหา ผู้ขับขี่ 3.โทรศัพท์มือถือ ยี่ห้อ SAMSUNG สีดำ หมายเลขเบอร์โทร 0973208662 ระบบทรูมูฟ เอซ IMEI1 359021821741090/01 IMEI2 : 359763691741094/01 : SN R58R521MEQB จำนวน 1 เครื่อง ตรวจยึดได้จาก    นายวณิชัย แซ่ท่อ ผู้ต้องหา 4.โทรศัพท์มือถือ ยี่ห้อ SAMSUNG สีดำ หมายเลขเบอร์โทร 0926100397 ระบบ AIS วัน-ทู-คอล IMEI 35899507995693/01 จำนวน 1 เครื่อง ตรวจยึดได้จาก นายวณิชัย แซ่ท่อ ผู้ต้องหา 5.ซิมการ์ดโทรศัพท์ ระบบ AIS วัน-ทู-คอล หมายเลขซิม 896603 2121 PRERAID 0435_2190 5 จำนวน 1 ซิม ตรวจยึดได้จาก นายวณิชัย แซ่ท่อ ผู้ต้องหา 6.ซิมการ์ดโทรศัพท์ unitel SIM Net หมายเลขซิม 4 4530123571 3 : 89700298 80 57 จำนวน 1 ซิม ตรวจยึดได้จาก นายวณิชัย แซ่ท่อ ผู้ต้องหา 7.ซิมการ์ดโทรศัพท์ ระบบ AIS วัน-ทู-คอล 896603 2042 AI5 PREPAID หมายเลขซิม 6735 78728 ตรวจยึดได้จาก นายวณิชัย แซ่ท่อ ผู้ต้องหา ตำแหน่งที่พบของกลาง -ของกลางรายการที่ 1 ตรวจค้นพบซุกซ่อนภายในช่องตัวถังรถ จุดติดตั้งเข็มขัดนิรภัย และช่องตัวถังรถใต้เบาะนั่งโดยสารตอนหลังของรถยนต์ ของกลางรายการที่ 2 -ของกลางรายการที่ 2 ตรวจยึดได้จาก ผู้ต้องหา  ใช้ในการซุกซ่อนและลำเลียงยาเสพติดของกลาง -ของกลางรายการที่ 3 ตรวจยึดได้จาก ผู้ต้องหา  ใช้ในการติดต่อสื่อสารในการลำเลียงยาเสพติดของกลาง -ของกลางรายการที่ 4 ตรวจยึดได้จาก ผู้ต้องหา  ใช้ในการติดต่อสื่อสารในการลำเลียงยาเสพติดของกลาง -ของกลางรายการที่ 5 ตรวจยึดได้จาก ผู้ต้องหา -ของกลางรายการที่ 6 ตรวจยึดได้จาก ผู้ต้องหา -ของกลางรายการที่ 7 ตรวจยึดได้จาก ผู้ต้องหา",
#         "พฤติการณ์ในการจับกุม": "ก่อนเกิดเหตุ เจ้าพนักงานตำรวจชุดจับกุมได้รับแจ้งจากสายลับว่า มีกลุ่มบุคคลผู้ลักลอบลำเลียงยาเสพติดชื่อ    นายวณิชัย แซ่ท่อ ที่มีภูมิลำเนาอยู่ในพื้นที่ จว.น่าน กับพวก มีพฤติการณ์ร่วมกันลักลอบลำเลียงยาเสพติดจากพื้นที่ชายแดนภาคเหนือ ไปส่งจำหน่ายให้กับลูกค้าในพื้นที่ภาคเหนือตอนล่าง และภาคกลาง โดยมีนายทุนผู้จำหน่ายยาเสพติด เป็นผู้ว่าจ้างและจัดหายาเสพติด  จัดการประสานงานการส่งมอบให้กับลูกค้าอยู่เป็นประจำ เจ้าพนักงานตำรวจ บก.สกส.บช.ปส. จึงได้ตรวจสอบข้อมูลบุคคล ยาพาหนะ และข้อมูลอื่นๆ ที่เกี่ยวข้อง แล้วได้รายงานให้ผู้บังคับบัญชาทราบ และผู้บังคับบัญชาได้สั่งการให้ประสานข้อมูลกับหน่วยงานที่เกี่ยวข้อง เพื่อการบูรณาการในการสืบสวน พิสูจน์ทราบ ติดตามพฤติการณ์ของกลุ่มบุคคลดังกล่าว ต่อมาสายลับแจ้งว่าห้วงวันที่ 22-23 ธันวาคม 2565 นายวณิชัย แซ่ท่อ กับพวก จะลักลอบลำเลียงยาเสพติด จำนวนมาก จากพื้นที่ จว.เชียงราย เพื่อนำไปส่งมอบให้กับลูกค้าตามสั่งการของผู้ว่าจ้าง โดยจะใช้รถยนต์ 3ขก 8984 กรุงเทพมหานคร เป็นยานพาหนะ ที่จะใช้ในการซุกซ่อนและลำเลียงยาเสพติด ในครั้งนี้ โดยจะใช้เส้นทาง จว.เชียงราย -   จว.พะเยา - จว.น่าน - จว.แพร่ - จว.สุโขทัย - จว.ตาก เมื่อทราบข้อมูลจากสายลับ เจ้าพนักงานตำรวจชุดจับกุม จึงได้รายงานให้ผู้บังคับบัญชาทราบ และได้เฝ้าระวังยานพาหนะที่จะใช้ลำเลียงยาเสพติด ดังกล่าว ด้วยระบบกล้อง อ่านแผ่นป้ายทะเบียนอัตโนมัติ ของ บก.สกส.บช.ปส. และได้วางแผนในการตรวจค้นจับกุมบุคคลดังกล่าวหากพบว่ามีการพฤติการณ์กระทำความผิดเกี่ยวกับยาเสพติดจริง ต่อมาเมื่อวันที่ 22 ธันวาคม 2565  เวลาประมาณ  22.00 น. เจ้าพนักงานตำรวจชุดปฏิบัติการ พร้อมเจ้าหน้าที่ทหาร พร้อมกับหน่วยงานที่เกี่ยวข้อง ได้ร่วมกันจัดวางกำลัง ซุ่มสังเกตการณ์ ในเส้นทาง อ.ลอง - อ.วังชิ้น (1023) ,          อ.ศรีสัชนาลัย - อ.สวรรคโลก (101) (102) , ถนนสายสุโขทัย - พิษณุโลก (12) และเส้นทางเชื่อมต่อใกล้เคียง พร้อมทั้งได้ตรวจสอบข้อมูลที่เกี่ยวข้อง พร้อมทั้งข้อมูลความเคลื่อนไหวของรถยนต์ผ่านระบบกล้องอ่านแผ่นป้ายทะเบียนอัตโนมัติ ของ บก.สกส.บช.ปส. ต่อมาเวลาประมาณ 22.30 น. ของวันเดียวกัน ( 22 ธันวาคม 2565 ) เจ้าพนักงานตำรวจชุดปฏิบัติการ พบรถยนต์ยี่ห้อโตโยต้า สีขาว ทะเบียน 3ขก 8984 กรุงเทพมหานคร (ตรงตามข้อมูลที่สายลับแจ้งไว้ในตอนต้น) ขับมาในเส้นทาง อ.ลอง - อ.วังชิ้น (1023)  ผ่านพื้นที่ อ.ลอง จว.แพร่  มุ่งหน้าไปทาง อ.วังชิ้น จว.แพร่   เจ้าพนักงานตำรวจชุดปฏิบัติการ จึงได้ขับรถยนต์สะกดรอยติดตามไปห่างๆ พบว่ารถยนต์ทะเบียน 3ขก 8984 กรุงเทพมหานคร ขับขี่ โดยใช้เส้นทาง อ.ลอง - อ.วังชิ้น จว.แพร่ - อ.ศรีสัชนาลัย จว.สุโขทัย  มุ่งหน้าไปทาง อ.สวรรค์โลก จว.สุโขทัย ตามข้อมูลที่ได้รับแจ้งจากสายลับ เจ้าพนักงานตำรวจชุดปฏิบัติการ จึงได้รายงานให้ผู้บังคับบัญชาทราบ ผู้บังคับบัญชาจึงได้สั่งการให้ทำการสกัดกั้น ตรวจสอบ ตรวจค้น รถยนต์เป้าหมาย ในพื้นที่ที่สามารถปฏิบัติการได้ด้วยความปลอดภัย และเหมาะสม  เจ้าพนักงานตำรวจชุดปฏิบัติการ จึงได้ประสานงานกับเจ้าพนักงานตำรวจ สภ.ศรีสัชนาลัย เพื่อร่วมสกัดกั้นตรวจค้นรถยนต์เป้าหมายในพื้นที่แยกสารจิตร  ต.สารจิตร อ.ศรีสัชนาลัย จว.สุโขทัย ต่อมาเวลาประมาณ 00.30 น. ของวันที่ 23 ธันวาคม 2565 รถยนต์เป้าหมายทะเบียน 3ขก 8984 กรุงเทพมหานคร ขับถึงบริเวณแยกสารจิตร  ต.สารจิตร อ.ศรีสัชนาลัย จว.สุโขทัย (ที่เกิดเหตุ) เจ้าพนักงานตำรวจชุดปฏิบัติการ จึงได้ขับรถยนต์เข้าไปสกัดกั้น พร้อมทั้งแสดงตัวเป็นเจ้าพนักงานตำรวจเพื่อขอตรวจค้น  พบ นายวณิชัย แซ่ท่อ ผู้ต้องหา เป็นผู้ขับขี่  จึงได้เชิญตัวลงจากรถ แล้วได้ซักถามข้อมูลการเดินทาง นายวณิชัย แซ่ท่อ มีอาการตื่นเต้นตกใจ ตัวสั่น ตอบคำถามด้วยน้ำเสียงสั่นเครือ  จากนั้น เจ้าพนักงานตำรวจชุดปฏิบัติการ ได้แจ้งเหตุแห่งการตรวจค้นให้ นายวณิชัย แซ่ท่อ ทราบและเข้าใจดีแล้ว ยินยอมให้ทำการตรวจค้น ก่อนทำการตรวจค้น เจ้าพนักงานตำรวจชุดปฏิบัติการ ได้แสดงความบริสุทธิใจให้ นายวณิชัย แซ่ท่อ ดูจนเป็นที่พอใจแล้ว จึงได้ทำการตรวจค้น ผลการตรวจค้นพบยาเสพติดของกลางรายการที่ 1 ซุกซ่อนอยู่ภายในช่องตัวถังรถ จุดติดตั้งเข็มขัดนิรภัย และช่องตัวถังรถใต้เบาะนั่งโดยสารตอนหลังของรถยนต์ ทะเบียน 3ขก 8984 กรุงเทพมหานคร จึงได้ซักถามข้อมูลการกระทำความผิดจากนายวณิชัย แซ่ท่อ  ซึ่ง นายวณิชัย แซ่ท่อ ได้ให้การรับว่าได้ลำเลียงยาเสพติดของกลางมาจากพื้นที่ จว.เชียงราย เพื่อส่งมอบให้กับผู้รับซึ่งเป็นลูกค้า ในพื้นที่ จว.ตาก โดยผู้ว่าจ้างตกลงให้ค่าจ้าง เป็นเงินจำนวน 100,000 บาท เมื่อทราบข้อมูลดังนั้น เจ้าพนักงานตำรวจชุดจับกุม จึงได้แจ้งข้อกล่าวหากับ นายวณิชัย แซ่ท่อ   ว่า “ จำหน่ายโดยการมีไว้เพื่อจำหน่ายซึ่งยาเสพติดให้โทษประเภท 1 (เมทแอมเฟตามีนหรือยาบ้า) โดยฝ่าฝืนต่อกฎหมายอันเป็นการทำให้เกิดผลกระทบต่อความมั่นคง ของรัฐหรือความปลอดภัยของประชาชนทั่วไป ” พร้อมทั้งได้แจ้งสิทธิตามกฎหมายให้ ผู้ต้องหา ทราบดังนี้ 1.สิทธิจะให้การหรือไม่ให้การก็ได้และถ้อยคำของของผู้ต้องหาอาจใช้เป็นพยานหลักฐานในการพิจารณาคดีได้ ๒.สิทธิพบและปรึกษาทนายความหรือผู้ซึ่งจะเป็นทนายความ ๓.สิทธิจะแจ้งให้ญาติหรือบุคคลที่ผู้ต้องหา ไว้วางใจให้ทราบถึงการจับกุมที่สามารถดำเนินการได้โดยสะดวกหากไม่เป็นการขัดขวางแห่งการจับหรือการควบคุมผู้ต้องหา หรือทำให้เกิดความไม่ปลอดภัยแก่บุคคลอื่นบุคคลใด และแจ้งให้ นายวณิชัย แซ่ท่อ ผู้ต้องหา ทราบตามประมวลกฎหมายยาเสพติด พ.ศ.2564  มาตรา 153 ให้ทราบว่า “ถ้าศาลเห็นว่าผู้กระทำความผิดผู้ใดได้ให้ข้อมูลที่สำคัญและเป็นประโยชน์อย่างยิ่งในการปราบปรามการกระทำความผิดเกี่ยวกับยาเสพติดต่อเจ้าพนักงาน ปปส. หรือพนักงานฝ่ายปกครอง หรือตำรวจซึ่งเป็นผู้จับกุม หรือพนักงานสอบสวนในคดีนั้น เมื่อพนักงานอัยการระบุในคำฟ้องหรือยื่นคำร้องต่อศาล ศาลจะลงโทษผู้นั้นน้อยกว่าอัตราโทษที่กฎหมายกำหนดไว้สำหรับความผิดนั้นก็ได้” ในชั้นจับกุมผู้ต้องหาทราบ และเข้าใจข้อกล่าวหา และสิทธิดังกล่าวข้างต้นเป็นอย่างดีแล้ว จากนั้น จึงได้ควบคุมตัวผู้ต้องหาพร้อมของกลาง มาที่ กก.2 บก.สกส.บช.ปส. ต.เชียงรากน้อย อ.บางปะอิน          จว.พระนครศรีอยุธยา เพื่อดำเนินการจัดทำบันทึกการจับกุม , บันทึกอื่นๆ ที่เกี่ยวข้อง พร้อมทั้งนำยาบ้าของกลางบางส่วนตรวจสอบด้วยน้ำยาเคมีมาร์ควิส ให้ผลทำปฏิกิริยากับยาบ้า เปลี่ยนเป็นสีสมและน้ำตาลตามลำดับ น่าเชื่อว่าเป็นยาบ้าจริง ต่อหน้าผู้ต้องหา ได้ประสานงานให้เจ้าพนักงานตำรวจพิสูจน์หลักฐาน ดำเนินการจัดเก็บหลักฐานทางนิติวิทยาศาสตร์ จากหีบห่อบรรจุยาเสพติดของกลาง และ ของกลางอื่นๆ เพื่อประกอบการดำเนินคดีกับผู้กระทำความผิด ต่อไป ในชั้นจับกุม นายวณิชัย แซ่ท่อ ผู้ต้องหา ได้ให้การรับว่า ข้าฯ ชื่อนายวณิชัย แซ่ท่อ เลขบัตรประชาชน 5550101071562 อายุ 51 ปี ที่อยู่ 158 หมู่ที่ 6 ต.สะเนียน อ.เมืองน่าน จว.น่าน ใช้โทรศัพท์มือถือ หมายเลขเบอร์โทร 0973208662 และโทรศัพท์มือถือ หมายเลขเบอร์โทร 0926100397 อาชีพทำไร่ข้าวโพด รายได้ต่อปี 200,000 – 400,000 บาท ให้การรับสารภาพว่าในคดีนี้ตนได้รับการว่าจ้างจากนายวัฒนา พรสุขรันดร เลขประจำตัวประชาชน 5570400030949 ที่อยู่ 49 หมู่ 17 ต.ตับเต่า อ.เทิง จ.เชียงราย ใช้โทรศัพท์มือถือ หมายเลข 0970177885 ซึ่งนายวณิชัย แซ่ท่อ บันทึกชื่อไว้ในเครื่องว่า “Mua D” และหมายเลขเบอร์โทร 0984060709 ซึ่งนายวณิชัย แซ่ท่อ บันทึกชื่อไว้ในเครื่องว่า “Muas,”ใช้รถยนต์ หมายเลขทะเบียน 3ขฐ 8541 กรุงเทพมหานคร ว่าจ้างให้ลำเลียงยาเสพติดของกลางจำนวน 160,000 เม็ด ดังกล่าวจากพื้นที่รอยต่อ อ.เทิง จว.เชียงราย และ อ.เมืองเชียงราย จว.เชียงราย มาส่งมอบให้กับลูกค้าตามสั่งการของนายวัฒนา    พรสุขรันดร ในพื้นที่ อ.เมืองตาก จว.ตาก โดยจะให้ค่าจ้างเป็นเงินจำนวน 100,000 บาท เมื่อสามารถลักลอบลำเลียงยาบ้าของกลางส่งมอบให้กับผู้รับปลายทางสำเร็จ โดยนายวัฒนา พรสุขรันดร จัดหารถยนต์ที่ใช้ในการลำเลียงยาเสพติด ดังกล่าว เป็นรถยนต์นั่งส่วนบุคคลไม่เกิน 7 คน ยี่ห้อ TOYOTA รุ่น HILUX REVO สีขาว หมายเลขทะเบียน 3ขก 8984 กรุงเทพมหานคร ซึ่งรถยนต์ดังกล่าวมีชื่อนายวัฒนา พรสุขรันดร ที่อยู่ 49/2 หมู่ 17 ตำบลตับเต่า อำเภอเทิง จังหวัดเชียงราย เป็นผู้ครอบครอง ต่อมาเมื่อวันที่ 22 ธ.ค.65 เวลาประมาณ 06.00 น. นายวัฒนา พรสุขรันดร ได้ติดต่อมายังนายวณิชัย แซ่ท่อ ผู้ต้องหาให้เดินทางไปขับรถยนต์ หมายเลขทะเบียน 3ขก 8984 กรุงเทพมหานคร ซึ่งใช้ซุกซ่อนและลำเลียงยาเสพติด และจอดอยู่ริมถนนสายเทิง-เชียงราย หมายเลขถนน 1020 ก่อนถึงศาลเจ้าพ่อม่อนแดง เชียงเคี่ยน ตำบล เชียงเคี่ยน อำเภอ เทิง จังหวัด เชียงราย (ระยะจากห่างจากที่พักประมาณ 30-40 กม.) ก่อนที่จะมารับงานขนลำเลียงยาเสพติด นายวณิชัย แซ่ท่อ ได้เปิดรีสอร์ทพักอยู่ที่ภูชี้ฟ้า อ.เทิง จว.เชียงราย (จดจำชื่อรีสอร์ทไม่ได้) เพื่อรอรับว่าจ้างขนลำเลียงยาเสพติดให้กับนายวัฒนา พรสุขรันดร จากนั้นช่วงเวลาประมาณ 07.00 น. ได้มีชายไม่ทราบชื่อ อายุ 14-15 ปี ซึ่งเป็นลูกน้องของนายวัฒนา พรสุขรันดร ขับขี่รถจักรยานยนต์ ไม่สามารถจดจำทะเบียน สี และยี่ห้อได้ มารับนายวณิชัย แซ่ท่อ ที่รีสอร์ท ภูชี้ฟ้า อ.เทิง จว.เชียงราย หลังจากนั้นได้พานายวณิชัย แซ่ท่อ มารับรถยนต์ หมายเลขทะเบียน 3ขก 8984 กรุงเทพมหานคร ซึ่งใช้ซุกซ่อนและลำเลียงยาเสพติด ซึ่งจอดอยู่บริเวณในป่าต้นสักริมถนนริมถนนสายเทิง-เชียงราย ห่างจากที่พักประมาณ 30-40 กม. เมื่อนายวณิชัย แซ่ท่อ มาถึงพบรถยนต์ ดังกล่าวจอดอยู่ในป่าต้นสัก และลูกน้องของนายวัฒนา พรสุขรันดร แจ้งว่าได้นำเงินสดจำนวน 5,000 บาท วางไว้บริเวณช่องเกียร์รถยนต์ เพื่อเป็นค่าใช้จ่ายในการเดินทาง หลังจากที่ได้รับมอบรถยนต์ หมายเลขทะเบียน 3ขก 8984 กรุงเทพมหานคร ซึ่งใช้ซุกซ่อนและลำเลียงยาเสพติด นายวณิชัย แซ่ท่อ ได้ขับรถยนต์ ใช้ถนนสาย อ.เทิง - อ.แม่ลอยไร่ จว.เชียงราย - อ.จุน - อ.เมืองพะเยา - อ.งาว จว.ลำปาง - อ.สอง - อ.ลอง - อ.วังชิ้น จว.แพร่ – อ.ศรีสัชนาลัย จว.สุโขทัย ซึ่งเส้นทางดังกล่าวเป็นเส้นทางที่หลบเจ้าหน้าที่ตำรวจ จนกระทั่งถูกเจ้าหน้าที่ตำรวจเข้าทำการสกัดกั้นรถยนต์ พร้อมของกลางในที่เกิดเหตุ และได้ให้การรับเพิ่มเติมว่า ก่อนหน้านี้ประมาณวันที่ 16 ธ.ค.65 นายวณิชัย แซ่ท่อ ใช้รถยนต์นั่งส่วนบุคคลไม่เกิน 7 คน ยี่ห้อ TOYOTA รุ่น HILUX REVO สีขาว หมายเลขทะเบียน 3ขก 8984 กรุงเทพมหานคร สำรวจเส้นทางร่วมกับลูกน้องของนายวัฒนา พรสุขรันดร โดยใช้เส้นทาง ถนนสาย อ.เทิง - อ.แม่ลอยไร่ จว.เชียงราย - อ.จุน - อ.เมืองพะเยา -      อ.งาว จว.ลำปาง - อ.สอง - อ.ลอง - อ.วังชิ้น จว.แพร่ – อ.ศรีสัชนาลัย จว.สุโขทัย เป็นความจริง เพื่อประโยชน์ในการสืบสวนขยายผลการจับกุมเครือข่ายยาเสพติดคดีนี้ พ.ต.ต.อดิสรณ์  อักษร  สว.กก.2 บก.สกส.บช.ปส. เจ้าพนักงาน ป.ป.ส. เลขที่ 562950  พร้อมพวก จึงใช้อำนาจเจ้าพนักงาน ป.ป.ส. ควบคุมตัวไว้มีกำหนด      ไม่เกิน ๓ วัน เพื่อทำการ สอบสวนขยายผลก่อนนำตัวส่งพนักงานสอบสวนต่อไป จากนั้นได้นำผู้ต้องหา พร้อมของกลาง ส่งพนักงานสอบสวน  บก.ปส.3 บช.ปส.  ดำเนินคดีกับผู้กระทำความผิดในคดีนี้ ต่อไป ได้อ่านบันทึกการจับกุม และบันทึกอื่นๆ ที่เกี่ยวข้องให้ ผู้เกี่ยวข้อง  ฟังและให้อ่านเองเข้าใจข้อความในบันทึกการจับกุมนี้เป็นอย่างดี และรับว่าถูกต้องตรงตามความจริงทุกประการ ฟังแล้ว เข้าใจรับรองว่าถูกต้องตรงตามความจริง จึงให้ลงลายมือชื่อไว้เป็นหลักฐาน อนึ่งในการจับกุมครั้งนี้ เจ้าพนักงานตำรวจทุกนาย ได้กระทำไปตามอำนาจหน้าที่ มิได้บังคับ ขู่เข็ญ หลอกลวง หรือทำให้ผู้ใดได้รับอันตรายแก่กายหรือจิตใจมิได้เรียกร้องทรัพย์สินหรือยึดทรัพย์ไปเพื่อประโยชน์ส่วนตนแต่อย่างใด และมิได้ทำให้ทรัพย์สินของผู้ใดสูญหายเสียหาย เสื่อมค่า หรือ ไร้ประโยชน์ แต่อย่างใด  (ลงชื่อ)..........................................................ผู้ต้องหา / ได้รับสำเนาบันทึกจับกุมไว้แล้ว ( นายวณิชัย แซ่ท่อ )  (ลงชื่อ)..............................................................ผู้จับกุม            (ลงชื่อ).....................................................ผู้จับกุม (ลงชื่อ)..............................................................ผู้จับกุม            (ลงชื่อ).....................................................ผู้จับกุม (ลงชื่อ)..............................................................ผู้จับกุม            (ลงชื่อ).....................................................ผู้จับกุม (ลงชื่อ)..............................................................ผู้จับกุม            (ลงชื่อ).....................................................ผู้จับกุม (ลงชื่อ)..............................................................ผู้จับกุม            (ลงชื่อ).....................................................ผู้จับกุม (ลงชื่อ)..............................................................ผู้จับกุม            (ลงชื่อ).....................................................ผู้จับกุม (ลงชื่อ)..............................................................ผู้จับกุม            (ลงชื่อ).....................................................ผู้จับกุม (ลงชื่อ)..............................................................ผู้จับกุม            (ลงชื่อ).....................................................ผู้จับกุม (ลงชื่อ)..............................................................ผู้จับกุม            (ลงชื่อ).....................................................ผู้จับกุม (ลงชื่อ)..............................................................ผู้จับกุม            (ลงชื่อ).....................................................ผู้จับกุม (ลงชื่อ)..............................................................ผู้จับกุม            (ลงชื่อ).....................................................ผู้จับกุม (ลงชื่อ)..............................................................ผู้จับกุม            (ลงชื่อ).....................................................ผู้จับกุม (ลงชื่อ)..............................................................ผู้จับกุม            (ลงชื่อ).....................................................ผู้จับกุม (ลงชื่อ)..............................................................ผู้จับกุม            (ลงชื่อ).....................................................ผู้จับกุม (ลงชื่อ)..............................................................ผู้จับกุม            (ลงชื่อ).....................................................ผู้จับกุม (ลงชื่อ)..............................................................ผู้จับกุม            (ลงชื่อ).....................................................ผู้จับกุม (ลงชื่อ)..............................................................ผู้จับกุม            (ลงชื่อ).....................................................ผู้จับกุม (ลงชื่อ)..............................................................ผู้จับกุม            (ลงชื่อ).....................................................ผู้จับกุม (ลงชื่อ)..............................................................ผู้จับกุม            (ลงชื่อ).....................................................ผู้จับกุม (ลงชื่อ)..............................................................ผู้จับกุม            (ลงชื่อ).....................................................ผู้จับกุม (ลงชื่อ)..............................................................ผู้จับกุม            (ลงชื่อ).....................................................ผู้จับกุม (ลงชื่อ)..............................................................ผู้จับกุม            (ลงชื่อ).....................................................ผู้จับกุม (ลงชื่อ)..............................................................ผู้จับกุม            (ลงชื่อ).....................................................ผู้จับกุม (ลงชื่อ)..............................................................ผู้จับกุม            (ลงชื่อ).....................................................ผู้จับกุม (ลงชื่อ)..............................................................ผู้จับกุม/บันทึก/อ่าน",
#         "วัน/เดือน/ปี ที่จับกุม": "วันที่ 23 ธันวาคม 2565 เวลาประมาณ 00.30 น.",
#         "วัน/เดือน/ปี ที่บันทึก": "วันที่ 23 ธันวาคม 2565 เวลาประมาณ 13.00 น.",
#         "ศอ.ปส.ตร.": "การอำนวยการ พล.ต.อ.ชินภัทร สารสิน รอง ผบ.ตร.(กม)/ผอ.ศอ.ปส.ตร., พล.ต.ท.ประจวบ วงศ์สุข ผช.ผบ.ตร./รอง ผอ.ศอ.ปส.ตร",
#         "สถานที่ทำการบันทึก": "กก.2 บก.สกส.บช.ปส. ต.เชียงรากน้อย อ.บางปะอิน จว.พระนครศรีอยุธยา",
#         "สถานที่เกิดเหตุ / จับกุม": "บริเวณริมถนนสี่แยกสารจิตร ถนนหมายเลข 102 ต.สารจิตร อ.ศรีสัชนาลัย จว.สุโขทัย เมื่อวันที่ 23 ธันวาคม 2565 เวลาประมาณ 00.30 น.",
#         "สำนักงาน ป.ป.ส.": "การอำนวยการ นายวิชัย ไชยมงคล เลขาธิการ ป.ป.ส., นายธนกร คัยนันท์ รองเลขาธิการ ป.ป.ส., นายมานะ ศิริพิทยาวัฒน์ รองเลขาธิการ ป.ป.ส., นายปิยะศิริ วัฒนวรางกูร รองเลขาธิการ ป.ป.ส., นายปฤณ เมฑานันท์ ผอ.สปป. , นายวงศ์สว่าง แดงสนั่น ผอ.ปป.8",
#         "สำนักงานตำรวจแห่งชาติ": "ภายใต้การอำนวยการ พล.ต.อ.ดำรงศักดิ์ กิตติประภัสร์ ผบ.ตร.",
#         "สำนักงานศุลกากรภาคที่ 3": "โดย นายดิเรก คชารักษ์ ผู้อำนวยการสำนักงานศุลกากรภาคที่ 3  , นายบุญรอด เขจรานนท์ , นายพงศกร ละฟู่ , นายอรรถกร อ่อนชูศรี",
#         "เจ้าพนักงาน ป.ป.ส. สปป.": "น.ส.ปิยมาพร นามวงษ์ นักสืบสวนสอบสวนชำนาญการ , นายบรรพต เปรมวิจิตร นักสืบสวนสอบสวนชำนาญการ และ นายภาสกร รอยอินทรัตน์ นักสืบสวนสอบสวนชำนาญการ , นายกิตติพงศ์ เกษมสิน นักสืบสวนสอบสวนชำนาญการ",
#         "เจ้าพนักงานงานตำรวจ ศูนย์วิเคราะห์ข่าวยาเสพติดกรุงเทพ บก.ขส.บช.ปส.": "พ.ต.อ.อุดมรัตน์ อิทธิโสภาพันธุ์ ผกก.กลุ่มงานการข่าว, พ.ต.ท.ธีรยุทธ อ่ำโพธิ์ รอง ผกก.กลุ่มงานการข่าว, พ.ต.ท.อำนาจ สุขจิต, พ.ต.ท.กฤษณพงษ์ เตมีย์สุวรรณ, พ.ต.ต.วรวัตต์ อุดรรัตนา, พ.ต.ต.จิรวัฒน์ ภูงามตา สว.กลุ่มงานการข่าว, ร.ต.อ.ปรียากร เสนาหนอก, ร.ต.อ.วันชัย ชูศักดิ์, ร.ต.อ.เจริญศักดิ์ จรุงกิจสุวรรณ, ร.ต.อ.ธัญพีรสิษฐ์ จุลพิภพ, ร.ต.อ.ธนกร อธิสุขเมธา รอง สว.กลุ่มงานการข่าว, ด.ต.วราวุฒิ วัฒนมาลา, ด.ต.อชิตพล ปะตังเวสา, ด.ต.หญิง ลาวัณย์ ปันเขื่อนขัติ, ด.ต.หญิง นารี อ้นมี, ส.ต.อ.สัณฐิติ ภู่บุบผา, ส.ต.อ.พุฒิพงศ์ เผ่าพันธุ์เจริญ, ส.ต.อ.ชาญชัย จันทร์หอม, ส.ต.อ.จักรพงษ์ เรืองจันทร์, ส.ต.ท.พลาวัสภ์ อุทัยวัฒน์, ส.ต.ต.เจษฎา ตั้นเส้ง ผบ.หมู่ กลุ่มงานการข่าว",
#         "เจ้าพนักงานงานตำรวจ ศูนย์วิเคราะห์ข่าวยาเสพติดเชียงใหม่ บก.ขส.บช.ปส.": "พ.ต.อ.โชคชัย วระศาสตร์  ผกก.กลุ่มงานการข่าว บก.ขส.บช.ปส., พ.ต.ท.ประเทือง  แตงอ่อน รอง ผกก.กลุ่มงานการข่าว บก.ขส.บช.ปส.,  พ.ต.ท.ธีรสิทธิ  วิสุทธสิน,ร.ต.อ.ศุภชัย แต้มแก้ว , ร.ต.ท.เอกภพ  บัวฉ่ำ ,ว่าที่ ร.ต.ต.ธนกฤต หงษ์ฤทัย รอง สว.กลุ่มงานการข่าว บก.ขส.บช.ปส.,ด.ต.ชยาพล  รักษาดี, ด.ต.ชุมพล  ถาวรเรืองฤทธิ์, ด.ต.พจน์  ทองอินทร์, ด.ต.พิทักษ์สันติ  บุญเสนอ, ด.ต.เอกฤทัย  เอี่ยมสะอาด, ด.ต.พิเชษฐ  ดวงเกิด, ด.ต.เอกชาย  คำมูล, ด.ต.หญิง ศรีไพร  โศณณายะ, ด.ต.หญิง คชาภรณ์  สังข์ศรี, ด.ต.หญิง ภาวนา  หงษ์ทอง  ผบ.หมู่ กลุ่มงานการข่าว บก.ขส.บช.ปส.",
#         "เจ้าพนักงานชุดจับกุม": "",
#         "เจ้าพนักงานตำรวจ กก.3 บก.สกส.บช.ปส.": "พ.ต.อ.บุญส่ง สนธยานานนท์ , พ.ต.ท.กุลวิช หลวงวรรณา , พ.ต.ท.มารุต วงษ์พูล , พ.ต.ท.หญิง อัญชลี เนตรมุกดา พ.ต.ท.ฉัตรชัย รักฉ่ำพงษ์ , พ.ต.ต.เดชชาติ จักจังหรีด , พ.ต.ต.พฤกษ์ ธนรักษ์โยธิน , ร.ต.อ.พสิษฐ์ ชูศรี , ร.ต.อ.อภิสิทธิ์   พลขันธ์ , ร.ต.อ.ดนัย เต๋จ๊ะใหม่ , ร.ต.อ.โอฬาร มีผลกิจ , ร.ต.อ.หญิง ชุติกาญจน์ ธนวัฒน์กิตติกุล , ร.ต.ท.สุรศักดิ์ วงศ์ใหญ่ ร.ต.ต.หญิง วงค์จันทร์ ม่วงทอง , ร.ต.ต.สุริยัน กองมา ,ร.ต.ต.วิรุษ  แก้วรากมุข , ด.ต.เด่นศักดิ์ ปัญญาวัน , ด.ต.อำนวย เรืองจิต , ด.ต.วีรชน วชิรภักดี , ด.ต.รัชวิศน์ ฟักแก้ว , ด.ต.กำธร ทาระบุตร , ด.ต.อิทธิพัฒน์ จันต๊ะ, ด.ต.ประคอง แปงโนจา ด.ต.ธีรวิศท์  ชุ่มมะโน , ด.ต.มนัส  ไชยสาร , ด.ต.นครินทร์  สุทธพันธ์ , ด.ต.ชนะศึก ขุนทอง , ด.ต.ฤทธิไกร ใจกว้าง ,      ด.ต.จตุรงค์  กำยาน , ด.ต.ชัยพิสิษฐ์ ทานันชัยสกุล , ด.ต.สมคิด บุญเรืองศรี , ด.ต.พรชัย นีระพจน์ , ด.ต.ยงยุทธ สุทธิกุลชัย ด.ต.นริศ งามวงษ์ , ด.ต.หญิง  อลิสา มังฉกรรจ์ , ส.ต.อ.อภิศักดิ์ อิศรี , ส.ต.อ.ชัยณรงค์ ชุ่มเชย , ส.ต.อ.ประพาส         สายธิไชย , ส.ต.อ.ณัฐชา ปั้นพิพัฒน์",
#         "เจ้าพนักงานตำรวจ กก.๑ บก.สกส.บช.ปส.": "พ.ต.อ.ไพฑูรย์  งามลาภ , พ.ต.ท.ประสงค์ พันธ์สวัสดิ์ , พ.ต.ท.มงคล ออมทรัพย์ , พ.ต.ท.สุภเวช มั่งคั่ง ,          พ.ต.ท.ชินธันย์  จิตติพัทธพงศ์ , พ.ต.ต.สุระ บุตรสืบสาย , พ.ต.ต.พุทธพงษ์  กุลโท , ร.ต.อ.อำนวย กาญจนโพชน์ ,       ร.ต.อ.มนตรี  เฉลิมวัฒน์ ,  ร.ต.อ.ทศพล  รอดสงค์ , ร.ต.อ.หญิง วราลักษณ์  อุ่มอ่อนศรี , ร.ต.อ.หญิง ยูศิริ  แน่นชารี , ร.ต.อ.อาทิตย์ ฟังเย็น , ร.ต.ต.พงษ์พุทธะ เส็งไสวบุญมา , ร.ต.ต.นรินทร์ ดวงดี, ด.ต.สัมพันธ์ ปานบ้านเกร็ด, ด.ต.อรุณ      ยูงทอง , ด.ต.สรายุทธ มีมาก , ด.ต.หญิง ศจิกา อินทร์ไชยมาศ , ด.ต.หญิงรุจิรา ไกรนรา , ด.ต.หญิง อุไรรัตน์ ตันศรีนุกูล ,ด.ต.อายุทธ เป้าทอง ,ด.ต.คมคาย มีก่ำ ,ด.ต.พิสิฐชัย ชาติเวช , จ.ส.ต.ภานุเดช เยี่ยมมโน , ส.ต.อ.อธิภัทร ธาดาสิริสกุล ,    ส.ต.อ.จิรวัฒน์  คงทัพ , ส.ต.อ.วราวุฒิ แก้วขาว,ส.ต.อ.จักรินทร์  สายแก้ว ,ส.ต.อ.คุณากร จันทมุณี , ส.ต.อ.พงศธร เนตรเขมา, ส.ต.ท.ณัชพล รัตนบุรี , ส.ต.ท.อนิรุจ รีเรียบ , ส.ต.ท.ทัตธน สุจิตโต",
#         "เจ้าพนักงานตำรวจ กก.๒ บก.สกส.บช.ปส.": "พ.ต.อ.ประสงค์ ศิริทิพย์วาณิช รอง ผบก.สกส.บช.ปส. รรท.ผกก.2 บก.สกส. , พ.ต.ท.พิทยา  สองเมือง ,         พ.ต.ท.ถนัดกิจ  ตั้งมานะสกุล , พ.ต.ต.อดิสรณ์  อักษร , พ.ต.ต.ชัยนิวัฒน์  เพชรทรัพย์สกุล , ร.ต.อ.สนาม  โพธิ์วิเศษ ,     ร.ต.อ.เตชินท์ แก้วเจือ , ร.ต.อ.บรรเจิด คุณากรวงศ์ ,ร.ต.อ.อดิศร  ไชยสงคราม ร.ต.อ.คมสันต์ วรทรัพย์ , ร.ต.อ.ครรชิต เจริญพันธ์ , ร.ต.อ.หญิง พนัชกร  ทองแถม , ร.ต.ท.ชนินทร์ รามณี , ร.ต.ท.เจษฎา เย็นวัฒนา , ว่าที่ ร.ต.ต.เทียนชัย  ชูพูน , ว่าที่ ร.ต.ต.พันธุ์ศักดิ์  ใจภักดี ,  ด.ต.ธนภัทร  ศรีวงษา , ด.ต.อาทิตย์  ป้องหล้า  , ด.ต.รักพงษ์  จันทร์มา , ด.ต.ทศพร  ศรีลิโก , ด.ต.บุญรัตน์  รุ่งธรรม, ด.ต.ทรงเมือง  จิตรกลาง, ด.ต.ก้อง  เรืองนุช , ด.ต.หญิง ชญานิศ  ยุทธมานพ , ด.ต.สมเกียรติ์   ผ่องศาลา ,จ.ส.ต.วิรัตน์  แสงอาจ , จ.ส.ต.สิทธิชัย  หนูฟุ่น , จ.ส.ต.กฤติกร  อุทัยชิต , จ.ส.ต.ทศพร  น้อยนอนเมือง , ส.ต.อ.องอาจ  โวหารลึก ส.ต.อ.วิรุฬห์  พันธ์สีมา , ส.ต.อ.ธวัชชัย โสวะพันธ์ , ส.ต.อ.วีรพล  วรรณสัมผัส , ส.ต.อ.มธิดล  เม่นเผือก ,ส.ต.อ.ทินกร  ชูคำมั่น , ส.ต.อ.พงษ์สันต์  พลราชม",
#         "เจ้าพนักงานตำรวจ บช.ปส.": "การอำนวยการ พล.ต.ท.สรายุทธ สงวนโภคัย ผบช.ปส., พล.ต.ต.นพดล ศรสำราญ, พล.ต.ต.จิระวัฒน์ พยุงธรรม, พล.ต.ต.พรพิทักษ์ รู้ยืนยง , พล.ต.ต.บรรพต มุ่งขอบกลาง รอง ผบช.ปส., พล.ต.ต.พลัฏฐ์ วิเศษสิงห์ ผบก.สกส.บช.ปส., พล.ต.ต.เอกภพ อินทวิวัฒน์ ผบก.ขส.บช.ปส., พ.ต.อ.วัสสา วัสสานนท์ , พ.ต.อ.อิทธิพล จันทร์ศรีบุตร , พ.ต.อ.ประสงค์ ศิริทิพย์วานิช รอง ผบก.สกส.บช.ปส. , พ.ต.อ.วันชนะ บวรบุญ , พ.ต.อ.หญิง บุศรา จงรักชอบ รอง ผบก.ขส.บช.ปส.",
#         "เจ้าพนักงานตำรวจศูนย์วิเคราะห์ข่าวยาเสพติดอุดรธานี บก.ขส.บช.ปส.": "พ.ต.อ.สาคร เจิมขุนทด ผกก.กลุ่มงานการข่าวฯ , พ.ต.ต.อุดมการ บุตรเกตุ  สว.กลุ่มงานการข่าวฯ , ร.ต.อ.สุวิทย์ แสนแก้ว  รอง สว.กลุ่มงานการข่าวฯ , ด.ต.ฐานิต กัณหา , ด.ต.ทักษิณ กะสังข์ , ส.ต.อ.อนุชาติ บุราณเดช , ส.ต.อ.จักราวุฒิ บรรยง  ผบ.หมู่ กลุ่มงานการข่าว",
#         "โดยกล่าวหาว่า": "จำหน่ายยาเสพติดให้โทษประเภท 1 (เมทแอมเฟตามีนหรือยาบ้า) การมีไว้เพื่อจำหน่าย ฝ่าฝืนต่อกฎหมายอันเป็นการทำให้เกิดผลกระทบต่อความมั่นคงของรัฐหรือความปลอดภัยของประชาชนทั่วไป ”",
#         "ได้ทำการตรวจยึดเอกสาร ไว้เพื่อประกอบคดี": "จำนวน 4 รายการ  1. ตารางกรมธรรม์ประกันภัยคุ้มครองผู้ประสบภัยจากรถ ของบริษัท ไอโออิ กรุงเทพ ประกันภัย จำกัด (มหาชน) กรมธรรม์ประกันภัยเลขที่ : 1220133542264 ระบุชื่อผู้เอาประกันภัย คุณวัฒนา พรสุขรันดร ที่อยู่ 49 หมู่ 17 ต.ตับเต่า  อ.เทิง จ.เชียงราย จำนวน 1 แผ่น ตรวจยึดได้จากรถยนต์ หมายเลขทะเบียน 3ขก 8984 กรุงเทพมหานคร 2. ใบตรวจสอบการส่งมอบรถยนต์ใหม่ ชื่อลูกค้า นายวัฒนา พรสุขรันดร ที่อยู่ 49 หมู่ 17 ต.ตับเต่า อ.เทิง        จ.เชียงราย จำนวน 1 แผ่น ตรวจยึดได้จากรถยนต์ หมายเลขทะเบียน 3ขก 8984 กรุงเทพมหานคร 3. หนังสือรับรองการจำหน่ายรถยนต์ ของบริษัทโตโยต้าเชียงราย จำกัด ให้กับนายวัฒนา พรสุขรันดร ลงวันที่    23 เม.ย.2565 จำนวน 1 แผ่น ตรวจยึดได้จากรถยนต์ หมายเลขทะเบียน 3ขก 8984 กรุงเทพมหานคร 4. สำเนารายการจดทะเบียน รถยนต์นั่งส่วนบุคคลไม่เกิน 7 คน ยี่ห้อ TOYOTA รุ่น HILUX REVO สีขาว หมายเลขทะเบียน 3ขก 8984 กรุงเทพมหานคร จำนวน 1 แผ่น ตรวจยึดได้จากรถยนต์ หมายเลขทะเบียน 3ขก 8984 กรุงเทพมหานคร",
#         "ได้ร่วมกันจับกุมตัวผู้กระทำความผิดเกี่ยวกับยาเสพติดให้โทษ 1 ราย": "จำนวน 1 คน คือ นายวณิชัย แซ่ท่อ เลขบัตรประจำตัวประชาชน  5550101071562 เกิดเมื่อวันที่ 10 เมษายน 2514 อายุ 51 ปี  ที่อยู่ 158 หมู่ 6 ตำบลสะเนียน อำเภอเมือง จังหวัดน่าน"
#     }

# pprint(norm_key(d)['out_of_scope'])