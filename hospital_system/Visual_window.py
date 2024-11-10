import tkinter as tk
from tkinter import messagebox
import json
import os

# 定义数据文件
USER_FILE = 'users.json'
PATIENT_FILE = 'patients.json'
DRUG_FILE = 'drugs.json'
EXAM_FILE = 'exams.json'
EXAM_PROJECT_FILE = 'exam_projects.json'
MY_ID = ''

# 初始化数据文件
def init_files():
    Administrators = {'username': 'A1', 'password': '123456', 'role': 'Administrator'}
    if not os.path.exists(USER_FILE):
        with open(USER_FILE, 'w') as file:
            json.dump([Administrators], file)
    if not os.path.exists(PATIENT_FILE):
        with open(PATIENT_FILE, 'w') as file:
            json.dump([], file)
    if not os.path.exists(DRUG_FILE):
        with open(DRUG_FILE, 'w') as file:
            json.dump([], file)
    if not os.path.exists(EXAM_FILE):
        with open(EXAM_FILE, 'w') as file:
            json.dump([], file)
    if not os.path.exists(EXAM_PROJECT_FILE):
        with open(EXAM_PROJECT_FILE, 'w') as file:
            json.dump([], file)


# 解析json数据
def load_data(file_name):
    with open(file_name, 'r') as file:
        return json.load(file)

# 保存json数据
def save_data(file_name, data):
    with open(file_name, 'w') as file:
        json.dump(data, file)

# 用户登录管理
def login(username, password):
    users = load_data(USER_FILE)
    for user in users:
        if user['username'] == username and user['password'] == password:
            return user
    return None

# 注册用户
def register_user(username, password, role):
    users = load_data(USER_FILE)
    for user in users:
        if user['username'] == username:
            print("Username already exists.")
            return False
    users.append({'username': username, 'password': password, 'role': role})
    save_data(USER_FILE, users)
    return True

def create_login_window():
    def attempt_login():
        username = username_entry.get()
        password = password_entry.get()
        user = login(username, password)
        if user:
            global MY_ID
            MY_ID = username
            messagebox.showinfo("Login Success", f"Logged in as {user['username']} with role {user['role']}")
            # 根据角色展示不同的界面
            if user['role'] == 'Administrator':
                login_window.destroy()
                create_admin_window()
                create_login_window()
            elif user['role'] == 'RBS':
                login_window.destroy()
                create_rbs_window()
                create_login_window()
            elif user['role'] == 'doctor':
                login_window.destroy()
                create_doctor_window()
                create_login_window()
            elif user['role'] == 'pharmacy':
                login_window.destroy()
                create_pharmacy_window()
                create_login_window()
            elif user['role'] == 'examiner':
                login_window.destroy()
                create_examiner_window()
                create_login_window()
        else:
            password_entry.delete(0,tk.END)
            messagebox.showerror("Login Failed", "The account or password is incorrect, login failed.")

    """def attempt_register():
        username = username_entry.get()
        password = password_entry.get()
        if register_user(username, password, role='patient'):
            messagebox.showinfo("Registration Success", "Registration successful.")
        else:
            messagebox.showerror("Registration Failed", "Registration failed.")"""

    login_window = tk.Tk()
    login_window.title("Login")
    login_window.geometry('540x240')

    tk.Label(login_window,text="\n").pack()
    tk.Label(login_window, text="Username:").pack()
    username_entry = tk.Entry(login_window)
    username_entry.pack()

    tk.Label(login_window, text="Password:").pack()
    password_entry = tk.Entry(login_window, show='*')
    password_entry.pack()

    tk.Button(login_window, text="Login", command=attempt_login).pack()
    # tk.Button(login_window, text="Register", command=attempt_register).pack()

    login_window.mainloop()



# 最高权限管理员界面
def delete_user(username):
    users = load_data(USER_FILE)
    for user in users:
        if user['username'] == username:
            users.remove(user)
            save_data(USER_FILE, users)
            return True
    print("Username doesn't exist.")
    return False

