from flask import Blueprint, request, jsonify, render_template, url_for, redirect, flash
from flask_login import login_required
from link import *
from api.sql import *

manager = Blueprint('manager', __name__, template_folder='../templates')

@manager.route('/', methods=['GET', 'POST'])
@login_required
def home():
    return redirect(url_for('manager.patent_case'))

#########################################################################
##### patent_case.html
#########################################################################

@manager.route('/patent_case', methods=['GET', 'POST'])
@login_required
def patent_case():

    patent_case_data = patent_case_info()
    return render_template('patent_case.html', data=patent_case_data)

def patent_case_info():
    patent_case_row = PatentCase.get_patent_case()
    patent_case_data = []
    for i in patent_case_row:
        patent_case = {
            '案件編號': i[0],
            '客戶名稱': i[1],
            '委託日': i[2],
            '專利名稱': i[3],
            '專利類型': i[4],
            '專利權人': i[5],
            '案件狀態': i[6],
            '負責工程師': i[7]
        }
        patent_case_data.append(patent_case)
    return patent_case_data

@manager.route('/patent_case_add', methods=['GET', 'POST'])
@login_required
def patent_case_add():

    # 新增
    if request.method == 'POST':
        cId = request.values.get('cId')
        commissionDate = request.values.get('commissionDate')
        pName = request.values.get('pName')
        pType = request.values.get('pType')
        patentee = request.values.get('patentee')
        inventor = request.values.get('inventor')
        eId = request.values.get('eId')
        aId = request.values.get('aId')
        applicationDate = request.values.get('applicationDate')
        certificateId = request.values.get('certificateId')
        startDate = request.values.get('startDate')
        endDate = request.values.get('endDate')

        if cId is None or commissionDate is None or pName is None or pType is None or patentee is None or inventor is None:
            flash('欄位必填，請確認輸入內容。')
            return redirect(url_for('manager.patent_case'))
        
        PatentCase.add_patent_case(
            {
                'cId' : cId,
                'commissionDate' : commissionDate,
                'pName' : pName,
                'pType' : pType,
                'patentee' : patentee,
                'inventor':inventor,
                'eId' : eId or None,
                'aId' : aId,
                'applicationDate' : applicationDate,
                'certificateId' : certificateId,
                'startDate':startDate,
                'endDate' : endDate,
            }
        )

        return redirect(url_for('manager.patent_case'))
    
    return render_template('patent_case.html')

@manager.route('/patent_case_manager', methods=['GET', 'POST'])
@login_required
def patent_case_manager():

    # 刪除
    if 'delete' in request.values:
        pId = request.values.get('delete')
        PatentCase.delete_patent_case(pId)
    
    # 點擊修改
    elif 'edit' in request.values:
        pId = request.values.get('edit')
        return redirect(url_for('manager.patent_case_edit', pId=pId))

    patent_case_data = patent_case_info()
    return render_template('patent_case.html', data=patent_case_data)

#########################################################################
##### patent_case_edit.html
#########################################################################

