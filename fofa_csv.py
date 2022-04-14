# Author: jax
import requests
import base64
import csv
import codecs
import argparse
import re
import time

def get_response(s_str):
    condition_str = s_str
    encodestr = base64.b64encode(condition_str.encode('utf-8'))
    encode_str = str(encodestr,'utf-8')
    
    url = "https://fofa.info/api/v1/search/all?"+ api_key +"&qbase64="+ encode_str + "&fields=ip,port,server,domain,host&size=10000"

    try:
        response = requests.get(url)
        json_data = response.json()
        s = requests.session()
        s.keep_alive = False
        time.sleep(2)
        return json_data
    except requests.exceptions.HTTPError as e:
        print(e)
        time.sleep(2)

def json2csv(csv_name, json_return):
    csvfile = open(csv_name + '.csv', 'a+', newline='', encoding="utf-8")  # python3
    csvfile.write(codecs.BOM_UTF8.decode())
    writer = csv.writer(csvfile, delimiter=',')
    keys = ['ip', 'port', 'server', 'domain','host', 'csv_name']
    writer.writerow(keys)

    for n in range(10000):
        try:
            ip = json_return['results'][n][0]
            port = json_return['results'][n][1]
            server = json_return['results'][n][2]
            domain = json_return['results'][n][3]
            host = json_return['results'][n][4]
            writer.writerow([ip, port, server, domain, host, csv_name])
        except:
            break
    csvfile.close()

if __name__ == '__main__':
    print("""
    
  ______ ____  ______        _____  _______      __
 |  ____/ __ \|  ____/\     / ____|/ ____\ \    / /
 | |__ | |  | | |__ /  \   | |    | (___  \ \  / / 
 |  __|| |  | |  __/ /\ \  | |     \___ \  \ \/ /  
 | |   | |__| | | / ____ \ | |____ ____) |  \  /   
 |_|    \____/|_|/_/    \_\ \_____|_____/    \/    
                        ______                     
                       |______|                    
    """)
    print("code by jax\n")
    parser = argparse.ArgumentParser(description="FOFA批量查询导出CSV文件 (请先新建api_key.ini文件并写入email=xxx&key=xxx)")
    parser.add_argument('-s', '--str', type=str, help="the search condition like: domain=xx.com")
    parser.add_argument('-f', '--file', type=str, help="存放查询语句的文件，一行一条查询语句")
    args = parser.parse_args()

    try:
        with open('api_key.ini') as file_obj:
            content = file_obj.read()
            content = str(content)
            api_key = '{}'.format(content)
    except Exception as e:
        print(e)

    if args.file != None or args.str != None :
        if(args.str != None ):
            s_str = args.str
            filename = cleaned_up_filename = re.sub(r'[/\\:*?"<>|]', '', s_str)
            json_return = get_response(s_str)
            json2csv(filename, json_return)
            print("end")
        if (args.file != None):
            str_file = args.file
            file = open(str_file)
            while 1:
                s_str = file.readline().strip('\n')
                if not s_str:
                    break
                filename = cleaned_up_filename = re.sub(r'[/\\:*?"<>|]', '', s_str)
                json_return = get_response(s_str)
                json2csv(filename, json_return)
                print("The task <" + s_str + "> finished!")
            file.close()
    else:
        print("""For example:\n    python3 fofa_csv.py -f test.txt\n    python3 fofa_csv.py -s domain=xx.com\n    批量查询时在文件中每行一条查询语句\n    注意：请先新建api_key.ini文件并写入email=xxx&key=xxx""")
            
"""
【可选参数】字段列表，默认为host，用逗号分隔多个参数，如(fields=ip,title)
可选的列表有：
host title ip domain port country province city country_name header 
server protocol banner cert isp as_number as_organization latitude 
longitude structinfo icp fid cname type jarm

暂选：ip,port,host,domain,title,server,country
"""