def create_admin_window():

    # 创建工作人员账号
    def register_worker():
        username = username_entry.get()
        password = password_entry.get()
        role = role_entry.get()
        if not username or not password or not role:
            messagebox.showerror("Error","Please input username, password, and role!")
            return
        if register_user(username, password, role):
            messagebox.showinfo("Registration Success", "Registration successful.")
            password_entry.delete(0,tk.END)
            role_entry.delete(0,tk.END)
        else:
            messagebox.showerror("Registration Failed", "Username already exists.")
            password_entry.delete(0, tk.END)
            role_entry.delete(0, tk.END)

    # 删除工作人员账号
    def delete_worker():
        username = username_entry.get()
        if not username:
            messagebox.showerror("Error","Please input username!")
            return
        if delete_user(username):
            messagebox.showinfo("Deletion Success", "Delete successful.")
            username_entry.delete(0,tk.END)
        else:
            messagebox.showerror("Deletion Failed", "Username doesn't exist.")

    # 查看所有工作人员列表
    def update_worker_list():
        workers = load_data(USER_FILE)
        workers.sort(key=lambda x: x["username"])
        worker_list.delete(0, tk.END)
        for worker in workers:
            if worker['role'] != 'patient':
                worker_list.insert(tk.END, f"Username: {worker['username']}, Role: {worker['role']}")
        save_data(USER_FILE,workers)

    # 创建tkinter窗口
    admin_window = tk.Tk()
    admin_window.title("Admin Panel")
    admin_window.geometry('960x540')

    # 创建账号
    tk.Label(admin_window, text="Username:").pack()
    username_entry = tk.Entry(admin_window)
    username_entry.pack()

    tk.Label(admin_window, text="Password:").pack()
    password_entry = tk.Entry(admin_window, show='*')
    password_entry.pack()

    tk.Label(admin_window, text="Role:").pack()
    role_entry = tk.Entry(admin_window)
    role_entry.pack()

    tk.Button(admin_window, text="Register Worker", command=register_worker).pack()

    # 删除账号
    tk.Button(admin_window, text="Delete Worker", command=delete_worker).pack()

    # 工作人员账号列表
    tk.Button(admin_window, text="Find Worker Account", command=update_worker_list).place(x=660,y=120)
    worker_list = tk.Listbox(admin_window)
    worker_list.pack(fill=tk.BOTH, expand=True)

    admin_window.mainloop()

