import streamlit as st
from streamlit_option_menu import option_menu
import pymysql
import pandas as pd
import plotly.express as px
import requests
import json
from  PIL import Image

mydb= pymysql.connect(host = '127.0.0.1',
                      user='root',
                      passwd='Mounish007@',
                      database='phonepay_pulse')

cursor=mydb.cursor()

# aggre_insurance
cursor.execute("SELECT * FROM aggregated_insurance")
mydb.commit()
table1= cursor.fetchall()

Aggre_insurance= pd.DataFrame(table1,columns=("States", "Years", "Quarter", "Transaction_type", "Transaction_count", "Transaction_amount"))


# aggre_transaction
cursor.execute("SELECT * FROM aggregated_transaction")
mydb.commit()
table2= cursor.fetchall()

Aggre_transaction= pd.DataFrame(table2,columns=("States", "Years", "Quarter", "Transaction_type", "Transaction_count", "Transaction_amount"))


# aggre_user
cursor.execute("SELECT * FROM aggregated_user")
mydb.commit()
table3= cursor.fetchall()
Aggre_user= pd.DataFrame(table3,columns=("States", "Years", "Quarter", "Brands", "Transaction_count", "Percentage"))


# map_insurance
cursor.execute("SELECT * FROM map_insurance")
mydb.commit()
table4= cursor.fetchall()
map_insurance= pd.DataFrame(table4,columns=("States", "Years", "Quarter", "District", "Transaction_count", "Transaction_amount"))


# map_transaction
cursor.execute("SELECT * FROM map_transaction")
mydb.commit()
table5= cursor.fetchall()
map_transaction= pd.DataFrame(table5,columns=("States", "Years", "Quarter", "District", "Transaction_count", "Transaction_amount"))


# map_user
cursor.execute("SELECT * FROM map_user")
mydb.commit()
table6= cursor.fetchall()
map_user= pd.DataFrame(table6,columns=("States", "Years", "Quarter", "District", "RegisteredUsers", " AppOpens"))


#top_insurance
cursor.execute("SELECT * FROM top_insurance")
mydb.commit()
table7= cursor.fetchall()

top_insurance= pd.DataFrame(table7, columns=("States", "Years", "Quarter", "Pincodes",
                                               "Transaction_count", "Transaction_amount"))



# top_transaction
cursor.execute("SELECT * FROM top_transaction")
mydb.commit()
table8= cursor.fetchall()
top_transaction= pd.DataFrame(table8,columns=("States", "Years", "Quarter", "Pincodes", "Transaction_count", "Transaction_amount"))


# top_users
cursor.execute("SELECT * FROM top_users")
mydb.commit()
table9= cursor.fetchall()
top_users= pd.DataFrame(table9,columns=("States", "Years", "Quarter", "Pincodes", "RegisteredUsers"))

def Transaction_amount_count_Y(df,year):
    tacy= df[df["Years"] == year]
    tacy.reset_index(drop= True,inplace=True)

    tacyg= tacy.groupby("States")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace=True)

    fig_amount= px.bar(tacyg, x="States", y="Transaction_amount", title=f"{year}TRANSACTION AMOUNT",
                    color_discrete_sequence=px.colors.sequential.Agsunset)
    st.plotly_chart(fig_amount)


    fig_count= px.bar(tacyg, x="States", y="Transaction_count", title=f"{year}TRANSACTION COUNT",
                    color_discrete_sequence=px.colors.sequential.Aggrnyl)
    st.plotly_chart(fig_count)

    

    url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response= requests.get(url)
    data1= json.loads(response.content)
    states_name= []
    for feature in data1["features"]:
        states_name.append(feature["properties"]["ST_NM"])

    states_name.sort()

    fig_india_1= px.choropleth(tacyg,geojson=data1, locations="States", featureidkey= "properties.ST_NM",
                                color= "Transaction_amount",color_continuous_scale="turbo",
                                range_color=(tacyg["Transaction_amount"].min(),tacyg["Transaction_amount"].max()),
                                hover_name = "States", title=f"{year} TRANSACTION AMOUNT", fitbounds= "locations",
                                height= 700,width= 700)

    fig_india_1.update_geos(visible=False)
    st.plotly_chart(fig_india_1)

    
    fig_india_2= px.choropleth(tacyg,geojson=data1, locations="States", featureidkey= "properties.ST_NM",
                                color= "Transaction_count",color_continuous_scale="turbo",
                                range_color=(tacyg["Transaction_count"].min(),tacyg["Transaction_count"].max()),
                                hover_name = "States", title=f"{year} TRANSACTION COUNT", fitbounds= "locations",
                                height= 700,width= 700)

    fig_india_2.update_geos(visible=False)
    st.plotly_chart(fig_india_2)

    return tacy