@manager.route('/patent_case_edit/<int:pId>', methods=['GET', 'POST'])
@login_required
def patent_case_edit(pId):

    patent_case_data = patent_case_edit_info(pId)

    if request.method == 'POST':

        aId = request.values.get('aId')
        certificateId = request.values.get('certificateId')

        if aId and certificateId:
            PatentCase.update_patent_case(
                {
                    'pId' : request.values.get('pId'),
                    'cId' : request.values.get('cId'),
                    'commissionDate' : request.values.get('commissionDate'),
                    'pName' : request.values.get('pName'),
                    'pType' : request.values.get('pType'),
                    'patentee' : request.values.get('patentee'),
                    'inventor' : request.values.get('inventor'),
                    'eId' : request.values.get('eId') or None,
                    'aId' : request.values.get('aId'),
                    'applicationDate' : request.values.get('applicationDate'),
                    'certificateId' : request.values.get('certificateId'),
                    'startDate' : request.values.get('startDate'),
                    'endDate' : request.values.get('endDate')
                }
            )
            return redirect(url_for('manager.patent_case'))
        elif aId and certificateId is None:
            PatentCase.update_no_certificateId(
                {
                    'pId' : request.values.get('pId'),
                    'cId' : request.values.get('cId'),
                    'commissionDate' : request.values.get('commissionDate'),
                    'pName' : request.values.get('pName'),
                    'pType' : request.values.get('pType'),
                    'patentee' : request.values.get('patentee'),
                    'inventor' : request.values.get('inventor'),
                    'eId' : request.values.get('eId') or None,
                    'aId' : request.values.get('aId'),
                    'applicationDate' : request.values.get('applicationDate'),
                    'startDate' : request.values.get('startDate'),
                    'endDate' : request.values.get('endDate')
                }
            )
            return redirect(url_for('manager.patent_case'))
        elif aId is None and certificateId:
            PatentCase.update_no_aId(
                {
                    'pId' : request.values.get('pId'),
                    'cId' : request.values.get('cId'),
                    'commissionDate' : request.values.get('commissionDate'),
                    'pName' : request.values.get('pName'),
                    'pType' : request.values.get('pType'),
                    'patentee' : request.values.get('patentee'),
                    'inventor' : request.values.get('inventor'),
                    'eId' : request.values.get('eId') or None,
                    'applicationDate' : request.values.get('applicationDate'),
                    'certificateId' : request.values.get('certificateId'),
                    'startDate' : request.values.get('startDate'),
                    'endDate' : request.values.get('endDate')
                }
            )
            return redirect(url_for('manager.patent_case'))
        else:
            PatentCase.update_no_both(
                {
                    'pId' : request.values.get('pId'),
                    'cId' : request.values.get('cId'),
                    'commissionDate' : request.values.get('commissionDate'),
                    'pName' : request.values.get('pName'),
                    'pType' : request.values.get('pType'),
                    'patentee' : request.values.get('patentee'),
                    'inventor' : request.values.get('inventor'),
                    'eId' : request.values.get('eId') or None,
                    'applicationDate' : request.values.get('applicationDate'),
                    'startDate' : request.values.get('startDate'),
                    'endDate' : request.values.get('endDate')
                }
            )  
            return redirect(url_for('manager.patent_case'))
    
    else:
        return render_template('patent_case_edit.html', data=patent_case_data)

def patent_case_edit_info(pId=None):
    pId = pId
    data = PatentCase.show_patent_case(pId)
    cId = data[11]
    commissionDate = data[1]
    pName = data[2]
    pType = data[3]
    patentee = data[4]
    inventor = data[5]
    eId = data[12]
    aId = data[6]
    applicationDate = data[7]
    certificateId = data[8]
    startDate = data[9]
    endDate = data[10]

    patent_case = {
        '案件編號': pId,
        '客戶編號': cId,
        '委託日': commissionDate,
        '專利名稱': pName,
        '專利類型': pType,
        '專利權人': patentee,
        '發明人': inventor,
        '工程師編號': eId or None,
        '申請號': aId if aId is not None else '',
        '申請日': applicationDate,
        '證書號': certificateId if certificateId is not None else '',
        '專利權開始': startDate,
        '專利權結束': endDate
    }
    return patent_case

#########################################################################
##### office.html
#########################################################################

@manager.route('/office', methods=['GET', 'POST'])
@login_required
def office():

    if 'select' in request.values:
        officeName = request.values.get('officeName')
        office_data = office_select(officeName)
        
        if office_data:
            return render_template('office.html', data=office_data)
        elif officeName:
            flash('N/A')

    office_data = office_info()
    return render_template('office.html', data=office_data)

def office_select(officeName=None):
    office_row = Office.select_office(officeName)
    office_data = []
    if office_row:
        for i in office_row:
            office = {
                '分部名稱': i[0],
                '聯絡人': i[1],
                '聯絡電話': i[2],
                '電子郵件': i[3],
                '地址': i[4]
            }
            office_data.append(office)
    return office_data

def office_info():
    office_row = Office.get_office()
    office_data = []
    for i in office_row:
        office = {
            '分部名稱': i[0],
            '聯絡人': i[1],
            '聯絡電話': i[2],
            '電子郵件': i[3],
            '地址': i[4]
        }
        office_data.append(office)
    return office_data

@manager.route('/office_add', methods=['GET', 'POST'])
@login_required
def office_add():

    # 新增
    if request.method == 'POST':
        officeName = request.values.get('officeName')
        contactPerson = request.values.get('contactPerson')
        phone = request.values.get('phone')
        email = request.values.get('email')
        address = request.values.get('address')

        if officeName is None:
            flash('分部名稱必填，請確認輸入內容。')
            return redirect(url_for('manager.office'))
        
        Office.add_office(
            {
                'officeName' : officeName,
                'contactPerson' : contactPerson,
                'phone' : phone,
                'email' : email,
                'address':address
            }
        )

        return redirect(url_for('manager.office'))
    
    return render_template('office.html')

