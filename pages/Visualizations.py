# import the necessary packages
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pydeck as pdk
import datetime as dt
import seaborn as sns
import zipfile

import timeit
import warnings
warnings.filterwarnings("ignore")
import streamlit as st

#st.title('Credit Card Fraud Detection')

# Load the dataset from the csv file using pandas

# dbx = dropbox.Dropbox('sl.BcV124sZ3ZDaT0jEy9nC9eh13w7BmxlC4HosooXGOlOgXA-4KOZPf8sOiqxGtMtF1DM5w7iTlcuqs6valuIrfWPgQytMB1MvozhANgNlTYnDmu-TVaGOYZhaUoWsG11OYeU6itM')

# res = dbx.files_download('https://www.dropbox.com/s/rzzuq3htmkw6011/fraudTrain.csv?dl=1')
# data = pd.read_csv(res.raw)
# st.write(data)
#https://www.dropbox.com/s/rzzuq3htmkw6011/fraudTrain.csv?dl=0

url = 'https://www.dropbox.com/s/rzzuq3htmkw6011/fraudTrain.csv?dl=1'
df = pd.read_csv(url, error_bad_lines=False)


# df=st.cache_data(read_csv(url))
# df = df.sample(frac=0.1, random_state = 48)

main_tab1, main_tab2, main_tab3 = st.tabs(["Show what the dataframe looks like", 
                                           "Show fraud and valid transaction details", 
                                           "Show Visualization"])

with main_tab1:
# Print shape and description of the data
#if st.sidebar.checkbox('Show what the dataframe looks like'):
    tab1_df, tab2_df = st.tabs(['Dataframe', 'Desription'])
    with tab1_df:
        st.subheader('DataFrame')
        st.write(df.head(100))
    with tab2_df:
        st.subheader('Description of DataFrame')
        st.write('Shape of the dataframe: ',df.shape)
        st.write('Data decription: \n',df.describe())

# Print valid and fraud transactions
fraud=df[df.is_fraud==1]
valid=df[df.is_fraud==0]
outlier_percentage=(df.is_fraud.value_counts()[1]/df.is_fraud.value_counts()[0])*100

with main_tab2:
#if st.sidebar.checkbox('Show fraud and valid transaction details'):
    st.subheader('Fraud and Valid Transactions')

    st.write('Fraudulent transactions are: %.3f%%'%outlier_percentage)
    st.write('Fraud Cases: ',len(fraud))
    st.write('Valid Cases: ',len(valid))

with main_tab3:
#if st.sidebar.checkbox('Show Visualization'):

    st.subheader('Visuals')

    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["Fraud", "Gender", "Categories", "State and Street(Frauds", 'Age', 'Job'])

    with tab1:
        st.bar_chart(df.is_fraud.value_counts())
        expander = st.expander("See explanation")
        expander.write("""
            The chart above shows the number of Fraud transactions(1) and Valid transactions (0).
        """)
        #expander.image("https://static.streamlit.io/examples/dice.jpg")

    with tab2:
        st.bar_chart(df.gender.value_counts())
        expander = st.expander("See explanation")
        expander.write("""
            The chart above shows the number of Males and Females.
        """)

    with tab3:
        category_df = df.groupby(['category']).mean()
        category_df['amt'] = category_df['amt'].astype(int)
        st.bar_chart(category_df['amt'])
        expander = st.expander("See explanation")
        expander.write("""
            The chart above shows the average amount of transactions per category.
        """)

    with tab4:
        state_df = df[df['is_fraud'] == 1]
        st.bar_chart(df.state.value_counts(normalize=True))
        st.bar_chart(df.street.value_counts(normalize=True)[:10].index)
        expander = st.expander("See explanation")
        expander.write("""
            The chart above shows the number of Fraud transactions(1) per state.
        """)

    with tab5:
        df['age']=dt.date.today().year-pd.to_datetime(df['dob']).dt.year
        age_df = df[df['is_fraud'] == 1]
        df['age']=dt.date.today().year-pd.to_datetime(df['dob']).dt.year
        fig = plt.figure(figsize=(9,7))
        ax=sns.kdeplot(x='age',data=df, hue='is_fraud', common_norm=False)
        ax.set_xlabel('Credit Card Holder Age')
        ax.set_ylabel('Density')
        plt.xticks(np.arange(0,110,5))
        plt.title('Age Distribution in Fraudulent vs Normal Transactions')
        plt.legend(title='Type', labels=['Fraud', 'Legit'])

        st.pyplot(fig)

        expander = st.expander("See explanation")
        expander.write("""
            The chart above shows the number of Fraud transactions(1) and Valid transactions (0) 
            per age group.
        """)

    with tab6:
        job_df = df[df['is_fraud'] == 1]
        st.bar_chart(job_df.job.value_counts().nlargest(10))

        expander = st.expander("See explanation")
        expander.write("""
            The chart above shows the number of Fraud transactions(1) per job.
        """)

# if st.sidebar.checkbox('Show Visualization'):
#     if st.checkbox('Fraud'):
#         st.bar_chart(df.is_fraud.value_counts())
#     if st.checkbox('Gender'):
#         st.bar_chart(df.gender.value_counts())
#     if st.checkbox('Categories'):
#         category_df = df.groupby(['category']).mean()
#         category_df['amt'] = category_df['amt'].astype(int)
#         st.bar_chart(category_df['amt'])
#     if st.checkbox('State and Street(Frauds)'):
#         state_df = df[df['is_fraud'] == 1]
#         st.bar_chart(df.state.value_counts(normalize=True))
#         st.bar_chart(df.street.value_counts(normalize=True)[:10].index)
#     if st.checkbox('Age'):
#         df['age']=dt.date.today().year-pd.to_datetime(df['dob']).dt.year
#         age_df = df[df['is_fraud'] == 1]
#         df['age']=dt.date.today().year-pd.to_datetime(df['dob']).dt.year
#         fig = plt.figure(figsize=(9,7))
#         ax=sns.kdeplot(x='age',data=df, hue='is_fraud', common_norm=False)
#         ax.set_xlabel('Credit Card Holder Age')
#         ax.set_ylabel('Density')
#         plt.xticks(np.arange(0,110,5))
#         plt.title('Age Distribution in Fraudulent vs Normal Transactions')
#         plt.legend(title='Type', labels=['Fraud', 'Legit'])

#         st.pyplot(fig)

#     if st.checkbox('Jobs'):
#         job_df = df[df['is_fraud'] == 1]
#         st.bar_chart(job_df.job.value_counts().nlargest(10))




