import re

class PrePro:    
    @staticmethod
    def filter(code):
        code = re.sub("('.*?)\n", '\n', code)
        code = code.replace("\t", "")
        return code