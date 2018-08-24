
def features(stentence):
    u_0_0 = list(stentence)  # 仅仅考虑当前词的标签
    u_1_0 = []  # 考虑当前词和这个词前一个词的标签
    u_2_0 = []

    for i in range(len(u_0_0)):
        w_1 = u_0_0[i - 1] + '/' + u_0_0[i] if i else '_B-1/' + u_0_0[i]
        u_1_0.append(w_1)

        if i == 0:
            w_2 = '_B-2/' + '_B-1/' + u_0_0[i]
        elif i == 1:
            w_2 = '_B-1/' + u_0_0[i - 1] + '/' + u_0_0[i]
        else:
            w_2 = u_0_0[i - 2] + '/' + u_0_0[i - 1] + '/' + u_0_0[i]
        u_2_0.append(w_2)

    return u_0_0, u_1_0, u_2_0


def viterbi(stentence, uni_fea={}, bi_fea={}, weights={}, use_bi=False, states=['B', 'E', 'M', 'S']):
    length = len(states)
    max = []  # 记录最大的概率
    route = []  # 记录最优的路径

    f_u00, f_u10, f_u20 = features(stentence)

    for i in range(len(f_u00)):

        # 状态特征 f(y_i,x_i)
        state_weights = [0.0 for _ in range(length)]
        for w in range(length):
            w_u00 = weights[uni_fea[f_u00[i]]+w] if f_u00[i] in uni_fea else 0.0  # 仅考虑当前词
            w_u10 = weights[uni_fea[f_u10[i]]+w] if f_u10[i] in uni_fea else 0.0  # 考虑当前词 和 前一个词
            w_u20 = weights[uni_fea[f_u20[i]]+w] if f_u20[i] in uni_fea else 0.0  # 考虑当前词 和 前两个词

            state_weights[w] = w_u00 + w_u10 + w_u20

        # 转移特征 f(y_i_1,y_i,x_i)
        word = f_u00[i]

        bi_id = bi_fea[word] if use_bi or word not in bi_fea else 0
        e_weights = [[weights[bi_id + j + i * length] for j in range(length)] for i in range(length)]

        if i == 0:
            temp_max = state_weights
            max.append(temp_max)
            route = [str(w) for w in range(length)]
        else:
            last_max = max[-1]  # 到上一步的最大距离
            temp_max = []
            temp_rout = [0 for _ in range(length)]

            for m in range(length):
                max_lenth = -1e37
                state = 0

                for n in range(length):
                    # 维特比递推 max(上一状态的max + 转移的 + 当前的)
                    if last_max[n] + e_weights[n][m] + state_weights[m] > max_lenth:
                        max_lenth = last_max[n] + e_weights[n][m] + state_weights[m]
                        state = n
                temp_rout[m] = route[state] + str(m)  # 记录最大的路径
                temp_max.append(max_lenth)

            route = temp_rout
            max.append(temp_max)

    last = max[-1]
    max_1, state_1 = -1e37, 0
    for k in range(length):
        if last[k] > max_1:
            max_1 = last[k]
            state_1 = k
    final_route = route[state_1]

    result = ''
    for r in list(final_route):
        result += states[int(r)]

    return final_route,result, max_1

