import psycopg2
from psycopg2 import pool

class DB:
    connection_pool = pool.SimpleConnectionPool(
        1, 100,  # 最小和最大連線數
            user='project_3',
            password='hck8fv',
            host='140.117.68.66',
            port='5432',
            dbname='project_3'
    )

    @staticmethod
    def connect():
        return DB.connection_pool.getconn()

    @staticmethod
    def release(connection):
        DB.connection_pool.putconn(connection)

    @staticmethod
    def execute_input(sql, input):
        if not isinstance(input, (tuple, list)):
            raise TypeError(f"Input should be a tuple or list, got: {type(input).__name__}")
        connection = DB.connect()
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql, input)
                connection.commit()
        except psycopg2.Error as e:
            print(f"Error executing SQL: {e}")
            connection.rollback()
            raise e
        finally:
            DB.release(connection)

    @staticmethod
    def execute(sql):
        connection = DB.connect()
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql)
        except psycopg2.Error as e:
            print(f"Error executing SQL: {e}")
            connection.rollback()
            raise e
        finally:
            DB.release(connection)

    @staticmethod
    def fetchall(sql, input=None):
        connection = DB.connect()
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql, input)
                return cursor.fetchall()
        except psycopg2.Error as e:
            print(f"Error fetching data: {e}")
            raise e
        finally:
            DB.release(connection)

    @staticmethod
    def fetchone(sql, input=None):
        connection = DB.connect()
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql, input)
                return cursor.fetchone()
        except psycopg2.Error as e:
            print(f"Error fetching data: {e}")
            raise e
        finally:
            DB.release(connection)

#########################################################################
##### 登入 
#########################################################################

class Administrator:
    @staticmethod
    def get_admin(account):
        sql = '''
                SELECT * 
                FROM PatentOffice.Administrator 
                WHERE account = %s
            '''
        return DB.fetchone(sql, (account,))
    
#########################################################################
##### 申請案管理 
#########################################################################

