import re

class PrePro:    
    @staticmethod
    def filter(code):
        code = re.sub("('.*?)\n", '', code)
        return code.replace("\n","")