# RBS界面
# 创建RBS窗口
def create_rbs_window():

    # 挂号模块
    def register_patient():
        patient_id = patient_id_entry.get()
        patient_name = patient_name_entry.get()
        doctor_id = doctor_id_entry.get()
        if not patient_name or not patient_id or not doctor_id:
            messagebox.showerror("Error", "Please enter patient name, patient ID and doctor ID!")
            return
        patients = load_data(PATIENT_FILE)
        for patient in patients:
            if patient['patient_id'] == patient_id and patient['statement'] == 'current':
                messagebox.showerror("Error", "Patient ID already exists.")
                return
        patients.append({'patient_id': patient_id, 'name': patient_name, 'doctor_id': doctor_id, 'diagnosis': '',
                         'prescription': [], 'statement': 'current'})
        save_data(PATIENT_FILE, patients)
        messagebox.showinfo("Success", "Patient registered successfully.")

    # 更新病人状态，结束看病
    def update_patient_statement(patient_id):
        patients = load_data(PATIENT_FILE)
        exams = load_data(EXAM_FILE)
        for patient in patients:
            if patient['patient_id'] == patient_id:
                patient['statement'] = 'history'
                messagebox.showinfo("Success","Patient Statement is already change.")
                break
        for exam in exams:
            if exam['patient_id'] == patient_id:
                exam['statement'] = 'history'
                messagebox.showinfo("Success","Exam Statement is already change.")
                break
        save_data(PATIENT_FILE, patients)
        save_data(EXAM_FILE, exams)

    # 收费模块
    def charge_patient():
        patient_id = patient_id_entry.get()
        drugs = load_data(DRUG_FILE)
        if not patient_id:
            messagebox.showerror("Error", "Please enter patient ID.")
            return
        amount = 0
        patients = load_data(PATIENT_FILE)
        exams = load_data(EXAM_FILE)
        for patient in patients:
            if patient['patient_id'] == patient_id and patient['statement'] == 'current':
                for i in range(len(patient['prescription'])):
                    for drug in drugs:
                        if drug['drug_name'] == patient['prescription'][i]['drug_name']:
                            amount += float(drug['price'])*int(patient['prescription'][i]['quantity'])
                            break
                for exam in exams:
                    if exam['patient_id'] == patient_id and exam['statement'] == 'current':
                        amount += float(exam['price'])
                if amount != 0:
                    messagebox.showinfo("Success", f"Charged {amount} to patient ID {patient_id}.")
                    update_patient_statement(patient_id)
                else:
                    messagebox.showerror("Error","you don't buy any medicine or make any exam.")
                return
        messagebox.showerror("Error", "Patient ID not found.")

    # 更新病人列表
    def update_patient_list():
        patients = load_data(PATIENT_FILE)
        patient_list.delete(0, tk.END)
        patients.sort(key = lambda x:x['statement'])
        for patient in patients:
            patient_list.insert(tk.END, f"ID: {patient['patient_id']}, Name: {patient['name']}, "
                                        f"Statement: {patient['statement']},用药如下：")
            for i in range(len(patient['prescription'])):
                patient_list.insert(tk.END,f"   Drug_name: {patient['prescription'][i]['drug_name']}, Quantity: "
                                           f"{patient['prescription'][i]['quantity']}")
        save_data(PATIENT_FILE, patients)


    # tkinter窗口创建
    rbs_window = tk.Tk()
    rbs_window.title("RBS Panel")
    rbs_window.geometry('960x540')

    # 挂号模块
    tk.Label(rbs_window, text="Patient ID:").pack()
    patient_id_entry = tk.Entry(rbs_window)
    patient_id_entry.pack()

    tk.Label(rbs_window, text="Patient Name:").pack()
    patient_name_entry = tk.Entry(rbs_window)
    patient_name_entry.pack()

    tk.Label(rbs_window, text="Doctor ID:").pack()
    doctor_id_entry = tk.Entry(rbs_window)
    doctor_id_entry.pack()

    tk.Button(rbs_window, text="Register Patient", command=register_patient).pack()

    #  收费模块
    tk.Button(rbs_window, text="Charge Patient", command=charge_patient).pack()

    # 查看药物需求
    tk.Button(rbs_window,text="Find Patients Information",command=update_patient_list).place(x=660,y=150)
    patient_list = tk.Listbox(rbs_window)
    patient_list.pack(fill=tk.BOTH, expand=True)

    rbs_window.mainloop()

