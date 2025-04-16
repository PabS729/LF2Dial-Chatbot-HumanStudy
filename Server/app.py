from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin

from functions import *

app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
conv_student = []
chat_history = ""
conv_teacher = []
conv_t_2 = []
conv_s_2 = []
chat_his = ""

@app.route("/k", methods = ["POST"])
@cross_origin()
def home():
    global chat_history
    teacher_res = opening()
    print("ran")
    
    chat_history = "teacher: " + teacher_res + "\n"
    conv_teacher.clear()
    conv_student.clear()
    conv_teacher.append(teacher_res)
    print(len(conv_teacher))
    print(teacher_res)
    return jsonify(teacher_res)

@app.route("/s", methods = ["POST"])
@cross_origin()
def home_s():
    global chat_his
    teacher_res = response_baseline(conv_teacher, conv_student)
    print("ran")
    
    chat_his = "teacher: " + teacher_res + "\n"
    conv_t_2.clear()
    conv_s_2.clear()
    conv_t_2.append(teacher_res)
    print(len(conv_teacher))
    print(teacher_res)
    return jsonify(teacher_res)

@app.route("/getReply-Base", methods = ['POST'])
@cross_origin()
def get_res_base():
    global chat_his
    print("called response baseline")
    req_data = request.get_json()
    print(req_data)
    temp = req_data['temp']
    print(temp)
    student_res = temp['msg']
    print(student_res)
    if "end conversation!" in student_res:
        f = open("demofile3_base.txt", "w")
        f.write(chat_his)
        f.close()
        return jsonify("ok, we are done.")
    conv_s_2.append(student_res)
    chat_his += "student: " + student_res + "\n"
    teacher_res = response_baseline(conv_t_2, conv_s_2)
    conv_t_2.append(teacher_res)
    chat_his += "teacher: " + teacher_res + "\n"
    # chat_history += "student: " + student_res + "\n"
    print(len(conv_s_2), len(conv_t_2))
    return jsonify(teacher_res)


@app.route("/getReply", methods = ['POST'])
@cross_origin()
def get_response():
    global chat_history
    print("called response")
    req_data = request.get_json()
    print(req_data)
    temp = req_data['temp']
    print(temp)
    student_res = temp['msg']
    print(student_res)
    if "end conversation!" in student_res:
        f = open("demofile3.txt", "w")
        f.write(chat_history)
        f.close()
        return jsonify("ok, we are done.")
    conv_student.append(student_res)
    
    chat_history += "student: " + student_res + "\n"
    thought, rle = check_student_response(chat_history=student_res)
    
    if thought in [6, 7]:
        teacher_res = predefined_response(thought, 2, conv_teacher, relevance=rle)
    else:
        teacher_res = FSM_response(student_res, conv_teacher, conv_student)
    conv_teacher.append(teacher_res)
    chat_history += "teacher: " + teacher_res + "\n"
    # chat_history += "student: " + student_res + "\n"
    print(len(conv_student), len(conv_teacher))
    return jsonify(teacher_res)

if __name__ == "__main__":
    app.run()