# Generate-Composite-Image

## 背景说明：
    文学作品在记忆文字时难度较大，使用图像辅助记忆效率更高，在查阅资料时发现记忆宫殿法，考虑通过分词或自行输入关键词送入ERNIE-ViLG生成图像覆盖记忆宫殿图像对应位置，方便想象和记忆。记忆宫殿法的要点在于记忆关键词要与背景物品进行一一对应的想象，基于此，添加了使用ERNIE的自由问答对记忆关键词与背景对应物品造句的功能，使用自由问答造的句子再生成图像更有利于联想。

## 文件和文件夹说明：
### 文件夹
  result_pic：生成的结果图像  
  save_img：ERNIE-ViLG生成的各关键词图像 
### 文件
  main.py：主程序  
  background_information.txt：背景图像（记忆宫殿）的物品名称及对应坐标  
  get_ernie_vilg_pic.py：利用ERNIE-ViLG为输入关键词生成图像  
  get_keywords.py：若使用分词属性功能，此文件提供LAC、jieba、jieba（使用paddle）三种分词方案可供选择  
  use_qa_adjust_keywords.py：使用ERNIE自由问答实现造句功能

## 使用说明：
  1、在get_ernie_vilg_pic.py与use_qa_adjust_keywords.py中补充API Key与Secret Key  
  2、运行main.py文件  
　　python main.py  
  3、输入分词方案及内容信息  
　　分词方案：LAC、jieba、jieba_use_paddle、key_words  
　　key_words为自己输入关键词,关键词用逗号隔开  
　　例： LAC 太阳依傍山峦渐渐下落，黄河向着大海滔滔流趟。  
　　　　jieba 太阳依傍山峦渐渐下落，黄河向着大海滔滔流趟。  
　　　　jieba_use_paddle 太阳依傍山峦渐渐下落，黄河向着大海滔滔流趟。  
　　　　key_words 太阳,山峦,黄河,大海  
  4、提示是否使用造句功能，输入“yes”为使用，否则不使用  
  5、操作完毕（ERNIE-ViLG生成的图像保存在save_img文件夹，整合后的图像保存在result_pic文件夹）
