from PIL import Image
import time
import hashlib
import math
import os
'''
im=Image.open('captcha.gif')          代码1
im.convert('P')
his=im.histogram()
values={}
for i in range(256):
    values[i]=his[i]
print(sorted(values.items(),key=lambda x:x[1],reverse=True)[:10])
'''
'''
向量空间搜索引擎实现
解释：
有 2篇文档，我们要怎么计算它们之间的相似度呢？
2 篇文档所使用的相同的单词越多，那这两篇文章就越相似！
但是这单词太多怎么办，就由我们来选择几个关键单词，选择的单词又被称作特征
，每一个特征就好比空间中的一个维度（x，y，z 等），一组特征就是一个矢量，
每一个文档我们都能得到这么一个矢量，只要计算矢量之间的夹角就能得到文章的相似度了。

'''
class VectorCompare:
    def magnitude(self,concordance):      #计算矢量的大小
        total=0
        for word,count in concordance.items():
            total+=count**2
        return  math.sqrt(total)
    def relation(self,concordance1,concordance2):  #计算两个矢量的夹角
        relevance=0
        topvalue=0
        for word,count in concordance1.items():
            if word in concordance2:
                topvalue+=count*concordance2[word]
        return topvalue/(self.magnitude(concordance1)*self.magnitude(concordance2))    #计算向量夹角的公式

def buildvector(im):          #将图片转换为矢量
    d1={}
    count=0
    for i in im.getdata():
        d1[count]=i
        count+=1
    return d1

v=VectorCompare()

iconset=['0','1','2','3','4','5','6','7','8','9','0','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']

#加载训练集
imageset=[]
for letter in  iconset:
    for img in os.listdir('./iconset/%s/'%(letter)):
        if img!='Thumbs.db' and img!='.DS_Store':
            temp=buildvector(Image.open('./iconset/%s/%s'%(letter,img)))
            imageset.append({letter:temp})


im=Image.open('captcha.gif')
im.convert('P')
im2=Image.new('P',im.size,255)
for i in range(im.size[1]):
    for j in range(im.size[0]):
        pix=im.getpixel((j,i))
        if pix==220 or pix==227:         #这两个值是我画直方图得到的两个最大值，即图片主要是这两种颜色构成
            im2.putpixel((j,i),0)        #详情见代码1


inletter = False
foundletter=False
start = 0
end = 0

letters = []             #将验证图按列序号切割，每个元组包含一个数字的开始和结束列序号
for y in range(im2.size[0]):
    for x in range(im2.size[1]):
        pix = im2.getpixel((y,x))
        if pix != 255:
            inletter = True
    if foundletter == False and inletter == True:
        foundletter = True
        start = y

    if foundletter == True and inletter == False:
        foundletter = False
        end = y
        letters.append((start,end))
    inletter=False


count=0
for letter in letters:
    #md5=hashlib.md5()        #哈希散列md5加密

    #对验证码图片进行切割
    im3=im2.crop((letter[0],0,letter[1],im2.size[1])) #box的四个参数,第一个参数左上角横坐标，第二个左上角竖坐标，第三个右下角横坐标，第四个右下角竖坐标
    #md5.update(('%s%s'%(time.time(),count)).encode('utf-8'))
    #im3.save('./%s.gif'%(md5.hexdigest()))
    guess=[]
    for image in imageset:                        #将验证码图片与训练集图片对比，返回对比值最高的值
        for x,y in image.items():
            guess.append((v.relation(y,buildvector(im3)),x))
    guess.sort(reverse=True)
    print('',guess[0])
    count+=1