def Transaction_amount_count_Y_Q(df,quarter):
    tacy= df[df["Quarter"] ==quarter]
    tacy.reset_index(drop= True,inplace=True)

    tacyg= tacy.groupby("States")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace=True)

    fig_amount= px.bar(tacyg, x="States", y="Transaction_amount", title=f"{tacy['Years'].min()} YEAR {quarter} QUARTER TRANSACTION AMOUNT",
                    color_discrete_sequence=px.colors.sequential.Agsunset)
    st.plotly_chart(fig_amount)


    fig_count= px.bar(tacyg, x="States", y="Transaction_count", title=f"{tacy['Years'].min()} YEAR {quarter} QUARTER TRANSACTION COUNT",
                    color_discrete_sequence=px.colors.sequential.Aggrnyl)
    st.plotly_chart(fig_count)


    url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response= requests.get(url)
    data1= json.loads(response.content)
    states_name= []
    for feature in data1["features"]:
        states_name.append(feature["properties"]["ST_NM"])

    states_name.sort()

    fig_india_1= px.choropleth(tacyg,geojson=data1, locations="States", featureidkey= "properties.ST_NM",
                                color= "Transaction_amount",color_continuous_scale="turbo",
                                range_color=(tacyg["Transaction_amount"].min(),tacyg["Transaction_amount"].max()),
                                hover_name = "States", title=f"{tacy['Years'].min()} YEAR {quarter} QUARTER TRANSACTION AMOUNT", fitbounds= "locations",
                                height= 700,width= 700)

    fig_india_1.update_geos(visible=False)
    st.plotly_chart(fig_india_1)

    
    fig_india_2= px.choropleth(tacyg,geojson=data1, locations="States", featureidkey= "properties.ST_NM",
                                color= "Transaction_count",color_continuous_scale="turbo",
                                range_color=(tacyg["Transaction_count"].min(),tacyg["Transaction_count"].max()),
                                hover_name = "States",title=f"{tacy['Years'].min()} YEAR {quarter} QUARTER TRANSACTION COUNT", fitbounds= "locations",
                                height= 700,width= 700)

    fig_india_2.update_geos(visible=False)
    st.plotly_chart(fig_india_2)

    return tacy
# transaction_type
def Aggre_Tran_Transaction_type(df,state):

    tacy=df[df["States"] ==state]
    tacy.reset_index(drop= True,inplace=True)


    tacyg= tacy.groupby("Transaction_type")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace=True)

    fig_pie_1= px.pie(data_frame= tacyg, names= "Transaction_type", values= "Transaction_amount",
                    width= 600, title=f"{state.upper()} TRANSACTION AMOUNT", hole= 0.4)
    st.plotly_chart(fig_pie_1)


    fig_pie_2= px.pie(data_frame= tacyg, names= "Transaction_type", values= "Transaction_count",
                    width= 600, title=f"{state.upper()} TRANSACTION COUNT", hole= 0.4)
    st.plotly_chart(fig_pie_2)


# aggred_user_analysis 1
def Aggre_user_plot_1(df, year):
    aguy= df[df["Years"]== year]
    aguy.reset_index(drop= True, inplace= True)

    aguyg=pd.DataFrame(aguy.groupby("Brands")["Transaction_count"].sum())
    aguyg.reset_index(inplace= True)

    fig_bar_1= px.bar(aguyg, x="Brands", y="Transaction_count", title=f"{year} BRANDS AND TRANSACTION COUNT",
                    width= 1000, color_discrete_sequence= px.colors.sequential.Magenta,hover_name= "Brands")
    st.plotly_chart(fig_bar_1)

    return aguy

# Aggre_user_analysis2
def Aggre_user_plot_2(df, Quarter):
    aguyq=df[df["Quarter"]== 2]
    aguyq.reset_index(drop= True, inplace= True)

    aguyqg= pd.DataFrame(aguyq.groupby("Brands")["Transaction_count"].sum())
    aguyqg.reset_index(inplace= True)

    fig_bar_1= px.bar(aguyqg, x="Brands", y="Transaction_count", title=f"{Quarter} QUARTER, BRANDS AND TRANSACTION COUNT",
                    width= 1000, color_discrete_sequence= px.colors.sequential.Aggrnyl, hover_name= "Brands")
    st.plotly_chart(fig_bar_1)
    
    return aguyq

#Aggre_user_analysis_3
def Aggre_user_plot_3(df,state):
    auyqs= df[df["States"] == state]
    auyqs.reset_index(drop= True,inplace= True)

    hover_data = {'Percentage': True}  # Assuming 'Percentage' is the column name
    fig_line_1 = px.line(auyqs, x="Brands", y="Transaction_count", hover_data=hover_data,

                title=f"{state.upper()}BRANDS, TRANSACITON COUNT, PERCENTAGE",width= 1000, markers= True)
    st.plotly_chart(fig_line_1)

