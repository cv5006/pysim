import os
import csv
from plotly.graph_objects import Figure, Scatter


MSG_NUM_IDX = 0
TIME_OFFSET_IDX = 1
TxRx_IDX = 4
DATA_LEN_IDX = 5
DATA_START_IDX = 6

def JoinHexStr2Int16(high_byte_str, low_byte_str):
    val = int(high_byte_str + low_byte_str, 16)
    if val & (1 << 15):
        val -= (1 << 16)
    return val


def ExtractPCAN_Data(data_file_path):
    print('└ Reading file...', end='')
    with open(data_file_path, 'r') as f:
        lines = f.readlines()
        nlines = len(lines)
    print('\r└ Reading file... Done!')

    timd, intd = [], []
    for idx, line in enumerate(lines):
        if not line:
            break
        elif line[0] == ';':
            # Skip header
            nlines -= 1
            continue

        progress = int((idx+1)/nlines*100)
        print(f'\r└ Joining data... {progress}%', end='')
        col = line.strip().split()

        if col[TxRx_IDX] != "Rx":
            # Skip Tx message
            continue

        num_hex_str = int(col[DATA_LEN_IDX])
        num_data = int(num_hex_str/2)
        msg_idx = int(col[MSG_NUM_IDX])-1
        hexd = col[DATA_START_IDX:DATA_START_IDX+num_hex_str]
        
        for i in range(num_data):
            int_data = JoinHexStr2Int16(hexd[2*i+1], hexd[2*i])
            intd.append(int_data)
            timd.append((msg_idx + i/num_data))
    
    print('\r└ Joining data... Done!')
    return timd, intd


def ExportPlotHTML(timd, intd, res_file_path):    
    print("└ Drawing plot...", end='')
    fig = Figure()
    fig.add_trace(Scatter(x=timd, y=intd))
    fig.update_layout(xaxis_title='time [ms]',
                      yaxis_title='raw data')
    print('\r└ Drawing plot... Done!')

    print("└ Exporting html...", end='')
    fig.write_html(res_file_path)
    print("\r└ Exporting html... Done!")


def ExportCSV(timd, intd, res_file_path):    
    N = len(timd)
    with open(res_file_path, 'w', newline='') as f:
        wcsv = csv.writer(f)
        for i, t in enumerate(timd):
            progress = int((i+1)/N*100)
            print(f'\r└ Exporting csv... {progress}%', end='')
            wcsv.writerow([t, intd[i]])

    print(f'\r└ Exporting csv... Done!')


def main():
    os.system('cls')
    data_file_root = './data'
    res_file_root = './res'
    
    if not os.path.isdir(data_file_root):
        print(f'"{data_file_root}" folder not found')

    else:
        export_csv = input("Export CSV? y/n: ") == 'y'
        print()

        if not os.path.isdir(res_file_root):
            os.mkdir(res_file_root)

        data_files = [file for file in os.listdir(data_file_root) if file.endswith('.trc')]
        N = len(data_files)
        print(f'Found {N} data files\n')

        for i, f in enumerate(data_files):
            print('---------------------------------')
            print(f'{i+1}/{N} Processing "{f}"!')
            html_file_name = f.split('.')[0] + '.html'
            csv_file_name = f.split('.')[0] + '.csv'

            data_file_path = os.path.join(data_file_root, f)
            html_file_path = os.path.join(res_file_root, html_file_name)
            csv_file_path  = os.path.join(res_file_root, csv_file_name)
            
            
            res_exist = os.path.isfile(csv_file_path) if export_csv else os.path.isfile(html_file_path)
            if res_exist:
                print('└ Result already exsist. Skip!')
                print()
            else:
                timd, intd = ExtractPCAN_Data(data_file_path)
                ExportPlotHTML(timd, intd, html_file_path)
                if export_csv:
                    ExportCSV(timd, intd, csv_file_path)
                print()
    
    os.system('pause')

if __name__ == '__main__':
    main()