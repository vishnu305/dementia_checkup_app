from flask import Flask,render_template,request,flash,redirect,url_for
from werkzeug.utils import secure_filename

from PIL import ImageTk, Image, ImageDraw
import PIL
from tkinter import *
import datetime
from skimage.metrics import structural_similarity
import cv2
import numpy as np

import os

app = Flask(__name__)
app.secret_key = "secret key"

@app.route('/')
def front_page():
    return render_template('3.html')
@app.route('/4')
def page4():
    return render_template('4.html')
@app.route('/phase1')
def phase1():
    return render_template('phase1.html')
@app.route('/phase1test1')
def phase1test1():
    width = 200  # canvas width
    height = 200 # canvas height
    center = height//2
    white = (155, 155, 155) # canvas back
    
    def save(master):
        global count
        count =0
        # save image to hard drive
        # filename = "user_input.jpg"
        # output_image.save(filename)
        
        # with open('Image.jpg', 'rb') as f:
        #     content1 = f.read()
        # with open('user_input.jpg', 'rb') as f:
        #     content2 = f.read()
        # if content1 == content2:
        #     count = count +1
        # else:
        #     count=0
        image1 = cv2.imread('Image.jpg',0)
        # image2 = cv2.imread('user_input.jpg',0)
        if orb_sim(image1,np.asarray(output_image))*100 > 95:
            count = count+1
        else:
            count = 0

        master.destroy()  
        
        
    def orb_sim(img1,img2):
        orb = cv2.ORB_create()
        kp_a, desc_a = orb.detectAndCompute(img1,None)
        kp_b, desc_b = orb.detectAndCompute(img2,None)
        bf = cv2.BFMatcher(cv2.NORM_HAMMING,crossCheck=True)
        matches = bf.match(desc_a,desc_b)
        similarity_regions = [i for i in matches if i.distance<50]
        if len(matches) == 0:
            return 0
        return len(similarity_regions)/len(matches)
    def paint(event):
        x1, y1 = (event.x - 1), (event.y - 1)
        x2, y2 = (event.x + 1), (event.y + 1)
        canvas.create_oval(x1, y1, x2, y2, fill="black",width=5)
        draw.line([x1, y1, x2, y2],fill="black",width=5)

    master = Tk()

    # create a tkinter canvas to draw on
    canvas = Canvas(master, width=width, height=height, bg='white')
    canvas.pack()

    # create an empty PIL image and draw object to draw on
    output_image = PIL.Image.new("RGB", (width, height), color=(255,255,255))
    draw = ImageDraw.Draw(output_image)
    canvas.pack(expand=YES, fill=BOTH)
    canvas.bind("<B1-Motion>", paint)

    # add a button to save the image
    button=Button(text="submit",command=lambda: save(master))
    button.pack()

    master.mainloop()
    if(count==1):
            result1 = "You  are not having Dementia"
    else:
        result1="You are suspected for having Dementia"
    return render_template('resultphase1test1.html',resulttext=result1,resultvalue=count)
 
@app.route('/phase1test2part1',methods=['GET','POST'])
def phase1test2part1():
    if request.method == 'GET':
        return render_template('p1test2part1.html')
    else:
        value = request.form['p1t2p1']
        global countp1t2
        if value=='1' or value==1:
            countp1t2 = 1
        else:
            countp1t2 = 0
        return render_template('p1test2part2.html',count=countp1t2)
@app.route('/phase1test2part2',methods=['GET','POST'])
def phase1test2part2():
    if request.method == 'POST':
        value = request.form['p1t2p2']
        countp1t2 = request.form['count1']
        countp1t2 = int(countp1t2)
        if value=='2' or value==2:
            countp1t2 += 1
        return render_template('p1test2part3.html',count=countp1t2)