@manager.route('/office_manager', methods=['GET', 'POST'])
@login_required
def office_manager():

    # 刪除
    if 'delete' in request.values:
        officeName = request.values.get('delete')
        data = Office.delete_check()
        
        if officeName in data:
            Office.delete_office(officeName)
        else:
            flash('failed')
    
    # 點擊修改
    elif 'edit' in request.values:
        officeName = request.values.get('edit')
        return redirect(url_for('manager.office_edit', officeName=officeName))

    office_data = office_info()
    return render_template('office.html', data=office_data)

#########################################################################
##### office_edit.html
#########################################################################

@manager.route('/office_edit/<officeName>', methods=['GET', 'POST'])
@login_required
def office_edit(officeName):

    office_data = office_edit_info(officeName)

    if request.method == 'POST':
        Office.update_office(
            {
                'officeName' : request.values.get('officeName'),
                'contactPerson' : request.values.get('contactPerson'),
                'phone' : request.values.get('phone'),
                'email' : request.values.get('email'),
                'address' : request.values.get('address')
            }
        )
        
        return redirect(url_for('manager.office'))
    
    else:
        return render_template('office_edit.html', data=office_data)

def office_edit_info(officeName=None):
    officeName = officeName
    data = Office.select_office(officeName)
    contactPerson = data[0][1]
    phone = data[0][2]
    email = data[0][3]
    address = data[0][4]

    office = {
        '分部名稱': officeName,
        '聯絡人': contactPerson,
        '聯絡電話': phone,
        '電子郵件': email,
        '地址': address
    }
    return office

#########################################################################
##### personnal.html 
#########################################################################

@manager.route('/personnel')
@login_required
def personnel():
    return render_template('personnel.html')

@manager.route('/get_data', methods=['POST'])
@login_required
def get_data():
    data_type = request.json.get('type')

    if data_type == 'engineer':
        try:
            results = engineer_info()
            if results:
                return jsonify({'status': 'success', 'data': results})
            else:
                return jsonify({'status': 'error', 'message': 'No engineers found'})
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)})
    
    elif data_type == 'customerservice':
        try:
            results = customerservice_info()
            if results:
                return jsonify({'status': 'success', 'data': results})
            else:
                return jsonify({'status': 'error', 'message': 'No customerservices found'})
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)})
    
    else:
        try:
            results = client_info()
            if results:
                return jsonify({'status': 'success', 'data': results})
            else:
                return jsonify({'status': 'error', 'message': 'No clients found'})
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)})
        
def engineer_info():
    engineer_row = Personnel.get_engineer()
    engineer_data = []
    if engineer_row:
        for i in engineer_row:
            engineer = {
                '工程師編號': i[0],
                '姓名': i[1],
                '聯絡電話': i[2],
                '專業領域': i[3],
                '公司分部': i[4]
            }
            engineer_data.append(engineer)
    return engineer_data

def customerservice_info():
    customerservice_row = Personnel.get_customerservice()
    customerservice_data = []
    if customerservice_row:
        for i in customerservice_row:
            customerservice = {
                '客服編號': i[0],
                '姓名': i[1],
                '聯絡電話': i[2],
                '電子郵件': i[3],
                '公司分部': i[4]
            }
            customerservice_data.append(customerservice)
    return customerservice_data

def client_info():
    client_row = Personnel.get_client()
    client_data = []
    if client_row:
        for i in client_row:
            client = {
                '客戶編號': i[0],
                '客戶名稱': i[1],
                '聯絡電話': i[2],
                '電子郵件': i[3],
                '地址': i[4],
                '責任客服': i[5]
            }
            client_data.append(client)
    return client_data

#########################################################################
##### statistic.html 
#########################################################################

@manager.route('/statistic')
@login_required
def statistic():
    return render_template('statistic.html')

@manager.route('/get_statistic', methods=['POST'])
@login_required
def get_statistic():
    data_type = request.json.get('type')

    if data_type == 'yearlyData':
        try:
            results = yearly_info()
            if results:
                return jsonify({'status': 'success', 'data': results})
            else:
                return jsonify({'status': 'error', 'message': 'No data found'})
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)})
    
    elif data_type == 'typeData':
        try:
            results = type_info()
            if results:
                return jsonify({'status': 'success', 'data': results})
            else:
                return jsonify({'status': 'error', 'message': 'No data found'})
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)})
    

def yearly_info():
    yearly_row = Statistic.get_yearly_count()
    yearly_data = []
    if yearly_row:
        for i in yearly_row:
            yearly = {
                '委託年度': i[0],
                '數量': i[1]
            }
            yearly_data.append(yearly)
    return yearly_data

def type_info():
    type_row = Statistic.get_type_count()
    type_data = []
    if type_row:
        for i in type_row:
            type = {
                '專利案類型': i[0],
                '數量': i[1]
            }
            type_data.append(type)
    return type_data