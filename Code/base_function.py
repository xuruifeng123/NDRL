# @Descripttion ：
# -*- codeing: utf-8 -*-
# @time ：2024/11/25 14:56
# @Author : Ruifeng Xu
# @Site : 
# @file : base_function.py
# @Sofeware : PyCharm


import numpy as np
from Model.RL_Agent.Agent import sub_policy_improve,sub_policy_improve_unit
from Model.RL_environment.Cotton.dssat import IRVAL_update,run_external_command,Fertilier_update
from data_process.cox_process import make_xbuild
from data_process.extract_data import Preparedata
from loguru import logger
import math
import copy


# -----------------------------unit_RL-----------------------------------------------------
def Sub_Update_unit(args,env_unit,agent_unit,epsilon,DAYS,state,type):
    update_episode = 0
    stand=0
    max_IRVAL_total=None
    max_fertilizer_total=None
    current_sub_state_seq = []
    agent_unit.clear_unit()
    for i in range(len(DAYS)):
        env_unit.sub_pos["IRVAL"][i]=state["IRVAL_dis"][i]
        env_unit.sub_pos["Fertilizer"][i]=state["Fert_dis"][i]
    while True:
        current_q_value_1=None
        current_sub_state=None
        max_IRVAL = []
        MAX_Fertilizer = []
        for _ in  range(10):
            sub_state=env_unit.sub_reset()
            sub_state_seq=sub_state["Iter"]
            current_q_value=[]
            for i in range(env_unit.sub_steps):
                harvest_IRVAL_Fertilizer = {"harvest": 0, "IRVAL": [0,0], "Fertilizer": [0,0]}
                # Agent interaction
                epsilon_0 = 0.1 + 0.9 * math.exp(-1 * stand / epsilon)
                DAY_choice,sub_act_W,sub_act_F=agent_unit.sub_play_unit(action_W_diss=state["IRVAL_dis"],action_F_diss=state["Fert_dis"],epsilon=epsilon_0,state=sub_state)
                logger.info("当前日期修改:"+str(DAY_choice)+"   当前灌溉量："+str(sub_act_W) +"   当前施肥量："+str(sub_act_F))
                action_seq_0 = ((sub_act_W+env_unit.step_IRVAL - state["IRVAL_dis"][DAY_choice]) // env_unit.step_IRVAL) * (
                        (env_unit.step_Fert*2) // env_unit.step_Fert)
                action_seq_1 = ((sub_act_F+env_unit.step_Fert - state["Fert_dis"][DAY_choice]) // env_unit.step_Fert) + action_seq_0
                if sub_act_W <0 :
                    sub_act_W = 0
                if sub_act_F <0 :
                    sub_act_F = 0
                next_sub_state,Harvest,IRVAL_sub,Fertilizer_sub=env_unit.sub_step_unit(sub_action_W=sub_act_W,
                                                                        sub_action_F=sub_act_F,DAYS=DAYS,
                                                                        DAY_choice=DAY_choice)
                harvest_IRVAL_Fertilizer["harvest"]=Harvest
                harvest_IRVAL_Fertilizer["IRVAL"]=IRVAL_sub
                harvest_IRVAL_Fertilizer["Fertilizer"]=Fertilizer_sub
                logger.info(f"================================={harvest_IRVAL_Fertilizer}=============")
                current_sub_state_seq.append(copy.deepcopy(harvest_IRVAL_Fertilizer))
                logger.info( "子状态产量: "+str(Harvest))
                #  Q-update
                sub_act=[sub_act_W,sub_act_F]
                reward = env_unit.sub_reward_unit(Harvest=Harvest, action_W=sub_act_W,action_F=sub_act_F,
                                                  WSGD=env_unit.sub_pos["WSGD"][DAY_choice],NSTD=env_unit.sub_pos["NSTD"][DAY_choice])
                return_val = reward + agent_unit.sub_gamma * (0 if next_sub_state["Iter"] ==2 else np.max([item[3] for item in agent_unit.sub_value_q[next_sub_state["Iter"], :]]))

                q_value=agent_unit.sub_value_q[sub_state_seq][action_seq_1][3]
                agent_unit.sub_value_q[sub_state_seq][action_seq_1]=(DAY_choice,sub_act_W,sub_act_F,
                                                               q_value+(return_val - q_value)
                                                               *(final_lr + (initial_lr - final_lr) * np.exp(-1. * update_episode / total_eps)))

                current_q_value.append(agent_unit.sub_value_q[sub_state_seq][action_seq_1][3])
                # state_update
                sub_state_seq=next_sub_state["Iter"]
                sub_state=next_sub_state

                stand+=1
            update_episode += 1
            logger.info("当前子状态更新轮数:  "+str(update_episode))
            current_q_value_1=current_q_value
            current_sub_state=sub_state

        ret=sub_policy_improve_unit(agent_unit,current_q_value_1)
        if not  ret :
            max_Harvest_0=current_sub_state["Harvest"]
            IRVAL=current_sub_state["IRVAL"]
            Fertilizer=current_sub_state["Fertilizer"]
            for i in range(len(DAYS)):
                IRVAL_update(env_unit.file_path,DAYS[i],agent_unit.sub_pi[i][1])
                Fertilier_update(env_unit.file_path,DAYS[i],agent_unit.sub_pi[i][2])
            inputdata = Preparedata(args.file_path, IR_FER_ALL=False)
            make_xbuild(inputdata=inputdata, output_path=args.file_cox)
            max_Harvest_1, _ = run_external_command("A", args.file_cox, run_data_path="../dssat_tool/")
            if max_Harvest_1 >=max_Harvest_0:
                logger.info("子策略"+str(agent_unit.sub_pi))
                logger.info("子策略下最大产量:"+str(max_Harvest_1))
                for i in range(len(IRVAL)):
                    max_IRVAL.append(agent_unit.sub_pi[i][1])
                    MAX_Fertilizer.append(agent_unit.sub_pi[i][2])
                max_Harvest=max_Harvest_1
                max_IRVAL_total = max_IRVAL
                max_fertilizer_total = MAX_Fertilizer
                for i in range(len(IRVAL)):
                    IRVAL_update(env_unit.file_path, DAYS[i], max_IRVAL[i])
                    Fertilier_update(env_unit.file_path, DAYS[i], max_fertilizer_total[i])
                inputdata = Preparedata(args.file_path, IR_FER_ALL=False)
                make_xbuild(inputdata=inputdata, output_path=args.file_cox)
            else:
                max_Harvest=max_Harvest_0
                max_IRVAL=IRVAL
                max_fertilizer = Fertilizer
                max_IRVAL_total=max_IRVAL
                max_fertilizer_total=max_fertilizer
                logger.info("子策略" + str(max_IRVAL))
                logger.info("子策略下最大产量:"+str(max_Harvest_0))
                for i in range(len(max_IRVAL)):
                    IRVAL_update(env_unit.file_path, DAYS[i], max_IRVAL[i])
                    Fertilier_update(env_unit.file_path, DAYS[i], max_fertilizer_total[i])
                inputdata = Preparedata(args.file_path, IR_FER_ALL=False)
                make_xbuild(inputdata=inputdata, output_path=args.file_cox)
            break
    logger.info(f"长度{len(current_sub_state_seq)}:{current_sub_state_seq}")
    for harvest_dirct in current_sub_state_seq:
        if harvest_dirct["harvest"]>max_Harvest:
            if abs(max_Harvest-harvest_dirct["harvest"])<5:
                if np.sum(np.array(max_IRVAL_total))>np.sum(np.array(harvest_dirct["IRVAL"])) or np.sum(np.array(max_fertilizer_total))>np.sum(np.array(harvest_dirct["Fertilizer"])):
                    max_Harvest = harvest_dirct["harvest"]
                    max_IRVAL_total = harvest_dirct["IRVAL"]
                    max_fertilizer_total=harvest_dirct["Fertilizer"]
                else:
                    continue
            else:
                max_Harvest=harvest_dirct["harvest"]
                max_IRVAL_total=harvest_dirct["IRVAL"]
                max_fertilizer_total=harvest_dirct["Fertilizer"]
        else:
            if abs(max_Harvest-harvest_dirct["harvest"])<5:
                if np.sum(np.array(max_IRVAL_total))>np.sum(np.array(harvest_dirct["IRVAL"])) or np.sum(np.array(max_fertilizer_total))>np.sum(np.array(harvest_dirct["Fertilizer"])):
                    max_Harvest = harvest_dirct["harvest"]
                    max_IRVAL_total = harvest_dirct["IRVAL"]
                    max_fertilizer_total=harvest_dirct["Fertilizer"]
                else:
                    continue
            else:
                continue

    for i in range(len(max_IRVAL_total)):
        IRVAL_update(env_unit.file_path, DAYS[i], max_IRVAL_total[i])
        Fertilier_update(env_unit.file_path, DAYS[i], max_fertilizer_total[i])
        agent_unit.sub_pi[i][1]=max_IRVAL_total[i]
        agent_unit.sub_pi[i][2]=max_fertilizer_total[i]
    inputdata = Preparedata(args.file_path, IR_FER_ALL=False)
    make_xbuild(inputdata=inputdata, output_path=args.file_cox)
    logger.info("当前最大产量1:" + str(max_Harvest))
    logger.info("当前最大子策略" + str(max_IRVAL_total)+"  "+str(max_fertilizer_total))

    return  np.max([item[3] for item in agent_unit.sub_value_q[1, :]]),max_Harvest,max_IRVAL_total,max_fertilizer_total