@app.route('/phase1test2part3',methods=['GET','POST'])
def phase1test2part3():
    if request.method == 'POST':
        value = request.form['p1t2p3']
        countp1t2 = request.form['count1']
        countp1t2 = int(countp1t2)
        if value=='2' or value==2:
            countp1t2 += 1
        if countp1t2 >= 2:
            resulttext='You are not having dementia'
        else:
            resulttext='Your are suspected for having dementia'
        print(countp1t2)
        return render_template('resultphase1test2.html',resulttext=resulttext,resultvalue=countp1t2)
@app.route('/phase2')
def phase2():
    return render_template('p2.html')
@app.route('/phase2test1',methods=['GET','POST'])
def phase2test1():
    if request.method == 'GET':
        return render_template('p2test1.html')
@app.route('/phase2test1part2',methods=['GET','POST'])
def phase2test1part2():
    if request.method == 'GET':
        return render_template('p2test1part2.html')
    else:
        name = request.form['p2t1name']
        address = request.form['p2t1address']
        if name.lower()=='lucky sehwag' and address.lower()=='indira nagar lucknow':
            count=2
        elif name.lower()=='lucky sehwag' or address.lower()=='indira nagar lucknow':
            count=1
        else:
            count=0
        print('phase2 test1 result',count)
        countforD=0
        countforSD=0
        countforND=0
        if(count==0):
            countforD=countforD+1
        elif(count==1):
            countforSD=countforSD+1
        elif(count==2):
            countforND=countforND+1
        return render_template('p2test2.html',countforD=countforD,countforSD=countforSD,countforND=countforND)
@app.route('/phase2test2',methods=['GET','POST'])
def phase2test2():
    if request.method == 'POST':
        year = int(request.form['p2t2year'])
        month = int(request.form['p2t2month'])
        day = int(request.form['p2t2day'])
        countforD = request.form['countforD']
        countforSD = request.form['countforSD']
        countforND = request.form['countforND']

        current_time = datetime.datetime.now()
        y=current_time.year
        m=current_time.month
        d=current_time.day
        count=0
        if year == y and month == m and day==d:
            count = int(count)+2
        elif year==y and month==m or month==m and day==d or day==d and year==y:
            count = int(count)+1
        print('phase2 test2 result',count)
        if(count==0):
            countforD=int(countforD)+1
        elif(count==1):
            countforSD=int(countforSD)+1
        elif(count==2):
            countforND=int(countforND)+1
        return render_template('p2test3.html',countforD=countforD,countforSD=countforSD,countforND=countforND)

@app.route('/phase2test3',methods=['GET','POST'])
def phase2test3():
    if request.method == 'POST':
        response = request.form['p2t3q1']
        response1 = request.form['p2t3q2']
        response2 = request.form['p2t3q3']
        response3 = request.form['p2t3q4']
        response4 = request.form['p2t3q5']
        response5 = request.form['p2t3q6']
        countforD = request.form['countforD']
        countforSD = request.form['countforSD']
        countforND = request.form['countforND']
        count=0
        if(response=='Yes'or response=='yes' or response=='YES'):
            count=1+count
        else:
            count=0+count
        if(response1=='Yes'or response1=='yes' or response1=='YES'):
            count=1+count
        else:
            count=0+count
        if(response2=='Yes'or response2=='yes' or response2=='YES'):
            count=1+count
        else:
            count=0+count
        if(response3=='Yes'or response3=='yes' or response3=='YES'):
            count=1+count
        else:
            count=0+count
        if(response4=='Yes'or response4=='yes' or response4=='YES'):
            count=1+count
        else:
            count=0+count
        if(response5=='Yes'or response5=='yes' or response5=='YES'):
            count=1+count
        else:
            count=0+count
        
        print('result of phase2 test3 is',count)
        if(count>4):
            countforND=int(countforND) + 1

        elif (count>=2 and count<=4 ):
            countforSD=int(countforSD) + 1
        else:
            countforD=int(countforD)+ 1
        return render_template('p2test4.html',countforD=countforD,countforSD=countforSD,countforND=countforND)
            
