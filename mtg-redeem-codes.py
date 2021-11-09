import argparse
from utils import load_code_list_file
from utils import BrowserOperator

parser = argparse.ArgumentParser(description='Redeem MTG codes')

parser.add_argument('-cd', '--codes', type=str,help='Codes file to redeem')
parser.add_argument('-c', '--config', type=str, 
                    help='Config file with credentials')
parser.add_argument('-o', '--output', type=str, help='Output file')

args = parser.parse_args()


codes_file = args.codes
config_file = args.config
output_file = args.output


if __name__ == '__main__':
    codes_list = load_code_list_file(codes_file)
    browser_operartor = BrowserOperator(file_name=config_file)

    browser_operartor.reedem_batch(codes_list)

    browser_operartor.export_results(output_file)
    
