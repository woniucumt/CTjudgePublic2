def qianji():
    rizhi=[]
    jizongshu=100
    qianzongshu=100
    gongji=1
    for i in range(20):
        muji=1
        for i in range(33):
            xiaoji=100-gongji-muji
            if gongji*50+muji*30+xiaoji*10/3==1000:
                print(gongji,muji,xiaoji)
            muji+=1
        gongji+=1
    return 0
#qt   
  #xunhuan  
    
    

        