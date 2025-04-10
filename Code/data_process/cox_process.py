'''
Descripttion: 
Author: Ruifeng Xu
version: 1.0
Date: 2024-11-22 23:30:32
LastEditors: Ruifeng Xu
LastEditTime: 2024-12-18 11:01:45
'''

import os
import logging
import pandas as pd
import os
from datetime import  datetime
import re
from loguru import logger


from data_process.extract_data import *

from path import Absolute_path



def make_xbuild(inputdata,output_path,overwrite=True):
    output_path=os.path.join(Absolute_path,"Model/RL_environment/Cotton/"+output_path)

    if not os.path.exists(output_path):
        with open(output_path,'w',encoding='UTF-8') as f:
            print('create cox files and input !')
            f.write("")

    if overwrite:
        with open(output_path,'w',encoding='UTF-8') as f:

            f.write("*EXP.DETAILS: " + inputdata[0]['general']['exp_details'] + "\n")

            f.write('\n')
            f.write("*GENERAL\n@PEOPLE\n")
            #general stuff
            f.write(" " + "{:<12s}".format(inputdata[0]["general"]["PEOPLE"]) + "\n")
            f.write('@ADDRESS\n')
            f.write(" " + "{:<12s}".format(inputdata[0]["general"]["ADDRESS"]) + "\n")
            f.write('@SITE\n')
            f.write(" " + "{:<12s}".format(inputdata[0]["general"]["SITE"]) + "\n")
            f.write('@NOTE\n')
            f.write(" " + "{:<12s}".format(inputdata[0]["general"]["NOTES"]) + "\n")
            f.write('\n')
            #treatments
            f.write("*TREATMENTS                        -------------FACTOR LEVELS------------\n")
            f.write("@N R O C TNAME.................... CU FL SA IC MP MI MF MR MC MT ME MH SM\n")
            for i in range(len(inputdata[1]['treatments'])):
                f.write("{:2d}{:2d}{:2d}{:2d}".format(int(inputdata[1]['treatments']['N'].tolist()[i]),int(inputdata[1]['treatments']['R'].tolist()[i]),
                                                      int(inputdata[1]['treatments']['O'].tolist()[i]),int(inputdata[1]['treatments']['C'].tolist()[i]))
                        + " " +
                        "{:<25s}{:3d}{:3d}{:3d}{:3d}{:3d}{:3d}{:3d}{:3d}{:3d}{:3d}{:3d}{:3d}{:3d}".format(inputdata[1]['treatments']['TNAME'].tolist()[i],
                                                                                                          int(inputdata[1]['treatments']['CU'].tolist()[i]),
                                                                                                          int(inputdata[1]['treatments']['FL'].tolist()[i]),
                                                                                                          int(inputdata[1]['treatments']['SA'].tolist()[i]),
                                                                                                          int(inputdata[1]['treatments']['IC'].tolist()[i]),
                                                                                                          int(inputdata[1]['treatments']['MP'].tolist()[i]),
                                                                                                          int(inputdata[1]['treatments']['MI'].tolist()[i]),
                                                                                                          int(inputdata[1]['treatments']['MF'].tolist()[i]),
                                                                                                          int(inputdata[1]['treatments']['MR'].tolist()[i]),
                                                                                                          int(inputdata[1]['treatments']['MC'].tolist()[i]),
                                                                                                          int(inputdata[1]['treatments']['MT'].tolist()[i]),
                                                                                                          int(inputdata[1]['treatments']['ME'].tolist()[i]),
                                                                                                          int(inputdata[1]['treatments']['MH'].tolist()[i]),
                                                                                                          int(inputdata[1]['treatments']['SM'].tolist()[i]))
                        + "\n"
                        )
            f.write('\n')
            #cultivrs
            f.write("*CULTIVARS\n")
            f.write("@C CR INGENO CNAME\n")
            for i in range(len(inputdata[2]['cultivars'])):
                f.write("{:2d}".format(int(inputdata[2]['cultivars']['C'].tolist()[i])) + " " + "{:2s}".format(inputdata[2]['cultivars']['CR'].tolist()[i])
                        + " " +
                        "{:6s}".format(inputdata[2]['cultivars']['INGENO'].tolist()[i]) + " " + "{:<12s}".format(inputdata[2]['cultivars']['CNAME'].tolist()[i])
                        + "\n"
                        )
            f.write("\n")

            #fields
            f.write("*FIELDS\n")
            f.write("@L ID_FIELD WSTA....  FLSA  FLOB  FLDT  FLDD  FLDS  FLST SLTX  SLDP  ID_SOIL    FLNAME\n")
            for i in range(len(inputdata[3]['fields'])):
                f.write("{:2d}".format(int(inputdata[3]['fields']['L'].tolist()[i])) + " " + "{:<8s}".format(inputdata[3]['fields']['ID_FIELD'].tolist()[i])
                        + " " +
                        "{:<8s}".format(inputdata[3]['fields']['WSTA'].tolist()[i]) + "{:6d}".format(int(inputdata[3]['fields']['FLSA'].tolist()[i])) +
                                        "{:6d}".format(int(inputdata[3]['fields']['FLOB'].tolist()[i])) +
                                        "{:>6s}".format(str(inputdata[3]['fields']['FLDT'].tolist()[i])) +
                                        "{:6d}".format(int(inputdata[3]['fields']['FLDD'].tolist()[i])) +
                                        "{:6d}".format(int(inputdata[3]['fields']['FLDS'].tolist()[i])) +
                                        "{:6d}".format(int(inputdata[3]['fields']['FLST'].tolist()[i])) + " " +
                                        "{:<4s}".format(str(inputdata[3]['fields']['SLTX'].tolist()[i])) +
                                        "{:6d}".format(int(inputdata[3]['fields']['SLDP'].tolist()[i])) + "  " +
                                        "{:<10s}".format(str(inputdata[3]['fields']['ID_SOIL'].tolist()[i])) + " " +
                                        "{:<12s}".format(str(inputdata[3]['fields']['FLNAME'].tolist()[i])) + '\n'
                        )
            f.write("@L ...........XCRD ...........YCRD .....ELEV .............AREA .SLEN .FLWR .SLAS FLHST FHDUR\n")
            for i in range(len(inputdata[3]['fields'])):
                f.write("{:2d}".format(int(inputdata[3]['fields']['L'].tolist()[i]))+ " " +
                        "{:15.3f}".format(int(inputdata[3]['fields']['XCRD'].tolist()[i])) + " " +
                        "{:15.3f}".format(int(inputdata[3]['fields']['YCRD'].tolist()[i])) + " " +
                        "{:9d}".format(int(inputdata[3]['fields']['ELEV'].tolist()[i])) + " " +
                        "{:17d}".format(int(inputdata[3]['fields']['AREA'].tolist()[i])) + " " +
                        "{:5d}".format(int(inputdata[3]['fields']['SLEN'].tolist()[i])) + " " +
                        "{:5d}".format(int(inputdata[3]['fields']['FLWR'].tolist()[i])) + " " +
                        "{:5d}".format(int(inputdata[3]['fields']['SLAS'].tolist()[i])) + " " +
                        "{:5d}".format(int(inputdata[3]['fields']['FLHST'].tolist()[i])) + " " +
                        "{:5d}".format(int(inputdata[3]['fields']['FHDUR'].tolist()[i]))  + "\n"

                        )
            f.write('\n')

            #soil analysis 暂时不分析
            # for i in range(len(inputdata)):
            #     print(inputdata[i].keys())
            # dict_keys(['general'])
            # dict_keys(['treatments'])
            # dict_keys(['cultivars'])
            # dict_keys(['fields'])
            # dict_keys(['ini_cond_properties'])
            # dict_keys(['ini_cond_profile'])
            # dict_keys(['planting'])
            # dict_keys(['irrigation'])
            # dict_keys(['fertilization'])
            # dict_keys(['environment'])
            # dict_keys(['sim_ctrl'])
            # dict_keys(['auto_mgmt'])
            #
            #initial conditions
            if len(inputdata[1]['treatments']['IC'].unique()) > 1 or inputdata[1]['treatments']['IC'].unique() != 0 :
                f.write("*INITIAL CONDITIONS\n")
                ini_cond_NO = inputdata[4]['ini_cond_properties']['C'].unique()
                for i in range(len(ini_cond_NO)):
                    f.write("@C   PCR ICDAT  ICRT  ICND  ICRN  ICRE  ICWD ICRES ICREN ICREP ICRIP ICRID ICNAME\n")
                    ini_cond_profile_sub = inputdata[5]['ini_cond_profile'][inputdata[5]['ini_cond_profile']['C'] == ini_cond_NO[i]]
                    f.write("{:2d}".format(int(inputdata[4]['ini_cond_properties']['C'].tolist()[i])) + " " +
                            "{:>5s}".format(str(inputdata[4]['ini_cond_properties']['PCR'].tolist()[i])) + " " +
                            "{:5s}".format(str(inputdata[4]['ini_cond_properties']['ICDAT'].tolist()[i])) + " " +
                            "{:5d}".format(int(inputdata[4]['ini_cond_properties']['ICRT'].tolist()[i])) + " " +
                            "{:5d}".format(int(inputdata[4]['ini_cond_properties']['ICND'].tolist()[i])) + " " +
                            "{:5d}".format(int(inputdata[4]['ini_cond_properties']['ICRN'].tolist()[i])) + " " +
                            "{:5d}".format(int(inputdata[4]['ini_cond_properties']['ICRE'].tolist()[i])) + " " +
                            "{:5d}".format(int(inputdata[4]['ini_cond_properties']['ICWD'].tolist()[i])) + " " +
                            "{:5d}".format(int(inputdata[4]['ini_cond_properties']['ICRES'].tolist()[i])) + " " +
                            "{:5d}".format(int(inputdata[4]['ini_cond_properties']['ICREN'].tolist()[i])) + " " +
                            "{:5d}".format(int(inputdata[4]['ini_cond_properties']['ICREP'].tolist()[i])) + " " +
                            "{:5d}".format(int(inputdata[4]['ini_cond_properties']['ICRIP'].tolist()[i])) + " " +
                            "{:5d}".format(int(inputdata[4]['ini_cond_properties']['ICRID'].tolist()[i])) + " " +
                            "{:<12s}".format(str(inputdata[4]['ini_cond_properties']['ICNAME'].tolist()[i])) + "\n"
                            )
                    f.write("@C  ICBL  SH2O  SNH4  SNO3\n")

                    for j in range(len(ini_cond_profile_sub)):
                        f.write("{:2d}".format(int(ini_cond_profile_sub['C'].tolist()[j])) + " " +
                                "{:5.0f}".format(int(ini_cond_profile_sub['ICBL'].tolist()[j])) + " " +
                                "{:5.2f}".format(int(ini_cond_profile_sub['SH2O'].tolist()[j])) + " " +
                                "{:5.0f}".format(int(ini_cond_profile_sub['SNH4'].tolist()[j])) + " " +
                                "{:5.0f}".format(int(ini_cond_profile_sub['SNO3'].tolist()[j])) + "\n"
                                )
                f.write('\n')

            #planting details
            if len(inputdata[1]['treatments']['MP'].unique()) > 1 or inputdata[1]['treatments']['MP'].unique() != 0 :
                f.write("*PLANTING DETAILS\n")
                PL_NO = inputdata[6]['planting']['P'].unique()
                for i in range(len(PL_NO)):
                    PL_sub = inputdata[6]['planting'][inputdata[6]['planting']['P'] == PL_NO[i]]
                    f.write("@P PDATE EDATE  PPOP  PPOE  PLME  PLDS  PLRS  PLRD  PLDP  PLWT  PAGE  PENV  PLPH  SPRL                        PLNAME\n")
                    for j in range(len(PL_sub)):
                        f.write("{:2d}".format(int(PL_sub['P'].tolist()[j])) + ' ' +
                                "{:5s}".format(str(PL_sub['PDATE'].tolist()[j])) + ' ' +
                                "{:5s}".format(str(PL_sub['EDATE'].tolist()[j])) + ' ' +
                                "{:5d}".format(int(PL_sub['PPOP'].tolist()[j])) + ' ' +
                                "{:5d}".format(int(PL_sub['PPOE'].tolist()[j])) + ' ' +
                                "{:>5s}".format(str(PL_sub['PLME'].tolist()[j])) + ' ' +
                                "{:>5s}".format(str(PL_sub['PLDS'].tolist()[j])) + ' ' +
                                "{:5d}".format(int(PL_sub['PLRS'].tolist()[j])) + ' ' +
                                "{:5d}".format(int(PL_sub['PLRD'].tolist()[j])) + ' ' +
                                "{:5d}".format(int(PL_sub['PLDP'].tolist()[j])) + ' ' +
                                "{:5d}".format(int(PL_sub['PLWT'].tolist()[j])) + ' ' +
                                "{:5d}".format(int(PL_sub['PAGE'].tolist()[j])) + ' ' +
                                "{:5d}".format(int(PL_sub['PENV'].tolist()[j])) + ' ' +
                                "{:5d}".format(int(PL_sub['PLPH'].tolist()[j])) + ' ' +
                                "{:5d}".format(int(PL_sub['SPRL'].tolist()[j])) + ' ' +
                                "{:>29s}".format(str(PL_sub['PLNAME'].tolist()[j])) + '\n'

                                )
                f.write('\n')
            #Irrigation and water management
            if len(inputdata[1]['treatments']['MI'].unique()) > 1 or inputdata[1]['treatments']['MI'].unique() != 0 :
                f.write("*IRRIGATION AND WATER MANAGEMENT\n")
                irrigation_NO = inputdata[7]['irrigation']['I'].unique()

                for i in range(len(irrigation_NO)):
                    irrigation_sub = inputdata[7]['irrigation'][inputdata[7]['irrigation']['I'] == irrigation_NO[i]]
                    f.write("@I  EFIR  IDEP  ITHR  IEPT  IOFF  IAME  IAMT IRNAME\n")
                    f.write("{:2d}".format(int(irrigation_sub['I'].tolist()[0])) + ' ' +
                            "{:5.0f}".format(-99) + ' ' +
                            "{:5.0f}".format(-99) + ' ' +
                            "{:5.0f}".format(-99) + ' ' +
                            "{:5.0f}".format(-99) + ' ' +
                            "{:5.0f}".format(-99) + ' ' +
                            "{:5.0f}".format(-99) + ' ' +
                            "{:5.0f}".format(-99) + ' ' +
                            "{:12s}".format(str(-99)) + '\n'
                            )

                    f.write("@I IDATE  IROP IRVAL\n")

                    for j in range(len(irrigation_sub)):

                        f.write("{:2d}".format(int(irrigation_sub['I'].tolist()[j])) + ' ' +
                                "{:5.0f}".format(int(irrigation_sub['IDATE'].tolist()[j])) + ' ' +
                                "{:>5s}".format(str(irrigation_sub['IROP'].tolist()[j])) + ' ' +
                                "{:5.0f}".format(int(irrigation_sub['IRVAL'].tolist()[j])) + '\n'
                                )

                f.write('\n')
            #FERTILIZERS
            if len(inputdata[1]['treatments']['MF'].unique()) > 1 or inputdata[1]['treatments']['MF'].unique() != 0 :
                f.write("*FERTILIZERS (INORGANIC)\n")
                fer_NO = inputdata[8]['fertilization']['I'].unique()
                f.write("@F FDATE  FMCD  FACD  FDEP  FAMN  FAMP  FAMK  FAMC  FAMO  FOCD FERNAME\n")
                for i in range(len(fer_NO)):
                    fer_sub = inputdata[8]['fertilization'][inputdata[8]['fertilization']['I'] == fer_NO[i]]
                    for j in range(len(fer_sub)):
                        f.write("{:2d}".format(int(fer_sub['I'].tolist()[j])) + ' ' +
                                "{:5.0f}".format(int(fer_sub['FDATE'].tolist()[j])) + ' ' +
                                "{:5s}".format(str(fer_sub['FMCD'].tolist()[j])) + ' ' +
                                "{:5s}".format(str(fer_sub['FACD'].tolist()[j])) + ' ' +
                                "{:5.0f}".format(int(fer_sub['FDEP'].tolist()[j])) + ' ' +
                                "{:5.0f}".format(int(fer_sub['FAMN'].tolist()[j])) + ' ' +
                                "{:5.0f}".format(int(fer_sub['FAMP'].tolist()[j])) + ' ' +
                                "{:5.0f}".format(int(fer_sub['FAMK'].tolist()[j])) + ' ' +
                                "{:5.0f}".format(int(fer_sub['FAMC'].tolist()[j])) + ' ' +
                                "{:5.0f}".format(int(fer_sub['FAMO'].tolist()[j])) + ' ' +
                                "{:5.0f}".format(int(fer_sub['FOCD'].tolist()[j])) + ' ' +
                                "{:<12s}".format(str(fer_sub['FERNAME'].tolist()[j])) + '\n'
                                )
                f.write('\n')

            #tillage 暂时没有耕种方式
            # for i in range(len(inputdata)):
            #     print(inputdata[i].keys())
            # dict_keys(['general'])
            # dict_keys(['treatments'])
            # dict_keys(['cultivars'])
            # dict_keys(['fields'])
            # dict_keys(['ini_cond_properties'])
            # dict_keys(['ini_cond_profile'])
            # dict_keys(['planting'])
            # dict_keys(['irrigation'])
            # dict_keys(['fertilization'])
            # dict_keys(['environment'])
            # dict_keys(['sim_ctrl'])
            # dict_keys(['auto_mgmt'])
            #
            #ENVIRONMENT MODIFICATIONS
            if len(inputdata[1]['treatments']['ME'].unique()) > 1 or inputdata[1]['treatments']['ME'].unique() != 0 :
                f.write("*ENVIRONMENT MODIFICATIONS\n")
                ENV_NO = inputdata[-3]['environment']['E'].unique()
                f.write("@E ODATE EDAY  ERAD  EMAX  EMIN  ERAIN ECO2  EDEW  EWIND ENVNAME\n")
                for i in range(len(ENV_NO)):
                    ENV_sub = inputdata[-3]['environment'][inputdata[-3]['environment']['E'] == fer_NO[i]]
                    for j in range(len(ENV_sub)):
                        f.write("{:2d}".format(int(ENV_sub['E'].tolist()[j])) + ' ' +
                                "{:5s}".format(str(ENV_sub['ODATE'].tolist()[j])) + ' ' +
                                "{:5s}".format(str(ENV_sub['EDAY'].tolist()[j])) + ' ' +
                                "{:5s}".format(str(ENV_sub['ERAD'].tolist()[j])) + ' ' +
                                "{:5s}".format(str(ENV_sub['EMAX'].tolist()[j])) + ' ' +
                                "{:5s}".format(str(ENV_sub['EMIN'].tolist()[j])) + ' ' +
                                "{:5s}".format(str(ENV_sub['ERAIN'].tolist()[j])) + ' ' +
                                "{:5s}".format(str(ENV_sub['ECO2'].tolist()[j])) + ' ' +
                                "{:5s}".format(str(ENV_sub['EDEW'].tolist()[j])) + ' ' +
                                "{:5s}".format(str(ENV_sub['EWIND'].tolist()[j])) + ' ' +
                                "{:<12s}".format(str(ENV_sub['ENVAME'].tolist()[j])) + '\n'
                                )
                f.write('\n')
            #Harvest Details 暂时无细节

            #simulation controls
            f.write("*SIMULATION CONTROLS\n")
            Sim_NO = inputdata[-2]['sim_ctrl']['N'].unique()
            for i in range(len(Sim_NO)):
                f.write("@N GENERAL     NYERS NREPS START SDATE RSEED SNAME.................... SMODEL\n")
                f.write("{:2d}".format(int(inputdata[-2]['sim_ctrl']['N'].tolist()[i])) + ' ' +
                        "{:<11s}".format(str(inputdata[-2]['sim_ctrl']['GENERAL'].tolist()[i])) + ' ' +
                        "{:5d}".format(int(inputdata[-2]['sim_ctrl']['NYERS'].tolist()[i])) + ' ' +
                        "{:5d}".format(int(inputdata[-2]['sim_ctrl']['NREPS'].tolist()[i])) + ' ' +
                        "{:>5s}".format(str(inputdata[-2]['sim_ctrl']['START'].tolist()[i])) + ' ' +
                        "{:5s}".format(str(inputdata[-2]['sim_ctrl']['SDATE'].tolist()[i])) + ' ' +
                        "{:5d}".format(int(inputdata[-2]['sim_ctrl']['RSEED'].tolist()[i])) + ' ' +
                        "{:<25s}".format(str(inputdata[-2]['sim_ctrl']['SNAME'].tolist()[i])) + ' ' +
                        "{:<6s}".format(str(inputdata[-2]['sim_ctrl']['SMODEL'].tolist()[i])) + '\n'
                        )
                f.write("@N OPTIONS     WATER NITRO SYMBI PHOSP POTAS DISES  CHEM  TILL   CO2\n")
                f.write("{:2d}".format(int(inputdata[-2]['sim_ctrl']['N'].tolist()[i])) + ' ' +
                        "{:<11s}".format(str(inputdata[-2]['sim_ctrl']['OPTIONS'].tolist()[i])) + ' ' +
                        "{:>5s}".format(str(inputdata[-2]['sim_ctrl']['WATER'].tolist()[i])) + ' ' +
                        "{:>5s}".format(str(inputdata[-2]['sim_ctrl']['NITRO'].tolist()[i])) + ' ' +
                        "{:>5s}".format(str(inputdata[-2]['sim_ctrl']['SYMBI'].tolist()[i])) + ' ' +
                        "{:>5s}".format(str(inputdata[-2]['sim_ctrl']['PHOSP'].tolist()[i])) + ' ' +
                        "{:>5s}".format(str(inputdata[-2]['sim_ctrl']['POTAS'].tolist()[i])) + ' ' +
                        "{:>5s}".format(str(inputdata[-2]['sim_ctrl']['DISES'].tolist()[i])) + ' ' +
                        "{:>5s}".format(str(inputdata[-2]['sim_ctrl']['CHEM'].tolist()[i])) + ' ' +
                        "{:>5s}".format(str(inputdata[-2]['sim_ctrl']['TILL'].tolist()[i])) + ' ' +
                        "{:>5s}".format(str(inputdata[-2]['sim_ctrl']['CO2'].tolist()[i])) + '\n'
                        )
                f.write("@N METHODS     WTHER INCON LIGHT EVAPO INFIL PHOTO HYDRO NSWIT MESOM MESEV MESOL\n")
                f.write("{:2d}".format(int(inputdata[-2]['sim_ctrl']['N'].tolist()[i])) + ' ' +
                        "{:<11s}".format(str(inputdata[-2]['sim_ctrl']['METHODS'].tolist()[i])) + ' ' +
                        "{:>5s}".format(str(inputdata[-2]['sim_ctrl']['WTHER'].tolist()[i])) + ' ' +
                        "{:>5s}".format(str(inputdata[-2]['sim_ctrl']['INCON'].tolist()[i])) + ' ' +
                        "{:>5s}".format(str(inputdata[-2]['sim_ctrl']['LIGHT'].tolist()[i])) + ' ' +
                        "{:>5s}".format(str(inputdata[-2]['sim_ctrl']['EVAPO'].tolist()[i])) + ' ' +
                        "{:>5s}".format(str(inputdata[-2]['sim_ctrl']['INFIL'].tolist()[i])) + ' ' +
                        "{:>5s}".format(str(inputdata[-2]['sim_ctrl']['PHOTO'].tolist()[i])) + ' ' +
                        "{:>5s}".format(str(inputdata[-2]['sim_ctrl']['HYDRO'].tolist()[i])) + ' ' +
                        "{:5d}".format(int(inputdata[-2]['sim_ctrl']['NSWIT'].tolist()[i])) + ' ' +
                        "{:>5s}".format(str(inputdata[-2]['sim_ctrl']['MESOM'].tolist()[i])) + ' ' +
                        "{:>5s}".format(str(inputdata[-2]['sim_ctrl']['MESEV'].tolist()[i])) + ' ' +
                        "{:5d}".format(int(inputdata[-2]['sim_ctrl']['MESOL'].tolist()[i])) + '\n'
                        )
                f.write("@N MANAGEMENT  PLANT IRRIG FERTI RESID HARVS\n")
                f.write("{:2d}".format(int(inputdata[-2]['sim_ctrl']['N'].tolist()[i])) + ' ' +
                        "{:<11s}".format(str(inputdata[-2]['sim_ctrl']['MANAGEMENT'].tolist()[i])) + ' ' +
                        "{:>5s}".format(str(inputdata[-2]['sim_ctrl']['PLANT'].tolist()[i])) + ' ' +
                        "{:>5s}".format(str(inputdata[-2]['sim_ctrl']['IRRIG'].tolist()[i])) + ' ' +
                        "{:>5s}".format(str(inputdata[-2]['sim_ctrl']['FERTI'].tolist()[i])) + ' ' +
                        "{:>5s}".format(str(inputdata[-2]['sim_ctrl']['RESID'].tolist()[i])) + ' ' +
                        "{:>5s}".format(str(inputdata[-2]['sim_ctrl']['HARVS'].tolist()[i])) + '\n'
                        )
                f.write("@N OUTPUTS     FNAME OVVEW SUMRY FROPT GROUT CAOUT WAOUT NIOUT MIOUT DIOUT VBOSE CHOUT OPOUT\n")
                f.write("{:2d}".format(int(inputdata[-2]['sim_ctrl']['N'].tolist()[i])) + ' ' +
                        "{:<11s}".format(str(inputdata[-2]['sim_ctrl']['OUTPUTS'].tolist()[i])) + ' ' +
                        "{:>5s}".format(str(inputdata[-2]['sim_ctrl']['FNAME'].tolist()[i])) + ' ' +
                        "{:>5s}".format(str(inputdata[-2]['sim_ctrl']['OVVEW'].tolist()[i])) + ' ' +
                        "{:>5s}".format(str(inputdata[-2]['sim_ctrl']['SUMRY'].tolist()[i])) + ' ' +
                        "{:>5s}".format(str(inputdata[-2]['sim_ctrl']['FROPT'].tolist()[i])) + ' ' +
                        "{:>5s}".format(str(inputdata[-2]['sim_ctrl']['GROUT'].tolist()[i])) + ' ' +
                        "{:>5s}".format(str(inputdata[-2]['sim_ctrl']['CAOUT'].tolist()[i])) + ' ' +
                        "{:>5s}".format(str(inputdata[-2]['sim_ctrl']['WAOUT'].tolist()[i])) + ' ' +
                        "{:>5s}".format(str(inputdata[-2]['sim_ctrl']['NIOUT'].tolist()[i])) + ' ' +
                        "{:>5s}".format(str(inputdata[-2]['sim_ctrl']['MIOUT'].tolist()[i])) + ' ' +
                        "{:>5s}".format(str(inputdata[-2]['sim_ctrl']['DIOUT'].tolist()[i])) + ' ' +
                        "{:>5s}".format(str(inputdata[-2]['sim_ctrl']['VBOSE'].tolist()[i])) + ' ' +
                        "{:>5s}".format(str(inputdata[-2]['sim_ctrl']['CHOUT'].tolist()[i])) + ' ' +
                        "{:>5s}".format(str(inputdata[-2]['sim_ctrl']['OPOUT'].tolist()[i])) + '\n')

                f.write('\n')


                #automatic management
                f.write("@  AUTOMATIC MANAGEMENT\n")
                f.write("@N PLANTING    PFRST PLAST PH2OL PH2OU PH2OD PSTMX PSTMN\n")
                f.write("{:2d}".format(int(inputdata[-1]['auto_mgmt']['N'][i])) + ' ' +
                        "{:<11s}".format(str(inputdata[-1]['auto_mgmt']['PLANTING'].tolist()[i])) + ' ' +
                        "{:5s}".format(str(inputdata[-1]['auto_mgmt']['PFRST'].tolist()[i])) + ' ' +
                        "{:5s}".format(str(inputdata[-1]['auto_mgmt']['PLAST'].tolist()[i])) + ' ' +
                        "{:5d}".format(int(inputdata[-1]['auto_mgmt']['PH2OL'].tolist()[i])) + ' ' +
                        "{:5d}".format(int(inputdata[-1]['auto_mgmt']['PH2OU'].tolist()[i])) + ' ' +
                        "{:5d}".format(int(inputdata[-1]['auto_mgmt']['PH2OD'].tolist()[i])) + ' ' +
                        "{:5d}".format(int(inputdata[-1]['auto_mgmt']['PSTMX'].tolist()[i])) + ' ' +
                        "{:5d}".format(int(inputdata[-1]['auto_mgmt']['PSTMN'].tolist()[i])) + '\n'
                        )
                f.write("@N IRRIGATION  IMDEP ITHRL ITHRU IROFF IMETH IRAMT IREFF\n")
                f.write("{:2d}".format(int(inputdata[-1]['auto_mgmt']['N'][i])) + ' ' +
                        "{:<11s}".format(str(inputdata[-1]['auto_mgmt']['IRRIGATION'].tolist()[i])) + ' ' +
                        "{:5d}".format(int(inputdata[-1]['auto_mgmt']['IMDEP'].tolist()[i])) + ' ' +
                        "{:5d}".format(int(inputdata[-1]['auto_mgmt']['ITHRL'].tolist()[i])) + ' ' +
                        "{:5d}".format(int(inputdata[-1]['auto_mgmt']['ITHRU'].tolist()[i])) + ' ' +
                        "{:5s}".format(str(inputdata[-1]['auto_mgmt']['IROFF'].tolist()[i])) + ' ' +
                        "{:s}".format(str(inputdata[-1]['auto_mgmt']['IMETH'].tolist()[i])) + ' ' +
                        "{:5d}".format(int(inputdata[-1]['auto_mgmt']['IRAMT'].tolist()[i])) + ' ' +
                        "{:5d}".format(int(inputdata[-1]['auto_mgmt']['IREFF'].tolist()[i])) + '\n'
                        )
                f.write("@N NITROGEN    NMDEP NMTHR NAMNT NCODE NAOFF\n")
                f.write("{:2d}".format(int(inputdata[-1]['auto_mgmt']['N'][i])) + ' ' +
                        "{:<11s}".format(str(inputdata[-1]['auto_mgmt']['NITROGEN'].tolist()[i])) + ' ' +
                        "{:5d}".format(int(inputdata[-1]['auto_mgmt']['NMDEP'].tolist()[i])) + ' ' +
                        "{:5d}".format(int(inputdata[-1]['auto_mgmt']['NMTHR'].tolist()[i])) + ' ' +
                        "{:5d}".format(int(inputdata[-1]['auto_mgmt']['NAMNT'].tolist()[i])) + ' ' +
                        "{:5s}".format(str(inputdata[-1]['auto_mgmt']['NCODE'].tolist()[i])) + ' ' +
                        "{:5s}".format(str(inputdata[-1]['auto_mgmt']['NAOFF'].tolist()[i])) + '\n'
                        )
                f.write("@N RESIDUES    RIPCN RTIME RIDEP\n")
                f.write("{:2d}".format(int(inputdata[-1]['auto_mgmt']['N'][i])) + ' ' +
                        "{:<11s}".format(str(inputdata[-1]['auto_mgmt']['RESIDUES'].tolist()[i])) + ' ' +
                        "{:5d}".format(int(inputdata[-1]['auto_mgmt']['RIPCN'].tolist()[i])) + ' ' +
                        "{:5d}".format(int(inputdata[-1]['auto_mgmt']['RTIME'].tolist()[i])) + ' ' +
                        "{:5d}".format(int(inputdata[-1]['auto_mgmt']['RIDEP'].tolist()[i])) + '\n'
                        )
                f.write("@N HARVEST     HFRST HLAST HPCNP HPCNR\n")
                f.write("{:2d}".format(int(inputdata[-1]['auto_mgmt']['N'][i])) + ' ' +
                        "{:<11s}".format(str(inputdata[-1]['auto_mgmt']['HARVEST'].tolist()[i])) + ' ' +
                        "{:5d}".format(int(inputdata[-1]['auto_mgmt']['HFRST'].tolist()[i])) + ' ' +
                        "{:5d}".format(int(inputdata[-1]['auto_mgmt']['HLAST'].tolist()[i])) + ' ' +
                        "{:5d}".format(int(inputdata[-1]['auto_mgmt']['HPCNP'].tolist()[i])) + ' ' +
                        "{:5d}".format(int(inputdata[-1]['auto_mgmt']['HPCNR'].tolist()[i])) + '\n'
                        )
                f.write('\n')

            f.close()
            # with open(output_path,'r') as file:
            #     context = file.read()
            # print(context)
            # file_name = re.search(r"[^\\]+$", output_path).group(0)
        
    else:
        with open(output_path,'a',encoding='UTF-8') as f:
            f.write('Temporarily do not add content' + '-'*6 + str(datetime.now()))
    logger.info("Finish build management file: " + str(output_path))





# inputdata = Preparedata("Xinput_v0.xlsx", IR_FER_ALL=False)
# make_xbuild(inputdata=inputdata, output_path="XJHX1123.COX")










