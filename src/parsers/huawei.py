import re
import os
import textfsm
import pandas as pd

class OspfParserHuawei:
    def __init__(self):
        self.template_path = os.path.join(os.getenv('TEMPLATE_PATH'), 'huawei_ospf.textsfm')

    def extract_lsa_header(self, block: str) -> dict:
        header = {}
    
        type_match = re.search(r"Type\s+:\s+(\S+)", block)
        ls_match = re.search(r"Ls id\s+:\s+(\S+)", block)
        adv_match = re.search(r"Adv rtr\s+:\s+(\S+)", block)
    
        header["TYPE"] = type_match.group(1) if type_match else None
        header["LS_ID"] = ls_match.group(1) if ls_match else None
        header["ADV_RTR"] = adv_match.group(1) if adv_match else None
    
        return header

    def process_nbr(self, block: str) -> pd.DataFrame:
        try:
            header_data = self.extract_lsa_header(block)
            with open(self.template_path) as template:
                fsm = textfsm.TextFSM(template)
                result = fsm.ParseText(block + "\n")                
            df = pd.DataFrame(result, columns=fsm.header)
            for key, value in header_data.items():
                df[key] = value
            return df
        except Exception as e:
            raise Exception(f"Error processing block: {e}")
        
    def process_area(self, text: str) -> pd.DataFrame:
        try:
            area = re.search(r'Area: (\d+.\d+.\d+.\d+)', text).group(1)
            text = re.sub(r'Link State Database', '', text)
            blocks = text.split('\n\n')
            blocks = blocks[1:]
            nbrs = []
            for block in blocks:
                block = block.lstrip()
                nbrs.append(self.process_nbr(block))
            df = pd.concat(nbrs)
            df['AREA'] = area
            return df
        except Exception as e:
            raise Exception(f"Error processing area: {e}")
    
    def process_ospf(self, text:str) -> pd.DataFrame:
        try:
            blocks:list[str]= re.findall(r'Area: \d+.\d+.\d+.\d+.*?(?=Area: \d+.\d+.\d+.\d+)', text, re.DOTALL)
            if not blocks:
                blocks = re.findall(r'Area: \d+.\d+.\d+.\d+.*', text, re.DOTALL)
                if not blocks:
                    raise Exception("No areas found in OSPF output")
            areas = []
            for block in blocks:
                block = block.lstrip()
                areas.append(self.process_area(block))
            df = pd.concat(areas)
            return df
        except Exception as e:
            raise Exception(f"Error processing OSPF: {e}")
    
    def run(self, file: str) -> pd.DataFrame:
        try:
            with open(file) as f:
                template = f.read()
            return self.process_ospf(template)
        except Exception as e:
            raise Exception(f"Error running parser: {e}")