# 医生界面
def create_doctor_window():

    # 更新诊断结果
    def update_diagnosis():
        patient_id = patient_id_entry.get()
        diagnosis = diagnosis_entry.get()
        if not patient_id and not diagnosis:
            messagebox.showerror("Error","Please input patient_id and diagnosis!")
            return
        patients = load_data(PATIENT_FILE)
        for patient in patients:
            if patient['patient_id'] == patient_id and patient['statement'] == 'current':
                if patient['doctor_id'] != MY_ID:
                    messagebox.showerror("Error","This is not your patient.")
                    return False
                patient['diagnosis'] = diagnosis
                save_data(PATIENT_FILE, patients)
                messagebox.showinfo("Success","Update diagnosis successfully.")
                return True
        messagebox.showerror("Error","input patient_id is incorrect!")

    # 申请检验功能
    def add_exams_application():
        patient_id = patient_id_entry.get()
        exam_project = exam_project_entry.get()
        if not patient_id or not exam_project:
            messagebox.showerror("Error","Please input patient_id and exam_project!")
            return
        exams = load_data(EXAM_FILE)
        for exam in exams:
            if exam['patient_id']==patient_id and exam['statement']=='current' and exam['exam_project']==exam_project:
                messagebox.showerror("Error","Project is already exists.")
                return False
        exams.append({'patient_id': patient_id, 'exam_project': exam_project, 'price':  '',  'examiner': '',
                      'result': '', 'statement': 'current'})
        messagebox.showinfo("Success","Exam application is accepted.")
        save_data(EXAM_FILE, exams)

    # 查看所有挂自己号的病人
    def find_patients():
        patients = load_data(PATIENT_FILE)
        patient_list.delete(0, tk.END)
        for patient in patients:
            if patient['doctor_id'] == MY_ID:
                patient_list.insert(tk.END,patient)

    # 查看检验结果
    def find_exams_result():
        patient_id = patient_id_entry.get()
        if not patient_id:
            messagebox.showerror("Error","Please input patient_id!")
        patient_list.delete(0, tk.END)
        exams = load_data(EXAM_FILE)
        for exam in exams:
            if exam['patient_id'] == patient_id and exam['statement'] == 'current':
                patient_list.insert(tk.END,exam)

    # 查看已有项目
    def find_project_class():
        patient_list.delete(0, tk.END)
        exam_projects = load_data(EXAM_PROJECT_FILE)
        patient_list.insert(tk.END, "以下是所有检验项目： ")
        for project in exam_projects:
            patient_list.insert(tk.END, f"  name:  {project['name']}   price:  {project['price']}")

    # 给病人开处方
    def add_prescription():
        patient_id = patient_id_entry.get()
        drug_name = drug_name_entry.get()
        quantity = quantity_entry.get()
        if not patient_id or not drug_name or not quantity:
            messagebox.showerror("Error","Please input patient_id, drug_name and quantity!")
        patients = load_data(PATIENT_FILE)
        drugs = load_data(DRUG_FILE)
        for patient in patients:
            if patient['patient_id'] == patient_id and patient['statement'] == 'current':
                for drug in drugs:
                    if drug_name == drug['drug_name']:
                        patient['prescription'].append({'drug_name': drug_name, 'quantity': int(quantity)})
                        messagebox.showinfo("Success","Add prescription successfully.")
                        save_data(PATIENT_FILE, patients)
                        return
                messagebox.showerror("Error","Pharmacy don't exist this medicine.")
                return
        messagebox.showerror("Error","Input patient_id or quantity is incorrect.")

    # tkinter窗口创建
    doctor_window = tk.Tk()
    doctor_window.title("Doctor Panel")
    doctor_window.geometry('960x540')

    tk.Label(doctor_window, text="Patient_ID: ").pack()
    patient_id_entry = tk.Entry(doctor_window)
    patient_id_entry.pack()

    # 诊断功能
    tk.Label(doctor_window, text="Diagnosis Result: ").pack()
    diagnosis_entry = tk.Entry(doctor_window)
    diagnosis_entry.pack()
    tk.Button(doctor_window, text="Update Diagnosis", command=update_diagnosis).pack()

    # 申请检验功能
    tk.Label(doctor_window, text="Exam Project: ").pack()
    exam_project_entry = tk.Entry(doctor_window)
    exam_project_entry.pack()
    tk.Button(doctor_window, text="Add Exam Application", command=add_exams_application).pack()

    # 查看病人信息,查看检查结果,查看已有项目
    tk.Button(doctor_window, text="Find Patients", command=find_patients).place(x=660,y=90)
    tk.Button(doctor_window, text="Find Exam Result", command=find_exams_result).place(x=660,y=150)
    tk.Button(doctor_window, text="Find Project Class", command=find_project_class).place(x=660,y=120)
    patient_list = tk.Listbox(doctor_window)
    patient_list.pack(fill=tk.BOTH, expand=True)

    # 开药功能
    tk.Label(doctor_window, text="Drug Name: ").pack()
    drug_name_entry = tk.Entry(doctor_window)
    drug_name_entry.pack()
    tk.Label(doctor_window, text="Quantity: ").pack()
    quantity_entry = tk.Entry(doctor_window)
    quantity_entry.pack()
    tk.Button(doctor_window, text="Add Prescription", command=add_prescription).pack()

    doctor_window.mainloop()