# MAP_INSURANCE_DISTRICT
def Map_insur_District(df,state):

    tacy=df[df["States"] ==state]
    tacy.reset_index(drop= True,inplace=True)

    tacyg = tacy.groupby("District")[["Transaction_count", "Transaction_amount"]].sum()

    tacyg.reset_index(inplace=True)

    fig_bar_1= px.bar(tacyg, x= "Transaction_amount", y="District", orientation= "h", height=600,
                      title= f"{state.upper()} DISTRICT AND TRANSACTION AMOUNT", color_discrete_sequence=px.colors.sequential.Magenta_r)
    st.plotly_chart(fig_bar_1)

    
    fig_bar_2= px.bar(tacyg, x= "Transaction_count", y="District", orientation= "h", height= 600,
                      title= f"{state.upper()} DISTRICT AND TRANSACTION  COUNT", color_discrete_sequence=px.colors.sequential.Mint_r)
    st.plotly_chart(fig_bar_2)

# map_user_plot_1
def map_user_plot_1(df,year):
    muy = df[df["Years"] == year]
    muy.reset_index(drop=True, inplace=True)
    muy_copy = muy.copy()

    muy_copy.rename(columns={' AppOpens': 'AppOpens'}, inplace=True)
    muyg = muy_copy.groupby("States")[["RegisteredUsers", "AppOpens"]].sum().reset_index()

    muyg.reset_index(inplace=True)
    fig_line_1=px.line(muyg, x="States", y=["RegisteredUsers", "AppOpens"],
                        title= f"{year} REGISTERED USERS APPOPENS",width= 1000, height= 800,markers= True)
    st.plotly_chart(fig_line_1)

    return muy

# map_user_plot_2
def map_user_plot_2(df,quarter):
    muyq = df[df["Quarter"] == quarter]
    muyq.reset_index(drop=True, inplace=True)
    muyq_copy = muyq.copy()

    muyq_copy.rename(columns={' AppOpens': 'AppOpens'}, inplace=True)
    muyqg = muyq_copy.groupby("States")[["RegisteredUsers", "AppOpens"]].sum().reset_index()

    muyqg.reset_index(inplace=True)
    fig_line_1=px.line(muyqg, x="States", y=["RegisteredUsers", "AppOpens"],
                        title= f"{df['Years'].min()} YEAR {quarter} QUARTER REGISTERED USERS APPOPENS",width= 1000, height= 800,markers= True,
                        color_discrete_sequence= px.colors.sequential.Rainbow_r)
    st.plotly_chart(fig_line_1)

    return muyq

#map_user_plot_3
def map_user_plot_3(df,states):
    muyqs = df[df["States"] == states]
    muyqs.reset_index(drop=True, inplace=True)

    muyqs_copy = muyqs.copy()

    muyqs_copy.rename(columns={'AppOpens': 'AppOpens'}, inplace=True)

    fig_map_user_bar_1 = px.bar(muyqs_copy, x="RegisteredUsers", y="District", orientation="h",
                                title=f"{states.upper()} REGISTERED USERS", height=800, color_discrete_sequence=px.colors.sequential.Rainbow)
    st.plotly_chart(fig_map_user_bar_1)
    muyqs_copy.columns = muyqs_copy.columns.str.strip()

    fig_map_user_bar_2 = px.bar(muyqs_copy, x="AppOpens", y="District", orientation="h",
                                title=f"{states.upper()} APPOPENS", height=800, color_discrete_sequence=px.colors.sequential.Rainbow_r)
    st.plotly_chart(fig_map_user_bar_2)
# Top_insurance_plot_1
def Top_insurance_plot_1(df,state):
    tiy=df[df["States"]== state]
    tiy.reset_index(drop=True, inplace= True)

    tiyg = tiy.groupby("Pincodes")[["Transaction_count", "Transaction_amount"]].sum()
    tiyg.reset_index(inplace=True)

    fig_top_insur_bar_1 = px.bar(tiy, x="Quarter", y= "Transaction_amount",hover_data= "Pincodes",
                                title="TRANSACTION AMOUNT", height=800, color_discrete_sequence=px.colors.sequential.Magenta_r)
    st.plotly_chart(fig_top_insur_bar_1)

    
    fig_top_insur_bar_2 = px.bar(tiy, x="Quarter", y= "Transaction_count",hover_data= "Pincodes",
                                title="TRANSACTION COUNT", height=800, color_discrete_sequence=px.colors.sequential.Aggrnyl_r)
    st.plotly_chart(fig_top_insur_bar_2)

# top_users_plot_1
def top_users_plot_1(df,year):
    tuy= top_users[top_users["Years"]==2020]
    tuy.reset_index(drop= True, inplace= True)

    tuyg=pd.DataFrame(tuy.groupby(["States","Quarter"])["RegisteredUsers"].sum())
    tuyg.reset_index(inplace= True)

    fig_top_plot_1=px.bar(tuyg, x="States", y="RegisteredUsers", color="Quarter",width= 1000, height= 800,
                        color_discrete_sequence=px.colors.sequential.Blugrn, hover_name= "States",
                        title= f"{year} REGISTERED USERS")
    st.plotly_chart(fig_top_plot_1)

    return tuy

