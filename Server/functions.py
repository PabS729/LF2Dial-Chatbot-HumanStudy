
from respond_role import *
from prompts_toulmin import * 
from prompt_fsm_experimental import * 
from Intent_prompts import *
from random import random
states = []
disagr_bank = []
agr_bank = []

model_teacher = "gpt-4o"
model_student = "gpt-4o"
model_agent = "gpt-4o-mini"
# example_sentence = "I mean, whether we like it or not, and we could be very politically correct, but whether we like it or not, there is a problem. And we have to be sure that Muslims come in and report when they see something going on. When they see hatred going on, they have to report it. As an example, in San Bernardino, many people saw the bombs all over the apartment of the two people that killed 14 and wounded many, many people."
# example_sentence = "And I’ll be a president that will turn our inner cities around and will give strength to people and will give economics to people and will bring jobs back. Because NAFTA, signed by her husband, is perhaps the greatest disaster trade deal in the history of the world. Not in this country."
example_sentence = "Al Gore and I are committed to continuing this acquisition program, transforming the military. There's still fewer people in uniform today, but person - to - person, person - by - person, unit - by - unit, this is the most powerful and effective military, not only in the world today, but in the history of the world. And again, Al Gore and I will do whatever is necessary to keep it that way."
# chat_history = ""
count_states = {"1":0,"2":0,"3":0,"4":0,"5":0}
FSM_STATES = ["3"]


#first round where the teacher starts. Decomposing using toulmin's model, then pointing out LF
def opening():
    teacher_res = generate_res("teacher", model_teacher, example_sentence, None, None, None, [], [], OPENING_PROMPT, 0)
            # teacher_res = await generate_res("teacher", model_teacher, example_sentence, None, None, None, conv_teacher, conv_student, PROMPT_TEACHER_ARGUE_DS, 0)
            # teacher_res = await generate_res("teacher", model_teacher, example_sentence, None, None, None, conv_teacher, conv_student, PROMPT_TEACHER_ARGUE_BASELINE, 0)
    teacher_res = teacher_res.choices[0].message.content

    utterance_teacher = teacher_res
    print(utterance_teacher)
    return utterance_teacher

#check if student response is relevant/has already mentioned examples, and redirect to dedicated outputs
def check_student_response(chat_history):
    thought = 0
    relevance_res = generate_res("check", model_agent, example_sentence, disagr_bank, 
                                                               chat_history, agr_bank, None, None, PROMPT_CHECK_RELEVANCE_AGENT, 0)
    relevance = load_json(relevance_res.choices[0].message.content)
    while relevance == False:
        relevance_res = generate_res("check", model_agent, example_sentence, disagr_bank, 
                                                               chat_history, agr_bank, None, None, PROMPT_CHECK_RELEVANCE_AGENT, 0)
        relevance = load_json(relevance_res.choices[0].message.content)

    print("relevance check: ", relevance)

    if "yes" not in relevance["Q1"].lower():
        thought = 6
    elif "yes" in relevance["Q4"]:
        thought = 7
    elif "yes" not in relevance["Q2"].lower(): 
        disagr_bank.append(relevance["Q1"])


    elif "yes" not in relevance["Q4"] and "yes" in relevance["Q5"]:
        disagr_bank.append(relevance["Q5"])
                                # thought = 7
                            
    elif "yes" in relevance["Q3"].lower(): 
        thought = 7
    else:
        thought = 2
    return thought, relevance

