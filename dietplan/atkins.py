import sqlite3
from sqlite3 import Error
from random import *
import os

print("************In atkins.py")

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return None

def Diff(li1, li2):
    return (list(set(li1) - set(li2)))

def atkinsphase1(conn, min_cal, max_cal, pref, med_hist):
    """
    Atkins Diet (suitable for weight loss)
    meals: stores all the meals
    meal_type: key in the meals to get the meals of Dinner, ...
    """
    #initialisation of the dictionaries to store the meals
    meals = {}
    meals['Lunch']={}
    meals['BreakfastorSnacks']={}
    meals['Dinner'] = {}
    meals['Snacks'] = {}
    ######################################################
    #print("Ketogenic Diet")
    diet_name = "Atkins Diet Phase 1"
    print("Atkins Diet Phase 1")
    print("Food Item   Quantity  Calories  Proteins  Carbs  Fats")
    nonveg = ['Salmon','Mackerel','Chicken','Chicken Breast','Indian Chicken','Egg Bhurji','Egg White','Boiled Egg','Egg Fried','Omelet']
    eggveg = ['Salmon','Mackerel','Chicken','Chicken Breast','Indian Chicken']
    cholesterol = ['Butter','Cheese Slices','Processed Milk','Yoghurt','Boiled Egg','Egg Fried','Omelet','Egg Bhurji']
    diabetes = ['Peanut Butter','Peanut Butter Sandwich','Cereal','Apple Juice','Orange Juice','Pineapple Juice','Fruit Salad','Banana']
    hypothyroidism = ['Brocolli','Cauliflower','Cabbage','Corn','Soy Patty','Soybeans','Paneer','Butter','Beans','Legumes','Peanut Butter','Peanut Butter Sandwich','Spinach (Boiled)','Sweet Potato']

    totalcal = [0,0,0]

    """ Breakfast/ Snacks """
    print ('\nBreakfast or Snacks')
    meal_type = 'BreakfastorSnacks'
    breakfast1 = ['Processed Milk',
			'Buttermilk',
			'Yoghurt'
			]
    breakfast2 = ['Egg White',
                'Boiled Egg',
                'Egg Fried',
                'Omelet',
                'Oatmeal',
                'Cheese Slices',
                'Butter',
                'Cereal',
                'Veg Patty',
                'Soy patty']
    if pref == 1:
        breakfast2 = Diff(breakfast2, nonveg)
    if pref == 2:
        breakfast2 = Diff(breakfast2, eggveg)
    if med_hist == 1:
        breakfast2 = Diff(breakfast2, cholesterol)
        breakfast1 = Diff(breakfast1, cholesterol)
    if med_hist == 2:
        breakfast2 = Diff(breakfast2, diabetes)
        breakfast1 = Diff(breakfast1, diabetes)
    if med_hist == 3:
        breakfast2 = Diff(breakfast2, hypothyroidism)
        breakfast1 = Diff(breakfast1, hypothyroidism)
    cur = conn.cursor()
    i=1
    while i<4:
        print ("\nPlan ",i)
        planno = 'plan'+str(i)
        quantity1 = 0;
        quantity2 = 0;
        weight1 = 0
        cal1=0
        protein1=0
        carb1=0
        fat1=0
        bf1 = breakfast1[randint(0, len(breakfast1)-1)]
        while cal1 <= min_cal*1/10:
            cur.execute("SELECT weight FROM food where name =?", (bf1,))
            rows1 = cur.fetchall()
            for row1 in rows1:
                weight1 = weight1 + int(row1[0])
            cur.execute("SELECT cal FROM food where name =?", (bf1,))
            rows2 = cur.fetchall()
            for row2 in rows2:
                cal1 = cal1 + int(row2[0])
                totalcal[i-1] = totalcal[i-1] + cal1
            cur.execute("SELECT protein FROM food where name =?", (bf1,))
            rows3 = cur.fetchall()
            for row3 in rows3:
                protein1 = protein1 + int(row3[0])
            cur.execute("SELECT carb FROM food where name =?", (bf1,))
            rows4 = cur.fetchall()
            for row4 in rows4:
                carb1 = carb1 + int(row4[0])
            cur.execute("SELECT fat FROM food where name =?", (bf1,))
            rows5 = cur.fetchall()
            for row5 in rows5:
                fat1 = fat1 + int(row5[0])
            quantity1 = quantity1 + 1

        cal2=0
        weight2 = 0
        protein2=0
        carb2=0
        fat2=0
        bf2 = breakfast2[randint(0, len(breakfast2)-1)]
        while cal2 <= min_cal*1/10:
            cur.execute("SELECT weight FROM food where name =?", (bf2,))
            rows3 = cur.fetchall()
            for row3 in rows3:
                weight2 = weight2 + int(row3[0])
            cur.execute("SELECT cal FROM food where name =?", (bf2,))
            rows4 = cur.fetchall()
            for row4 in rows4:
                cal2 = cal2 + int(row4[0])
                totalcal[i-1] = totalcal[i-1] + cal2
            cur.execute("SELECT protein FROM food where name =?", (bf2,))
            rows3 = cur.fetchall()
            for row3 in rows3:
                protein2 = protein2 + int(row3[0])
            cur.execute("SELECT carb FROM food where name =?", (bf2,))
            rows4 = cur.fetchall()
            for row4 in rows4:
                carb2 = carb2 + int(row4[0])
            cur.execute("SELECT fat FROM food where name =?", (bf2,))
            rows5 = cur.fetchall()
            for row5 in rows5:
                fat2 = fat2 + int(row5[0])
            quantity2 = quantity2 + 1

        meals[meal_type][planno] = {"item1":bf1,"item1Quantity":weight1,
                                    "item1Cals":cal1,"item1Proteins":protein1,
                                    "item1Carbs":carb1,"item1Fats":fat1,
                                    "item2":bf2,"item2Quantity":weight2,
                                    "item2Cals":cal2,"item2Proteins":protein2,
                                    "item2Carbs":carb2,"item2Fats":fat2}
        print (bf1," x ",weight1,"g  ",cal1,"kcal  ",protein1,"g  ",carb1,"g  ",fat1,"g")
        print (bf2," x ",weight2,"g  ",cal2,"kcal  ",protein2,"g  ",carb2,"g  ",fat2,"g")
        i=i+1

    """ Lunch """
    print ('\nLunch')
    meal_type = 'Lunch'
    lunch = ['Spinach (Boiled)',
			'Brocolli',
			'Cauliflower',
			'Lettuce',
			'Cabbage',
			'Green Peas',
			'Soybeans',
			'Paneer',
			'Vegetables',
			'Salmon',
			'Mackerel',
			'Chicken',
			'Chicken Breast',
			'Indian Chicken'
			]
    if pref == 1:
        lunch = Diff(lunch, nonveg)
    if pref == 2:
        lunch = Diff(lunch, eggveg)
    if med_hist == 1:
        lunch = Diff(lunch, cholesterol)
    if med_hist == 2:
        lunch = Diff(lunch, diabetes)
    if med_hist == 3:
        lunch = Diff(lunch, hypothyroidism)
    cur = conn.cursor()
    i=1
    while i<4:
        print ("\nPlan ",i)
        planno = 'plan'+str(i)
        quantity1 = 0;
        quantity2 = 0;
        quantity3 = 0;
        weight = 0
        cal1=0
        protein1=0
        carb1=0
        fat1=0
        veggies = lunch[randint(0, len(lunch)-1)]
        while cal1 <= min_cal*0.5/10:
            """Veggies"""
            cur.execute("SELECT weight FROM food where name =?", (veggies,))
            rows1 = cur.fetchall()
            for row1 in rows1:
                weight = weight + int(row1[0])
            cur.execute("SELECT cal FROM food where name =?", (veggies,))
            rows2 = cur.fetchall()
            for row2 in rows2:
                cal1 = cal1 + int(row2[0])
                totalcal[i-1] = totalcal[i-1] + cal1
            cur.execute("SELECT protein FROM food where name =?", (veggies,))
            rows3 = cur.fetchall()
            for row3 in rows3:
                protein1 = protein1 + int(row3[0])
            cur.execute("SELECT carb FROM food where name =?", (veggies,))
            rows4 = cur.fetchall()
            for row4 in rows4:
                carb1 = carb1 + int(row4[0])
            cur.execute("SELECT fat FROM food where name =?", (veggies,))
            rows5 = cur.fetchall()
            for row5 in rows5:
                fat1 = fat1 + int(row5[0])
            quantity1 = quantity1 + 1

        cal2=0
        protein2=0
        carb2=0
        fat2=0
        while cal2 <= min_cal*2/10:
            """Roti"""
            cur.execute("SELECT * FROM food where name = 'Roti'")
            rows1 = cur.fetchall()
            #for row3 in rows3:
                #print(row3)
            cur.execute("SELECT cal FROM food where name = 'Roti'")
            rows2 = cur.fetchall()
            for row2 in rows2:
                cal2 = cal2 + int(row2[0])
                totalcal[i-1] = totalcal[i-1] + cal2
            cur.execute("SELECT cal FROM food where name = 'Roti'")
            rows3 = cur.fetchall()
            for row3 in rows3:
                protein2 = protein2 + int(row3[0])
            cur.execute("SELECT cal FROM food where name = 'Roti'")
            rows4 = cur.fetchall()
            for row4 in rows4:
                carb2 = carb2 + int(row4[0])
            cur.execute("SELECT cal FROM food where name = 'Roti'")
            rows5 = cur.fetchall()
            for row5 in rows5:
                fat2 = fat2 + int(row5[0])
            quantity2 = quantity2 + 1

        meals[meal_type][planno] = {"item1":veggies,"item1Quantity":weight,
                                    "item1Cals":cal1,"item1Proteins":protein1,
                                    "item1Carbs":carb1,"item1Fats":fat1,
                                    "item2":'Roti',"item2Quantity":quantity2,
                                    "item2Cals":cal2,"item2Proteins":protein2,
                                    "item2Carbs":carb2,"item2Fats":fat2}
        print (veggies," x ",weight,"g  ",cal1,"kcal  ",protein1,"g  ",carb1,"g  ",fat1,"g")
        print ("Roti x",quantity2,"  ",cal2,"kcal  ",protein2,"g  ",carb2,"g  ",fat2,"g")
        #print "Rice x",quantity3,"g"
        i=i+1

    """ Dinner """
    print ('\nDinner')
    meal_type = 'Dinner'
    dinner = ['Spinach (Boiled)',
			'Brocolli',
			'Cauliflower',
			'Lettuce',
			'Cabbage',
			'Vegetables',
			'Salmon',
			'Mackerel',
			'Chicken',
			'Chicken Breast',
			'Indian Chicken',
			'Egg Bhurji',
			'Green Peas',
			'Soybeans',
			'Paneer'
			]
    if pref == 1:
        dinner = Diff(dinner, nonveg)
    if pref == 2:
        dinner = Diff(dinner, eggveg)
    if med_hist == 1:
        dinner = Diff(dinner, cholesterol)
    if med_hist == 2:
        dinner = Diff(diner, diabetes)
    if med_hist == 3:
        dinner = Diff(dinner, hypothyroidism)
    cur = conn.cursor()
    i=1
    while i<4:
        print ("\nPlan ",i)
        planno = 'plan'+str(i)
        quantity1 = 0;
        quantity2 = 0;
        weight = 0
        cal=0
        veggies = dinner[randint(0, len(dinner)-1)]
        while cal1 <= min_cal*0.5/10:
            """Veggies"""
            cur.execute("SELECT weight FROM food where name =?", (veggies,))
            rows1 = cur.fetchall()
            for row1 in rows1:
                weight = weight + int(row1[0])
            cur.execute("SELECT cal FROM food where name =?", (veggies,))
            rows2 = cur.fetchall()
            for row2 in rows2:
                cal1 = cal1 + int(row2[0])
                totalcal[i-1] = totalcal[i-1] + cal1
            cur.execute("SELECT protein FROM food where name =?", (veggies,))
            rows3 = cur.fetchall()
            for row3 in rows3:
                protein1 = protein1 + int(row3[0])
            cur.execute("SELECT carb FROM food where name =?", (veggies,))
            rows4 = cur.fetchall()
            for row4 in rows4:
                carb1 = carb1 + int(row4[0])
            cur.execute("SELECT fat FROM food where name =?", (veggies,))
            rows5 = cur.fetchall()
            for row5 in rows5:
                fat1 = fat1 + int(row5[0])
            quantity1 = quantity1 + 1

        cal2=0
        while cal2 <= min_cal*2/10:
            """Roti"""
            cur.execute("SELECT * FROM food where name = 'Roti'")
            rows1 = cur.fetchall()
            #for row3 in rows3:
                #print(row3)
            cur.execute("SELECT cal FROM food where name = 'Roti'")
            rows2 = cur.fetchall()
            for row2 in rows2:
                cal2 = cal2 + int(row2[0])
                totalcal[i-1] = totalcal[i-1] + cal2
            cur.execute("SELECT cal FROM food where name = 'Roti'")
            rows3 = cur.fetchall()
            for row3 in rows3:
                protein2 = protein2 + int(row3[0])
            cur.execute("SELECT cal FROM food where name = 'Roti'")
            rows4 = cur.fetchall()
            for row4 in rows4:
                carb2 = carb2 + int(row4[0])
            cur.execute("SELECT cal FROM food where name = 'Roti'")
            rows5 = cur.fetchall()
            for row5 in rows5:
                fat2 = fat2 + int(row5[0])
            quantity2 = quantity2 + 1

        meals[meal_type][planno] = {"item1":veggies,"item1Quantity":weight,
                                    "item1Cals":cal1,"item1Proteins":protein1,
                                    "item1Carbs":carb1,"item1Fats":fat1,
                                    "item2":'Roti',"item2Quantity":quantity2,
                                    "item2Cals":cal2,"item2Proteins":protein2,
                                    "item2Carbs":carb2,"item2Fats":fat2}
        print (veggies," x ",weight,"g  ",cal1,"kcal  ",protein1,"g  ",carb1,"g  ",fat1,"g")
        print ("Roti x",quantity2,"  ",cal2,"kcal  ",protein2,"g  ",carb2,"g  ",fat2,"g")
        #print "Rice x",quantity3,"g"
        i=i+1
    #print "Total Cal Plan 1 = ",totalcal[0]
    #print "Total Cal Plan 2 = ",totalcal[1]
    #print "Total Cal Plan 3 = ",totalcal[2]
    print(meals)
    return meals