# top_users_plot_2
def top_users_plot_2(df,state):
    tuys = df[df["States"] == state]
    tuys.reset_index(drop=True, inplace=True)

    fig_top_plot_2=px.bar(tuys, x="Quarter", y="RegisteredUsers", title= "REGISTEREDUSERS, PINCODES,QUARTER",
                        width= 1000, height= 800, color= "RegisteredUsers", hover_data= "Pincodes",
                        color_continuous_scale= px.colors.sequential.Magenta)
    st.plotly_chart(fig_top_plot_2)


def top_chart_transaction_amount(table_name):
    mydb= pymysql.connect(host = '127.0.0.1',
                        user='root',
                        passwd='Mounish007@',
                        database='phonepay_pulse')

    cursor=mydb.cursor()

    # plot_1
    query_1=f'''select States, sum(Transaction_amount) as Transaction_amount
                from {table_name}
                group by States
                order by Transaction_amount desc
                limit 10
                '''
    cursor.execute(query_1)
    table_1= cursor.fetchall()
    mydb.commit()

    df_1=pd.DataFrame(table_1,columns=("States","Transaction_amount"))
    fig_amount_1= px.bar(df_1, x="States", y="Transaction_amount", title="TOP 10 TRANSACTION AMOUNT",hover_name= "States",
                    color_discrete_sequence=px.colors.sequential.Agsunset, height= 650,width= 600)
    st.plotly_chart(fig_amount_1)

    #plot_2

    query_2=f'''select States, sum(Transaction_amount) as Transaction_amount
                from {table_name}
                group by States
                order by Transaction_amount 
                limit 10
                '''
    cursor.execute(query_2)
    table_2= cursor.fetchall()
    mydb.commit()

    df_2=pd.DataFrame(table_2,columns=("States","Transaction_amount"))
    fig_amount_2= px.bar(df_2, x="States", y="Transaction_amount", title="LAST 10 OF  TRANSACTION AMOUNT",hover_name= "States",
                    color_discrete_sequence=px.colors.sequential.Aggrnyl_r, height= 650,width= 600)
    st.plotly_chart(fig_amount_2)


    #plot_3

    query_3=f'''select States, avg(Transaction_amount) as Transaction_amount
                from {table_name}
                group by States
                order by Transaction_amount 
                '''
    cursor.execute(query_3)
    table_3= cursor.fetchall()
    mydb.commit()

    df_3=pd.DataFrame(table_3,columns=("States","Transaction_amount"))
    fig_amount_3= px.bar(df_3, x="Transaction_amount", y="States", title="AVERAGE OF TRANSACTION AMOUNT",hover_name= "States",orientation= "h",
                    color_discrete_sequence=px.colors.sequential.Bluered_r, height= 800, width= 1000)
    st.plotly_chart(fig_amount_3)                   



def top_chart_transaction_count(table_name):
    mydb= pymysql.connect(host = '127.0.0.1',
                        user='root',
                        passwd='Mounish007@',
                        database='phonepay_pulse')

    cursor=mydb.cursor()

    # plot_1
    query_1=f'''select States, sum(Transation_count) as Transation_count
                from {table_name}
                group by States
                order by Transation_count desc
                limit 10
                '''
    cursor.execute(query_1)
    table_1= cursor.fetchall()
    mydb.commit()

    df_1=pd.DataFrame(table_1,columns=("States","Transation_count"))
    fig_amount_1= px.bar(df_1, x="States", y="Transation_count", title="TOP 10 OF TRANSACTION COUNT",hover_name= "States",
                    color_discrete_sequence=px.colors.sequential.Agsunset, height= 650,width= 600)
    st.plotly_chart(fig_amount_1)

    #plot_2

    query_2=f'''select States, sum(Transation_count) as Transation_count
                from {table_name}
                group by States
                order by Transation_count
                limit 10
                '''
    cursor.execute(query_2)
    table_2= cursor.fetchall()
    mydb.commit()

    df_2=pd.DataFrame(table_2,columns=("States","Transation_count"))
    fig_amount_2= px.bar(df_2, x="States", y="Transation_count", title="LAST 10 OF TRANSACTION COUNT",hover_name= "States",
                    color_discrete_sequence=px.colors.sequential.Aggrnyl_r, height= 650,width= 600)
    st.plotly_chart(fig_amount_2)


    #plot_3

    query_3=f'''select States, avg(Transation_count) as Transation_count
                from {table_name}
                group by States
                order by Transation_count
                '''
    cursor.execute(query_3)
    table_3= cursor.fetchall()
    mydb.commit()

    df_3=pd.DataFrame(table_3,columns=("States","Transation_count"))
    fig_amount_3= px.bar(df_3, x="Transation_count", y="States", title="AVERAGE OF TRANSACTION COUNT",hover_name= "States",orientation= "h",
                    color_discrete_sequence=px.colors.sequential.Bluered_r, height= 800, width= 1000)
    st.plotly_chart(fig_amount_3) 