# 药房界面
def create_pharmacy_window():

    # 发药更新库存
    def update_drug_stock():
        patient_id = patient_id_entry.get()
        patients = load_data(PATIENT_FILE)
        for patient in patients:
            if patient['patient_id'] == patient_id and patient['statement'] == 'current':
                if len(patient['prescription']) == 0:
                    messagebox.showerror("Error","Doctor is not create the prescription!")
                    return
                drugs = load_data(DRUG_FILE)
                for i in range(len(patient['prescription'])):
                    drug_name = patient['prescription'][i]['drug_name']
                    quantity = patient['prescription'][i]['quantity']
                    flag = 1
                    for drug in drugs:
                        if drug['drug_name'] == drug_name:
                            drug['stock'] -= int(quantity)
                            flag = 0
                        if flag:
                            messagebox.showerror("Error",f"Pharmacy don't have {drug_name}!")
                messagebox.showinfo("Success", "Dispensing successfully!")
                save_data(DRUG_FILE, drugs)
                return
        messagebox.showerror("Error","Patient_ID is incorrect!")

    # 添加药品库存
    def add_drug():
        drug_name = drug_name_entry.get()
        drug_id = drug_id_entry.get()
        stock = stock_entry.get()
        price = price_entry.get()
        if not drug_name or not drug_id or not stock or not price:
            messagebox.showerror("Error","Please input drug_name, drug_id, stock and price!")
            return
        drugs = load_data(DRUG_FILE)
        for drug in drugs:
            if drug['drug_id'] == drug_id:
                drug['stock'] += int(stock)
                messagebox.showinfo("Success","Drug exist, already add stock.")
                save_data(DRUG_FILE, drugs)
                return
        drugs.append({'drug_id': drug_id, 'drug_name': drug_name, 'stock': int(stock), 'price': float(price)})
        messagebox.showinfo("Success","Add drup successfully!")
        save_data(DRUG_FILE, drugs)

    # 查看所有库存
    def find_stock():
        drug_list.delete(0, tk.END)
        drugs = load_data(DRUG_FILE)
        drug_list.insert(tk.END,"以下为药品库存： ")
        for drug in drugs:
            drug_list.insert(tk.END, f"  {drug}")

    # 查看所有用药需求
    def find_drug_requirement():
        drug_list.delete(0,tk.END)
        patients = load_data(PATIENT_FILE)
        patients.sort(key = lambda x:x['statement'])
        save_data(PATIENT_FILE, patients)
        for patient in patients:
            drug_list.insert(tk.END,"Patient_id: %s, Statement: %s 以下是所需的药品：" % (patient['patient_id']
                                                                                         ,patient['statement']))
            for i in range(len(patient['prescription'])):
                drug_list.insert(tk.END,"   Drug_name: %s, Quantity: %s"
                      % (patient['prescription'][i]['drug_name'], patient['prescription'][i]['quantity']))

    def delete_drug():
        drug_id = drug_id_entry.get()
        if not drug_id:
            messagebox.showerror("Error","Please input drug_id!")
            return
        drugs = load_data(DRUG_FILE)
        for drug in drugs:
            if drug['drug_id'] == drug_id:
                drugs.pop(drugs.index(drug))
                messagebox.showinfo("Success","Delete drug successfully!")
                save_data(DRUG_FILE, drugs)
                return
        messagebox.showerror("Error","Don't exist this drug!")


    # 创建tkinter窗口
    pharmacy_window = tk.Tk()
    pharmacy_window.title("Pharmacy Panel")
    pharmacy_window.geometry('960x540')

    # 发药
    tk.Label(pharmacy_window, text="Patient ID: ").pack()
    patient_id_entry = tk.Entry(pharmacy_window)
    patient_id_entry.pack()
    tk.Button(pharmacy_window, text="Dispensing", command=update_drug_stock).pack()

    # 删除药品
    tk.Label(pharmacy_window, text="Drug ID: ").pack()
    drug_id_entry = tk.Entry(pharmacy_window)
    drug_id_entry.pack()
    tk.Button(pharmacy_window, text="Delete Drug", command=delete_drug).pack()

    # 更新库存
    tk.Label(pharmacy_window, text="Drug Name: ").pack()
    drug_name_entry = tk.Entry(pharmacy_window)
    drug_name_entry.pack()
    """tk.Label(pharmacy_window, text="Quantity: ").pack()
    quantity_entry = tk.Entry(pharmacy_window)
    quantity_entry.pack()"""
    # tk.Button(pharmacy_window, text="Dispensing", command=update_drug_stock).pack()

    """# 删除药品
    tk.Label(pharmacy_window, text="Drug ID: ").pack()
    drug_id_entry = tk.Entry(pharmacy_window)
    drug_id_entry.pack()
    tk.Button(pharmacy_window, text="Delete Drug", command=delete_drug).pack()"""

    # 更新库存
    tk.Label(pharmacy_window, text="stock: ").pack()
    stock_entry = tk.Entry(pharmacy_window)
    stock_entry.pack()
    tk.Label(pharmacy_window, text="price: ").pack()
    price_entry = tk.Entry(pharmacy_window)
    price_entry.pack()
    tk.Button(pharmacy_window, text="Add Drug", command=add_drug).pack()

    # 显示需要、库存
    tk.Button(pharmacy_window, text="Find Stock", command=find_stock).place(x=660,y=150)
    tk.Button(pharmacy_window, text="Find Drug Requirement", command=find_drug_requirement).place(x=660,y=180)
    drug_list = tk.Listbox(pharmacy_window)
    drug_list.pack(fill=tk.BOTH,expand=True)

    pharmacy_window.mainloop()