class PatentCase:
    @staticmethod
    def get_patent_case():
        sql = '''
                SELECT p.pId AS 案件編號, 
                       c.cName AS 客戶名稱, 
                       p.commissionDate AS 委託日,
                       p.pName AS 專利名稱, 
                       p.pType AS 專利類型, 
                       p.patentee AS 專利權人, 
                       CASE 
                           WHEN p.certificateId LIKE 'C%' THEN '已結案'
                           WHEN p.aId LIKE 'A%' THEN '申請中'
                           ELSE '立案'
                       END AS 案件狀態, 
                       COALESCE(e.eName, 'X') AS 負責工程師
                FROM PatentOffice.PatentCase AS p
                INNER JOIN PatentOffice.Client AS c ON p.cId = c.cId
                LEFT JOIN PatentOffice.PatentEngineer AS e ON p.eId = e.eId
                ORDER BY p.pId DESC
            '''
        return DB.fetchall(sql)
    
    @staticmethod
    def add_patent_case(input_data):
        sql = '''
                INSERT INTO PatentOffice.PatentCase (commissionDate, pName, pType, patentee, inventor, aId, applicationDate, certificateId, startDate, endDate, cId, eId)
                VALUES (TO_DATE(%s, 'YYYY-MM-DD'), %s, %s, %s, %s, NULLIF(%s, ''),
                        TO_DATE(NULLIF(%s, ''), 'YYYY-MM-DD'), NULLIF(%s, ''), 
                        TO_DATE(NULLIF(%s, ''), 'YYYY-MM-DD'), TO_DATE(NULLIF(%s, ''), 'YYYY-MM-DD'), %s, %s)
            '''
        DB.execute_input(sql, (input_data['commissionDate'], input_data['pName'], input_data['pType'], input_data['patentee'], input_data['inventor'], input_data['aId'], input_data['applicationDate'], input_data['certificateId'], input_data['startDate'], input_data['endDate'], input_data['cId'], input_data['eId']))

    @staticmethod
    def delete_patent_case(pid):
        sql = '''
                DELETE FROM PatentOffice.PatentCase 
                WHERE pid = %s
            '''
        DB.execute_input(sql, (pid,))

    @staticmethod
    def show_patent_case(pid):
        sql = '''
                SELECT *
                FROM PatentOffice.PatentCase
                WHERE pId = %s
            '''
        return DB.fetchone(sql, (pid,))

    @staticmethod
    def update_patent_case(input_data):
        sql = '''
                UPDATE PatentOffice.PatentCase
                SET cId = %s,
                    commissionDate = TO_DATE(%s, 'YYYY-MM-DD'),
                    pName = %s,
                    pType = %s,
                    patentee = %s,
                    inventor = %s,
                    eId = %s,
                    aId = NULLIF(%s, NULL),
                    applicationDate = TO_DATE(NULLIF(%s, ''), 'YYYY-MM-DD'),
                    certificateId = NULLIF(%s, NULL),
                    startDate = TO_DATE(NULLIF(%s, ''), 'YYYY-MM-DD'),
                    endDate = TO_DATE(NULLIF(%s, ''), 'YYYY-MM-DD')
                WHERE pId = %s
            '''
        DB.execute_input(sql, (input_data['cId'], input_data['commissionDate'], input_data['pName'], input_data['pType'], input_data['patentee'], input_data['inventor'], input_data['eId'], input_data['aId'], input_data['applicationDate'], input_data['certificateId'], input_data['startDate'], input_data['endDate'], input_data['pId']))

    @staticmethod
    def update_no_certificateId(input_data):
        sql = '''
                UPDATE PatentOffice.PatentCase
                SET cId = %s,
                    commissionDate = TO_DATE(%s, 'YYYY-MM-DD'),
                    pName = %s,
                    pType = %s,
                    patentee = %s,
                    inventor = %s,
                    eId = %s,
                    aId = NULLIF(%s, NULL),
                    applicationDate = TO_DATE(NULLIF(%s, ''), 'YYYY-MM-DD'),
                    startDate = TO_DATE(NULLIF(%s, ''), 'YYYY-MM-DD'),
                    endDate = TO_DATE(NULLIF(%s, ''), 'YYYY-MM-DD')
                WHERE pId = %s
            '''
        DB.execute_input(sql, (input_data['cId'], input_data['commissionDate'], input_data['pName'], input_data['pType'], input_data['patentee'], input_data['inventor'], input_data['eId'], input_data['aId'], input_data['applicationDate'], input_data['startDate'], input_data['endDate'], input_data['pId']))

    @staticmethod
    def update_no_aId(input_data):
        sql = '''
                UPDATE PatentOffice.PatentCase
                SET cId = %s,
                    commissionDate = TO_DATE(%s, 'YYYY-MM-DD'),
                    pName = %s,
                    pType = %s,
                    patentee = %s,
                    inventor = %s,
                    eId = %s,
                    applicationDate = TO_DATE(NULLIF(%s, ''), 'YYYY-MM-DD'),
                    certificateId = NULLIF(%s, NULL),
                    startDate = TO_DATE(NULLIF(%s, ''), 'YYYY-MM-DD'),
                    endDate = TO_DATE(NULLIF(%s, ''), 'YYYY-MM-DD')
                WHERE pId = %s
            '''
        DB.execute_input(sql, (input_data['cId'], input_data['commissionDate'], input_data['pName'], input_data['pType'], input_data['patentee'], input_data['inventor'], input_data['eId'], input_data['applicationDate'], input_data['certificateId'], input_data['startDate'], input_data['endDate'], input_data['pId']))
    
    @staticmethod
    def update_no_both(input_data):
        sql = '''
                UPDATE PatentOffice.PatentCase
                SET cId = %s,
                    commissionDate = TO_DATE(%s, 'YYYY-MM-DD'),
                    pName = %s,
                    pType = %s,
                    patentee = %s,
                    inventor = %s,
                    eId = %s,
                    applicationDate = TO_DATE(NULLIF(%s, ''), 'YYYY-MM-DD'),
                    startDate = TO_DATE(NULLIF(%s, ''), 'YYYY-MM-DD'),
                    endDate = TO_DATE(NULLIF(%s, ''), 'YYYY-MM-DD')
                WHERE pId = %s
            '''
        DB.execute_input(sql, (input_data['cId'], input_data['commissionDate'], input_data['pName'], input_data['pType'], input_data['patentee'], input_data['inventor'], input_data['eId'], input_data['applicationDate'], input_data['startDate'], input_data['endDate'], input_data['pId']))
    