def top_chart_registered_user(table_name,state):
    mydb= pymysql.connect(host = '127.0.0.1',
                        user='root',
                        passwd='Mounish007@',
                        database='phonepay_pulse')

    cursor=mydb.cursor()

    # plot_1
    query_1=f'''select District, sum(RegisteredUsers) as RegisteredUsers
                from {table_name}
                where States= '{state}'
                group by District
                order by RegisteredUsers desc
                limit 10;
                '''
    cursor.execute(query_1)
    table_1= cursor.fetchall()
    mydb.commit()

    df_1=pd.DataFrame(table_1,columns=("District","RegisteredUsers"))
    fig_amount_1= px.bar(df_1, x="District", y="RegisteredUsers", title="TOP 10 OF REGISTERDUSERS",hover_name= "District",
                    color_discrete_sequence=px.colors.sequential.Agsunset, height= 650,width= 600)
    st.plotly_chart(fig_amount_1)

    #plot_2

    query_2=f'''select District, sum(RegisteredUsers) as RegisteredUsers
                from {table_name}
                where States= '{state}'
                group by District
                order by RegisteredUsers 
                limit 10;
                '''
    cursor.execute(query_2)
    table_2= cursor.fetchall()
    mydb.commit()

    df_2=pd.DataFrame(table_2,columns=("District","RegisteredUsers"))
    fig_amount_2= px.bar(df_2, x="District", y="RegisteredUsers", title="LAST 10 REGISTERED USER",hover_name= "District",
                    color_discrete_sequence=px.colors.sequential.Aggrnyl_r, height= 650,width= 600)
    st.plotly_chart(fig_amount_2)


    #plot_3

    query_3=f'''
                select District, avg(RegisteredUsers) as RegisteredUsers
                from {table_name}
                where States= '{state}'
                group by District
                order by RegisteredUsers;
                '''
    cursor.execute(query_3)
    table_3= cursor.fetchall()
    mydb.commit()

    df_3=pd.DataFrame(table_3,columns=("District","RegisteredUsers"))
    fig_amount_3= px.bar(df_3, x="RegisteredUsers", y="District", title="AVERAGE OF REGISTERD USER",hover_name= "District",orientation= "h",
                    color_discrete_sequence=px.colors.sequential.Bluered_r, height= 800, width= 1000)
    st.plotly_chart(fig_amount_3)



def top_chart_appopens(table_name,state):
    mydb= pymysql.connect(host = '127.0.0.1',
                        user='root',
                        passwd='Mounish007@',
                        database='phonepay_pulse')

    cursor=mydb.cursor()

    # plot_1
    query_1=f'''select District, sum(AppOpens) as AppOpens
                from {table_name}
                where States= '{state}'
                group by District
                order by AppOpens desc
                limit 10;
                '''
    cursor.execute(query_1)
    table_1= cursor.fetchall()
    mydb.commit()

    df_1=pd.DataFrame(table_1,columns=("District","AppOpens"))
    fig_amount_1= px.bar(df_1, x="District", y="AppOpens", title="TOP 10 OF APPOPENS",hover_name= "District",
                    color_discrete_sequence=px.colors.sequential.Agsunset, height= 650,width= 600)
    st.plotly_chart(fig_amount_1)

    #plot_2

    query_2=f'''select District, sum(AppOpens) as AppOpens
                from {table_name}
                where States= '{state}'
                group by District
                order by AppOpens
                limit 10;
                '''
    cursor.execute(query_2)
    table_2= cursor.fetchall()
    mydb.commit()

    df_2=pd.DataFrame(table_2,columns=("District","AppOpens"))
    fig_amount_2= px.bar(df_2, x="District", y="AppOpens", title="LAST 10 APPOPENS",hover_name= "District",
                    color_discrete_sequence=px.colors.sequential.Aggrnyl_r, height= 650,width= 600)
    st.plotly_chart(fig_amount_2)


    #plot_3

    query_3=f'''
                select District, avg(AppOpens) as AppOpens
                from {table_name}
                where States= '{state}'
                group by District
                order by AppOpens;
                '''
    cursor.execute(query_3)
    table_3= cursor.fetchall()
    mydb.commit()

    df_3=pd.DataFrame(table_3,columns=("District","AppOpens"))
    fig_amount_3= px.bar(df_3, x="AppOpens", y="District", title="AVERAGE OF APPOPENS",hover_name= "District",orientation= "h",
                    color_discrete_sequence=px.colors.sequential.Bluered_r, height= 800, width= 1000)
    st.plotly_chart(fig_amount_3)


