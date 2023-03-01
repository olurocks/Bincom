from fractions import Fraction
import psycopg2
import json
import math
import statistics


color_dict = {
    "green" : '1',
    "green" : '2',
    "yellow" : '3',
    "brown" : '4',
    "blue" : '5',
    "pink" : '6',
    "orange" : '7',
    "red" : '8',
    "white" : '9',
    "arsh" : '10',
    "black": '11',
    "blew": '12',
    "cream": '13'
}

week_outfit_col = {
    "monday" : 'GREEN, YELLOW, GREEN, BROWN, BLUE, PINK, BLUE, YELLOW, ORANGE, CREAM, ORANGE, RED, WHITE, BLUE, WHITE, BLUE, BLUE, BLUE, GREEN',
    "tuesday" : 'ARSH, BROWN, GREEN, BROWN, BLUE, BLUE, BLEW, PINK, PINK, ORANGE, ORANGE, RED, WHITE, BLUE, WHITE, WHITE, BLUE, BLUE, BLUE',
    "wednesday" : 'GREEN, YELLOW, GREEN, BROWN, BLUE, PINK, RED, YELLOW, ORANGE, RED, ORANGE, RED, BLUE, BLUE, WHITE, BLUE, BLUE, WHITE, WHITE',
    "thursday" : 'BLUE, BLUE, GREEN, WHITE, BLUE, BROWN, PINK, YELLOW, ORANGE, CREAM, ORANGE, RED, WHITE, BLUE, WHITE, BLUE, BLUE, BLUE, GREEN',
    "friday" : 'GREEN, WHITE, GREEN, BROWN, BLUE, BLUE, BLACK, WHITE, ORANGE, RED, RED, RED, WHITE, BLUE, WHITE, BLUE, BLUE, BLUE, WHITE'
}


color_list = []
for k in week_outfit_col:
    cols = week_outfit_col[k].split(", ")
    for col in cols:
        color_list.append(col)



def list_colors_as_ints(col_list:list):
    col_int_list =[]
    for col in col_list:
        col_int_list.append(int(color_dict[col.lower()]))
    return col_int_list

col_int_list = list_colors_as_ints(color_list)




#saving the frequency of colors in a postgresql db.
#The first table is a table of days of the week and the frequency of each color for that week
#The second table consists of all the colors worn through the week and their respective frequencies
freq = {}
for i in color_list:
    if not i in freq:
        freq[i] = 1
    else:
        freq[i] += 1
conn = None
cursor = None

try :
    conn = psycopg2.connect(
        host ='localhost',
        database = 'mytest',
        user = 'postgres',
        password= "dbsecret",
    )
    print("connected to database")
    cursor = conn.cursor()

    create_table_2= """
        CREATE TABLE IF NOT EXISTS table_2 (
            day varchar(50) PRIMARY KEY,
            frequencies jsonb
            )
            """
    cursor.execute(create_table_2)
                                                                                                                                                                                   

    for day, outfit in week_outfit_col.items():
        clothing_items = week_outfit_col[day].split(", ")
        counts = {}
        for item in clothing_items:
            if not item in counts:
                counts[item] = 1
            else:
                counts[item] += 1
        cursor.execute("""
            INSERT INTO table_2 (day, frequencies)
            VALUES (%s, %s)
        """,(day, json.dumps(counts))
        )


    create_table1 = """
        CREATE TABLE IF NOT EXISTS table_4 (
            day varchar(50) PRIMARY KEY,
            frequencies int
            )
            """

    cursor.execute(create_table1)

    for key,value in freq.items():
        cursor.execute("""
                INSERT INTO table_4 (day, frequencies)
                VALUES (%s, %s)
            """,(key, value)
            )
    conn.commit()

except Exception as error:
    print(error)
finally:
    if cursor is not None:
        cursor.close()
    if conn is not None:
        conn.close()
        print("data has been uploaded to your database and now closed")


#mean function to return the mean color
def mean(ncol:list):
    mean = sum(ncol)/len(ncol)
    for key in color_dict:
        if color_dict[key] == str(math.ceil(mean)):
            return key


#mode function to return the modal color
def mode(ncol:list):
    modal_no = statistics.mode(ncol)
    for key in color_dict:
        if color_dict[key] == str(modal_no):
            return key
        

#variance function to return the measure of spred
def calc_var(ncol:list):
    m_s_d = 0
    mean_no = (sum(ncol)/len(ncol))
    for i in ncol:
        s = (i - mean_no)**2
        m_s_d += s #mean squared deviation
    vari= m_s_d/(len(ncol)-1)
    return vari


#function to calculate probability of picking a color
def probability(col,colors):
    count = 0
    for i in colors:
        if i.lower() == col:
            count += 1
    return Fraction(count)/len(colors)
    
print(f"The probability of a color chosen at random to be red is : {probability('red',color_list)}") 

variance = round(calc_var(col_int_list), 2)
print(f"the variance of the distribution is : {variance} ")

print(f"the modal color is : {mode(col_int_list)}")

print(f"the mean color is {mean(col_int_list)}")