#########################################################################
##### 分部管理 
#########################################################################

class Office:
    @staticmethod
    def get_office():
        sql = '''
                SELECT * 
                FROM PatentOffice.Office
            '''
        return DB.fetchall(sql)
    
    @staticmethod
    def select_office(officeName):
        if officeName:
            sql = '''
                    SELECT * 
                    FROM PatentOffice.Office 
                    WHERE officeName LIKE %s
                '''
            return DB.fetchall(sql, ('%' + officeName + '%',))
        
    @staticmethod   
    def add_office(input_data):
        sql = '''
                INSERT INTO PatentOffice.Office (officeName, contactPerson, phone, email, address)
                VALUES (%s, %s, %s, %s, %s)
            '''
        DB.execute_input(sql, (input_data['officeName'], input_data['contactPerson'], input_data['phone'], input_data['email'], input_data['address']))

    @staticmethod   
    def delete_check():
        sql = '''
                SELECT officeName
                FROM PatentOffice.Office
                WHERE officeName NOT IN (
                    SELECT officeName
                    FROM PatentOffice.PatentEngineer
                )
                AND officeName NOT IN (
                    SELECT officeName
                    FROM PatentOffice.CustomerService
                )
            '''
        result = DB.fetchall(sql)
        return [row[0] for row in result] if result else []

    @staticmethod   
    def delete_office(officename):
        sql = '''
                DELETE FROM PatentOffice.Office 
                WHERE officeName = %s
            '''
        return DB.execute_input(sql, (officename,))
    
    @staticmethod   
    def update_office(input_data):
        sql = '''
                UPDATE PatentOffice.Office
                SET contactPerson = %s,
                    phone = %s,
                    email = %s,
                    address = %s
                WHERE officeName = %s
            '''
        DB.execute_input(sql, (input_data['contactPerson'], input_data['phone'], input_data['email'], input_data['address'], input_data['officeName']))
    
#########################################################################
##### 人員管理 
#########################################################################

class Personnel:
    @staticmethod
    def get_engineer():
        sql = '''
                SELECT e.eId, 
                       e.eName, 
                       e.phone,
                       STRING_AGG(x.expertise, ', '), 
                       e.officeName
                FROM PatentOffice.PatentEngineer AS e
                LEFT JOIN PatentOffice.Expertise AS x ON e.eId = x.eId
                GROUP BY e.eId
                ORDER BY e.eId ASC
            '''
        return DB.fetchall(sql)

    @staticmethod
    def get_customerservice():
        sql = '''
                SELECT * 
                FROM PatentOffice.CustomerService
            '''
        return DB.fetchall(sql)

    @staticmethod
    def get_client():
        sql = '''
                SELECT c.cId,
                       c.cName,
                       c.phone,
                       c.email,
                       c.address,
                       cs.csName 
                FROM PatentOffice.Client AS c
                INNER JOIN PatentOffice.CustomerService AS cs ON c.csId = cs.csId
            '''
        return DB.fetchall(sql)

#########################################################################
##### 統計數據 
#########################################################################

class Statistic:
    @staticmethod
    def get_yearly_count():
        sql = '''
                SELECT EXTRACT(YEAR FROM commissionDate) AS year, 
                       COUNT(*) AS total_count
                FROM PatentOffice.PatentCase
                GROUP BY year
                ORDER BY year
            '''
        return DB.fetchall(sql)
    
    @staticmethod
    def get_type_count():
        sql = '''
                SELECT ptype, 
                       COUNT(*) AS total_count
                FROM PatentOffice.PatentCase
                GROUP BY ptype
                ORDER BY total_count DESC
            '''
        return DB.fetchall(sql)