def top_chart_registered_users(table_name):
    mydb= pymysql.connect(host = '127.0.0.1',
                        user='root',
                        passwd='Mounish007@',
                        database='phonepay_pulse')

    cursor=mydb.cursor()

    # plot_1
    query_1=f'''select States, sum(RegisteredUsers) as RegisteredUsers
                from {table_name}
                group by States
                order by RegisteredUsers desc
                limit 10
                '''
    cursor.execute(query_1)
    table_1= cursor.fetchall()
    mydb.commit()

    df_1=pd.DataFrame(table_1,columns=("States","RegisteredUsers"))
    fig_amount_1= px.bar(df_1, x="States", y="RegisteredUsers", title="TOP 10 OF REGISTERDUSERS",hover_name= "States",
                    color_discrete_sequence=px.colors.sequential.Agsunset, height= 650,width= 600)
    st.plotly_chart(fig_amount_1)

    #plot_2

    query_2=f'''
                SELECT States, SUM(RegisteredUsers) AS RegisteredUsers
                FROM {table_name}
                GROUP BY States
                ORDER BY RegisteredUsers 
                LIMIT 10;
                '''
    
    cursor.execute(query_2)
    table_2= cursor.fetchall()
    mydb.commit()

    df_2=pd.DataFrame(table_2,columns=("States","RegisteredUsers"))
    fig_amount_2= px.bar(df_2, x="States", y="RegisteredUsers", title="LAST 10 REGISTERED USERs",hover_name= "States",
                    color_discrete_sequence=px.colors.sequential.Aggrnyl_r, height= 650,width= 600)
    st.plotly_chart(fig_amount_2)


    #plot_3

    query_3=f'''
                SELECT States, avg(RegisteredUsers) AS RegisteredUsers
                FROM {table_name}
                GROUP BY States
                ORDER BY RegisteredUsers;'''
    
    cursor.execute(query_3)
    table_3= cursor.fetchall()
    mydb.commit()

    df_3=pd.DataFrame(table_3,columns=("States","RegisteredUsers"))
    fig_amount_3= px.bar(df_3, x="RegisteredUsers", y="States", title="AVERAGE OF REGISTERD USERS",hover_name= "States",orientation= "h",
                    color_discrete_sequence=px.colors.sequential.Bluered_r, height= 800, width= 1000)
    st.plotly_chart(fig_amount_3)


# streamlit

st.set_page_config(layout="wide")

st.title("PHONEPAY DATA VISUALIZATION AND EXPLORATION")

with st.sidebar:
    select= option_menu("Main Menu",["HOME", "DATA EXPLORATION", "TOP CHARTS"])


if select =="HOME":
    
    col1,col2=st.columns(2)

    with col1:
        st.header("PHONEPE")
        st.subheader("INDIA'S BEST TRANSACTION APP")
        st.markdown("PhonePe  is an Indian digital payments and financial technology company")
        st.write("****FEATURES****")
        st.write("****Credit & Debit card linking****")
        st.write("****Bank Balance check****")
        st.write("****Money Storage****")
        st.write("****PIN Authorization****")
        st.download_button("DOWNLOAD THE APP NOW", "https://www.phonepe.com/app-download/")
    with col2:
        st.video("C:\\Users\\thang\\OneDrive\\文档\\Desktop\\WhatsApp Video 2024-04-07 at 11.56.59_98551753.mp4")

   
    col3,col4= st.columns(2)
    
    with col3:
       st.video("C:\\Users\\thang\\OneDrive\\文档\\Desktop\\WhatsApp Video 2024-04-07 at 12.06.35_415e195f.mp4")


    with col4:
        st.write("****Easy Transactions****")
        st.write("****One App For All Your Payments****")
        st.write("****Your Bank Account Is All You Need****")
        st.write("****Multiple Payment Modes****")
        st.write("****PhonePe Merchants****")
        st.write("****Multiple Ways To Pay****")
        st.write("****1.Direct Transfer & More****")
        st.write("****2.QR Code****")
        st.write("****Earn Great Rewards****")

   
    col5,col6= st.columns(2)

    with col5:
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.write("****No Wallet Top-Up Required****")
        st.write("****Pay Directly From Any Bank To Any Bank A/C****")
        st.write("****Instantly & Free****")

    with col6:
       st.video("C:\\Users\\thang\\OneDrive\\文档\\Desktop\\WhatsApp Video 2024-04-07 at 12.06.40_e3a24ac2.mp4")



