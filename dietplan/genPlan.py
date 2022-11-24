import json
import psycopg2
from dietplan import rf

print("************In the genPlan script.")

def generate(user_id, user_BMR, user_calorieintake):
    print("**************In genPlan.generate() calling rf.py")
    data = rf.classify(user_calorieintake)
    try:
        conn = psycopg2.connect("dbname='virtualdietitian' user='postgres' host='localhost' password='password'")
        print("************connected to postgres db")
    except:
        print ("************I am unable to connect to the postgres database")
    cur = conn.cursor()
    #print(data)

    dp = json.dumps(data)
    execstr = "UPDATE dietplan_userdetails SET \"dietPlan\" = \'"+dp+"\' WHERE user_id = "+str(user_id)
    #print(execstr)
    cur.execute(execstr)
    # ans = cur.fetchall()
    # print(ans)
    print("************commiting dietplan to postgres database ... ")
    try:
        conn.commit()
        print("************Commited dietplan")
    except:
        print("************didn't commit")

    #adding BMR to db
    execstr = "UPDATE dietplan_userdetails SET \"BMR\" = " + str(user_BMR) + " WHERE user_id = " + str(user_id)
    cur.execute(execstr)
    try:
        conn.commit()
        print("************Commited BMR")
    except:
        print("************didn't commit BMR")

    #Adding Calorie intake to db
    execstr = "UPDATE dietplan_userdetails SET \"calorieintake\" = " + str(user_calorieintake) + " WHERE user_id = " + str(user_id)
    cur.execute(execstr)
    try:
        conn.commit()
        print("************Commited calorieintake")
    except:
        print("************didn't commit Calorie Intake")
    conn.close()
# data = {'Breakfast': {
#                         'Plan1': {
#                                 'breakfast1': 'Orange', 'breakfast1Weight': 393,
#                                 'breakfast2': 'Egg White', 'breakfast2Weight': 726
#                                 },
#                         'Plan2': {
#                                 'breakfast1': 'Butter', 'breakfast1Weight': 30,
#                                 'breakfast2': 'Egg White', 'breakfast2Weight': 726
#                                 },
#                         'Plan3': {
#                                 'breakfast1': 'Apple', 'breakfast1Weight': 414,
#                                 'breakfast2': 'Egg White', 'breakfast2Weight': 726
#                                 }},
#         'Lunch': {
#                 'Plan1': {
#                         'veggies':'Mackerel', 'weight': 100,
#                         'Roti': 'Roti', 'rotiQuantity': 3},
#                 'Plan2': {'veggies': 'Paneer', 'weight': 100,
#                         'Roti': 'Roti', 'rotiQuantity': 3},
#                 'Plan3': {'veggies': 'Salmon', 'weight': 113,
#                         'Roti': 'Roti', 'rotiQuantity': 3}},
#         'PreWorkout': {
#                     'Plan1': {
#                             'preworkout': 'Peanuts', 'weight': 37},
#                     'Plan2': {'preworkout': 'Almonds', 'weight': 36},
#                     'Plan3': {'preworkout': 'Peanut Butter', 'weight': 32}},
#         'PostWorkout': {
#                     'Plan1': {
#                             'postworkout1': 'Soy patty', 'postworkout1Weight': 210,
#                             'postworkout2': 'Boiled Egg', 'postworkout2Weight': 200},
#                     'Plan2': {'postworkout1': 'Soy patty', 'postworkout1Weight': 210,
#                                 'postworkout2': 'Processed Milk', 'postworkout2Weight': 777},
#                     'Plan3': {'postworkout1': 'Soy patty', 'postworkout1Weight': 210,
#                                 'postworkout2': 'Egg White', 'postworkout2Weight': 594}},
#         'Dinner': {
#                     'Plan1': {'veggies': 'Brocolli', 'weight': 322,
#                                 'Roti': 'Roti', 'rotiQuantity': 3,
#                                 'Rice': 'Rice', 'riceQuantity': 7},
#                     'Plan2': {'veggies': 'Paneer', 'weight': 100,
#                                 'Roti': 'Roti', 'rotiQuantity': 3,
#                                 'Rice': 'Rice', 'riceQuantity': 14},
#                     'Plan3': {'veggies': 'Chicken Breast', 'weight': 100,
#                                 'Roti': 'Roti', 'rotiQuantity': 3, 'Rice': 'Rice', 'riceQuantity': 21}}
#     }
