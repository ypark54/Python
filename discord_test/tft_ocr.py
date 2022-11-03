import easyocr
import cv2
import numpy as np
import requests
import json
import Levenshtein as lev

def non_black(img, row, start, threshold):
    index = start
    while img[row][index] < threshold:
        index = index+1
    return index

def crop(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY )
    invert = cv2.bitwise_not(gray)
    
    h, w = gray.shape
        
    c1 = non_black(gray,176,20, 80)
    #print(f'c1:{c1}')
    n1 = non_black(gray,176,c1+71, 80)
    #print(f'n1:{n1}')
    edge = non_black(gray,215,int(w/2), 20)
    c2 = non_black(gray,176,int(w/2), 80)
    xw = n1-169-c1
    rows = int((h-15-196)/48)
    print(f'41:{c1+1},{c1+66}:{n1}, {edge+1}:{c2+30-xw}, {c2+30}:{c2+195}')
    crop_img = [invert[196:h-15, 41:c1+1], invert[196:h-15, c1+66:n1], invert[196:h-15, edge+1:c2+30-xw], invert[196:h-15, c2+30:c2+195]]
    return crop_img, rows


def msg_to_img(m):
    if m['attachments']:
        url = m['attachments'][0]['url']
        image_nparray = np.asarray(bytearray(requests.get(url).content), dtype=np.uint8)
        image = cv2.imdecode(image_nparray, cv2.IMREAD_COLOR)
        return image

def read_num(img, rows, reader):
    height_resize, width_resize = img.shape
    result = []
    for i in range(rows):
        if i < rows-1:
            segment = img[int(i*height_resize/rows):int((i+1)*height_resize/rows), 0:width_resize]
        else:
            segment = img[int(i*height_resize/rows):height_resize, 0:width_resize]
        segment_result = reader.readtext(segment, allowlist='012345689')
        #print(segment_result)
        if segment_result:
            #print(f'original result is {segment_result[0][1]}')
            if segment_result[0][2] < 0.96:
                if segment_result[0][1] == '1' or segment_result[0][1] == '7':
                    is_one = reader.readtext(segment, allowlist='1')
                    is_seven = reader.readtext(segment, allowlist='7')
                    if is_one[0][2] > is_seven[0][2]:
                        segment_result = is_one
                    else:
                        segment_result = is_seven
                else:
                    #print(f'read letter is {segment_result[0][1]}, accuracy is :{segment_result[0][2]}')
                    segment_result = reader.readtext(segment, allowlist='0123456789')
                    #print(f'accuracy was low. new result is {segment_result[0][1]}')
        else:
            segment_result = reader.readtext(segment, allowlist='0123456789')
            #print(f'result did not exist. new result is{segment_result[0][1]}')
        if segment_result:
            result.append(segment_result[0][1])

    return result

def read_name(img, reader, name_list):
    initial_result = reader.readtext(img, width_ths=20)
    result = []
    #for r in initial_result:
    #    print(r)
    for r in initial_result:
        old_ratio = 0
        match = ''
        if r[1].lower() in name_list:
            #print(f'{r[1]} was found')
            result.append(r[1].lower())
            pass
        else:
            #print(f'{r[1]} was not found')
            for e in name_list:
                temp_ratio = lev.ratio(r[1].lower(),e)
                #print(e, temp_ratio)
                if temp_ratio>old_ratio:
                    old_ratio = temp_ratio
                    match = e
            #print(f'closest match is{match}')
            result.append(match)
    return result

def img_to_text(img, reader, name_list):
    crop_img, rows = crop(img)
    #for index, c in enumerate(crop_img):
    #    cv2.imwrite(f'image{index}.png', c)
    setwidth = 300
    width = crop_img[0].shape[1]
    img_resize_0 = cv2.resize(crop_img[0], dsize=(0, 0), fx=setwidth/width, fy=setwidth/width, interpolation=cv2.INTER_CUBIC)
    #cv2.imwrite('img_resize_0.png', img_resize_0)
    num_0 = cv2.blur(img_resize_0, (4,4))
    print('processing num col 1')
    result_num_0 = read_num(num_0, rows, reader)

    #print(result_num_0)
    
    width = crop_img[2].shape[1]
    img_resize_1 = cv2.resize(crop_img[2], dsize=(0, 0), fx=setwidth/width, fy=setwidth/width, interpolation=cv2.INTER_CUBIC)
    #cv2.imwrite('img_resize_1.png', img_resize_1)
    num_1 = cv2.blur(img_resize_1, (4,4))
    print('processing num col 2')
    result_num_1 = read_num(num_1, rows, reader)
    #print(result_num_1)
    
    

    img_resize_2 = cv2.resize(crop_img[1], dsize=(0, 0), fx=setwidth/width, fy=setwidth/width, interpolation=cv2.INTER_CUBIC)
    sharpen_2 = cv2.threshold(img_resize_2, 200, 255, cv2.THRESH_BINARY)[1]
    print('processing name col 1')
    result_name_0 = read_name(sharpen_2, reader, name_list)
    #print(result_name_0)
    
    img_resize_3 = cv2.resize(crop_img[3], dsize=(0, 0), fx=setwidth/width, fy=setwidth/width, interpolation=cv2.INTER_CUBIC)
    sharpen_3 = cv2.threshold(img_resize_3, 200, 255, cv2.THRESH_BINARY)[1]
    print('processing name col 2')
    result_name_1 = read_name(sharpen_3, reader, name_list)
    #print(result_name_1)


    return result_name_0+result_name_1, result_num_0+result_num_1

    

if __name__ == '__main__':
    reader = easyocr.Reader(['en'])
    f = open('currency.json')
    data = json.load(f)
    name_list=list(data['essences'].keys())
    f.close()
    img = cv2.imread('test9.png')
    name, num = img_to_text(img, reader, name_list)
    print(name)
    print(num)