@app.route('/phase2test4',methods=['GET','POST'])
def phase2test4():
    if request.method == 'POST':
        countforD = request.form['countforD']
        countforSD = request.form['countforSD']
        countforND = request.form['countforND']
        count=0
        name = request.form['p2t4name']
        address = request.form['p2t4address']
        if name.lower()=='lucky sehwag' and address.lower()=='indira nagar lucknow':
            count=2
        elif name.lower()=='lucky sehwag' or address.lower()=='indira nagar lucknow':
            count=1
        else:
            count=0
        print('phase2 test4 result',count)
        if(count==0):
            countforD=int(countforD)+1
        elif(count==1):
            countforSD=int(countforSD)+1
        elif(count==2):
            countforND=int(countforND)+1
        return render_template('p2test5.html',countforD=countforD,countforSD=countforSD,countforND=countforND)

@app.route('/phase2test5',methods=['GET','POST'])
def phase2test5():
    if request.method == 'POST':
        response = request.form['p2t5q1']
        response1 = request.form['p2t5q2']
        response2 = request.form['p2t5q3']
        response3 = request.form['p2t5q4']
        response4 = request.form['p2t5q5']
        response5 = request.form['p2t5q6']
        countforD = request.form['countforD']
        countforSD = request.form['countforSD']
        countforND = request.form['countforND']
        count=0
        if(response==''or response==''):
            count=count+0
        elif(response=='Maybe' or response=='maybe' or response=='MAYBE'):            
            count=count+2          
        elif(response=='No'or response=='no'):       
            count=count+2
        elif(response=='Yes' or response=='yes' or response=='YES') :
            count=count+3

        if(response1==''or response1==''):
            count=count+0
        elif(response1=='Maybe' or response1=='maybe' or response1=='MAYBE'):            
            count=count+2          
        elif(response1=='No'or response1=='no'):       
            count=count+2
        elif(response1=='Yes' or response1=='yes' or response1=='YES') :
            count=count+3

        if(response2==''or response2==''):
            count=count+0
        elif(response2=='Maybe' or response2=='maybe' or response2=='MAYBE'):            
            count=count+2          
        elif(response2=='No'or response2=='no'):       
            count=count+2
        elif(response2=='Yes' or response2=='yes' or response2=='YES') :
            count=count+3

        if(response3==''or response3==''):
            count=count+0
        elif(response3=='Maybe' or response3=='maybe' or response3=='MAYBE'):            
            count=count+2          
        elif(response3=='No'or response3=='no'):       
            count=count+2
        elif(response3=='Yes' or response3=='yes' or response3=='YES') :
            count=count+3

        if(response4==''or response4==''):
            count=count+0
        elif(response4=='Maybe' or response4=='maybe' or response4=='MAYBE'):            
            count=count+2          
        elif(response4=='No'or response4=='no'):       
            count=count+2
        elif(response4=='Yes' or response4=='yes' or response4=='YES') :
            count=count+3

        if(response5==''or response5==''):
            count=count+0
        elif(response5=='Maybe' or response5=='maybe' or response5=='MAYBE'):            
            count=count+2          
        elif(response5=='No'or response5=='no'):       
            count=count+2
        elif(response5=='Yes' or response5=='yes' or response5=='YES') :
            count=count+3
        
        print('phase2 test5 result',count)
        if(count>10):
            countforD=int(countforD) + 1
        elif(count>=6 and count<=10):
            countforSD=int(countforSD) + 1
        else:
            countforND=int(countforND) + 1
        return render_template('p2test6.html',countforD=countforD,countforSD=countforSD,countforND=countforND)
