import os
from plotly.graph_objects import Figure, Scatter

MSG_NUM_IDX = 0
TIME_OFFSET_IDX = 1
DATA_LEN_IDX = 5
DATA_START_IDX = 6

def JoinHexStr2Int16(high_byte_str, low_byte_str):
    val = int(high_byte_str + low_byte_str, 16)
    if val & (1 << 15):
        val -= (1 << 16)
    return val


def PlotPCAN_Data(data_file_path, res_file_path):
    print(f'└ Reading file...')
    with open(data_file_path, 'r') as f:
        lines = f.readlines()
        nlines = len(lines)

    timd, intd = [], []
    for idx, line in enumerate(lines):
        if not line:
            break
        elif line[0] == ';':
            # Skip header
            nlines -= 1
            continue

        progres = int((idx+1)/nlines*100)
        print(f'\r└ Joining data... {progres}%', end='')    
        col = line.strip().split()
        num_hex_str = int(col[DATA_LEN_IDX])
        num_data = int(num_hex_str/2)
        msg_idx = int(col[MSG_NUM_IDX])-1
        hexd = col[DATA_START_IDX:DATA_START_IDX+num_hex_str]
        
        for i in range(num_data):
            int_data = JoinHexStr2Int16(hexd[2*i+1], hexd[2*i])
            intd.append(int_data)
            timd.append((msg_idx + i/num_data))
    
    print()
    print("└ Drwing plot...")
    fig = Figure()
    fig.add_trace(Scatter(x=timd, y=intd))
    fig.update_layout(xaxis_title='time [ms]',
                      yaxis_title='raw data')

    print("└ Exporting html...")
    fig.write_html(res_file_path)

    print('└ Done!')
    print()


def main():
    os.system('cls')
    data_file_root = './data'
    res_file_root = './res'
    
    if not os.path.isdir(data_file_root):
        print(f'"{data_file_root}" folder not found')

    else:
        if not os.path.isdir(res_file_root):
            os.mkdir(res_file_root)

        data_files = [file for file in os.listdir(data_file_root) if file.endswith('.trc')]
        N = len(data_files)
        print(f'Found {N} data files\n')

        for i, f in enumerate(data_files):
            print('---------------------------------')
            print(f'{i+1}/{N} Processing "{f}"!')
            rf = f.split('.')[0] + '.html'            
            data_file_path = os.path.join(data_file_root, f)
            res_file_path =  os.path.join(res_file_root, rf)
            
            if os.path.isfile(res_file_path):
                print('└ Result already exsist. Skip!')
                print()
            else:
                PlotPCAN_Data(data_file_path, res_file_path)
    
    os.system('pause')

if __name__ == '__main__':
    main()