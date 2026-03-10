import os
import json
from uuid import uuid4
import networkx as nx
from pyvis import network as net
import pandas as pd
from collections import defaultdict

class OSPFGraphBuilder:
    def __init__(self) -> None:
        self.G = nx.MultiGraph()
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
            self.G.add_nodes_from([(r[nbr_ip_column], {'label':r[nbr_name_column], 'title':r[nbr_ip_column], 'size':10}) for _, r in dados.drop_duplicates(subset=nbr_column).iterrows()])
            grupos = self.group_dados(dados)
            for _, r in grupos.iterrows():
                self.G.add_edge(r['adj'][0], r['adj'][1], title=r['LABEL'][0], color=r['COLOR'][0], weight=1, label=r['NETWORK'])
        except Exception as e:
            raise e

    def group_dados(self, dados:pd.DataFrame) -> pd.DataFrame:
        try:
            grupos = dados.groupby('NETWORK').agg(list).reset_index()
            grupos['adj'] = grupos.apply(lambda x: list(dict.fromkeys(x['LINK_ID'] + x['ADV_RTR'])),axis=1)
            return grupos
        except Exception as e:
            raise e

    def plot(self, name) -> bool:
        try:
            nx.write_graphml(self.G, f'{name}.graphml')
            self.Net.options = self.options
            for node, data in self.G.nodes(data=True):
                self.Net.add_node(node, **data)
            edge_counter = defaultdict(int)
            for u, v, key, data in self.G.edges(keys=True, data=True):
                pair = tuple(sorted([u, v]))
                edge_counter[pair] += 1
                n = edge_counter[pair]
                if n == 1:
                    self.Net.add_edge(u, v, **data)
                else:
                    mid = f"mid_{uuid4()}"
                    self.Net.add_node(mid,label=" ",size=1,color="rgba(0,0,0,0)",physics=True)
                    self.Net.add_edge(u, mid, **data)
                    self.Net.add_edge(mid, v, **data)
            self.Net.save_graph(f'{name}.html')
            return True
        except Exception as e:
            return False