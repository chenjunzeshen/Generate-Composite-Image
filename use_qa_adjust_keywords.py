# -*- coding: utf-8 -*
import wenxin_api # 可以通过"pip install wenxin-api"命令安装
from wenxin_api.tasks.free_qa import FreeQA

wenxin_api.ak = ""  # 输入您的API Key
wenxin_api.sk = ""  # 输入您的Secret Key

def get_sentence(background_keyword, keyword):
    input_dict = {
        "text": f'问题：用"{background_keyword}”和:{keyword}”造句？\n回答：',
        "seq_len": 128,
        "topp": 0.5,
        "penalty_score": 1.2,
        "min_dec_len": 2,
        "min_dec_penalty_text": "。?：！[<S>]",
        "is_unidirectional": 0,
        "task_prompt": "qa",
        "mask_type": "paragraph"
    }
    rst = FreeQA.create(**input_dict)
    return rst['result']