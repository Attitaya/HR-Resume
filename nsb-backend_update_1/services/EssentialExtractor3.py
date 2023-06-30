import re
class EssentialExtractor():
    def find_header_value(self, patterns, dict, output_dict={}):
        for keys in dict.keys():
            text = keys
            for pattern in patterns:
                match = re.search(pattern, text)
                if match and match.group(0) != '' :
                    if text =='พฤติการณ์ในการจับกุม':
                        output_dict[match.group(0)] = dict[text].split("(ลงชื่อ)")[0]
                    else:
                        output_dict[match.group(0)] = dict[text]
        return output_dict

    def extract(self, dict):
        header_patterns = [
        r"(?:สถานที่บันทึก|สถานที่ทำการบันทึก)?",
        r"(?:วัน[/ ]เดือน[/ ]ปี ?เวลา?ที่?บันทึก|วัน[/ ]เดือน[/ ]ปี ที่บันทึก|วัน[/ ]เดือน[/ ]ปี ?เวลา? บันทึก)?",
        r"(?:วัน[/ ]เดือน[/ ]ปี ?เวลา?ที่?จับกุม|วัน[/ ]เดือน[/ ]ปี ที่จับกุม|วัน[/ ]เดือน[/ ]ปี ?เวลา? จับกุม|วัน[/ ]เดือน[/ ]ปี ตรวจค้น[/ ]จับกุม)?",
        r"(?:สถานที่จับกุม / เกิดเหตุ|สถานที่เกิดเหตุ / จับกุม|สถานที่จับกุม)?",
        r"(?:สถานที่จับกุม / เกิดเหตุ|สถานที่เกิดเหตุ / จับกุม|สถานที่เกิดเหตุ)?",
        r"ได้ร่วมกัน(?:.*(?:จับกุมตัว|ทำการจับกุมตัว|ทำการจับกุม).*)",
        r"พร้อม(?:ด้วย)?ของกลาง(?:ดังนี้)?",
        r"(?:โดยกล่าวหาว่า)?",
        #r"(?:พฤติการณ์ในการจับกุม|พฤติการณ์ในการตรวจค้นและจับกุม)?"
        ]
        output_dict = self.find_header_value(header_patterns, dict)
        return output_dict