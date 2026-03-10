import os
import sys
import logging
import pandas as pd


from dotenv import load_dotenv
from distinctipy import distinctipy

from src.parsers import huawei
from src.graph.graph_builder import OSPFGraphBuilder

load_dotenv()

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def plot(df:pd.DataFrame, output_path: str, filename: str):
    try:
        logger.info("Plotting graph...")
        df = df.map(lambda x: x.strip() if isinstance(x, str) else x)
        logger.info(f"DataFrame shape: {df.shape}")
        if df.empty:
            logger.warning("DataFrame is empty. No graph will be plotted.")
            raise ValueError("DataFrame is empty.")
        logger.info(f"Filtered DataFrame shape (P2P): {df.shape}")
        areas = df['AREA'].unique()
        random_colors = distinctipy.get_colors(len(areas))
        colors = {areas[i]:distinctipy.get_hex(random_colors[i]) for i in range(0, len(areas))}
        df['COLOR'] = df['AREA'].map(colors)
        df['LABEL'] = df.apply(lambda x: f"Area: {x['AREA']}\nRede: {x['NETWORK']}\nColor: {x['COLOR']}\nCost: {x['METRIC']}", axis=1)
        PG = OSPFGraphBuilder()
        PG.run(df)
        PG.plot(f'{output_path}/{filename}')
        logger.info(f"Graph plotted successfully: {output_path}/{filename}.html")
    except Exception as e:
        logger.error(f"Error plotting graph: {e}")
        raise e


def main():
    try:
        input_path = os.getenv('INPUT_PATH')
        output_path = os.getenv('OUTPUT_PATH')
        parser = huawei.OspfParserHuawei()
        df = parser.run(f'{input_path}/huawei_example.txt')
        plot(df, output_path, filename=sys.argv[1] if len(sys.argv) > 1 else 'graph')
    except Exception as e:
        logger.error(f"Error in main execution: {e}")

if __name__ == "__main__":    
    main()