elif select =="DATA EXPLORATION":

    tab1, tab2, tab3 = st.tabs(["Aggregated Analysis", "Map Analysis", "Top Analysis"])

    with tab1:
        method = st.radio("Select the method",["Insurance Analysis", "Transaction Analysis", "User Analysis"])

        if method == "Insurance Analysis":
           
           col1,col2= st.columns(2)
           with col1:
           
                years= st.slider("Select The Year",Aggre_insurance["Years"].min(),Aggre_insurance["Years"].max(),Aggre_insurance["Years"].min())        
                tac_y= Transaction_amount_count_Y(Aggre_insurance,years)

           col1,col2= st.columns(2)
           with col1:
               
               
                quarters= st.slider("Select The Quarter",tac_y["Quarter"].min(),tac_y["Quarter"].max(),tac_y["Quarter"].min())

           Transaction_amount_count_Y_Q(tac_y,quarters)
           
        elif method == "Transaction Analysis":
          
           
           col1,col2= st.columns(2)
           with col1:
           
                years= st.slider("Select The Year",Aggre_transaction["Years"].min(),Aggre_transaction["Years"].max(),Aggre_transaction["Years"].min())
           Aggre_tran_tac_y= Transaction_amount_count_Y(Aggre_transaction,years)

           col1,col2= st.columns(2)
           with col1:
               states= st.selectbox("Select The State",Aggre_tran_tac_y["States"].unique())

           Aggre_Tran_Transaction_type(Aggre_tran_tac_y,states)

           
           col1,col2= st.columns(2)
           with col1:
               
               
                quarters= st.slider("Select The Quarter",Aggre_tran_tac_y["Quarter"].min(),Aggre_tran_tac_y["Quarter"].max(),Aggre_tran_tac_y["Quarter"].min())


           Aggre_tran_tac_y_Q= Transaction_amount_count_Y_Q(Aggre_tran_tac_y,quarters)

           col1,col2= st.columns(2)
           with col1:
               states= st.selectbox("Select The State_Ty",Aggre_tran_tac_y_Q["States"].unique())

           Aggre_Tran_Transaction_type(Aggre_tran_tac_y_Q,states)

          
        elif method == "User Analysis":
            
           col1,col2= st.columns(2)
           with col1:
           
                years= st.slider("Select The Year",Aggre_user["Years"].min(),Aggre_user["Years"].max(),Aggre_user["Years"].min())
           Aggre_user_Y= Aggre_user_plot_1(Aggre_user,years)

           col1,col2= st.columns(2)
           with col1:
               
               
                quarters= st.slider("Select The Quarter",Aggre_user_Y["Quarter"].min(),Aggre_user_Y["Quarter"].max(),Aggre_user_Y["Quarter"].min())


           Aggre_user_Y_Q= Aggre_user_plot_2(Aggre_user_Y,quarters)

           
           col1,col2= st.columns(2)
           with col1:
               states= st.selectbox("Select The State",Aggre_user_Y_Q["States"].unique())

           Aggre_user_plot_3(Aggre_user_Y_Q,states)


    with tab2:

        method_2 = st.radio("Select the method",["Map Insurance", "Map Transaction", "map User"])

        if method_2 == "Map Insurance":
            
           col1,col2= st.columns(2)
           with col1:
           
                years= st.slider("Select The Year_mi",map_insurance["Years"].min(),map_insurance["Years"].max(),map_insurance["Years"].min())
           Map_insur_tac_y= Transaction_amount_count_Y(map_insurance,years)

           col1,col2= st.columns(2)
           with col1:
               states= st.selectbox("Select The State_mi",Map_insur_tac_y["States"].unique())

           Map_insur_District(Map_insur_tac_y,states)

           col1,col2= st.columns(2)
           with col1:
               
                quarters= st.slider("Select The Quarter_mi",Map_insur_tac_y["Quarter"].min(),Map_insur_tac_y["Quarter"].max(),Map_insur_tac_y["Quarter"].min())
           Map_insur_tac_y_Q= Transaction_amount_count_Y_Q(Map_insur_tac_y,quarters)

           col1,col2= st.columns(2)
           with col1:
               states= st.selectbox("Select The State_mi_y",Map_insur_tac_y_Q["States"].unique())

           Map_insur_District(Map_insur_tac_y_Q,states)


        elif method_2 == "Map Transaction":
            
           col1,col2= st.columns(2)
           with col1:
           
                years= st.slider("Select The Year_mt",map_transaction["Years"].min(),map_transaction["Years"].max(),map_transaction["Years"].min())
           Map_tran_tac_y= Transaction_amount_count_Y(map_transaction,years)

           col1,col2= st.columns(2)
           with col1:
               states= st.selectbox("Select The State_mt",Map_tran_tac_y["States"].unique())

           Map_insur_District(Map_tran_tac_y,states)

           col1,col2= st.columns(2)
           with col1:
               
                quarters= st.slider("Select The Quarter_mt",Map_tran_tac_y["Quarter"].min(),Map_tran_tac_y["Quarter"].max(),Map_tran_tac_y["Quarter"].min())
           Map_tran_tac_y_Q= Transaction_amount_count_Y_Q(Map_tran_tac_y,quarters)

           col1,col2= st.columns(2)
           with col1:
               states= st.selectbox("Select The State_mt_y",Map_tran_tac_y_Q["States"].unique())

           Map_insur_District(Map_tran_tac_y_Q,states)
           
            

        elif method_2 == "map User":
            
              
           col1,col2= st.columns(2)
           with col1:
           
                years= st.slider("Select The Year_mu",map_user["Years"].min(),map_user["Years"].max(),map_user["Years"].min())
           map_user_y= map_user_plot_1(map_user,years)

         
           col1,col2= st.columns(2)
           with col1:
               
                quarters= st.slider("Select The Quarter_mu",map_user_y["Quarter"].min(),map_user_y["Quarter"].max(),map_user_y["Quarter"].min())
           map_user_Y_Q= map_user_plot_2(map_user_y,quarters)

           col1,col2= st.columns(2)
           with col1:
               states= st.selectbox("Select The State_mu",map_user_Y_Q["States"].unique())

           map_user_plot_3(map_user_Y_Q,states)
           
            
    with tab3:

        method_3 = st.radio("Select the method",["Top Insurance", "Top Transaction", "Top User"])

        if method_3 == "Top Insurance":
             
               
           col1,col2= st.columns(2)
           with col1:
           
                years= st.slider("Select The Year_ti",top_insurance["Years"].min(),top_insurance["Years"].max(),top_insurance["Years"].min())
           top_insur_tac_y= Transaction_amount_count_Y(top_insurance,years)

        
           col1,col2= st.columns(2)
           with col1:
               states= st.selectbox("Select The State_ti",top_insur_tac_y["States"].unique())

           Top_insurance_plot_1(top_insur_tac_y,states)

            
           col1,col2= st.columns(2)
           with col1:
               
                quarters= st.slider("Select The Quarter_ti",top_insur_tac_y["Quarter"].min(),top_insur_tac_y["Quarter"].max(),top_insur_tac_y["Quarter"].min())
           top_insur_tac_y_Q= Transaction_amount_count_Y_Q(top_insur_tac_y,quarters)
        
        

        elif method_3 == "Top Transaction":
               
           col1,col2= st.columns(2)
           with col1:
           
                years= st.slider("Select The Year_tt",top_transaction["Years"].min(),top_transaction["Years"].max(),top_transaction["Years"].min())
           top_tran_tac_y= Transaction_amount_count_Y(top_transaction,years)

        
           col1,col2= st.columns(2)
           with col1:
               states= st.selectbox("Select The State_tt",top_tran_tac_y["States"].unique())

           Top_insurance_plot_1(top_tran_tac_y,states)

            
           col1,col2= st.columns(2)
           with col1:
               
                quarters= st.slider("Select The Quarter_tt",top_tran_tac_y["Quarter"].min(),top_tran_tac_y["Quarter"].max(),top_tran_tac_y["Quarter"].min())
           top_tran_tac_y_Q= Transaction_amount_count_Y_Q(top_tran_tac_y,quarters)
        
        elif method_3 == "Top User":

                
           col1,col2= st.columns(2)
           with col1:
           
                years= st.slider("Select The Year_tu",top_users["Years"].min(),top_users["Years"].max(),top_users["Years"].min())
           top_user_Y= top_users_plot_1(top_users,years)

            
           col1,col2= st.columns(2)
           with col1:
               states= st.selectbox("Select The State_tu",top_user_Y["States"].unique())

           top_users_plot_2(top_user_Y,states)

            


    
