#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gensim.models import KeyedVectors
from collections import OrderedDict
import json
import time
import push

try:
    from gensim.similarities.index import AnnoyIndexer
except ImportError:
    print('import gensim.annoy error')
    push.push_to_rtx(push.generate_rtx_markdown("gensim引导失败"))
    raise ValueError("anny indexer 加载失败")


class WordCalc:
    def __init__(self):
        # 0: 未训练
        # 1: 正在训练gensim版
        # 2: gensim版可用
        # 3: 正在训练annoy
        # 4: annoy版可用
        self.status = 0
        push.push_to_rtx(push.generate_rtx_markdown("wordcalc出仓状态良好"))

    def train_with_gensim(self):
        self.status = 1
        push.push_to_rtx(push.generate_rtx_markdown("gensim转子引擎开始加热"))
        self.tc_wv_model = KeyedVectors.load_word2vec_format(
            './Tencent_AILab_ChineseEmbedding.txt', binary=False)
        push.push_to_rtx(push.generate_rtx_markdown("gensim转子引擎加热完毕"))
        self.status = 2

    def train_with_annoy(self):
        self.status = 3
        push.push_to_rtx(push.generate_rtx_markdown("annoy向量空间开始注水"))
        self.annoy_index = AnnoyIndexer(self.tc_wv_model, 200)
        fname = 'tc_index_genoy.index'
        self.annoy_index.save(fname)
        # 导出训练结果，以后直接 load 即可
        # annoy_index = AnnoyIndexer()
        # annoy_index.load(fname)
        # annoy_index.model = tc_wv_model
        push.push_to_rtx(push.generate_rtx_markdown("annoy向量空间注水完毕"))
        self.status = 4

    def calc(self, positive_set, negative_set):
        if self.status == 2 or self.status == 3:
            result = self.tc_wv_model.most_similar(
                positive=positive_set, negative=negative_set, topn=10)
            return result
        elif self.status == 4:
            result = self.tc_wv_model.most_similar(
                positive=positive_set, negative=negative_set, indexer=self.annoy_index, topn=10)
            return result
        else:
            return []
