import re
import os
import textfsm
import pandas as pd

from ipaddress import ip_address, ip_network

class OspfParserHuawei:
    def __init__(self):
        self.template_path = os.path.join(os.getenv('TEMPLATE_PATH'), 'huawei_ospf.textsfm')

    def create_network(self, row) -> str:
        data = f"{row['LINK_ID']}/{row['DATA']}"
        network = ip_network(data, strict=False)
        return str(network)

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
    
    def find_network(self, ip:str, networks:list[str]) -> pd.DataFrame:
        for network in networks:
            if ip_address(ip) in ip_network(network):
                return network
        return None
    
    def process_ospf(self, text:str) -> pd.DataFrame:
        try:
            blocks:list[str]= re.findall(r'Area: \d+\.\d+\.\d+\.\d+[\s\S]*?(?=^Area: |\Z)', text, re.MULTILINE)
            if not blocks:
                blocks = re.findall(r'Area: \d+.\d+.\d+.\d+.*', text, re.MULTILINE)
                if not blocks:
                    raise Exception("No areas found in OSPF output")
            areas = []
            for block in blocks:
                block = block.lstrip()
                areas.append(self.process_area(block))
            df: pd.DataFrame = pd.concat(areas)
            df_ptp = df[df['LINK_TYPE'] == 'P-2-P']
            df_stub = df[df['LINK_TYPE'] == 'StubNet']
            df_stub['NETWORK'] = df_stub.apply(lambda x: self.create_network(x), axis=1)
            networks = df_stub['NETWORK'].unique()  
            df_ptp['NETWORK'] = df_ptp.apply(lambda x: self.find_network(x['DATA'], networks), axis=1)
            return df_ptp
        except Exception as e:
            raise Exception(f"Error processing OSPF: {e}")
    
    def run(self, file: str) -> pd.DataFrame:
        try:
            with open(file) as f:
                template = f.read()
            return self.process_ospf(template)
        except Exception as e:
            raise Exception(f"Error running parser: {e}")


