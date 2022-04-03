from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import sys


def get_time_period(st,et):
    st_list = st.split(":")
    et_list = et.split(":")
    
    
    if int(st_list[0]) == 12:
        st_list[0] = 0
    if int(et_list[0]) == 12:
        et_list[0] = 0
    
    if st_list[2] == "PM":
        st_list[0] = int(st_list[0]) +12
    if et_list[2] == "PM":
        et_list[0] = int(et_list[0]) +12
        
    del et_list[2], st_list[2]
    st_list = [int(x) for x in st_list ]
    et_list = [int(x) for x in et_list ]
    if et_list[1] > st_list[1]:
        st_list[1] = st_list[1]+60
        st_list[0] = st_list[0]-1
    hours =  st_list[0] - et_list[0]
    minutes = st_list[1] - et_list[1]
    if hours<0:
        hours = hours +24
    time_duration = (hours*60)+minutes
             

    return time_duration
 

app = Flask(__name__)

app.config["UPLOAD_FOLDER"] = "static/"

@app.route('/')
def upload_file():
    return render_template('index.html')
 
    
@app.route('/display', methods = ['GET', 'POST'])
def get_time_value():  
    if request.method == 'POST':       
        
        f = request.files['file']        
        filename = secure_filename(f.filename)
        f.save(app.config['UPLOAD_FOLDER'] + filename)
        f1 = open(app.config['UPLOAD_FOLDER']+filename,'r')
        matter = f1.read()
        mat=matter.upper();
        fomt="%I:%M:%p"
        totaltime=0;
        index=mat.find("TIME LOG:");
        if index!=-1:
            mat=mat[index+len("TIME LOG:"):]
            index=mat.find('-')
            count = 1
            while (index!=-1):
                if mat[index+1]==' ':
                    mat=mat[:index-1] + "#" + mat[index+2:];
                elif mat[index-1]==' ':
                    mat=mat[:index-2] + "#" + mat[index+1:]
                else:
                    mat=mat[:index-1] + "#" + mat[index+1:];
                index = mat.find("#",index-2,index+2);
                st = mat.rfind(" ",0,index);
                st = mat[st+1:index];
                et = mat.find("M",index,index+15);
                et = mat[index+1:et+1];
                st = st[:len(st)-2] + ":" + st[len(st)-2:]
                et = et[:len(et)-2] + ":" + et[len(et)-2:]
                
                try:                


                    st_list = st.split(":")
                    et_list = et.split(":")


                    if int(st_list[0]) >12 or int(et_list[0])> 12:
                        Error = "error at=",str(count)+"line"
                    else:                               
                        period = get_time_period(et,st)
                        Error = False

                    totaltime = totaltime + period

                except:
                    index = mat.find('-')
                    continue;
                index = mat.find('-')
                count = count+1
        
        if Error:
            output = Error
        else:
            output = "Total time spent by the author is "+str(int((totaltime)/60))+" hours "+str(int((totaltime)%60))+" mins"
        
            
        
        return render_template('index.html',prediction_text=output)
        
    return render_template('index.html')
                    

if __name__ == '__main__':
    app.run(debug = True)
