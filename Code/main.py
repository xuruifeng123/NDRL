# @Descripttion ：
# -*- codeing: utf-8 -*-
# @time ：2024/12/16 22:04
# @Author : Ruifeng Xu
# @Site : 
# @file : main.py.py
# @Sofeware : PyCharm
from loguru import logger
import argparse
from Irrigation import Irrigation_main
from Fertilizer import Fertilizer_main
import random
import copy
import numpy as np
import argparse
import math
from loguru import logger


from Water_Fertilizer import water_fertilizer_main
from data_process.cox_process import make_xbuild
from data_process.extract_data import Preparedata
from Model.RL_environment.Cotton.dssat import CLEAR_irrigation, get_times, IRVAL_update, run_external_command,Fertilier_update
from Model.RL_environment.Environment import Cropgo_env
from Model.RL_Agent.Agent import policy_improve, Agent
from path import Absolute_path
from base_function import Sub_Update
from Water_Fertilizer_limit import water_fertilizer_limit_main




def main():
    parser = argparse.ArgumentParser()
    # task definition
    parser.add_argument("--task", default="Water", type=str, help="Fertilizer or Water")
    parser.add_argument('--gpu', default=0, type=int)
    parser.add_argument('--unit',default='Y', type=str,help="N or Y")
    parser.add_argument('--limit',default='Y', type=str,help="N or Y")
    # parameters definitions_uint
    # ------------------------------
    # 64 60 4 4 24_parameter  初始状态 32，30
    # 60 90 4 4 23_parameter  初始状态 30，45
    # ------------------------------
    parser.add_argument('--max_IRVAL', default=44, type=int)
    parser.add_argument('--min_IRVAL', default=0, type=int)
    parser.add_argument('--step_IRVAL', default=11, type=int)
    parser.add_argument('--max_Fertilizer', default=28, type=int)
    parser.add_argument('--min_Fertilizer', default=0, type=int)
    parser.add_argument('--step_Fertilizer', default=7, type=int)
    parser.add_argument('--times', default=12, type=int, help="Number of Fertilizer")
    parser.add_argument('--step_time', default=2, type=int)
    parser.add_argument('--file_path', default="Xinput_v240.xlsx", type=str)
    parser.add_argument('--file_cox', default="XJHX1124.COX", type=str)
    parser.add_argument('--epsilon', default=1000, type=int)
    args = parser.parse_args()

    if args.task == 'Water'and args.unit=="N" and args.limit=='N':
        print("单水优化")
        Irrigation_main(args)
    elif args.task == 'Fertilizer'and args.unit=="N" and args.limit=='N':
        print("单肥优化")
        Fertilizer_main(args)
    elif args.unit=="Y" and args.limit=='Y':
        print("限制水肥一体化优化")
        water_fertilizer_limit_main(args)
    else:
        print("水肥一体化优化")
        water_fertilizer_main(args)
        
if __name__ == '__main__':
    logger.add("./log_{time:YYYY-MM-DD-HH-mm-ss}_v4.8.2_24_unit_limit.log", format="{time} - {level} - {message}", level="INFO")
    main()


   