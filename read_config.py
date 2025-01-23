def read_card_info(file):
    card_info = [[]]
    with open(file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        j = 0
        for line in lines:
            if line.startswith('##setname'):
                break
            if '#####' in line:
                continue
            if line.startswith('##'):
                if j != 4:
                    card_info.append([])
                j += 1
                continue
            if j == 4:
                continue
            line = line.replace('\n', '').split('\t')
            if line[1] == 'N/A':
                continue
            card_info[-1].append([line[0]])
            info = ''
            for i in range(1, len(line)):
                info += line[i]
            card_info[-1][-1].append(info)

    return card_info

if __name__ == '__main__':
    card_info = read_card_info('./config/cardinfo_chinese.txt')
    print(card_info)