@app.route('/phase2test6',methods=['GET','POST'])
def phase2test6():
    if request.method == 'POST':
        response = request.form['p2t6q1']
        response1 = request.form['p2t6q2']
        response2 = request.form['p2t6q3']
        response3 = request.form['p2t6q4']
        response4 = request.form['p2t6q5']
        response5 = request.form['p2t6q6']
        response6 = request.form['p2t6q7']
        response7 = request.form['p2t6q8']
        response8 = request.form['p2t6q9']
        response9 = request.form['p2t6q10']
        response10 = request.form['p2t6q11']
        response11= request.form['p2t6q12']
        response12 = request.form['p2t6q13']
        response13 = request.form['p2t6q14']
        response14 = request.form['p2t6q15']

        countforD = request.form['countforD']
        countforSD = request.form['countforSD']
        countforND = request.form['countforND']
        count=0
        if(response.lower()=='true'or response.lower()=='yes' ):
            count=count+1
        else: 
            count=count+0
        if(response1.lower()=='true'or response1.lower()=='yes' ):
            count=count+1
        else: 
            count=count+0
        if(response2.lower()=='true'or response2.lower()=='yes' ):
            count=count+1
        else: 
            count=count+0
        if(response3.lower()=='true'or response3.lower()=='yes' ):
            count=count+1
        else: 
            count=count+0
        if(response4.lower()=='true'or response4.lower()=='yes' ):
            count=count+1
        else: 
            count=count+0
        if(response5.lower()=='true'or response5.lower()=='yes' ):
            count=count+1
        else: 
            count=count+0
        if(response6.lower()=='true'or response6.lower()=='yes' ):
            count=count+1
        else: 
            count=count+0
        if(response7.lower()=='true'or response7.lower()=='yes' ):
            count=count+1
        else: 
            count=count+0
        if(response8.lower()=='true'or response8.lower()=='yes' ):
            count=count+1
        else: 
            count=count+0
        if(response9.lower()=='true'or response9.lower()=='yes' ):
            count=count+1
        else: 
            count=count+0
        if(response10.lower()=='true'or response.lower()=='yes' ):
            count=count+1
        else: 
            count=count+0
        if(response.lower()=='true'or response11.lower()=='yes' ):
            count=count+1
        else: 
            count=count+0
        if(response.lower()=='true'or response12.lower()=='yes' ):
            count=count+1
        else: 
            count=count+0
        if(response.lower()=='true'or response13.lower()=='yes' ):
            count=count+1
        else: 
            count=count+0
        if(response.lower()=='true'or response14.lower()=='yes' ):
            count=count+1
        else: 
            count=count+0
        print('result for phase 2 test6',count)
        if(count>=5 and count<=8):
            countforND=int(countforND) + 1
        elif(count>=9 and count<=12):
            countforSD=int(countforSD) + 1
        elif(count>=13 and count<=15):
            countforD=int(countforD) + 1
        return render_template('p2test7.html',countforD=countforD,countforSD=countforSD,countforND=countforND)
        
           
@app.route('/phase2test7',methods=['GET','POST'])
def phase2test7():
    if request.method == 'POST':
        response1 = request.form['firstimage']
        response2 = request.form['secondimage']
        response3 = request.form['thirdimage']
        countforD = request.form['countforD']
        countforSD = request.form['countforSD']
        countforND = request.form['countforND']
        count=0
        if(response1.lower()=='dog'):
            count=count+1
        if(response2.lower()=='cat'):
            count=count+1
        if(response3.lower()=='elephant'):
            count=count+1
        
        if(count==3):
            countforND=int(countforND) +1
        elif(count==2):
            countforSD=int(countforSD) + 1
        elif(count==1 or count==0):
            countforSD=int(countforSD) + 1
        else:
            countforD=int(countforD)+ 1
        print('phase2 test7 result',count)
        countforD=int(countforD)
        countforSD=int(countforSD)
        countforND=int(countforND)

        return render_template('resultphase2.html',countforD=countforD,countforSD=countforSD,countforND=countforND)

if __name__ == '__main__':
    app.run()