# 检验界面
def create_examiner_window():

    # 添加检验结果
    def add_exam_result():
        patient_id = patient_id_entry.get()
        result = result_entry.get()
        exams = load_data(EXAM_FILE)
        exam_projects = load_data(EXAM_PROJECT_FILE)
        if not result or not patient_id:
            messagebox.showerror("Error","Please input patient_id and result.")
            return
        for exam in exams:
            if exam['patient_id'] == patient_id and exam['statement'] == 'current':
                exam['result'] = result
                exam['examiner'] = MY_ID
                for project in exam_projects:
                    if exam['exam_project'] == project['name']:
                        exam['price'] = project['price']
                messagebox.showinfo("Success","Add exam result successfully.")
                save_data(EXAM_FILE, exams)
                return
        messagebox.showerror("Error","Don't find exam application.")

    # 查看检验申请
    def find_exam_application():
        exam_list.delete(0, tk.END)
        exams = load_data(EXAM_FILE)
        exams.sort(key = lambda x:x['statement'])
        for exam in exams:
            exam_list.insert(tk.END,"Patient_id：%s  Exam_Project: %s  Statement: %s  Result: %s  Price: %s"
                             % (exam['patient_id'], exam['exam_project'], exam['statement'], exam['result'],exam['price']))
        save_data(EXAM_FILE, exams)

    # 添加检验项目
    def add_exam_project():
        exam_projects = load_data(EXAM_PROJECT_FILE)
        exam_project = exam_project_entry.get()
        price = price_entry.get()
        if not exam_project or not price:
            messagebox.showerror("Error","Please input exam project and price!")
            return
        for project in exam_projects:
            if project['name'] == exam_project:
                project['price'] = price
                messagebox.showinfo("Success","It has already added!")
                return
        exam_projects.append({"name":exam_project,"price":price})
        save_data(EXAM_PROJECT_FILE, exam_projects)
        messagebox.showinfo("Success","It has already added!")


    # 查看已有项目
    def find_project_class():
        exam_list.delete(0, tk.END)
        exam_projects = load_data(EXAM_PROJECT_FILE)
        exam_list.insert(tk.END,"以下是所有检验项目： ")
        for project in exam_projects:
            exam_list.insert(tk.END,f"  name:  {project['name']}   price:  {project['price']}")


    # 创建tkinter窗口
    examiner_window = tk.Tk()
    examiner_window.title("Examiner Panel")
    examiner_window.geometry("960x540")

    # 检验结果
    tk.Label(examiner_window, text="Patient_ID: ").pack()
    patient_id_entry = tk.Entry(examiner_window)
    patient_id_entry.pack()
    tk.Label(examiner_window, text="Exam Result: ").pack()
    result_entry = tk.Entry(examiner_window)
    result_entry.pack()
    tk.Button(examiner_window, text="Add Exam Result", command=add_exam_result).pack()

    # 添加检验项目
    tk.Label(examiner_window, text="Exam Project: ").pack()
    exam_project_entry = tk.Entry(examiner_window)
    exam_project_entry.pack()
    tk.Label(examiner_window, text="Price: ").pack()
    price_entry = tk.Entry(examiner_window)
    price_entry.pack()
    tk.Button(examiner_window, text="Add Exam Project", command=add_exam_project).pack()

    # 查看检验申请
    tk.Button(examiner_window, text="Find Exam Application", command=find_exam_application).place(x=660,y=120)
    # 查看已有项目
    tk.Button(examiner_window, text="Find Project Class", command=find_project_class).place(x=660, y=150)
    exam_list = tk.Listbox(examiner_window)
    exam_list.pack(fill=tk.BOTH,expand=True)

    examiner_window.mainloop()

if __name__ == '__main__':
    init_files()
    create_login_window()
