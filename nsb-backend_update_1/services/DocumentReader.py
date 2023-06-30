import docx
from .EssentialExtractor import EssentialExtractor
from .NERExtractor import NERExtractor
class DocumentReader():
    def __init__(self, path_to_file):
        self.text = []
        self.essential = {}
        self.ner = {}
        self.others = {}

        self.setup(path_to_file)

    def setup(self, path_to_file):
        self.text = self.__set_text(path_to_file)

        # Extractor
        NER = NERExtractor()
        ner = NER.extract(path_to_file)
        esx = EssentialExtractor()
        essential = esx.extract(ner)
        self.essential = essential
        self.ner = ner

    def __set_text(self,path_to_file):
        # TODO read using docx
        self.text = docx.Document(path_to_file)

    def get_text(self):
        return self.text
    def get_ner(self):
        return self.ner
    def get_ess(self):
        return self.essential