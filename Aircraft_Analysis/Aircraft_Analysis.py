#!/usr/bin/env python
# coding: utf-8

# # Objective 

# The goal of this Data Analysis Project using Sql would to identifify opportunities to increase occupancy rate on low-performing flight, which can ultimately lead to increase profitabilty for airline 

# # Importing Liabraries

# In[97]:


import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')


# # Database Connection

# In[11]:


connection=sqlite3.connect("travel.sqlite")
cursor=connection.cursor()


# In[12]:


cursor.execute("""select name from sqlite_master where type='table';""")
print("list of tables present in the database")
table_list=[table[0] for table in cursor.fetchall()]
table_list


# # Data Exploration

# In[ ]:





# In[14]:


aircrafts_data=pd.read_sql_query("select * from aircrafts_data",connection)
aircrafts_data.head()


# In[17]:


aircrafts_data.shape


# In[23]:


airports_data=pd.read_sql_query("select * from airports_data",connection)
airports_data.head()


# In[29]:


boarding_passes=pd.read_sql_query("select * from boarding_passes",connection)
boarding_passes


# In[30]:


bookings=pd.read_sql_query("select * from bookings",connection)
bookings


# In[31]:


flights=pd.read_sql_query("select * from flights",connection)
flights


# In[32]:


seats=pd.read_sql_query("select * from seats",connection)
seats


# In[34]:


ticket_flights=pd.read_sql_query("select * from ticket_flights",connection)
ticket_flights


# In[35]:


tickets=pd.read_sql_query("select * from tickets",connection)
tickets


# In[42]:


for table in table_list:
    print('\ntable',table)
    column_info=connection.execute("PRAGMA table_info({})".format(table))
    for column in column_info.fetchall():
        print(column[1:3])


# In[ ]:


#Checking Missing Value


# In[44]:


for table in table_list:
    print('\ntable:',table)
    df_table=pd.read_sql_query(f"select * from {table}",connection)
    print(df_table.isnull().sum())


# # Basic Analysis

# In[54]:


# How many planes have more than 100 seats?


# In[55]:


pd.read_sql_query("""select aircraft_code, count(*) as num_seats from seats 
                         group by aircraft_code having num_seats >100""",connection)


# In[56]:


# How the number of tickets booked and total amount earned changed with the time


# In[67]:


tickets=pd.read_sql_query("""select * from tickets inner join bookings on tickets.book_ref=bookings.book_ref""",connection)

tickets['book_date']=pd.to_datetime(tickets['book_date'])

tickets['date']=tickets["book_date"].dt.date


# In[72]:


x=tickets.groupby('date')[['date']].count()

plt.figure(figsize=(18,6))
plt.plot(x.index,x['date'],marker= "^")
plt.xlabel('date',fontsize=20)
plt.ylabel('number of Tickets',fontsize=20)
plt.grid('b')
plt.show()


# In[79]:


bookings=pd.read_sql_query("select * from bookings",connection)
bookings['book_date']=pd.to_datetime(bookings['book_date'])

bookings['date']=bookings["book_date"].dt.date


# In[81]:


bookings.groupby('date')[['total_amount']].sum()


# In[73]:


# calculate the average charges for each aircraft with different fare conditions. 


# In[92]:


df=pd.read_sql_query("""select * from ticket_flights join flights on ticket_flights.flight_id=flights.flight_id""",connection)


# In[95]:


df=pd.read_sql_query("""select fare_conditions, aircraft_code, avg(amount)
                   from ticket_flights join flights on ticket_flights.flight_id=flights.flight_id
                   group by aircraft_code, fare_conditions""",connection)


# In[100]:


sns.barplot(data=df, x="aircraft_code",y='avg(amount)',hue='fare_conditions')


# In[89]:





# # Analyzing Occupancy rate

# In[101]:


#for each aircraft, calculate the total revenue per year and the average revenue per ticket


# In[104]:


pd.read_sql_query("""select aircraft_code, ticket_count, total_revenue/ticket_count as avg_revenue_per_ticket from
(select aircraft_code, count(*) as ticket_count, sum(amount) as total_revenue from ticket_flights
                  join flights on ticket_flights.flight_id=flights.flight_id group by aircraft_code)""",connection)


# In[105]:


#calculate the average occupancy per aircraft.


# In[123]:


occupancy_rate=pd.read_sql_query("""select a.aircraft_code, avg(a.seats_count) as booked_seats, b.num_seats, avg(a.seats_count)/b.num_seats as occupancy_rate
from
(select aircraft_code, flights.flight_id, count(*) as seats_count from boarding_passes
                    inner join flights
                    on boarding_passes.flight_id=flights.flight_id
                    group by aircraft_code, flights.flight_id) as a
                    inner join
                    (select aircraft_code, count(*) as num_seats from seats group by aircraft_code) as b
                    on a.aircraft_code=b.aircraft_code group by a.aircraft_code""",connection
                 )



# In[124]:


#Caculate by how much the total annual turnover could increase by giving 10%higher occupancy rate


# In[126]:


occupancy_rate["inc occupancy rate"]=occupancy_rate['occupancy_rate']+occupancy_rate['occupancy_rate']*0.1


# In[127]:


occupancy_rate


# In[128]:


#total revenue 


# In[137]:


total_revenue=pd.read_sql_query("""select aircraft_code, sum(amount) as total_revenue from ticket_flights
join flights on ticket_flights.flight_id = flights.flight_id group by aircraft_code""", connection)
occupancy_rate['inc Total annual Turnover']=(total_revenue['total_revenue']/occupancy_rate['occupancy_rate'])*occupancy_rate["inc occupancy rate"]


# In[142]:


pd.set_option("display.float_format",str)
occupancy_rate


# In[ ]:




