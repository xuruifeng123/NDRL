'''
Descripttion: 
Author: Ruifeng Xu
version: 1.0
Date: 2024-11-22 23:38:53
LastEditors: Ruifeng Xu
LastEditTime: 2024-12-08 09:57:39
'''

import logging
import pandas as pd
import os
from datetime import  datetime
import re
from loguru import logger


from data_process.utilities import *
from path import Absolute_path

#整理数据
def Preparedata(file_path,IR_FER_ALL = False):
    
    file_path=os.path.join(Absolute_path,"data/"+file_path)
    print(logger)
    logger.info("file_path: " +str(file_path))
    
    treatment = pd.read_excel(file_path,engine='openpyxl',sheet_name='Treatment',skiprows=3)
    addition = pd.read_excel(file_path,engine='openpyxl',sheet_name='Addition',skiprows=3)
    initial =  pd.read_excel(file_path,engine='openpyxl',sheet_name='Initial Conditions',skiprows=2)
    irrigation = pd.read_excel(file_path,engine='openpyxl',sheet_name='Irrigation',skiprows=3)
    
    fer = pd.read_excel(file_path,engine='openpyxl',sheet_name='Fertilizers',skiprows=3)
    simulation = pd.read_excel(file_path,engine='openpyxl',sheet_name='Simulation',skiprows=3)
    soilanalysis = pd.read_excel(file_path,engine='openpyxl',sheet_name='Soilanalysis',skiprows=3)
    envir = pd.read_excel(file_path,engine='openpyxl',sheet_name='Environment',skiprows=3)
    tillage = pd.read_excel(file_path,engine='openpyxl',sheet_name='Tillage',skiprows=3)
    harvest = pd.read_excel(file_path,engine='openpyxl',sheet_name='Harvest',skiprows=3)

    #推迟时间
    inputdict = {}
    measuredate = []

    # =======================================
    # treatment.iloc 相当于表格化我的excel表，完了
    # [:, 20]第21列每一行的值 这里从0开始
    # =======================================
    # 这里相当于提前十天

    # measuredate = [advanceday(str(d), 10) for d in treatment.iloc[:, 20].tolist()]
    measuredate = [advanceday(str(d), 10) for d in treatment.loc[:,'PDATE'].tolist()]
    # 制作成表格
    dftmp = pd.DataFrame(measuredate)
    # 设置列名是Measuredate
    dftmp.columns = ['Measuredate']
    #表链接 将提前数据放到表内
    treatment = pd.concat([treatment,dftmp],axis=1)
    # print(treatment)
    #General information
    treatment = treatment[~treatment.duplicated(subset=['INGENO'])]
    treatNO=len(treatment)
    
    # 实验细节相当于试验场地
    exp_details  = simulation.loc[:,'DETAILS'].tolist()[0]
    inputdict['exp_details'] = exp_details
    # 实验人员
    PEOPLE = simulation.loc[:,'PEOPLE'].tolist()[0]
    inputdict['PEOPLE'] = PEOPLE
    # 实验地点
    ADDRESS = simulation.loc[:,'DDRESS'].tolist()[0]
    inputdict['ADDRESS'] = ADDRESS

    # 站点信息
    SITE = simulation.loc[:,'SITE'].tolist()[0]
    inputdict['SITE'] = SITE

    # XJH2311 应该是天气信息
    NOTES = simulation.loc[:,'FileName'].tolist()[0]
    inputdict['NOTES'] = NOTES

    # XJH2311 应该是天气信息 字典改为了FILENAME
    FILENAME= simulation.loc[:,'FileName'].tolist()[0]
    inputdict['FILENAME'] = FILENAME

    # 通常信息一起存储
    inputdata_general = {'general':inputdict}
    inputdata = [inputdata_general]

    #Treament处理

    df_treaments = treatment.iloc[:,[0,1,2,3,4,5,6,7,8,11,10,12,9]]
    
    df_treaments.insert(9,'MC',[0]*treatNO)
    df_treaments.insert(9,'MR',[0]*treatNO)
    df_treaments.insert(1,'C',[0]*treatNO)
    df_treaments.insert(1,'O',[1]*treatNO)
    df_treaments.insert(1,'R',[1]*treatNO)
    # 相当于创造控制文件
    # *TREATMENTS                        -------------FACTOR LEVELS------------
    # @N R O C TNAME.................... CU FL SA IC MP MI MF MR MC MT ME MH SM
    #  1 0 0 0 Control - 350 ppm          1  1  0  1  1  1  1  0  1  0  1  0  1
    #  2 0 0 0 CO2 Enrichment - 550 ppm   1  1  0  1  1  1  1  0  1  0  2  0  1
    inputdata_treaments = {'treatments':df_treaments}
    inputdata.append(inputdata_treaments)

    #CULTIVARS
    # CU 是品种文件
    #
    CUtmp = treatment.loc[:,'CU']
    CUtmp = pd.DataFrame(CUtmp)

    # 选出没有重复的处理
    CUltivars_sub = treatment[~CUtmp.duplicated(subset=['CU'])]

    Data_CU = {
        'C':CUltivars_sub.loc[:,'CU'],
        'CR':CUltivars_sub.loc[:,'CR'],
        'INGENO':CUltivars_sub.loc[:,'INGENO'],
        'CNAME':CUltivars_sub.loc[:,'CNAME'],
    }
    df_cultivars = pd.DataFrame(Data_CU)

    inputdata_cultivars = {'cultivars':df_cultivars}

    inputdata.append(inputdata_cultivars)

    #Field
    # 将土壤信息补充到处理里面
    addition=pd.DataFrame(addition)
    addition=addition[~addition.duplicated(subset=["EDATE"])]
    treatment_sub = pd.concat([treatment,addition],axis=1)

    FLtmp = treatment_sub.loc[:,'FL']
    FLtmp = pd.DataFrame(FLtmp)
    field_sub = treatment_sub[~FLtmp.duplicated(subset=['FL'])]

    # 专门的土壤处理
    # 获得土壤id 这里我觉得应该是没有的时候去做出来的
    id_field = inputdata[0]['general']['FILENAME'][0:4] + "{:04.0f}".format(int(field_sub["FL"].iloc[0]))

    n_field=field_sub.shape[0]
    Data_FL = {
        'L':field_sub['FL'],
        'ID_FIELD':id_field,
        'WSTA':field_sub['WSTA'],
        'FLSA':[-99]*n_field,
        'FLOB':[-99]*n_field,
        'FLDT':field_sub.iloc[:,17],
        'FLDD':field_sub['FLDD'],
        'FLDS':field_sub['FLDS'],
        'FLST':field_sub['FLST'],
        'SLTX':field_sub['SLTX'],
        'SLDP':field_sub['SLDP'],
        'ID_SOIL':field_sub['ID_SOIL'],
        'FLNAME':[-99]*n_field,
        'XCRD':[0]*n_field,
        'YCRD':[0]*n_field,
        'ELEV':[0]*n_field,
        'AREA':[0]*n_field,
        'SLEN':[0]*n_field,
        'FLWR':[0]*n_field,
        'SLAS':[0]*n_field,
        'FLHST':[-99]*n_field,
        'FHDUR':[-99]*n_field
    }

    df_fields = pd.DataFrame(Data_FL)
    inputdata_fields = {'fields':df_fields}
    inputdata.append(inputdata_fields)

    #SOil analysis缺失


    # INITIAL CONDITIONS
    # 多种角度的条件初始化
    # 有残余
    INItmp = treatment.loc[:,'IC']
    INItmp = pd.DataFrame(INItmp)
    INI_sub = treatment_sub[~INItmp.duplicated(subset=['IC'])]

    Data_INI = {
        'C':INI_sub['IC'],
        'PCR':INI_sub['PCR'],
        'ICDAT':INI_sub['Measuredate'],
        'ICRT':INI_sub['ICRT'],
        'ICND':[-99]*len(INI_sub),
        'ICRN':[-99]*len(INI_sub),
        'ICRE':[-99]*len(INI_sub),
        'ICWD':[-99]*len(INI_sub),
        'ICRES':INI_sub['ICRES'],
        'ICREN':INI_sub['ICREN'],
        'ICREP':[-99]*len(INI_sub),
        'ICRIP':[-99]*len(INI_sub),
        'ICRID':[-99]*len(INI_sub),
        'ICNAME':[-99]*len(INI_sub),
    }
    df_ini_cond_properties = pd.DataFrame(Data_INI)
    inputdata_ini_cond_properties = {'ini_cond_properties':df_ini_cond_properties}
    inputdata.append(inputdata_ini_cond_properties)

    Data_INI_profile = {
        'C':initial['N'],
        'ICBL':initial['ICBL'],
        'SH2O':initial['SH2O'],
        'SNH4':initial['SNH4'],
        'SNO3':initial['SNO3']

    }
    df_ini_cond_profile = pd.DataFrame(Data_INI_profile)
    df_ini_cond_profile = rad(df_ini_cond_profile)
    inputdata_ini_cond_profile = {'ini_cond_profile':df_ini_cond_profile}
    inputdata.append(inputdata_ini_cond_profile)
    ICDAT = str(inputdata[-2]['ini_cond_properties']['ICDAT'].tolist()[0])
    ICDAT = ICDAT[-5:]
    inputdata[-2]['ini_cond_properties']['ICDAT'] = ICDAT

    # PLANTING DETAILS

    Platmp = treatment.loc[:,'MP']
    Platmp = pd.DataFrame(Platmp)
    planting_sub = treatment_sub[~Platmp.duplicated(subset=['MP'])]

    Data_Pla = {
        'P':planting_sub['MP'],
        'PDATE':planting_sub['PDATE'],
        'EDATE':planting_sub['EDATE'],
        'PPOP':planting_sub['PPOP'],
        'PPOE':planting_sub['PPOE'],
        'PLME':planting_sub['PLME'],
        'PLDS':planting_sub['PLDS'],
        'PLRS':planting_sub['PLRS'],
        'PLRD':planting_sub['PLRD'],
        'PLDP':planting_sub['PLDP'],
        'PLWT':planting_sub['PLWT'],
        'PAGE':[-99]*len(planting_sub),
        'PENV':[-99]*len(planting_sub),
        'PLPH':[-99]*len(planting_sub),
        'SPRL':[-99]*len(planting_sub),
        'PLNAME':[-99]*len(planting_sub),
    }

    #当有移植类生物时候需要一下信息 比如水稻,会有PAGE，PENV，PLPH，SPRL四个属性

    if(planting_sub['CR'].tolist()[0] == 'RI'):
           Data_Pla['PAGE'] = planting_sub['PAGE']
           Data_Pla['PENV'] = planting_sub['PENV']
           Data_Pla['PLPH'] = planting_sub['PLPH']
           Data_Pla['SPRL'] = planting_sub['SPRL']
    df_planting = pd.DataFrame(Data_Pla)

    inputdata_planting = {'planting':df_planting}
    inputdata.append(inputdata_planting)

    #data tranformer
    len_times = inputdata[-1]['planting']['PDATE'].shape[0]
    PDATE_list = []
    EDATE_list = []
    for i in range(len_times):
        PDATE = str(inputdata[-1]['planting']['PDATE'].tolist()[i])
        EDATE = str(inputdata[-1]['planting']['EDATE'].tolist()[i])
        PDATE = PDATE[-5:]
        EDATE = EDATE[-5:]
        PDATE_list.append(PDATE)
        EDATE_list.append(EDATE)
    df_PDATE = pd.DataFrame(PDATE_list)
    df_EDATE = pd.DataFrame(EDATE_list)
    inputdata[-1]['planting']['PDATE'] = df_PDATE
    inputdata[-1]['planting']['EDATE'] = df_EDATE
    #去重后的df——planting
    df_planting = rad(inputdata[-1]['planting'])

    #替换掉input中的
    inputdata[-1]['planting'] = df_planting

    #Irrigation
    if IR_FER_ALL==False:
        IRNO = treatment['MI'].unique()
        irrigation = irrigation.loc[irrigation['N'].isin(IRNO)]
    Data_Iri = {

        'I':irrigation['N'],
        'IDATE':irrigation['IDATE'],
        'IROP':irrigation['IROP'],
        'IRVAL':irrigation['IRVAL'],
        'IRRIG':irrigation['IRRIG']

    }
    df_irrigation = pd.DataFrame(Data_Iri)
    df_irrigation=df_irrigation[~df_irrigation.duplicated(subset=['IDATE'])]
    inputdata_irrigation = {'irrigation':df_irrigation}
    inputdata.append(inputdata_irrigation)

    #plantdate
    Plantdate = {
        'I':treatment['MI'],
        'PDATE':treatment['PDATE'],
    }

    plantdate = pd.DataFrame(Plantdate)
    plantdate =rad(plantdate)

    inputdata[-1]['irrigation'] = rad_irrigation(inputdata[-1]['irrigation'])

    inputdata[-1]['irrigation']  = pd.merge(inputdata[-1]['irrigation'] , plantdate, on="I", how="inner")

    # inputdata[-1]['irrigation'] = pd.concat([inputdata[-1]['irrigation'],plantdate],axis=1)

    #data change
    IDATE_list = []
    IDATE = (inputdata[-1]['irrigation']['IDATE'].tolist())
    PDATE = (inputdata[-1]['irrigation']['PDATE'].tolist())
    FERTI = inputdata[-1]['irrigation']['IRRIG'].tolist()

    for i in range(len(IDATE)):
        IDATE_tmp = transformday(str(IDATE[i]),str(FERTI[i]),str(PDATE[i]))
        IDATE_tmp = IDATE_tmp[-5:]
        IDATE_list.append(IDATE_tmp)

    df_IDATE = pd.DataFrame(IDATE_list)
    inputdata[-1]['irrigation']['IDATE'] = df_IDATE

    #Fertilizion
    if IR_FER_ALL == False:
        # print(treatment['MF'])
        FERNO = treatment['MF'].unique()
        fer = fer.loc[fer['N'].isin(FERNO)]

    Data_fer = {
        'I':fer['N'],
        'FDATE':fer['FDATE'],
        'FMCD':fer['FMCD'],
        'FACD':fer['FACD'],
        'FDEP':fer['FDEP'],
        'FAMN':fer['FAMN'],
        'FAMP':fer['FAMP'],
        'FAMK':fer['FAMK'],
        'FAMC': [-99] * len(fer),
        'FAMO':[-99]*len(fer),
        'FOCD':[-99]*len(fer),
        'FERNAME':[-99]*len(fer),
        'FERTI':fer['FERTI']
    }

    df_fer = pd.DataFrame(Data_fer)
    input_fer = {'fertilization':df_fer}
    inputdata.append(input_fer)
    plantdate_fer = {
        'I':treatment['MF'],
        'PDATE':treatment['PDATE']
    }
    plantdate_fer = pd.DataFrame(plantdate_fer)
    plantdate_fer = rad(plantdate_fer)
    inputdata[-1]['fertilization'] = rad_fertilization(inputdata[-1]['fertilization'])
    inputdata[-1]['fertilization'] = pd.merge(inputdata[-1]['fertilization'], plantdate_fer, on="I", how="inner")

    FDATE_list = []
    FDATE = inputdata[-1]['fertilization']['FDATE'].tolist()
    PDATE = inputdata[-1]['fertilization']['PDATE'].tolist()
    FERTI = inputdata[-1]['fertilization']['FERTI'].tolist()

    for i in range(len(FDATE)):
        FDATE_tmp = transformday(str(FDATE[i]),str(FERTI[i]),str(PDATE[i]))
        FDATE_tmp = FDATE_tmp[-5:]
        FDATE_list.append(FDATE_tmp)
    df_FDATE = pd.DataFrame(FDATE_list)
    inputdata[-1]['fertilization']['FDATE'] = df_FDATE

   #Tillage
    TiNo = treatment['MT'].unique()
    if len(TiNo)>1 or TiNo !=0:
        tillage = tillage.loc[tillage['N'].isin(TiNo)]
        Data_Till = {
            'T':tillage['N'],
            'TDATE':tillage['TDATE'],
            'TIMPL':tillage['TIMPL'],
            'TDEP':tillage['TDEP'],
            'TNAME':tillage['TNAME']
        }
        df_tillage = pd.DataFrame(Data_Till)
        input_tillage = {tillage:df_tillage}
        inputdata.append(input_tillage)
        TDATE = inputdata[-1]['tillage']['TDATE']
        TDATE_list = []
        for i in range(len(TDATE)):
            TDATE = str(inputdata[-1]['tillage']['TDATE'].tolist()[i])
            TDATE = TDATE[-5:]
            TDATE_list.append(TDATE)
        df_TDATE = pd.DataFrame(TDATE_list)
        inputdata[-1]['tillage']['TDATE'] = df_TDATE

    #Environment Modifications

    EnvirNo = treatment['ME'].unique()
    if(len(EnvirNo) > 1 or EnvirNo != 0):
        envir = envir.loc[envir['N'].isin(EnvirNo)]
        EDAY = ["{:4s}".format(sub_envir[1]) + sub_envir[0] for sub_envir in envir['EDAY']]
        ERAD = ["{:4s}".format(sub_envir[1]) + sub_envir[0] for sub_envir in envir['ERAD']]
        EMAX = ["{:4s}".format(sub_envir[1]) + sub_envir[0] for sub_envir in envir['EMAX']]
        EMIN = ["{:4s}".format(sub_envir[1]) + sub_envir[0] for sub_envir in envir['EMIN']]
        ERAIN = ["{:4s}".format(sub_envir[1]) + sub_envir[0] for sub_envir in envir['ERAIN']]
        ECO2 =  ["{:2s}".format(sub_envir[-1:]) + sub_envir[:-1] for sub_envir in envir['ECO2']]
        EDEW = ["{:4s}".format(sub_envir[1]) + sub_envir[0] for sub_envir in envir['EDEW']]
        EWIND= ["{:4s}".format(sub_envir[1]) + sub_envir[0] for sub_envir in envir['EWIND']]
        Data_envir = {
            'E':envir['N'],
            'ODATE':envir['ODATE'],
            'EDAY':EDAY,
            'ERAD':ERAD,
            'EMAX':EMAX,
            'EMIN':EMIN,
            'ERAIN':ERAIN,
            'ECO2':ECO2,
            'EDEW':EDEW,
            'EWIND':EWIND,
            'ENVAME':envir['ENVNAME']
        }
        df_environment = pd.DataFrame(Data_envir)
        input_environment = {'environment':df_environment}
        inputdata.append(input_environment)
        ODATE = inputdata[-1]['environment']['ODATE']
        ODATE_list = []
        for i in range(len(ODATE)):
            ODATE_tmp = str(df_environment['ODATE'].tolist()[i])
            ODATE_tmp = ODATE_tmp[-5:]
            ODATE_list.append(ODATE_tmp)
        df_ODATE = pd.DataFrame(ODATE_list)
        inputdata[-1]['environment']['ODATE'] = df_ODATE



    #Harvest
    HarvNO = treatment['MH'].unique()
    if len(HarvNO)>1 or HarvNO != 0:
        tillage = harvest.loc[harvest['N'].isin(HarvNO)]
        Data_Harv = {
            'T': harvest['N'],
            'TDATE': harvest['TDATE'],
            'TIMPL': harvest['TIMPL'],
            'TDEP': harvest['TDEP'],
            'TNAME': harvest['TNAME']
        }
        df_harvest = pd.DataFrame(Data_Harv)
        input_harvest = {harvest: df_harvest}
        inputdata.append(input_harvest)
        HDATE = inputdata[-1]['harvest']['HDATE']
        HDATE_list = []
        for i in range(len(HDATE)):
            HDATE = str(inputdata[-1]['harvest']['HDATE'].tolist()[i])
            HDATE = HDATE[-5:]
            HDATE_list.append(HDATE)
        df_HDATE = pd.DataFrame(HDATE_list)
        inputdata[-1]['tillage']['TDATE'] = df_HDATE


    #simulation control


    SimNo = treatment['SM'].unique()
    simulation = simulation.loc[simulation['N'].isin(SimNo)]
    simulationdate = treatment.loc[treatment['N'].isin(SimNo)]
    simulationdate = simulationdate[['N','Measuredate','PDATE']]
    #防止模拟时间早于其他时间让播种时间推迟10天
    Smi_PDATE = simulationdate['PDATE']
    Smi_date_list = []
    Smi_HDATE_list = []
    for i in range(len(Smi_PDATE)):
        Smi_PDATE_tmp = delayday(str(Smi_PDATE[i]),10)
        Smi_HDATE_tmp = delayday(str(Smi_PDATE[i]),365)
        Smi_HDATE_list.append(Smi_HDATE_tmp)
        Smi_date_list.append(Smi_PDATE_tmp)
    df_SmiSdate = pd.DataFrame(Smi_date_list)
    df_SmiHdate = pd.DataFrame(Smi_HDATE_list)
    simulationdate['PDATE'] = df_SmiSdate
    simulationdate['HLAST'] = df_SmiHdate

    #如果PFRST(开始播种窗口)为空 那么使用measuredate(测量数据的时间)
    # 如果PFRST(开始播种窗口)为空 那么使用measuredate(测量数据的时间)
    # df_tmp = {
    #     'N': [1,2,3,4],
    #     'B': [1,2,3,4],
    #     'C': [1, 2, 3, 4],
    #     'PFRST': [201310, -99, -99, 201320],
    # }
    # df_tmp_date = {
    #     'N':[2,3,4],
    #     'Measuredate':[201311,201312,201333]
    #
    # }
    # simulation_test = pd.DataFrame(df_tmp)
    # print(simulation_test)
    # simulation_date_test = pd.DataFrame(df_tmp_date)
    # tmp_Pfrst1 = simulation_test['PFRST'].loc[simulation_test['N'].isin(simulation_date_test['N'])]
    # change_aa = tmp_Pfrst1.index.tolist()
    # for i in range(len(tmp_Pfrst1)):
    #
    #         # simulation.loc[change_a[i],'PFRST'] = simulationdate['Measuredate'][i]
    #         simulation_test.loc[change_aa[i], 'PFRST'] = nafun(simulation_test.loc[change_aa[i], 'PFRST'],simulation_date_test['Measuredate'][i])
    # print(simulation_test)
    # exit()
    tmp_Pfrst = simulation['PFRST'].loc[simulation['N'].isin(simulationdate['N'])]
    change_a = tmp_Pfrst.index.tolist()
    for i in range(len(tmp_Pfrst)):
        # simulation.loc[change_a[i],'PFRST'] = simulationdate['Measuredate'][i]
        simulation.loc[change_a[i], 'PFRST'] = nafun(simulation.loc[change_a[i], 'PFRST'],simulationdate['Measuredate'][i])

    #PLAST(结束窗口)为空使用PDATE播种日期
    tmp_Plast = simulation['PLAST'].loc[simulation['N'].isin(simulationdate['N'])]
    change_b = tmp_Plast.index.tolist()
    for i in range(len(tmp_Plast)):
        simulation.loc[change_b[i], 'PLAST'] = nafun(simulation.loc[change_b[i], 'PLAST'],simulationdate['PDATE'][i])
    #HLAST为空使用HLAST，本来为空用的是PDATE推迟一年后的数据
    tmp_Hlast = simulation['HLAST'].loc[simulation['N'].isin(simulationdate['N'])]
    change_c = tmp_Hlast.index.tolist()
    for i in range(len(tmp_Hlast)):
        simulation.loc[change_c[i], 'HLAST'] = nafun(simulation.loc[change_c[i], 'HLAST'], simulationdate['HLAST'][i])
    SimNo = simulation.shape[0]
    Data_sim_ctrl = {
        'N':simulation['N'],
        'GENERAL':['GE']*SimNo,
        'NYERS':simulation['NYERS'],
        'NREPS': simulation['NREPS'],
        'START':['S']*SimNo,
        'SDATE': simulation['SDATE'],
        'RSEED': [2150] * SimNo,
        'SNAME':simulation['DETAILS'],
        'SMODEL': simulation['SMODEL'],
        'OPTIONS':['OP']*SimNo,
        'WATER': simulation['WATER'],
        'NITRO': simulation['NITRO'],
        'SYMBI': simulation['SYMBI'],
        'PHOSP': simulation['PHOSP'],
        'POTAS': simulation['POTAS'],
        'DISES': simulation['DISES'],
        'CHEM': simulation['CHEM'],
        'TILL': simulation['TILL'],
        'CO2': simulation['CO2'],
        'METHODS': ['ME']*SimNo,
        'WTHER':['M']*SimNo,
        'INCON': ['M'] * SimNo,
        'LIGHT': ['E'] * SimNo,
        'EVAPO': ['R'] * SimNo,
        'INFIL': ['S'] * SimNo,
        'PHOTO':simulation['PHOTO'],
        'HYDRO': ['R'] * SimNo,
        'NSWIT': [1] * SimNo,
        'MESOM': ['G'] * SimNo,
        'MESEV': ['S'] * SimNo,
        'MESOL': [2] * SimNo,
        'MANAGEMENT': ['M'] * SimNo,
        'PLANT':simulation['PLANT'],
        'IRRIG':simulation['IRRIG'],
        'FERTI':simulation['FERTI'],
        'RESID':simulation['RESID'],
        'HARVS':simulation['HARVS'],
        'OUTPUTS': ['OU'] * SimNo,
        'FNAME': ['N'] * SimNo,
        'OVVEW': ['Y'] * SimNo,
        'SUMRY': ['Y'] * SimNo,
        'FROPT':[1] * SimNo,
        'GROUT': ['Y'] * SimNo,
        'CAOUT': ['N'] * SimNo,
        'WAOUT': ['Y'] * SimNo,
        'NIOUT': ['Y'] * SimNo,
        'MIOUT': [1] * SimNo,
        'DIOUT': ['N'] * SimNo,
        'VBOSE': ['Y'] * SimNo,
        'CHOUT': ['N'] * SimNo,
        'OPOUT': ['N'] * SimNo,

    }
    df_sim_ctrl = pd.DataFrame(Data_sim_ctrl)
    df_sim_ctrl = rad(df_sim_ctrl)
    input_sim_ctrl = {'sim_ctrl':df_sim_ctrl}
    inputdata.append(input_sim_ctrl)
    SDATE = inputdata[-1]['sim_ctrl']['SDATE']
    SDATE_list = []
    for i in range(len(SDATE)):
        SDATE = str(SDATE.tolist()[i])
        SDATE = SDATE[-5:]
        SDATE_list.append(SDATE)
    df_SDATE = pd.DataFrame(SDATE_list)
    inputdata[-1]['sim_ctrl']['SDATE'] = df_SDATE

    ## AUTOMATIC MANAGEMENT，里面都是IR的参数
    Date_auto_mgmt = {
        'N':simulation['N'],
        'PLANTING':['PL']*SimNo,
        'PFRST':simulation['PFRST'],
        'PLAST':simulation['PLAST'],
        'PH2OL':[40]*SimNo,
        'PH2OU': [100] * SimNo,
        'PH2OD': [30] * SimNo,
        'PSTMX': [40] * SimNo,
        'PSTMN': [10] * SimNo,
        'IRRIGATION': ['IR'] * SimNo,
        'IMDEP': [30] * SimNo,
        'ITHRL': [50] * SimNo,
        'ITHRU': [100] * SimNo,
        'IROFF': ['GS000'] * SimNo,
        'IMETH': ['IR001'] * SimNo,
        'IRAMT': [10] * SimNo,
        'IREFF': [1] * SimNo,
        'NITROGEN': ['NI'] * SimNo,
        'NMDEP': [30] * SimNo,
        'NMTHR': [50] * SimNo,
        'NAMNT': [25] * SimNo,
        'NCODE': ['FE001'] * SimNo,
        'NAOFF': ['GS000'] * SimNo,
        'RESIDUES': ['RE'] * SimNo,
        'RIPCN': [100] * SimNo,
        'RTIME': [1] * SimNo,
        'RIDEP': [20] * SimNo,
        'HARVEST': ['HA'] * SimNo,
        'HFRST': [0] * SimNo,
        'HLAST': simulation['HLAST'],
        'HPCNP': [100] * SimNo,
        'HPCNR': [0] * SimNo,

    }
    df_auto_mgmt = pd.DataFrame(Date_auto_mgmt)
    input_auto_mgmt = {'auto_mgmt':df_auto_mgmt}
    inputdata.append(input_auto_mgmt)

    PFRST = inputdata[-1]['auto_mgmt']['PFRST']
    PLAST = inputdata[-1]['auto_mgmt']['PLAST']
    HLAST = inputdata[-1]['auto_mgmt']['HLAST']
    PFRST_list = []
    PLAST_list = []
    HLAST_list = []
    for i in range(len(PFRST)):
        PFRST= str(PFRST.tolist()[i])
        PLAST = str(PLAST.tolist()[i])
        HLAST = str(HLAST.tolist()[i])
        PFRST = PFRST[-5:]
        PLAST = PLAST[-5:]
        HLAST = HLAST[-5:]
        PFRST_list.append(PFRST)
        PLAST_list.append(PLAST)
        HLAST_list.append(HLAST)
    df_PFRST = pd.DataFrame(PFRST_list)
    df_PLAST = pd.DataFrame(PLAST_list)
    df_HLAST = pd.DataFrame(HLAST_list)
    inputdata[-1]['auto_mgmt']['PFRST'] = df_PFRST
    inputdata[-1]['auto_mgmt']['PLAST'] = df_PLAST
    inputdata[-1]['auto_mgmt']['HLAST'] = df_HLAST

    return inputdata
