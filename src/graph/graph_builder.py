import os
import json
import networkx as nx
from pyvis import network as net
import pandas as pd

class OSPFGraphBuilder:
    def __init__(self) -> None:
        self.G = nx.Graph()
        height = os.getenv("HEIGHT", "1000px")
        width = os.getenv("WIDTH", "100%")
        cdn_resources = os.getenv("CDN_RESOURCES", "remote")
        options_path = os.getenv("GRAPH__OPTIONS_PATH")
        self.Net = net.Network(height=height, width=width, select_menu=True, cdn_resources=cdn_resources, filter_menu=True)
        with open(options_path, 'r') as f:
            self.options = json.load(f)

    def run(self, dados:pd.DataFrame):
        try:
            nbr_column='LINK_ID' 
            nbr_name_column='LINK_ID'
            nbr_ip_column='LINK_ID'
            dados[nbr_name_column] = dados[nbr_name_column].fillna(dados[nbr_column])
            dados[nbr_ip_column] = dados[nbr_ip_column].fillna(dados[nbr_column])
            self.G.add_nodes_from([(r[nbr_ip_column], {'label':r[nbr_name_column], 'title':r[nbr_ip_column]}) for _, r in dados.drop_duplicates(subset=nbr_column).iterrows()])
            grupos = self.group_dados(dados)
            for _, r in grupos.iterrows():
                self.G.add_edge(r['adj'][0], r['adj'][1], title=r['LABEL'][0], color=r['COLOR'][0], weight=1)
        except Exception as e:
            raise e
        
    def group_dados(self, dados:pd.DataFrame) -> pd.DataFrame:
        try:
            dados['adj'] = (dados[['LINK_ID', 'LS_ID']].apply(lambda row: tuple(sorted(row)), axis=1))
            grupos = dados.groupby('adj').agg(list).reset_index()
            return grupos
        except Exception as e:
            raise e

    def plot(self, name) -> bool:
        try:
            self.Net.options = self.options
            self.Net.from_nx(self.G)
            self.Net.save_graph(f'{name}.html')
            nx.write_graphml(self.G, f'{name}.graphml')
            return True
        except:
            return False