def atkinsphase2(conn, min_cal, max_cal, pref, med_hist):
    """
    Atkins Diet (suitable for weight loss)
    """
    print("Atkins Diet Phase 2")
    diet_name = 'Atkins Diet Phase 2'
    print("Food Item   Quantity  Calories  Proteins  Carbs  Fats")
    nonveg = ['Salmon',
			'Mackerel',
			'Chicken',
			'Chicken Breast',
			'Indian Chicken',
			'Egg Bhurji',
			'Egg White',
			'Boiled Egg',
			'Egg Fried',
			'Omelet'
			]
    eggveg = ['Salmon',
			'Mackerel',
			'Chicken',
			'Chicken Breast',
			'Indian Chicken'
			]
    cholesterol = ['Butter',
			'Cheese Slices',
			'Processed Milk',
			'Yoghurt',
			'Boiled Egg',
			'Egg Fried',
			'Omelet',
			'Egg Bhurji'
			]
    diabetes = ['Peanut Butter',
			'Peanut Butter Sandwich',
			'Cereal',
			'Apple Juice',
			'Orange Juice',
			'Pineapple Juice',
			'Fruit Salad',
			'Banana'
			]
    hypothyroidism = ['Brocolli',
			'Cauliflower',
			'Cabbage',
			'Corn',
			'Soy Patty',
			'Soybeans',
			'Paneer',
			'Butter',
			'Beans',
			'Legumes',
			'Peanut Butter',
			'Peanut Butter Sandwich',
			'Spinach (Boiled)',
			'Sweet Potato'
			]
    totalcal = [0,0,0]

    """ Breakfast/ Snacks """
    print ('\nBreakfast or Snacks')
    meal_type = 'BreakfastorSnacks'
    breakfast1 = ['Processed Milk',
			'Buttermilk',
			'Yoghurt'
			]
    breakfast2 = ['Egg White',
                'Boiled Egg',
                'Egg Fried',
                'Omelet',
                'Oatmeal',
                'Cheese Slices',
                'Butter',
                'Cereal',
                'Veg Patty'
                ]
    if pref == 1:
        breakfast2 = Diff(breakfast2, nonveg)
    if pref == 2:
        breakfast2 = Diff(breakfast2, eggveg)
    if med_hist == 1:
        breakfast2 = Diff(breakfast2, cholesterol)
        breakfast1 = Diff(breakfast1, cholesterol)
    if med_hist == 2:
        breakfast2 = Diff(breakfast2, diabetes)
        breakfast1 = Diff(breakfast1, diabetes)
    if med_hist == 3:
        breakfast2 = Diff(breakfast2, hypothyroidism)
        breakfast1 = Diff(breakfast1, hypothyroidism)
    cur = conn.cursor()
    i=1
    while i<4:
        print ("\nPlan ",i)
        planno = 'plan'+str(i)
        quantity1 = 0;
        quantity2 = 0;
        weight1 = 0
        cal1=0
        protein1=0
        carb1=0
        fat1=0
        bf1 = breakfast1[randint(0, len(breakfast1)-1)]
        while cal1 <= min_cal*1/10:
            cur.execute("SELECT weight FROM food where name =?", (bf1,))
            rows1 = cur.fetchall()
            for row1 in rows1:
                weight1 = weight1 + int(row1[0])
            cur.execute("SELECT cal FROM food where name =?", (bf1,))
            rows2 = cur.fetchall()
            for row2 in rows2:
                cal1 = cal1 + int(row2[0])
                totalcal[i-1] = totalcal[i-1] + cal1
            cur.execute("SELECT protein FROM food where name =?", (bf1,))
            rows3 = cur.fetchall()
            for row3 in rows3:
                protein1 = protein1 + int(row3[0])
            cur.execute("SELECT carb FROM food where name =?", (bf1,))
            rows4 = cur.fetchall()
            for row4 in rows4:
                carb1 = carb1 + int(row4[0])
            cur.execute("SELECT fat FROM food where name =?", (bf1,))
            rows5 = cur.fetchall()
            for row5 in rows5:
                fat1 = fat1 + int(row5[0])
            quantity1 = quantity1 + 1

        cal2=0
        weight2 = 0
        protein2=0
        carb2=0
        fat2=0
        bf2 = breakfast2[randint(0, len(breakfast2)-1)]
        while cal2 <= min_cal*1/10:
            cur.execute("SELECT weight FROM food where name =?", (bf2,))
            rows3 = cur.fetchall()
            for row3 in rows3:
                weight2 = weight2 + int(row3[0])
            cur.execute("SELECT cal FROM food where name =?", (bf2,))
            rows4 = cur.fetchall()
            for row4 in rows4:
                cal2 = cal2 + int(row4[0])
                totalcal[i-1] = totalcal[i-1] + cal2
            cur.execute("SELECT protein FROM food where name =?", (bf2,))
            rows3 = cur.fetchall()
            for row3 in rows3:
                protein2 = protein2 + int(row3[0])
            cur.execute("SELECT carb FROM food where name =?", (bf2,))
            rows4 = cur.fetchall()
            for row4 in rows4:
                carb2 = carb2 + int(row4[0])
            cur.execute("SELECT fat FROM food where name =?", (bf2,))
            rows5 = cur.fetchall()
            for row5 in rows5:
                fat2 = fat2 + int(row5[0])
            quantity2 = quantity2 + 1

        meals[meal_type][planno] = {"item1":bf1,"item1Quantity":weight1,
                                    "item1Cals":cal1,"item1Proteins":protein1,
                                    "item1Carbs":carb1,"item1Fats":fat1,
                                    "item2":bf2,"item2Quantity":weight2,
                                    "item2Cals":cal2,"item2Proteins":protein2,
                                    "item2Carbs":carb2,"item2Fats":fat2}
        print (bf1," x ",weight1,"g  ",cal1,"kcal  ",protein1,"g  ",carb1,"g  ",fat1,"g")
        print (bf2," x ",weight2,"g  ",cal2,"kcal  ",protein2,"g  ",carb2,"g  ",fat2,"g")
        i=i+1

    """ Lunch """
    print ('\nLunch')
    meal_type = 'Lunch'
    lunch = ['Spinach (Boiled)',
			'Brocolli',
			'Cauliflower',
			'Lettuce',
			'Cabbage',
			'Green Peas',
			'Soybeans',
			'Paneer',
			'Vegetables',
			'Salmon',
			'Mackerel',
			'Chicken',
			'Chicken Breast',
			'Indian Chicken'
			]
    if pref == 1:
        lunch = Diff(lunch, nonveg)
    if pref == 2:
        lunch = Diff(lunch, eggveg)
    if med_hist == 1:
        lunch = Diff(lunch, cholesterol)
    if med_hist == 2:
        lunch = Diff(lunch, diabetes)
    if med_hist == 3:
        lunch = Diff(lunch, hypothyroidism)
    cur = conn.cursor()
    i=1
    while i<4:
        print ("\nPlan ",i)
        planno = 'plan'+str(i)
        quantity1 = 0;
        quantity2 = 0;
        quantity3 = 0;
        weight = 0
        cal1=0
        veggies = lunch[randint(0, len(lunch)-1)]
        while cal1 <= min_cal*0.5/10:
            """Veggies"""
            cur.execute("SELECT weight FROM food where name =?", (veggies,))
            rows1 = cur.fetchall()
            for row1 in rows1:
                weight = weight + int(row1[0])
            cur.execute("SELECT cal FROM food where name =?", (veggies,))
            rows2 = cur.fetchall()
            for row2 in rows2:
                cal1 = cal1 + int(row2[0])
                totalcal[i-1] = totalcal[i-1] + cal1
            cur.execute("SELECT protein FROM food where name =?", (veggies,))
            rows3 = cur.fetchall()
            for row3 in rows3:
                protein1 = protein1 + int(row3[0])
            cur.execute("SELECT carb FROM food where name =?", (veggies,))
            rows4 = cur.fetchall()
            for row4 in rows4:
                carb1 = carb1 + int(row4[0])
            cur.execute("SELECT fat FROM food where name =?", (veggies,))
            rows5 = cur.fetchall()
            for row5 in rows5:
                fat1 = fat1 + int(row5[0])
            quantity1 = quantity1 + 1

        cal2=0
        while cal2 <= min_cal*1.5/10:
            """Roti"""
            cur.execute("SELECT * FROM food where name = 'Roti'")
            rows1 = cur.fetchall()
            #for row3 in rows3:
                #print(row3)
            cur.execute("SELECT cal FROM food where name = 'Roti'")
            rows2 = cur.fetchall()
            for row2 in rows2:
                cal2 = cal2 + int(row2[0])
                totalcal[i-1] = totalcal[i-1] + cal2
            cur.execute("SELECT cal FROM food where name = 'Roti'")
            rows3 = cur.fetchall()
            for row3 in rows3:
                protein2 = protein2 + int(row3[0])
            cur.execute("SELECT cal FROM food where name = 'Roti'")
            rows4 = cur.fetchall()
            for row4 in rows4:
                carb2 = carb2 + int(row4[0])
            cur.execute("SELECT cal FROM food where name = 'Roti'")
            rows5 = cur.fetchall()
            for row5 in rows5:
                fat2 = fat2 + int(row5[0])
            quantity2 = quantity2 + 1

        meals[meal_type][planno] = {"item1":veggies,"item1Quantity":weight,
                                    "item1Cals":cal1,"item1Proteins":protein1,
                                    "item1Carbs":carb1,"item1Fats":fat1,
                                    "item2":'Roti',"item2Quantity":quantity2,
                                    "item2Cals":cal2,"item2Proteins":protein2,
                                    "item2Carbs":carb2,"item2Fats":fat2}
        print (veggies," x ",weight,"g  ",cal1,"kcal  ",protein1,"g  ",carb1,"g  ",fat1,"g")
        print ("Roti x",quantity2,"  ",cal2,"kcal  ",protein2,"g  ",carb2,"g  ",fat2,"g")
        #print "Rice x",quantity3,"g"
        i=i+1

    """Snacks """
    print ('\nSnacks')
    meal_type = 'Snacks'
    breakfast1 = ['Peanuts',
			'Almonds',
			'Cashew',
			'Walnuts',
			'Pistachios'
			]
    breakfast2 = ['Apple',
			'Pear',
			'Grapes',
			'Fruit Salad',
			'Orange',
			'Watermelon',
            'Pineapple',
			'Papaya',
			'Apple Juice',
			'Orange Juice',
			'Pineapple Juice'
			]
    if med_hist == 1:
        breakfast2 = Diff(breakfast2, cholesterol)
        breakfast1 = Diff(breakfast1, cholesterol)
    if med_hist == 2:
        breakfast2 = Diff(breakfast2, diabetes)
        breakfast1 = Diff(breakfast1, diabetes)
    if med_hist == 3:
        breakfast2 = Diff(breakfast2, hypothyroidism)
        breakfast1 = Diff(breakfast1, hypothyroidism)
    cur = conn.cursor()
    i=1
    while i<4:
        print ("\nPlan ",i)
        planno = 'plan'+str(i)
        quantity1 = 0;
        quantity2 = 0;
        weight1 = 0
        cal1=0
        protein1=0
        carb1=0
        fat1=0
        bf1 = breakfast1[randint(0, len(breakfast1)-1)]
        while cal1 <= min_cal*0.5/10:
            cur.execute("SELECT weight FROM food where name =?", (bf1,))
            rows1 = cur.fetchall()
            for row1 in rows1:
                weight1 = weight1 + int(row1[0])
            cur.execute("SELECT cal FROM food where name =?", (bf1,))
            rows2 = cur.fetchall()
            for row2 in rows2:
                cal1 = cal1 + int(row2[0])
                totalcal[i-1] = totalcal[i-1] + cal1
            cur.execute("SELECT protein FROM food where name =?", (bf1,))
            rows3 = cur.fetchall()
            for row3 in rows3:
                protein1 = protein1 + int(row3[0])
            cur.execute("SELECT carb FROM food where name =?", (bf1,))
            rows4 = cur.fetchall()
            for row4 in rows4:
                carb1 = carb1 + int(row4[0])
            cur.execute("SELECT fat FROM food where name =?", (bf1,))
            rows5 = cur.fetchall()
            for row5 in rows5:
                fat1 = fat1 + int(row5[0])
            quantity1 = quantity1 + 1

        cal2=0
        weight2 = 0
        protein2=0
        carb2=0
        fat2=0
        bf2 = breakfast2[randint(0, len(breakfast2)-1)]
        while cal2 <= min_cal*1/10:
            cur.execute("SELECT weight FROM food where name =?", (bf2,))
            rows3 = cur.fetchall()
            for row3 in rows3:
                weight2 = weight2 + int(row3[0])
            cur.execute("SELECT cal FROM food where name =?", (bf2,))
            rows4 = cur.fetchall()
            for row4 in rows4:
                cal2 = cal2 + int(row4[0])
                totalcal[i-1] = totalcal[i-1] + cal2
            cur.execute("SELECT protein FROM food where name =?", (bf2,))
            rows3 = cur.fetchall()
            for row3 in rows3:
                protein2 = protein2 + int(row3[0])
            cur.execute("SELECT carb FROM food where name =?", (bf2,))
            rows4 = cur.fetchall()
            for row4 in rows4:
                carb2 = carb2 + int(row4[0])
            cur.execute("SELECT fat FROM food where name =?", (bf2,))
            rows5 = cur.fetchall()
            for row5 in rows5:
                fat2 = fat2 + int(row5[0])
            quantity2 = quantity2 + 1

        meals[meal_type][planno] = {"item1":bf1,"item1Quantity":weight1,
                                    "item1Cals":cal1,"item1Proteins":protein1,
                                    "item1Carbs":carb1,"item1Fats":fat1,
                                    "item2":bf2,"item2Quantity":weight2,
                                    "item2Cals":cal2,"item2Proteins":protein2,
                                    "item2Carbs":carb2,"item2Fats":fat2}
        print (bf1," x ",weight1,"g  ",cal1,"kcal  ",protein1,"g  ",carb1,"g  ",fat1,"g")
        print (bf2," x ",weight2,"g  ",cal2,"kcal  ",protein2,"g  ",carb2,"g  ",fat2,"g")
        i=i+1

    """ Dinner """
    print ('\nDinner')
    meal_type = 'Dinner'
    dinner = ['Spinach (Boiled)',
			'Brocolli',
			'Cauliflower',
			'Lettuce',
			'Cabbage',
			'Vegetables',
			'Salmon',
			'Mackerel',
			'Chicken',
			'Chicken Breast',
			'Indian Chicken',
			'Egg Bhurji',
			'Green Peas',
			'Soybeans',
			'Paneer'
			]
    if pref == 1:
        dinner = Diff(dinner, nonveg)
    if pref == 2:
        dinner = Diff(dinner, eggveg)
    if med_hist == 1:
        dinner = Diff(dinner, cholesterol)
    if med_hist == 2:
        dinner = Diff(diner, diabetes)
    if med_hist == 3:
        dinner = Diff(dinner, hypothyroidism)
    cur = conn.cursor()
    i=1
    while i<4:
        print ("\nPlan ",i)
        planno = 'plan'+str(i)
        quantity1 = 0;
        quantity2 = 0;
        weight = 0
        cal=0
        veggies = dinner[randint(0, len(dinner)-1)]
        while cal1 <= min_cal*0.5/10:
            """Veggies"""
            cur.execute("SELECT weight FROM food where name =?", (veggies,))
            rows1 = cur.fetchall()
            for row1 in rows1:
                weight = weight + int(row1[0])
            cur.execute("SELECT cal FROM food where name =?", (veggies,))
            rows2 = cur.fetchall()
            for row2 in rows2:
                cal1 = cal1 + int(row2[0])
                totalcal[i-1] = totalcal[i-1] + cal1
            cur.execute("SELECT protein FROM food where name =?", (veggies,))
            rows3 = cur.fetchall()
            for row3 in rows3:
                protein1 = protein1 + int(row3[0])
            cur.execute("SELECT carb FROM food where name =?", (veggies,))
            rows4 = cur.fetchall()
            for row4 in rows4:
                carb1 = carb1 + int(row4[0])
            cur.execute("SELECT fat FROM food where name =?", (veggies,))
            rows5 = cur.fetchall()
            for row5 in rows5:
                fat1 = fat1 + int(row5[0])
            quantity1 = quantity1 + 1

        cal2=0
        while cal2 <= min_cal*1.5/10:
            """Roti"""
            cur.execute("SELECT * FROM food where name = 'Roti'")
            rows1 = cur.fetchall()
            #for row3 in rows3:
                #print(row3)
            cur.execute("SELECT cal FROM food where name = 'Roti'")
            rows2 = cur.fetchall()
            for row2 in rows2:
                cal2 = cal2 + int(row2[0])
                totalcal[i-1] = totalcal[i-1] + cal2
            cur.execute("SELECT cal FROM food where name = 'Roti'")
            rows3 = cur.fetchall()
            for row3 in rows3:
                protein2 = protein2 + int(row3[0])
            cur.execute("SELECT cal FROM food where name = 'Roti'")
            rows4 = cur.fetchall()
            for row4 in rows4:
                carb2 = carb2 + int(row4[0])
            cur.execute("SELECT cal FROM food where name = 'Roti'")
            rows5 = cur.fetchall()
            for row5 in rows5:
                fat2 = fat2 + int(row5[0])
            quantity2 = quantity2 + 1

        meals[meal_type][planno] = {"item1":veggies,"item1Quantity":weight,
                                    "item1Cals":cal1,"item1Proteins":protein1,
                                    "item1Carbs":carb1,"item1Fats":fat1,
                                    "item2":'Roti',"item2Quantity":quantity2,
                                    "item2Cals":cal2,"item2Proteins":protein2,
                                    "item2Carbs":carb2,"item2Fats":fat2}
        print (veggies," x ",weight,"g  ",cal1,"kcal  ",protein1,"g  ",carb1,"g  ",fat1,"g")
        print ("Roti x",quantity2,"  ",cal2,"kcal  ",protein2,"g  ",carb2,"g  ",fat2,"g")
        #print "Rice x",quantity3,"g"
        i=i+1
    #print "Total Cal Plan 1 = ",totalcal[0]
    #print "Total Cal Plan 2 = ",totalcal[1]
    #print "Total Cal Plan 3 = ",totalcal[2]
    print(meals)
    return meals

def main(user_calorieintake):
    #database = "db.sqlite3"

    # create a database connection
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sqlitedbpath = os.path.join(BASE_DIR,'db.sqlite3')
    conn = create_connection(sqlitedbpath)
    print("************Connection to the sqlite3 created")
    with conn:

        min_cal = user_calorieintake
        max_cal = 2995
        age = 21
        med_hist = "none"
        pref = 0 #0 - Non Veg, 1 - Veg, 2 - Egg Veg
        med_hist = 0 #0 - None, 1 - Cholesterol, 2 - Diabetes, 3 - Hypothyroidism
        meals = atkinsphase1(conn,min_cal,max_cal,pref,med_hist)
        print("************Done Executing Atkins script! returning the plan\n")
        return meals

if __name__ == '__main__':
    main()
