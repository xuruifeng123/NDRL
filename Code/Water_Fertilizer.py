# @Descripttion ：
# -*- codeing: utf-8 -*-
# @time ：2024/12/18 21:17
# @Author : Ruifeng Xu
# @Site : 
# @file : Water_Fertilizer.py
# @Sofeware : PyCharm

import random

import numpy as np

from loguru import logger

from data_process.cox_process import make_xbuild
from data_process.extract_data import Preparedata
from Model.RL_environment.Cotton.dssat import CLEAR_fertilizer,CLEAR_irrigation, get_times,  run_external_command,Fertilier_update,IRVAL_update
from Model.RL_environment.Environment import Cropgo_env_unit
from Model.RL_Agent.Agent import policy_improve_unit, Agent_unit

from base_function import Sub_Update_unit
import copy

EPS_START = 1.0
EPS_END = 0.1
def water_fertilizer_main(args):
    max_final_harvest = []
    max_final_action_0 = []
    max_final_action_1 = []
    Irrial_IRVAL_seq = []
    Irrial_Fertilizer_seq=[]
    # for Irrial,Fertili in zip(range(args.min_IRVAL, args.max_IRVAL, args.step_IRVAL),range(args.min_Fertilizer, args.max_Fertilizer, args.step_Fertilizer)):
    for Irrial,Fertili in zip(range(1),range(1)):
        update_episode = 0
        CLEAR_irrigation(args.file_path, 30, args.times)
        CLEAR_fertilizer(args.file_path, 45, args.times)
        logger.info("初始灌溉量： " + str(30) +"初始施肥量： "+str(45))

        total_times = get_times(args.file_path)
        stand = 0
        envs_unit = Cropgo_env_unit(args=args,min_IRVAL=args.min_IRVAL,max_IRVAL=args.max_IRVAL,step_IRVAL=args.step_IRVAL,max_Fertilizer=args.max_Fertilizer
                               ,min_Fertilizer=args.min_Fertilizer,step_Fertilizer=args.step_Fertilizer,
                               file_path=args.file_path,times=args.times,step_time=args.step_time)
        RL_Agent_unit = Agent_unit(args=args,env=envs_unit)
        Irrial_IRVAL_inital = []
        Fertilizer_fert_initial=[]
        while True:
            final_Harvest = 0
            for _ in range(2):
                if update_episode == 0:
                    Irrial_IRVAL_inital = [30] * args.times
                    Fertilizer_fert_initial = [45] * args.times
                    # Irrial_IRVAL_inital = [Irrial+20] * args.times
                    # Fertilizer_fert_initial = [Fertili+15] * args.times
                    IRAVL_optimal = [0] * args.times
                    Fert_optimal= [args.max_Fertilizer] * args.times
                   
                else:
                    Irrial_IRVAL_inital = copy.deepcopy(Irrial_IRVAL_inital)
                    IRAVL_optimal = copy.deepcopy(envs_unit.optimal_IRVAL)
                    Fertilizer_fert_initial = copy.deepcopy(Fertilizer_fert_initial)
                    Fert_optimal = copy.deepcopy(envs_unit.optimal_Fertilizer)
                state = envs_unit.reset()
                state_seq = copy.deepcopy(state["Iter"])
                IRVAL_seq = []
                Fert_seq=[]
                time = 0
                for date_pairs in total_times:
                    time += 1
                    harvest_initial_optimal, _ = run_external_command("A", args.file_cox,
                                                                      run_data_path="../dssat_tool/")
                    IRVAL_initial_optimal = Irrial_IRVAL_inital[time * 2 - 2:time * 2]
                    Fert_initial_optimal = Fertilizer_fert_initial[time * 2 - 2:time * 2]
                    IRAVL_optimal_days = IRAVL_optimal[time * 2 - 2:time * 2]
                    Fert_optimal_days= Fert_optimal[time * 2 - 2:time * 2]
                    for lens in range(len(IRAVL_optimal_days)):
                        IRVAL_update(file_path=args.file_path, IRVAL=IRAVL_optimal_days[lens], DAYS=date_pairs[lens])
                        Fertilier_update(file_path=args.file_path, fertilier=Fert_optimal_days[lens], DAYS=date_pairs[lens])
                    inputdata = Preparedata(args.file_path, IR_FER_ALL=False)
                    make_xbuild(inputdata=inputdata, output_path=args.file_cox)
                    harvest_optimal, _ = run_external_command("A", args.file_cox, run_data_path="../dssat_tool/")
                    IRAVL_optimal_days_array = np.sum(np.array(IRAVL_optimal_days))
                    Fert_optimal_days_array= np.sum(np.array(Fert_optimal_days))
                    if harvest_optimal > harvest_initial_optimal:
                        if harvest_optimal - harvest_initial_optimal < 5 and (np.sum(
                                np.array(IRVAL_initial_optimal)) < IRAVL_optimal_days_array or np.sum(np.array(Fert_initial_optimal)) < Fert_optimal_days_array):
                            for lens in range(len(IRVAL_initial_optimal)):
                                IRVAL_update(file_path=args.file_path, IRVAL=IRVAL_initial_optimal[lens],
                                             DAYS=date_pairs[lens])
                                Fertilier_update(file_path=args.file_path, fertilier=Fert_initial_optimal[lens],
                                             DAYS=date_pairs[lens])
                            inputdata = Preparedata(args.file_path, IR_FER_ALL=False)
                            make_xbuild(inputdata=inputdata, output_path=args.file_cox)
                            IRAVL_optimal_days=IRVAL_initial_optimal
                            Fert_optimal_days=Fert_initial_optimal
                        else:
                            for i in range(len(Irrial_IRVAL_inital)):
                                if i == time * 2 - 2:
                                    Irrial_IRVAL_inital[i] = IRAVL_optimal_days[0]
                                    Fertilizer_fert_initial[i]=Fert_optimal_days[0]
                                elif i == time * 2 - 1:
                                    Irrial_IRVAL_inital[i] = IRAVL_optimal_days[1]
                                    Fertilizer_fert_initial[i]=Fert_optimal_days[1] 
                    else:
                        if harvest_initial_optimal - harvest_optimal < 5 and(np.sum(
                                np.array(IRVAL_initial_optimal)) > IRAVL_optimal_days_array or np.sum(np.array(Fert_initial_optimal)) > Fert_optimal_days_array):
                            for i in range(len(Irrial_IRVAL_inital)):
                                if i == time * 2 - 2:
                                    Irrial_IRVAL_inital[i] = IRAVL_optimal_days[0]
                                    Fertilizer_fert_initial[i] = Fert_optimal_days[0]
                                elif i == time * 2 - 1:
                                    Irrial_IRVAL_inital[i] = IRAVL_optimal_days[1]
                                    Fertilizer_fert_initial[i] = Fert_optimal_days[1]        
                        else:
                            for irval in range(len(IRVAL_initial_optimal)):
                                IRVAL_update(file_path=args.file_path, IRVAL=IRVAL_initial_optimal[irval],
                                             DAYS=date_pairs[irval])
                                Fertilier_update(file_path=args.file_path, fertilier=Fert_initial_optimal[irval],DAYS=date_pairs[irval])
                            inputdata = Preparedata(args.file_path, IR_FER_ALL=False)
                            make_xbuild(inputdata=inputdata, output_path=args.file_cox)
                            IRAVL_optimal_days=IRVAL_initial_optimal
                            Fert_optimal_days=Fert_initial_optimal
                    harvest_optimal, _ = run_external_command("A", args.file_cox, run_data_path="../dssat_tool/")        
                    Irrial_IRVAL_inital=copy.deepcopy(Irrial_IRVAL_inital)
                    Fertilizer_fert_initial=copy.deepcopy(Fertilizer_fert_initial)
                    logger.info(f"----------------每次迭代初始灌溉产量：{harvest_optimal} ---------灌溉策略：{Irrial_IRVAL_inital}------------------")
                    logger.info(f"----------------每次迭代初始施肥产量：{harvest_optimal} ---------施肥策略：{Fertilizer_fert_initial}------------------")
                    max_action_diss, max_harvest = RL_Agent_unit.play_unit(date_pairs)
                    logger.info("当前状态日期:" + str(date_pairs))
                    logger.info("当前灌溉施肥量：" + str(max_action_diss))
                    logger.info("当前最大产量:" + str(max_harvest))
                    max_harvest_0 = max_harvest
                    logger.info("当前状态日期:" + str(date_pairs))
                    logger.info("当前最初始灌溉施肥量：" + str(IRAVL_optimal_days)+"  "+str(Fert_optimal_days))
                    logger.info("当前最初始产量:" + str(harvest_optimal))
                    if harvest_optimal >= max_harvest:
                        max_harvest_0 = harvest_optimal
                    elif abs(max_harvest - harvest_optimal) < 5:
                        if np.sum(np.array(max_action_diss[:2])) > IRAVL_optimal_days_array or np.sum(np.array(max_action_diss[2:])) > Fert_optimal_days_array:
                            max_harvest_0 = harvest_optimal
                    state["IRVAL_dis"] = max_action_diss[:2]
                    state["Fert_dis"]=max_action_diss[2:]
                    for i in range(len(state["IRVAL_dis"])):
                        IRVAL_update(args.file_path, date_pairs[i], max_action_diss[:2][i])
                        Fertilier_update(args.file_path, date_pairs[i], max_action_diss[2:][i])
                    action_seq_0 = ((max_action_diss[0] - args.min_IRVAL) // args.step_IRVAL) * (
                            (args.max_IRVAL - args.min_IRVAL) // args.step_IRVAL)* (
                            (args.max_Fertilizer - args.min_Fertilizer) // args.step_Fertilizer)*  (
                            (args.max_Fertilizer - args.min_Fertilizer) // args.step_Fertilizer)
                    action_seq_1 = ((max_action_diss[1] - args.min_IRVAL) // args.step_IRVAL)*(
                            (args.max_Fertilizer - args.min_Fertilizer) // args.step_Fertilizer)*  (
                            (args.max_Fertilizer - args.min_Fertilizer) // args.step_Fertilizer) + action_seq_0
                    action_seq_2= ((max_action_diss[2] - args.min_Fertilizer) // args.step_Fertilizer)*\
                                  ((args.max_Fertilizer - args.min_Fertilizer) // args.step_Fertilizer) + action_seq_1
                    action_seq_3= ((max_action_diss[3] - args.min_Fertilizer) // args.step_Fertilizer) + action_seq_2
                    reward, harvest, IRVAL,Fertilizer = Sub_Update_unit(args=args,state=state, env_unit=envs_unit, agent_unit=RL_Agent_unit, epsilon=args.epsilon,
                                                        DAYS=date_pairs, type=args.task)
                    # IRVAL_diss_array = np.sum(np.array(max_action_diss))
                    IRVAL_array = np.sum(np.array(IRVAL))
                    Fertilizer_array  = np.sum(np.array(Fertilizer))
                    if max_harvest_0 == harvest_optimal:
                        if ((IRAVL_optimal_days_array < IRVAL_array or Fertilizer_array < Fertilizer_array)
                            and abs(harvest - max_harvest_0) < 5) \
                                or (max_harvest_0 > harvest and max_harvest_0 - harvest > 5):
                            for i in range(len(IRAVL_optimal_days)):
                                IRVAL_update(args.file_path, date_pairs[i], IRAVL_optimal_days[i])
                                Fertilier_update(args.file_path, date_pairs[i], Fert_optimal_days[i])
                                envs_unit.sub_pos["IRVAL"][i] = IRAVL_optimal_days[i]
                                envs_unit.sub_pos["Fertilizer"][i] = Fert_optimal_days[i]
                            inputdata = Preparedata(args.file_path, IR_FER_ALL=False)
                            make_xbuild(inputdata=inputdata, output_path=args.file_cox)
                            harvest_optimal, _ = run_external_command("A", args.file_cox,
                                                                      run_data_path="../dssat_tool/")
                            logger.info("当前更新后状态日期-无更新:" + str(date_pairs))
                            logger.info("   当前更新后灌溉量-初始值：" + str(IRAVL_optimal_days))
                            logger.info("   当前更新后施肥量-初始值：" + str(Fert_optimal_days))
                            logger.info("当前更新后最大产量-初始值:" + str(harvest_optimal))
                            envs_unit.sub_pos["Harvest"] = harvest_optimal
                            envs_unit.sub_pos["IRVAL"] = IRAVL_optimal_days
                            envs_unit.sub_pos["Fertilizer"]=Fert_optimal_days
                            max_harvest_1 = harvest_optimal
                        else:
                            for i in range(len(IRVAL)):
                                IRVAL_update(args.file_path, date_pairs[i], IRVAL[i])
                                Fertilier_update(args.file_path, date_pairs[i], Fertilizer[i])
                                envs_unit.sub_pos["IRVAL"][i] = IRVAL[i]
                                envs_unit.sub_pos["Fertilizer"][i] = Fertilizer[i]
                            inputdata = Preparedata(args.file_path, IR_FER_ALL=False)
                            make_xbuild(inputdata=inputdata, output_path=args.file_cox)
                            harvest, _ = run_external_command("A", args.file_cox, run_data_path="../dssat_tool/")
                            logger.info("当前更新后状态日期:" + str(date_pairs))
                            logger.info("   当前更新后灌溉量：" + str(IRVAL))
                            logger.info("   当前更新后施肥量：" + str(Fertilizer))
                            logger.info("当前更新后最大产量:" + str(harvest))
                            envs_unit.sub_pos["Harvest"] = harvest
                            envs_unit.sub_pos["IRVAL"] = IRVAL
                            envs_unit.sub_pos["Fertilizer"] = Fertilizer
                            max_harvest_1 = harvest

                    elif max_harvest_0 == max_harvest and max_harvest > harvest:
                        for i in range(len(max_action_diss[:2])):
                            IRVAL_update(args.file_path, date_pairs[i], max_action_diss[:2][i])
                            Fertilier_update(args.file_path, date_pairs[i], max_action_diss[2:][i])
                            envs_unit.sub_pos["IRVAL"][i] = max_action_diss[:2][i]
                            envs_unit.sub_pos["Fertilizer"][i] = max_action_diss[2:][i]
                        inputdata = Preparedata(args.file_path, IR_FER_ALL=False)
                        make_xbuild(inputdata=inputdata, output_path=args.file_cox)
                        max_harvest, _ = run_external_command("A", args.file_cox, run_data_path="../dssat_tool/")
                        logger.info("当前更新后状态日期-无更新:" + str(date_pairs))
                        logger.info("   当前更新后灌溉量-无更新：" + str(max_action_diss[:2]))
                        logger.info("   当前更新后施肥量-无更新：" + str(max_action_diss[2:]))
                        logger.info("当前更新后最大产量-无更新:" + str(max_harvest))
                        envs_unit.sub_pos["Harvest"] = max_harvest
                        max_harvest_1 = max_harvest

                    else:
                        for i in range(len(IRVAL)):
                            IRVAL_update(args.file_path, date_pairs[i], IRVAL[i])
                            Fertilier_update(args.file_path, date_pairs[i], Fertilizer[i])
                            envs_unit.sub_pos["IRVAL"][i] = IRVAL[i]
                            envs_unit.sub_pos["Fertilizer"][i] = Fertilizer[i]
                        inputdata = Preparedata(args.file_path, IR_FER_ALL=False)
                        make_xbuild(inputdata=inputdata, output_path=args.file_cox)
                        harvest, _ = run_external_command("A", args.file_cox, run_data_path="../dssat_tool/")
                        envs_unit.sub_pos["Harvest"] = harvest
                        envs_unit.sub_pos["IRVAL"] = IRVAL
                        envs_unit.sub_pos["Fertilizer"]=Fertilizer
                        max_harvest_1 = harvest
                        logger.info("当前更新后状态日期:" + str(date_pairs))
                        logger.info("   当前更新后灌溉量：" + str(IRVAL))
                        logger.info("   当前更新后施肥量：" + str(Fertilizer))
                        logger.info("当前更新后最大产量:" + str(harvest))

                    state = envs_unit.update_unit(state)
                    logger.info(f"====================================================================={envs_unit.optimal_IRVAL}")
                    logger.info(f"====================================================================={envs_unit.optimal_Fertilizer}")
                    for j in range(len(envs_unit.optimal_IRVAL)):
                        IRAVL_optimal[j] = envs_unit.optimal_IRVAL[j]
                        Fert_optimal[j] = envs_unit.optimal_Fertilizer[j]
                        Irrial_IRVAL_inital[j] = envs_unit.optimal_IRVAL[j]
                        Fertilizer_fert_initial[j] = envs_unit.optimal_Fertilizer[j]
                    next_state = envs_unit.step(max_action_diss)
                    logger.info("当前大状态的iter是多少" + str(state["Iter"]))

                    if max_harvest_1 == harvest:
                        if np.sum(np.array(envs_unit.optimal_IRVAL)) > 537 or np.sum(np.array(envs_unit.optimal_Fertilizer))>250:
                            reward = -5370

                        # reward_total=envs.reward(reward,harvest,IRVAL_seq,time)
                        return_val = reward + RL_Agent_unit.gamma * (
                            0 if next_state["Iter"] == args.times // args.step_time else np.argmax(
                                RL_Agent_unit.value_q[next_state["Iter"], :]))
                        RL_Agent_unit.value_n[state_seq][action_seq_3] += 1
                        RL_Agent_unit.value_q[state_seq][action_seq_3] += (return_val - RL_Agent_unit.value_q[state_seq][
                            action_seq_3]) / \
                                                                     RL_Agent_unit.value_n[state_seq][action_seq_3]
                    elif max_harvest_1 == harvest_optimal:
                        if np.sum(np.array(envs_unit.optimal_IRVAL)) > 495 or np.sum(np.array(envs_unit.optimal_Fertilizer))>240:
                            reward = -5370
                            return_val = reward + RL_Agent_unit.gamma * (
                                0 if next_state["Iter"] == args.times // args.step_time else np.argmax(
                                    RL_Agent_unit.value_q[next_state["Iter"], :]))
                            RL_Agent_unit.value_n[state_seq][action_seq_3] += 1
                            RL_Agent_unit.value_q[state_seq][action_seq_3] += (return_val - RL_Agent_unit.value_q[state_seq][
                                action_seq_3]) / \
                                                                         RL_Agent_unit.value_n[state_seq][action_seq_3]
                        else:

                            # reward_total=envs.reward(max_harvest, max_harvest, IRVAL_seq, time)
                            return_val = 0 + RL_Agent_unit.gamma * (
                                0 if next_state["Iter"] == args.times // args.step_time else np.argmax(
                                    RL_Agent_unit.value_q[next_state["Iter"], :]))
                            RL_Agent_unit.value_n[state_seq][action_seq_3] += 1
                            RL_Agent_unit.value_q[state_seq][action_seq_3] += (return_val - RL_Agent_unit.value_q[state_seq][
                                action_seq_3]) / \
                                                                         RL_Agent_unit.value_n[state_seq][action_seq_3]
                    else:
                        if np.sum(np.array(envs_unit.optimal_IRVAL)) > 537 or np.sum(np.array(envs_unit.optimal_Fertilizer))>250:
                            max_harvest_1 = -5370
                        return_val = max_harvest_1 + RL_Agent_unit.gamma * (
                            0 if next_state["Iter"] == args.times // args.step_time else np.argmax(
                                RL_Agent_unit.value_q[next_state["Iter"], :]))
                        RL_Agent_unit.value_n[state_seq][action_seq_3] += 1
                        RL_Agent_unit.value_q[state_seq][action_seq_3] += (return_val - RL_Agent_unit.value_q[state_seq][
                            action_seq_3]) / \
                                                                     RL_Agent_unit.value_n[state_seq][action_seq_3]
                    state_seq = copy.deepcopy(next_state["Iter"])
                    state = next_state
                    stand += 1
                for op_IRVAL,op_Fert, date in zip(envs_unit.optimal_IRVAL,envs_unit.optimal_Fertilizer ,envs_unit.DAYS):
                    IRVAL_update(file_path=args.file_path, IRVAL=op_IRVAL, DAYS=date)
                    Fertilier_update(file_path=args.file_path, fertilier=op_Fert, DAYS=date)
                inputdata = Preparedata(args.file_path, IR_FER_ALL=False)
                make_xbuild(inputdata=inputdata, output_path=args.file_cox)
                final_Harvest, df_CroData = run_external_command("A", args.file_cox,
                                                                 run_data_path="../dssat_tool/")
                update_episode += 1
                logger.info(
                    f"初始灌溉施肥量：" + str(30) +"   "+str(45) + "当前轮数: " + str({update_episode}) + "   最佳灌溉量：" + str(
                        envs_unit.optimal_IRVAL)+"   最佳施肥量：" + str(
                        envs_unit.optimal_Fertilizer) + f"总的水量:{np.sum(np.array(envs_unit.optimal_IRVAL))}"
                    + f"总的肥量:{np.sum(np.array(envs_unit.optimal_Fertilizer))}"+"   最大产量：" + str(
                        final_Harvest))
                max_final_harvest.append(final_Harvest)
                max_final_action_0.append(copy.deepcopy(envs_unit.optimal_IRVAL))
                max_final_action_1.append(copy.deepcopy(envs_unit.optimal_Fertilizer))
                Irrial_IRVAL_seq.append(30)
                Irrial_Fertilizer_seq.append(45)

                optimal_IRVAL = np.array(envs_unit.optimal_IRVAL)
                optimal_Fertilizer = np.array(envs_unit.optimal_Fertilizer)
                optimal_IRVAL = np.sum(optimal_IRVAL)
                optimal_Fertilizer = np.sum(optimal_Fertilizer)
                tag = random.randint(0, 1)
                i = 1
                for op_IRVAL, op_Fert,date in zip(envs_unit.optimal_IRVAL, envs_unit.optimal_Fertilizer,envs_unit.DAYS):
                    
                    IRVAL_update(file_path=args.file_path, IRVAL=op_IRVAL, DAYS=date)
                    Fertilier_update(file_path=args.file_path, fertilier=op_Fert, DAYS=date)
                    Irrial_IRVAL_inital[i - 1] = op_IRVAL
                    Fertilizer_fert_initial[i - 1] = op_Fert
                    i+=1
                inputdata = Preparedata(args.file_path, IR_FER_ALL=False)
                make_xbuild(inputdata=inputdata, output_path=args.file_cox)

                logger.info(f"迭代初始施肥量：" + str(Irrial_IRVAL_inital) + "当前轮数: " + str({update_episode}))
            ret = policy_improve_unit(agent=RL_Agent_unit, final_harvest=final_Harvest, max_final_harvest=max_final_harvest,
                                 update_episode=update_episode)
            if not ret and update_episode > 2:
                break
    for IRVAL_seq, Fert_seq,HARVEST, ACTION_0,ACTION_1 in zip(Irrial_IRVAL_seq, Irrial_Fertilizer_seq,max_final_harvest, max_final_action_0,max_final_action_1,):
        logger.info("初始灌溉施肥量：" + str(IRVAL_seq)+"  "+str(Fert_seq) + "最终收获量：" + str(
            HARVEST) + f"   总水量： {np.sum(np.array(ACTION_0))}" + "   最佳灌溉量：" + str(ACTION_0)+ f"   总肥量： {np.sum(np.array(ACTION_1))}" + "   最佳施肥量：" + str(ACTION_1))



