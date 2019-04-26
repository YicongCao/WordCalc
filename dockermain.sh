#!/bin/bash
echo "before downloading dataset\n\n"
python push.py "正在下载数据集"
wget -q https://ai.tencent.com/ailab/nlp/data/Tencent_AILab_ChineseEmbedding.tar.gz --tries=3
ls
python push.py "数据集下载完毕，正在解压"
echo "before extracting files\n\n"
tar -xzvf Tencent_AILab_ChineseEmbedding.tar.gz
echo "after extracting files\n\n"
ls
python push.py "解压完毕，正在进入python态"
echo "before executing python\n\n"
python hello.py
python flaskmain.py
echo "after python\n\n"
python push.py "我已出仓，感觉药丸"