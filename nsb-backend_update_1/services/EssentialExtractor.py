import re
class EssentialExtractor():
    def find_header_value(self, patterns, dict, output_dict={}):
        for pattern in patterns:
            for text in dict.keys():
                match = re.search(pattern, text)
                if match and match.group(0) != '':
                    if match.group(0) in dict:
                        new_header = match.group(0)
                        new_header = re.sub('/',' ', new_header)
                        if new_header == 'พฤติการณ์ในการจับกุม':
                            output_dict[new_header] = dict[text].split("(ลงชื่อ)")[0]
                        else:
                            output_dict[new_header] = dict[text]
                    else:
                        output_dict[match.group(0)] = ""
        return output_dict

    def extract(self, dict):
        header_patterns = [
        r"(?:สถานที่บันทึก|สถานที่ทำการบันทึก)",
        r"(?:วัน[/ ]เดือน[/ ]ปี ?เวลา?ที่?บันทึก|วัน[/ ]เดือน[/ ]ปี ที่บันทึก|วัน[/ ]เดือน[/ ]ปี ?เวลา? บันทึก)",
        r"(?:วัน[/ ]เดือน[/ ]ปี ?เวลา?ที่?จับกุม|วัน[/ ]เดือน[/ ]ปี ที่จับกุม|วัน[/ ]เดือน[/ ]ปี ?เวลา? จับกุม|วัน[/ ]เดือน[/ ]ปี ตรวจค้น[/ ]จับกุม)",
        r"(?:สถานที่จับกุม / เกิดเหตุ|สถานที่เกิดเหตุ / จับกุม|สถานที่จับกุม)",
        r"(?:สถานที่จับกุม / เกิดเหตุ|สถานที่เกิดเหตุ / จับกุม|สถานที่เกิดเหตุ)",
        r"วัน เดือน ปี และสถานที่เกิดเหตุ",
        r"ได้ร่วมกัน(?:จับกุมตัว|ทำการจับกุมตัว)",
        r"(?:พร้อมของกลาง|พร้อมด้วยของกลาง)",
        r"(?:โดยกล่าวหาว่า)",
        #r"(?:พฤติการณ์ในการจับกุม)"
        ]
        output_dict = self.find_header_value(header_patterns, dict)
        return output_dict
    
    def __pattern_to_norm(self):
        return [
        r"(?:สถานที่บันทึก|สถานที่ทำการบันทึก)",
        r"(?:วัน[/ ]เดือน[/ ]ปี ?เวลา?ที่?บันทึก|วัน[/ ]เดือน[/ ]ปี ที่บันทึก|วัน[/ ]เดือน[/ ]ปี ?เวลา? บันทึก)",
        r"(?:วัน[/ ]เดือน[/ ]ปี ?เวลา?ที่?จับกุม|วัน[/ ]เดือน[/ ]ปี ที่จับกุม|วัน[/ ]เดือน[/ ]ปี ?เวลา? จับกุม|วัน[/ ]เดือน[/ ]ปี ตรวจค้น[/ ]จับกุม)",
        r"(?:สถานที่จับกุม / เกิดเหตุ|สถานที่เกิดเหตุ / จับกุม|สถานที่จับกุม)",
        r"(?:สถานที่จับกุม / เกิดเหตุ|สถานที่เกิดเหตุ / จับกุม|สถานที่เกิดเหตุ)",
        r"วัน เดือน ปี และสถานที่เกิดเหตุ",
        r"ได้ร่วมกัน(?:จับกุมตัว|ทำการจับกุมตัว)(?=\p{Z}|$)",
        r"(?:พร้อมของกลาง|พร้อมด้วยของกลาง)",
        r"(?:โดยกล่าวหาว่า)",
        #r"(?:พฤติการณ์ในการจับกุม)"
        ]
    
    def norm_key(self, d: dict):
        result = {}
        for topic, text in d.items():
            for pattern in self.__pattern_to_norm():
                if (re.findall(pattern, topic)):
                    print("ok")


