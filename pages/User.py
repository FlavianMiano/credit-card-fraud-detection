import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pydeck as pdk
import datetime as dt
import seaborn as sns
import plotly.express as px
import uuid
import time
import datetime

import timeit
import warnings
warnings.filterwarnings("ignore")
import streamlit as st

from sklearn.preprocessing import OrdinalEncoder

from pages.Visualizations import df
import pickle

model = pickle.load(open('./finalized_model.pkl', 'rb'))



maintab1, maintab2 = st.tabs(['Transact', 'Account'])

with maintab1:


    acc_num = st.number_input(
        'Enter you Account number',
        key="placeholder",
        )
        
    # acc_num = acc_num.astype(int)
    # acc_num = st.cache_data(acc_num)
    
    if acc_num:
        st.write('Your account number is: ', acc_num)

        #int_val = st.slider('Seconds', min_value=1, max_value=10, value=5, step=1)
        #int_val = st.number_input('Seconds', min_value=1, max_value=10, value=5, step=1)

        personal_df = df[df.cc_num == acc_num]

        first = personal_df['first'].to_list()
        last = personal_df['last'].to_list()

        st.write(last[0], ': Enter Desired transaction :bank: :')

        st.write()

        merchant_col, category_col, amt_col = st.columns([5, 5, 5])

        with merchant_col:
            merchants = df.merchant.unique()
            options = st.selectbox(
                'Merchant',
                merchants
            )

        with category_col:
            categories = df.category.unique()
            option = st.selectbox(
                'choose the category',
                categories
            )


            if option is categories[8]:
                cat_num = 1
            elif option is categories[1]:
                cat_num = 2
            elif option is categories[12]:
                cat_num = 3
            elif option is categories[4]:
                cat_num = 4
            elif option is categories[6]:
                cat_num = 5
            elif option is categories[10]:
                cat_num = 6
            elif option is categories[0]:
                cat_num = 7
            elif option is categories[5]:
                cat_num = 8
            elif option is categories[9]:
                cat_num = 9
            elif option is categories[2]:
                cat_num = 10
            elif option is categories[7]:
                cat_num = 11
            elif option is categories[11]:
                cat_num = 12
            elif option is categories[13]:
                cat_num = 13
            elif option is categories[3]:
                cat_num = 0


        with amt_col:
            amt = st.number_input(
                'Amount you want to spend:'
            )


        with st.form(key='my_form'): 

            trans_num = uuid.uuid4()

            submit_button = st.form_submit_button(label='Submit')

            today = pd.datetime.today()

            personal_df['dob']=pd.to_datetime(personal_df['dob'])

            personal_df['age'] = today - personal_df['dob']

            personal_df['age'] = personal_df['age'].dt.days

            personal_df['age'] = personal_df['age'] / 365

            personal_df['age'] = personal_df['age'].astype(int)

            personal_df['gender'] = personal_df['gender'].map({'M': 1, 'F': 0})

            enc = OrdinalEncoder(dtype=np.int64)

            enc.fit(personal_df.loc[:,['street', 'state']])

            personal_df.loc[:, ['street', 'state']] = enc.transform(personal_df[['street', 'state']])

            
            if submit_button:
                get_data = ({
                    'cc_num': acc_num, 
                    'trans_num': trans_num,
                    'merchant': options, 
                    'category': option, 
                    'amt': amt,
                    'first': first[0], 
                    'last': last[0],
                    'gender': personal_df.gender.unique(), 
                    'state': personal_df.state.unique(),
                    'street': personal_df.street.unique(),
                    'city': personal_df.street.unique(), 
                    'zip': personal_df.zip.unique(), 
                    'lat': personal_df.lat.unique(),
                    'long': personal_df.long.unique(),
                    'city_pop': personal_df.city_pop.unique(),
                    'job': personal_df.job.unique(),
                    'dob': personal_df.dob.unique(),
                    #'unix_time': time.mktime(dt.today().timetuple()),
                    'merch_lat':personal_df.merch_lat.unique()[0],
                    'merch_long': personal_df.merch_long.unique()[0],
                    'age': personal_df.age.unique(),
                    'hour':  pd.datetime.now(),
                    'trans_month': pd.datetime.now().month,
                })

                prediction_data = ({
                    'cc_num': acc_num,
                    'category': cat_num,
                    'amt': amt,
                    'gender': personal_df.gender.unique(),
                    'street': personal_df.street.unique(),
                    'state': personal_df.state.unique(),
                    'zip': personal_df.zip.unique(), 
                    'city_pop': personal_df.city_pop.unique(),
                    'hour':  pd.datetime.now().hour,
                    'trans_month': pd.datetime.now().month,
                    'age': personal_df.age.unique(),
                })

                data_1 = pd.DataFrame(get_data)
                data = pd.DataFrame(prediction_data)

                st.write(data_1)

                with st.spinner('Wait for confirmation...'):
                    time.sleep(5)
                    predict = model.predict(data)
                # st.success('Done!')
                # st.write(predict)
                
                if predict == 1:
                    st.warning('This is a Fraud transaction', icon="⚠️")
                    st.snow()
                elif predict == 0:
                    st.success('Done!')
                    st.balloons()
                
    else:
        st.write('INPUT ACCOUNT NUMBER')

    

with maintab2:
    if acc_num:
        personal_df = df[df.cc_num == acc_num]
        first = personal_df['first'].to_list()
        last = personal_df['last'].to_list()
        st.write('Name: ', first[0], last[0])
        st.write('Account Number: ', acc_num)

        if submit_button:
            st.write('Your new transaction:')
            st.write(pd.DataFrame(get_data))

        #st.write(personal_df)
        expander = st.expander("See Transaction History")
        expander.write(personal_df[['trans_num', 'trans_date_trans_time', 'category', 'merchant', 'amt']])

        # st.subheader('Transaction History')
        # st.write(personal_df[['trans_num', 'trans_date_trans_time', 'category', 'merchant', 'amt']])


        category_df = personal_df.groupby('category').sum()
        st.write('Graph: amount per category of expenditure')
        st.line_chart(category_df.amt)


        year_col, fraud_col = st.columns([7.5, 7.5])

        with year_col:
            personal_df['year'] = pd.to_datetime(personal_df.trans_date_trans_time).dt.year
            
            date_df = personal_df.groupby('year').sum()
            st.write('Graph: Expenditure per year')
            st.line_chart(date_df.amt)

        with fraud_col:
            st.write('Graph: Transactions fraud classification')
            st.bar_chart(personal_df.is_fraud.value_counts())

    else:
        st.write('''Nothing to display!! 
        Please input Account Number.''')



#Making predictions

# importing the model