import re


def model_features_groups(file='crf_model/model.txt'):
    pat_fea = '^[U|B]\d+'
    is_feature = '\w+\s\w+:'
    pat_weight = '^-?([1-9]\d*\.\d*|0\.\d*[1-9]\d*|0?\.0+|0)$'

    features = {}
    weight_list = []
    with open(file,encoding='utf-8-sig') as ff:
        lines = ff.readlines()
        for line in lines:
            line = line.strip()

            # 创建存放feature的字典
            if re.match(pat_fea,line) is not None:
                s = re.match(pat_fea,line)
                features[s.group()] = {}

            # 获取feature类型，id和字母，存放到字典中
            if re.match(is_feature, line) is not None:
                first = re.search('\s\w+:', line).start()
                end = re.search('\s\w+', line).end()

                id = line[:first-1]
                feature = line[first+1:end]
                word = line[end+1:]

                features[feature][word] = int(id)

            # 获取feature的权重
            if re.match(pat_weight,line) is not None:
                w = float(re.match(pat_weight, line).group())
                weight_list.append(w)

    weights = dict(zip(range(len(weight_list)), weight_list))

    return features, weights


def model_features(file='crf_model/model.txt'):
    is_feature = '\w+\s\w+:'
    pat_weight = '^-?([1-9]\d*\.\d*|0\.\d*[1-9]\d*|0?\.0+|0)$'

    features = {}
    features['B'] = {}
    features['U'] = {}
    weight_list = []
    with open(file,encoding='utf-8-sig') as ff:
        lines = ff.readlines()
        for line in lines:
            line = line.strip()

            # 获取feature类型，id和字母，存放到字典中
            if re.match(is_feature, line) is not None:
                first = re.search('\s\w+:', line).start()
                end = re.search('\s\w+', line).end()

                id = line[:first]
                feature = line[first + 1:first + 2]
                word = line[end+1:]


                features[feature][word] = int(id)

            # 获取feature的权重
            if re.match(pat_weight,line) is not None:
                w = float(re.match(pat_weight, line).group())
                weight_list.append(w)

    weights = dict(zip(range(len(weight_list)), weight_list))

    return features, weights


if __name__ == '__main__':
    features, weights = model_features()
    print(len(features))
    l = 0
    for k,_ in features.items():
        l += len(features[k])
    print(l)
    print(len(weights))

