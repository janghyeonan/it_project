# -*- coding: utf-8 -*-
"""
Created on Tue Apr 17 09:59:38 2018

@author: STU
"""

class Image4cut:
    def image4cut(self,file1,filesave1,size):       # 파일위치,저장위치
        from wand.image import Image
        import glob
        file = str(file1)+"/*.jpg"      # 불러올 파일 위치
        filesave= str(filesave1)      # 저장 위치
        file_list=glob.glob(file)

        cn=-1
        for t in file_list:
            cn+=1

            oldfilename = file_list[cn]
            row = 2
            col = 2

            with Image(filename = oldfilename) as image:
                height=image.size[1] 
                if height>=int(size):     # 세로 사이즈가 설정값 이상일때 처리
                    print("old : {0} , {1}".format(image.format , image.size))
                    
                    cropHeight = int(image.height/row) #조각별 세로길이
                    cropWidth = int(image.width/col)   #조각별 가로길이
                    
                    for i in range(0, row): #세로개수 만큼 반복
                        for j in range(0, col): #가로개수 만큼 반복
                            left = j*cropWidth
                            right = (j+1)*cropWidth
                            top = i*cropHeight
                            bottom = (i+1)*cropHeight
                            
                            #image[x1:x2, y1:y2] - 가로,세로 범위로 image 자르기
                            with image[left:right, top:bottom] as newimage:
                                print("new : {0} , {1}".format(newimage.format, newimage.size))
                                newimage.save(filename='{0}/{1}_{2}{3}.jpg'.format(filesave,oldfilename[file.rfind('/')+1:-4],i,j)) 
                                # {저장위치}/{파일명}_{상하단}{좌우}.jpg
                                
                                
class Imagedel:                               
    def imagedel(self,file1,size):
        from PIL import Image
        import os
        import glob
        file = str(file1)+"/*.jpg"          # 폴더 위치
        file_list=glob.glob(file)          # 파일 목록 저장
        
        DEL=[]  # 삭제할 사진들 주소 담기
        cn=-1
        for i in file_list:
            cn+=1
            i = Image.open('{}'.format(i)) #파일 경로 open
            width , height = i.size
            if height<=int(size):          # 포스터 세로 사이즈 500 이하일때 삭제
                DEL.append(file_list[cn])
                print("삭제되는 영화 포스터 사이즈",width, height)   # 사이즈가 너무 작아 인식을 못할 수 있음
                
                for j in DEL:
                    os.remove('{}'.format(j))
                    print("이미지가 삭제 되었습니다")  
        

class imagecut(Image4cut,Imagedel):
    def guide():
        print("변수=imagecut()")
        print("변수.image4cut(파일위치,저장위치,사이즈)")
        print("변수.imagedel(삭제위치,삭제할사이즈)")
        



if __name__=='__main__':                            # 모듈 설정
    print("image4cut(파일위치,저장위치,사이즈)")
    print("imagedel(삭제위치,삭제할사이즈)")