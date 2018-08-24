import crf_model as model
from crf_viterbi import viterbi


class CrfSeg():

    def __init__(self, model_file='crf_model/model.txt', USE_BI=False):
        features, self.weights = model.model_features(model_file)
        self.un_fea = features['U']
        self.bi_fea = features['B']
        self.use_bi = USE_BI

        del features
        print('crf model load success!')

    def __crf_seg(self, sentence, route):
        '''
        :param sentence:
        :param route:
        :return:
        '''
        if not len(sentence) == len(route):
            print('wrong!')
            return
        term = ''
        for i in range(len(sentence)):
            char = sentence[i]
            state = route[i]
            if state == '0':  # B
                term += char
            elif state == '1':  # E
                term += char + ' '
            elif state == '2':  # M
                term += char
            else:  # state == '3':   S
                term += char + ' '
        return term.strip().split(' ')

    def cut(self,sentence):

        final_route,result,max_p = viterbi(sentence, self.un_fea, self.bi_fea, self.weights, use_bi=self.use_bi)
        cut_result = self.__crf_seg(sentence, final_route)

        return cut_result


if __name__ == '__main__':
    crf = CrfSeg()
    rst = crf.cut("他要与中国人合作。")
    print('/'.join(rst))
    rst = crf.cut("扬帆远东做与中国合作的先行")
    print('/'.join(rst))
    rst = crf.cut("深夜的穆赫兰道发生一桩车祸，女子丽塔在车祸中失忆了")
    print('/'.join(rst))
    rst = crf.cut("多年来，中希贸易始终处于较低的水平，希腊几乎没有在中国投资。")
    print('/'.join(rst))

    rst = crf.cut("南京市长江大桥")
    print('/'.join(rst))
    rst = crf.cut("工信处女干事每月经过下属科室都要亲口交代24口交换机等技术性器件的安装工作")
    print('/'.join(rst))
