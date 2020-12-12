'''
Read topic_detection data with format txt 
convert to csv format -> save data.csv 
clean data, tokenize, ... for NLP project
'''

import pandas as pd 
import re
from libary import nlp_utils as nlp
import sys 
from underthesea import word_tokenize
from pyvi import ViTokenizer

sys.path.append('./library')

with open('./data/topic_detection_train.v1.0.txt') as f:
    lines_topic_detection = f.readlines()
print('Number data:' ,len(lines_topic_detection))

'''
để chuẩn hoá các từ stopword trong file giống format của pyvi
tạo file vietnamese-stopwords-pyvi.txt và lưu
'''
def tokenizer_stopwords():
    with open('./data/vietnamese-stopwords.txt') as f:
        lines_stopwords = f.readlines()

    with open('./data/vietnamese-stopwords-pyvi.txt', 'w') as fw:
        for line in lines_stopwords:
            tmp = ViTokenizer.tokenize(line)
            fw.write('{}\n'.format(tmp))
    return

def remove_stopword(line_data):
    stopwords = set()
    with open('./data/vietnamese-stopwords-pyvi.txt') as f:
        lines_stopwords = f.readlines()
    
    # add stopword from file to set()
    for line in lines_stopwords:
        line = re.sub('\n', '', line).strip()
        stopwords.add(line)
    
    # remove stopword from data
    words = []
    for word in line_data.strip().split():
        if word not in stopwords:
            words.append(word)
        
    return ' '.join(words)
text_test = 'cái đó là một thứ bảy tuyệt đẹp'
print(remove_stopword(text_test))

# function for text_process
def text_process(line_data):
    line_data = nlp.convert_unicode(line_data)
    # line_data = nlp.chuan_hoa_dau_cau_tieng_viet(line_data)   # bị lỗi chinh_tri_vẻ
    line_data = ViTokenizer.tokenize(line_data)
    line_data = line_data.lower()
    line_data = re.sub(r'\d','', line_data).strip()
    line_data = re.sub(r'[^\s\wáàảãạăắằẳẵặâấầẩẫậéèẻẽẹêếềểễệóòỏõọôốồổỗộơớờởỡợíìỉĩịúùủũụưứừửữựýỳỷỹỵđ_]',' ',line_data)
    line_data = re.sub(r'\s+', ' ', line_data).strip()
    line_data = remove_stopword(line_data)
    return line_data

# process for each line in data.txt
def preProcessing ():
    '''
    for train_data
    '''
    # with open ('./data/topic_detection_train.v1.0.txt') as f:
    #     lines_topic_detection = f.readlines()   

    '''
    for test data
    '''
    with open ('./data/Task/topic_detection_test_unlabel.v1.0.txt') as f:
        lines_topic_detection = f.readlines()

    clean_data = []
    for limit, line in enumerate(lines_topic_detection):
        # print(line)
        line = text_process(line)
        clean_data.append(line)
        print('after:\n',line)

        # for check code
        # if(limit >5):
        #     break
    return clean_data

# save data with pandas format to data.csv
def save_data_csv(): 
    clean_data = preProcessing()
    label = []
    text = []
    '''
    for train_data
    '''
    for line in clean_data:
        words = line.strip().split()
        text.append(' '.join(words[1:]))
        label.append(words[0])
    
    # remove __label__ 
    for i in range(len(label)):
        label[i]= label[i].strip('__label__')
    
    train_df = pd.DataFrame()
    train_df['label'] = label
    train_df['text'] = text
    train_df.to_csv('./data/data.csv', header = True, index= None)

    """
    for test_data
    """
    # for line in clean_data:
    #     # text.append(' '.join(line))
    #     text.append(line)
    # test_df = pd.DataFrame()
    # test_df['label'] = label
    # test_df['text'] = text
    # test_df.to_csv('./data/data_test.csv', header = True, index= None)
    return 



if __name__ == '__main__':
    # words = 'cái đó là một thứ bảy tuyệt đẹp'
    preProcessing()
    save_data_csv()


        
        

