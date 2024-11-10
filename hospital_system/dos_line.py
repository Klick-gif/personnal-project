import json
import os

# 定义数据文件
USER_FILE = 'users.json'
PATIENT_FILE = 'patients.json'
DRUG_FILE = 'drugs.json'
EXAM_FILE = 'exams.json'
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

def delete_user(username):
    users = load_data(USER_FILE)
    for user in users:
        if user['username'] == username:
            users.pop(users.index(user))
            save_data(USER_FILE, users)
            return True
    print("Username don't exist.")
    return False

def update_patient_statement(patient_id):
    patients = load_data(PATIENT_FILE)
    exams = load_data(EXAM_FILE)
    for patient in patients:
        if patient['patient_id'] == patient_id:
            patient['statement'] = 'history'
            print("PATIENT_FILE is already change.")
            break
    for exam in exams:
        if exam['patient_id'] == patient_id:
            exam['statement'] = 'history'
            print("EXAM_FILE is already change.")
            break
    save_data(PATIENT_FILE, patients)
    save_data(EXAM_FILE, exams)


# 最高权限管理员
def admin():
    while True:
        print("--" * 50)
        print("1. Create workers account")
        print("2. All worker")
        print("3. Delete account")
        print("4. Exit")
        print("--" * 50)
        choice = input("Enter your choice: ")
        if choice == '1':
            username = input("Enter username: ")
            password = input("Enter password: ")
            role = input("Enter role: ")
            if register_user(username, password, role):
                print("Registration successful.")
            else:
                print("Registration failed.")
        elif choice == '2':
            users = load_data(USER_FILE)
            users.sort(key = lambda x:x["username"])
            for user in users:
                if user['role'] != 'patient':
                    print(user)
        elif choice == '3':
            username = input("Enter username: ")
            if delete_user(username):
                print("Delete successful.")
            else:
                print("Delete failed.")

        elif choice == '4':
            break
        else:
            print("Invalid choice. Please try again.")

# 挂号收费人员
def add_patient(patient_id, name, doctor_id):
    patients = load_data(PATIENT_FILE)
    for patient in patients:
        if patient['patient_id'] == patient_id and patient['statement'] == 'current':
            print("patient already exits.")
            print("Registered failed.")
            return False

    patients.append({'patient_id': patient_id, 'name': name, 'doctor_id': doctor_id, 'diagnosis': '',
             'prescription': [], 'statement':'current'})
    print("Registered successfully.")
    save_data(PATIENT_FILE, patients)

def charge_patient():
    # 这里可以实现收费逻辑，例如记录收费信息等
    drugs = load_data(DRUG_FILE)
    find_drug_requirement()
    amount = 0
    patient_id = input("Enter patient_id: ")
    quantity = 1
    while True:
        drug_name = input("Enter drug_name: ")
        quantity = int(input("Enter quantity: "))
        if quantity == 0:
            break
        flag = 1
        for drug in drugs:
            if drug['drug_name'] == drug_name:
                price = drug["price"]
                amount += price * quantity
                flag = 0
                break
        if flag:
            print("Drug_name input error.")
    print(f"Charged {amount} for patient {patient_id}")
    update_patient_statement(patient_id)


def RBS():
    while True:
        print("--" * 50)
        print("1. Registered")  # 挂号
        print("2. Charges")     # 收费
        print("3. Exit")        # 离开
        print("--" * 50)
        choice = input("Enter your choice: ")
        if choice == '1':
            patient_id = input("Enter patient_id: ")
            name = input("Enter name: ")
            doctor = input("Enter doctor_id: ")
            add_patient(patient_id,name,doctor)
        elif choice == '2':
            charge_patient()
        elif choice == '3':
            break
        else:
            print("Invalid choice. Please try again.")


# 医生模块

def find_patients(MY_ID):
    patients = load_data(PATIENT_FILE)
    for patient in patients:
        if patient['doctor_id'] == MY_ID:
            print('  ',patient)
def update_diagnosis(patient_id, diagnosis):
    patients = load_data(PATIENT_FILE)
    for patient in patients:
        if patient['patient_id'] == patient_id and patient['statement'] == 'current':
            if patient['doctor_id'] != MY_ID:
                print("This is not your patient.")
                return False
            patient['diagnosis'] = diagnosis
            save_data(PATIENT_FILE, patients)
            return True
    print("input patient_id error!")

def add_exams_application(patient_id, exam_project):
    exams = load_data(EXAM_FILE)
    exams.append({'patient_id':patient_id,'exam_project':exam_project,'examiner':'',
                  'result':'','statement':'current'})
    save_data(EXAM_FILE, exams)

def find_exams_result(patient_id):
    exams = load_data(EXAM_FILE)
    for exam in exams:
        if exam['patient_id'] == patient_id and exam['statement'] == 'current':
            print(exam)

def add_prescription(patient_id, drug_name, quantity):
    patients = load_data(PATIENT_FILE)
    for patient in patients:
        if patient['patient_id'] == patient_id and patient['statement'] == 'current':
            patient['prescription'].append({'drug_name': drug_name, 'quantity': quantity})
            print("Add prescription successfully.")
            break
    save_data(PATIENT_FILE, patients)
