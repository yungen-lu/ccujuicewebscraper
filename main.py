import sys
import psycopg2
import os
import requests
import datetime
from dotenv import load_dotenv
from fake_useragent import UserAgent
from fake_useragent import FakeUserAgentError
class newConnection:
    def __init__(self,conn_string):
        self.conn_string = conn_string
    # def createConnection(self):
        try:
            conn = psycopg2.connect(self.conn_string)
            self.conn = conn
            self.cursor = conn.cursor()
            # return conn
        except Exception as e:
            print("Connection Failed")
            print(e)
            sys.exit('-1')

    def closeConnection(self):
        self.conn.commit()
        self.cursor.close()
        self.conn.close()
        print("Connection Closed")

    def checkTableExist(self,tableName):
        self.cursor.execute(f"SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_schema = 'public' AND table_name = '{tableName}');")
        re = self.cursor.fetchone()[0]
        if re == True:
            # print(f"{tableName} table exists")
            return True
        elif re == False:
            print(f"{tableName} table does not exists")
            return False
        else: sys.exit()
class newTable(newConnection):
    def __init__(self,tableName,parentName,valueType):
        self.tableName = tableName
        self.conn = parentName.conn
        self.cursor = parentName.cursor
        self.valueType = valueType
        # self.examValueType
    def createTable(self):
        try:
            self.cursor.execute(f"CREATE TABLE \"{self.tableName}\" {self.valueType};")
            print(f"{self.tableName} table created")
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def checkColumnExist(self,columnName):
        self.cursor.execute(f"SELECT EXISTS (SELECT FROM information_schema.column WHERE table_schema = 'public' AND table_name = '{self.tableName}' AND column_name = '{columnName}');")
        re = self.cursor.fetchone()[0]
        if re == True:
            # print(f"{self.tableName} exist")
            return True
        elif re == False:
            print(f"{columnName} column does not exist")
            return False
        else: sys.exit()
    
    def checkRowExist(self,columnID,rowID):
        self.cursor.execute(f"SELECT EXISTS (SELECT FROM \"{self.tableName}\" WHERE {columnID} = '{rowID}');")
        re = self.cursor.fetchone()[0]
        if re == True:
            # print(f"{self.tableName} exist")
            return True
        elif re == False:
            print(f"{rowID} does not exist")
            return False
        else: sys.exit()

    def insertTwoValues(self,values,valueName):
        try:
            self.cursor.execute(f"INSERT INTO \"{self.tableName}\" ({valueName[0]}, {valueName[1]}) VALUES (%s, %s);", (values[0],values[1]))
            print(f"{values} inserted")
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
    
    def insertThreeValues(self,values,valueName):
        try:
            self.cursor.execute(f"INSERT INTO \"{self.tableName}\" ({valueName[0]}, {valueName[1]}, {valueName[2]}) VALUES (%s, %s, %s);", (values[0],values[1],values[2]))
            print(f"{values} inserted")
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
    def insertEightValues(self,values,valueName):
        try:
            self.cursor.execute(f"INSERT INTO \"{self.tableName}\" ({valueName[0]}, {valueName[1]}, {valueName[2]}, {valueName[3]}, {valueName[4]}, {valueName[5]}, {valueName[6]}, {valueName[7]}) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);", (values[0],values[1],values[2],values[3],values[4],values[5],values[6],values[7]))
            print(f"{values} inserted")
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

def errorMessage():
    print("ERROR",file=sys.stderr)
    sys.exit("-1")
class createRequest:
    def __init__(self,BASE_URL,BASE_HEADER):
        self.url = BASE_URL
        self.headers = BASE_HEADER

    def getlogintoken(self,EMAIL,PASSWORD):
        url = self.url+"/api/auth/sign-in"
        payload = {"email":EMAIL,"password":PASSWORD}
        r = requests.post(url,headers=self.headers,json=payload)
        data_parsed =  r.json()
        if r.status_code == requests.codes.ok :
            print(data_parsed)
            TOKEN=data_parsed['data']['token']
            print("token get")
            self.token = TOKEN
            tmpObj = {'api-token': TOKEN}
            self.headers.update(tmpObj)
        else:
            errorMessage()

    def logout(self):
        url = self.url +"/api/auth/sign-out"
        r = requests.post(url,headers=self.headers)
        data_parsed =  r.json()
        if (r.status_code == requests.codes.ok) and (data_parsed['ok'] == True):
            print(data_parsed)
        else:
            errorMessage()
    def getCourses(self):
        url = self.url +"/api/account/courses"
        r = requests.get(url,headers=self.headers)
        data_parsed = r.json()
        if r.status_code == requests.codes.ok:
            arrayOfCourse = data_parsed['data']
            # print(arrayOfCourse)
            return arrayOfCourse
        else:
            errorMessage()
    def getLessons(self,COURSEID):
        url = self.url+ f"/api/courses/{COURSEID}/lessons"
        r = requests.get(url,headers=self.headers)
        data_parsed = r.json()
        if r.status_code == requests.codes.ok:
            arrayOfLesson = data_parsed['data']
            # print(arrayOfLesson)
            return arrayOfLesson
        else:
            errorMessage()
    def getExams(self,LESSONSID):
        url = self.url + f"/api/v2/questions"
        queryString = {"identify":LESSONSID}
        r = requests.get(url,params=queryString,headers=self.headers)
        data_parsed = r.json()
        if r.status_code == requests.codes.ok:
            arrayOfExams = data_parsed
            # print(arrayOfExams)
            return arrayOfExams
        else:
            errorMessage()