#respond to the student with FSM
def FSM_response(chat_history, conv_teacher, conv_student):
    transition = generate_res("agent", model_teacher, example_sentence, chat_history, None, None, None, None, CHECK_RESPONSE_TEACHER, 1)
    transition = load_json(transition.choices[0].message.content)
    while transition == False:
        transition = generate_res("agent", model_teacher, example_sentence, chat_history, None, None, None, None, CHECK_RESPONSE_TEACHER, 1)
        transition = load_json(transition.choices[0].message.content)
                        
    print("transition: ", transition)
    #In terms of precedence: request >> assumption (completeness) > examples (evidence) >= logical flaw (attacking point)
    if "yes" in transition["3"].lower():
        next_state = "3"
    # elif 'yes' not in cs['2'].lower():
    #     next_state = '2'
                        # else: 
                        #     tmp = []
                        #     for k in STS:
                        #         if "yes" in transition[k]:
                        #             tmp.append(k)
                        #     if len(tmp) != 0:
                        #         rds = random.randint(1,len(tmp)) 
                        #         next_state = tmp[rds - 1]
                        #     else:
                        #         next_state = "2"
    elif "yes" in transition["1"].lower():
        next_state = "1"

    elif "yes" in transition["4"].lower():
        next_state = "4"

    else:
        next_state = "2"

    count_states[next_state] += 1
    tmp_s = next_state
    print(count_states)
    print("before random generation: " + next_state)

    # if len(FSM_STATES) >= 3 and FSM_STATES[-2] == FSM_STATES[-1] and FSM_STATES[-1] == next_state and next_state != "3":
    #     new_sts = [i for i in STS if(i != next_state or i != "3") ]
    #                         # print("new states: " + new_sts)
    #     rds = random.randint(0,1)   
    #     next_state = new_sts[rds]
    #     count_states[next_state] += 1
    #     count_states[tmp_s] -= 1

    if "yes" in transition["1"].lower() and count_states["1"] >= count_states["4"] * 2 and count_states["4"] >= 0 and next_state != "3":
        next_state = "4"
        count_states[next_state] += 1
        count_states[tmp_s] -= 1
        if count_states["1"] >= count_states["2"] * 3 or count_states["4"] >= count_states["2"] * 2:
            next_state = "2"
            count_states[next_state] += 1
            count_states['4'] -= 1

                        # if next_state in ["1", "4"]:
                        #     res_T = await generate_res("sf", model_teacher, example_sentence, conv_student[-1], None, None, None, None, PRECONDITION, 1)
                        #     RES_T = res_T.choices[0].message.content
                        #     print("thought:", RES_T)
                        # if "no" in following[-1].lower() and "no" in following[-2].lower():
                        #     next_state = "2"
                        #     count_states[next_state] += 1
                        #     count_states[tmp_s] -= 1
                        
    # if next_state != curr_state:
    #     print("-----------------transitioning--------------------" + "from " + curr_state + " to " + next_state)
    print("next state is: "+ next_state)
                        # if "yes" in transition["5"].lower():
                        #     utterance_teacher = "It seems that you have not responded to my previous request. Would you please answer my question first, before proposing further arguments or requests?"
                        # else:
    teacher_res = generate_res("teacher", model_teacher, example_sentence, None, None, None, conv_teacher, conv_student, TEACHER_ACT_1 + STRAT_FOR_STATES_R[next_state] + TEACHER_ACT_2, 1)
                        
    FSM_STATES.append(next_state)

    check_following_res = generate_res("eval_s", model_student, example_sentence, teacher_res.choices[0].message.content, STRAT_FOR_STATES_R[next_state], None, None, None, CHECK_FOLLOW_FSM_AGENT, 0)
    cs = load_json(check_following_res.choices[0].message.content)
    while cs == False:
        check_following_res = generate_res("eval_s", model_student, example_sentence, teacher_res.choices[0].message.content, STRAT_FOR_STATES_R[next_state], None, None, None, CHECK_FOLLOW_FSM_AGENT, 0)
        cs = load_json(check_following_res.choices[0].message.content)
    print("is the teacher following the transition? " + cs['1'])
    print("is the teacher's question relevant? " + cs['2'])
                        
                        #rephrase the teacher's response, if we found that it is not following the expected state.
                        
    if ("no" in cs['1'].lower() or "no" in cs['2'].lower()) and next_state in ['1', '4', '2']:
        if next_state in ['1', '4']:
            pt = TEACHER_ACT_EX_AS
        else:
            pt = TEACHER_ACT_REFUTE
        teacher_res = generate_res("agents", model_teacher, example_sentence, teacher_res.choices[0].message.content, None, None, None, None, TEACHER_ACT_1 + STRAT_FOR_STATES_R[next_state] + pt, 1)
        check_following_res = generate_res("eval_s", model_student, example_sentence, teacher_res.choices[0].message.content, STRAT_FOR_STATES_R[next_state], None, None, None, CHECK_FOLLOW_FSM_AGENT, 0)
        cs = load_json(check_following_res.choices[0].message.content)
        while cs == False:
            check_following_res = generate_res("eval_s", model_student, example_sentence, teacher_res.choices[0].message.content, STRAT_FOR_STATES_R[next_state], None, None, None, CHECK_FOLLOW_FSM_AGENT, 0)
            cs = load_json(check_following_res.choices[0].message.content)
        print("is the teacher following the transition after rephrasing? " + cs['1'])
        print("is the teacher's question relevant after rephrasing? " + cs['2'])
    teacher_res = teacher_res.choices[0].message.content         
    return teacher_res

#respond to the student with predefined strategy
def predefined_response(thought, next_state, conv_teacher, relevance):
    if thought == 7:
        print("student response is already discussed ------------ ")

                        #teacher's response when the student is repeating topics that has been previously discussed
        if next_state in ["1", "4"]:
            teacher_res = generate_res("test", model_teacher, example_sentence, relevance["Q5"], conv_teacher[-1], None, [], None, PROMPT_RESTATE, 0)
        else:
            teacher_res = generate_res("cov", model_teacher, example_sentence, relevance["Q5"], None, None, [], None, PROMPT_REMIND_FOCUSED, 0)
                        
    else:
        print("student response is irrelevant ------------ ")
        teacher_res = generate_res("cov", model_teacher, example_sentence, relevance["Q1"], None, None, [], None, PROMPT_REMIND_RELEVANCE, 0)
    teacher_res = teacher_res.choices[0].message.content
    return teacher_res

#Done After the student's response.

def response_baseline(conv_teacher, conv_student):
    teacher_res = generate_res("tea", model_teacher, example_sentence, None, None, None, conv_teacher, conv_student, PROMPT_TEACHER_ARGUE_BASELINE, 0)
    teacher_res = teacher_res.choices[0].message.content
    return teacher_res

#check student agreement
async def check_agreement():
    return


