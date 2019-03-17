import re

class PrePro:    
    @staticmethod
    def filter(code):
        code = code.replace("\\n", "\n")
        return re.sub("('.*?)\n", ' ', code)