elif select =="TOP CHARTS":
    
    question= st.selectbox("Select the Question",["1. Transaction Amount and Count of Aggregated Insurance",

                                                    "2. Transaction Amount and Count of Map Insurance",

                                                    "3. Transaction Amount and Count of Top Insurance",

                                                    "4. Transaction Amount and Count of Aggregated Transaction",

                                                    "5. Transaction Amount and Count of Map Transaction",

                                                    "6. Transaction Amount and Count of Top Transaction",

                                                    "7. Transaction Count of Aggregated User",

                                                    "8. Registered users of Map User",

                                                    "9. App opens of Map User",

                                                    "10. Registered users of Top User ",
                                                    ])
    
    
    if question == "1. Transaction Amount and Count of Aggregated Insurance":

        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("aggregated_insurance")
        
        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("aggregated_insurance")


    
    elif question == "2. Transaction Amount and Count of Map Insurance":

        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("map_insurance")
        
        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("map_insurance")


    
    elif question == "3. Transaction Amount and Count of Top Insurance":

        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("top_insurance")
        
        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("top_insurance")


    
    elif question == "4. Transaction Amount and Count of Aggregated Transaction":

        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("aggregated_transaction")
        
        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("aggregated_transaction")



    
    elif question == "5. Transaction Amount and Count of Map Transaction":


        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("map_transaction")
        
        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("map_transaction")


   
    
    elif question == "6. Transaction Amount and Count of Top Transaction":

        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("top_transaction")
        
        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("top_transaction")


    
    
    elif question =="7. Transaction Count of Aggregated User":

        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("aggregated_user")
    

    
    elif question =="8. Registered users of Map User":

       states=st.selectbox("Select the state",map_user["States"].unique())

       st.subheader("REGISTERD USERS")
       top_chart_registered_user("map_user", states)


    
    elif question == "9. App opens of Map User":

       states=st.selectbox("Select the state",map_user["States"].unique())

       st.subheader("APPOPENS")
       top_chart_appopens("map_user", states)

    elif question == "10. Registered users of Top User ":

    
       st.subheader("REGISTERED USERS")
       top_chart_registered_users("top_users")
