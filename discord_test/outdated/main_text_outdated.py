import easyocr
import cv2


def non_black(img, row, start, threshold):
    index = start
    while img[row][index] < threshold:
        index = index+1
    return index


if __name__ == '__main__':
    reader = easyocr.Reader(['en'], gpu = False)
    for n in range(1):
        try:
            img = cv2.imread(f'test{n}.png')
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY )

            h, w, channels = img.shape
            print(type(img))
            index = 0
            c1 = non_black(gray,176,0, 40)
            n1 = non_black(gray,176,c1+71, 40)
            edge = non_black(gray,215,int(w/2), 30)
            c2 = non_black(gray,176,int(w/2), 40)
            xw = n1-169-c1
            print(f'n:{n} c1:{c1} n1:{n1} e:{edge} c2:{c2} xw:{xw}')
            
            crop_img1 = img[196:h-25, 40:c1]
            crop_img2 = img[196:h-25, n1-169:n1]
            crop_img3 = img[196:h-25, edge:c2+29-xw]
            crop_img4 = img[196:h-25, c2+29:c2+195]
            images = [crop_img1, crop_img2, crop_img3, crop_img4]
            im_h = cv2.hconcat(images)
            print(crop_img1.shape)
            print(crop_img2.shape)
            print(crop_img3.shape)
            print(crop_img4.shape)
            cv2.imwrite(f'test_resize{n}_crop1.png', crop_img1)
            cv2.imwrite(f'test_resize{n}_crop2.png', crop_img2)
            cv2.imwrite(f'test_resize{n}_crop3.png', crop_img3)
            cv2.imwrite(f'test_resize{n}_crop4.png', crop_img4)

            #cv2.imshow('image', crop_img1)
            #cv2.waitKey(0)
            #setwidth = 100
            #height, width = crop_img2.shape
            #crop_img1_ex = cv2.resize(crop_img1, dsize=(0, 0), fx=setwidth/width, fy=setwidth/width, interpolation=cv2.INTER_LINEAR)
            #height, width, channels = crop_img2.shape
            #crop_img2_ex = cv2.resize(crop_img2, dsize=(0, 0), fx=setwidth/width, fy=setwidth/width, interpolation=cv2.INTER_LINEAR)
            #height, width, channels = crop_img3.shape
            #crop_img3_ex = cv2.resize(crop_img3, dsize=(0, 0), fx=setwidth/width, fy=setwidth/width, interpolation=cv2.INTER_LINEAR)
            #height, width, channels = crop_img4.shape
            #crop_img4_ex = cv2.resize(crop_img4, dsize=(0, 0), fx=setwidth/width, fy=setwidth/width, interpolation=cv2.INTER_LINEAR)
            #print(crop_img1_ex.shape)
            #print(crop_img2_ex.shape)
            #print(crop_img3_ex.shape)
            #print(crop_img4_ex.shape)

            #start = time.time()
            #use allowlist ='0123456789' for numbers
            #results1 = reader.readtext(crop_img1_ex, detail=1, paragraph=False)
            #print(results1)
            
            
            #cv2.imshow('image', i)
            #cv2.waitKey(0)
            invert = cv2.bitwise_not(crop_img1)
            height, width, channel = invert.shape
            #print(height)
            #print(width)
            #i = invert[0:width, 0:width]

            #cv2.imwrite('asdf.png', invert)
            results = reader.readtext(invert[3*width:6*width, 0:width])
            for r in results:
                print(r[1])
            #results3 = reader.readtext(crop_img3_ex, detail=1, paragraph=False)
            #print(results3)
            #results4 = reader.readtext(crop_img4, detail=1, paragraph=False)
            #print(results4)
        except:
            pass