def CoursesToDB(connectionObj,requestObj,arrayOfCourse,tableName):
    valueName = ['courseindentify','name']
    valueType = f"({valueName[0]} VARCHAR(10) PRIMARY KEY, {valueName[1]} VARCHAR(50))"

    if connectionObj.checkTableExist(tableName)==True:
        tableOfListCourse = newTable(tableName,connectionObj,valueType)
    else :
        tableOfListCourse = newTable(tableName,connectionObj,valueType)
        tableOfListCourse.createTable()
    for obj in arrayOfCourse:
        courseName = obj["name"]
        courseIdentify = obj["identify"]
        values = [courseIdentify,courseName]
        if tableOfListCourse.checkRowExist(valueName[0],courseIdentify)==False:
            tableOfListCourse.insertTwoValues(values,valueName)
            sendNotify(f"\n新課程〈{courseName}〉發布了！")
        arrayOfLesson=requestObj.getLessons(courseIdentify) #COURSEID
        LessonToDB(connectionObj,requestObj,arrayOfLesson,tableName,courseIdentify)
def LessonToDB(connectionObj,requestObj,arrayOfLesson,parentTableName,courseIdentify):
    tableName = courseIdentify
    valueName = ['lessonindentify','name','parentcourse']
    valueType = f"({valueName[0]} VARCHAR(10) PRIMARY KEY, {valueName[1]} VARCHAR(50), {valueName[2]} VARCHAR(10) REFERENCES \"{parentTableName}\" (courseindentify))"

    if connectionObj.checkTableExist(tableName)==True:
        tableOfListLesson = newTable(tableName,connectionObj,valueType)
    else:
        tableOfListLesson = newTable(tableName,connectionObj,valueType)
        tableOfListLesson.createTable()
    for obj in arrayOfLesson:
        lessonName = obj["name"]
        lessonIdentify = obj["identify"]
        values = [lessonIdentify,lessonName,courseIdentify]
        if tableOfListLesson.checkRowExist(valueName[0],lessonIdentify)==False:
            tableOfListLesson.insertThreeValues(values,valueName)
            sendNotify(f"\n新題庫〈{lessonName}〉發布了！")
        arrayOfExams = requestObj.getExams(lessonIdentify)
        ValuesToDB(connectionObj,arrayOfExams,tableName,lessonIdentify,lessonName)
def ValuesToDB(connectionObj,arrayOfExams,parentTableName,lessonIdentify,lessonName):
    tableName = lessonIdentify
    valueName = ['examindentify','name','difficulty','passers','participants','published_date','published_time','parentlesson']
    valueType = f"({valueName[0]} VARCHAR(10) PRIMARY KEY, {valueName[1]} VARCHAR(50), {valueName[2]} INTEGER, {valueName[3]} INTEGER, {valueName[4]} INTEGER, {valueName[5]} DATE, {valueName[6]} TIME, {valueName[7]} VARCHAR(10) REFERENCES \"{parentTableName}\" (lessonindentify))"

    if connectionObj.checkTableExist(tableName)==True:
        tableOfListExams = newTable(tableName,connectionObj,valueType)
    else:
        tableOfListExams = newTable(tableName,connectionObj,valueType)
        tableOfListExams.createTable()
    for obj in arrayOfExams:
        examIdentify  = obj["identify"]
        examName = obj["name"]
        difficulty = obj["difficulty"]
        if obj["statistic"] != None:
            passers = obj["statistic"]["passers"]
            participants = obj["statistic"]["participants"]
        else:
            passers = 0
            participants = 0
        published_at = obj["published_at"]

        dtobj = datetime.datetime.strptime(published_at,'%Y-%m-%d %H:%M:%S')
        values = [examIdentify,examName,difficulty,passers,participants,dtobj.date(),dtobj.time(),lessonIdentify]

        if tableOfListExams.checkRowExist(valueName[0],examIdentify)==False:
            tableOfListExams.insertEightValues(values,valueName)
            sendNotify(f"\n新題目〈{examName}〉發布了！\n題庫名稱：{lessonName}\n發布於<{published_at}>")
def sendNotify(message):
    LINE_TOKEN = os.environ.get("LINE_TOKEN")
    headers = {
            "Authorization": "Bearer " + str(LINE_TOKEN),
            "Content-Type": "application/x-www-form-urlencoded"
    }
    params = {"message": message}
    r = requests.post("https://notify-api.line.me/api/notify",headers=headers, params=params)
    if r.status_code == requests.codes.ok:
        print("Message sented")
    else:
        errorMessage()
#------------------
load_dotenv()
host = "postgresdb" #docker service name
dbname = os.environ.get("POSTGRES_DB")
user = os.environ.get("POSTGRES_USER")
password = os.environ.get("POSTGRES_PASSWORD")
sslmode = 'allow'
conn_string = "host={0} user={1} dbname={2} password={3} sslmode={4}".format(host, user, dbname, password, sslmode)

connectToDB = newConnection(conn_string)
try:
    ua = UserAgent()
except FakeUserAgentError:
    pass

BASE_URL = 'https://ccu.juice.codes'
BASE_HEADER = {'accept':'application/json','origin':'https://ccu.juice.codes', 'content-type':'application/json','user-agent':ua.random}
EMAIL = os.environ.get("EMAIL")
PASSWORD = os.environ.get("PASSWORD")
connectToJuice = createRequest(BASE_URL,BASE_HEADER)
connectToJuice.getlogintoken(EMAIL,PASSWORD)
arrayOfCourse=connectToJuice.getCourses()
CoursesToDB(connectToDB,connectToJuice,arrayOfCourse,"masterTable")
connectToJuice.logout()
connectToDB.closeConnection()