def Doctor():
    while True:
        print("--" * 50)
        print("1. Diagnostics")  # 诊断
        print("2. Exit")
        print("--" * 50)
        choice = input("Enter your choice: ")
        if choice == '1':
            print("以下是你的病人： ")
            find_patients(MY_ID)
            patient_id = input("Enter patient_id: ")
            diagnosis = input("Enter diagnosis: ")
            update_diagnosis(patient_id, diagnosis)
            while True:
                print("--" * 50)
                print("1. Exam application")   # 检验申请
                print("2. Exam Result")        # 检验结果
                print("3. Prescribe")          # 开药
                print("4. diagnosis again")    #重新诊断
                print("5. Exit")
                print("--" * 50)
                choice2 = input("Enter your choice: ")
                if choice2 == '1':
                    exam_project = input("Enter exam_project: ")
                    add_exams_application(patient_id,exam_project)
                elif choice2 == '2':
                    print("检验结果如下： ")
                    find_exams_result(patient_id)
                elif choice2 == '3':
                    drug_name = input("Enter drug_name: ")
                    quantity = input("Enter quantity: ")

                    add_prescription(patient_id,drug_name,quantity)
                elif choice2 == '4':
                    diagnosis = input("Enter diagnosis: ")
                    update_diagnosis(patient_id, diagnosis)
                elif choice2 == '5':
                    break
                else:
                    print("Invalid choice. Please try again.")
        elif choice == '2':
            break
        else:
            print("Invalid choice. Please try again.")

# 药品管理
def add_drug(drug_id, drug_name, stock, price):
    drugs = load_data(DRUG_FILE)
    for drug in drugs:
        if drug['drug_id'] == drug_id:
            drug['stock'] += stock
            print("Drug exist, already add stock.")
            save_data(DRUG_FILE, drugs)
            return
    drugs.append({'drug_id': drug_id, 'drug_name': drug_name, 'stock': stock, 'price': price})
    print("Add drup successfully.")
    save_data(DRUG_FILE, drugs)

def update_drug_stock(drug_name, quantity):
    drugs = load_data(DRUG_FILE)
    for drug in drugs:
        if drug['drug_name'] == drug_name:
            drug['stock'] -= int(quantity)
            break
    print("Dispensing successfully.")
    save_data(DRUG_FILE, drugs)

def find_drug_requirement():
    patients = load_data(PATIENT_FILE)
    for patient in patients:
        if patient['statement'] == 'current':
            print("patient_id: %s, 以下是所需的药品："%(patient['patient_id']))
            for i in range(len(patient['prescription'])):
                print("drug_name: %s, quantity: %s"
                      %(patient['prescription'][i]['drug_name'],patient['prescription'][i]['quantity']),)
            break

def find_stock():
    drugs = load_data(DRUG_FILE)
    print("以下为药品库存： ")
    for drug in drugs:
        print('  ', drug)

def Pharmacy():
    while True:
        print("--" * 50)
        print("1. dispensing")  # 发药
        print("2. stock control")  # 库存管理
        print("3. find stock")    # 查看库存
        print("4. Exit")
        print("--" * 50)
        choice = input("Enter your choice: ")
        if choice == '1':
            find_drug_requirement()
            drug_name = input("Enter drug_name: ")
            quantity = input("Enter quantity: ")
            update_drug_stock(drug_name,quantity)
        elif choice == '2':
            drug_id = input("Enter drug_id: ")
            drug_name = input("Enter drug_name: ")
            stock = int(input("Enter stock: "))
            price = float(input("Enter price: "))
            add_drug(drug_id, drug_name, stock, price)
        elif choice == '3':
            find_stock()
        elif choice == '4':
            break
        else:
            print("Invalid choice. Please try again.")

# 检验结果管理
def add_exam_result():
    exams = load_data(EXAM_FILE)
    for exam in exams:
        if exam['statement'] == 'current':
            print("patient_id：%s  exam_project: %s"%(exam['patient_id'],exam['exam_project']))
    patient_id = input("Enter patient_id: ")
    result = input("Enter result: ")
    for exam in exams:
        if exam['patient_id'] == patient_id and exam['statement'] == 'current':
            exam['result'] = result
            exam['examiner'] = MY_ID
            print("Add exam result successfully.")
            break
    save_data(EXAM_FILE, exams)

def Examiner():
    while True:
        print("--" * 50)
        print("1. logging data")  # 录入检验数据
        print("2. Exit")
        print("--" * 50)
        choice = input("Enter your choice: ")
        if choice == '1':
            add_exam_result()
        elif choice == '2':
            break
        else:
            print("Invalid choice. Please try again.")



def main():
    while True:
        print("--" * 50)
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        print("--" * 50)
        choice = input("Enter your choice: ")
        if choice == '1':
            username = input("Enter username: ")
            password = input("Enter password: ")
            # role = input("Enter role: ")
            if register_user(username, password, role = 'patient'):
                print("Registration successful.")
            else:
                print("Registration failed.")
        elif choice == '2':
            username = input("Enter username: ")
            password = input("Enter password: ")
            user = login(username, password)
            if user:
                print(f"Logged in as {user['username']} with role {user['role']}")
                global MY_ID
                MY_ID = username
                # 这里可以添加登录后相关的功能实现
                if user['role'] == 'Administrator':
                    admin()
                elif user['role'] == 'RBS':
                    RBS()
                elif user['role'] == 'doctor':
                    Doctor()
                elif user['role'] == 'pharmacy':
                    Pharmacy()
                elif user['role'] == 'examiner':
                    Examiner()
            else:
                print("The account or password is incorrect, login failed.")
        elif choice == '3':
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == '__main__':
    init_files()
    main()
