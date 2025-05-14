import streamlit as st
import pandas as pd


from google.oauth2 import service_account
from google.cloud import bigquery



# Create API client.
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"]
)
client = bigquery.Client(credentials=credentials)
st.write("connection success")
# Perform query.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
@st.cache_data(ttl=100)
def run_query(query):
    st.write(query)
    query_job = client.query(query)
    rows_raw = query_job.result()
    # Convert to list of dicts. Required for st.cache_data to hash the return value.
    rows = [dict(row) for row in rows_raw]
    return rows

def insert_query(query,name,age):
    query_job = client.query(query,params={"name": name,"age":age},)
    #rows_raw = query_job.result()
    # Convert to list of dicts. Required for st.cache_data to hash the return value.
    #rows = [dict(row) for row in rows_raw]
    return query_job


# Create a connection object.
st.title("ABC Steel Data Input Form")
tab1, tab2, tab3 = st.tabs(["Update", "Read", "Analysis"])
df = pd.DataFrame(run_query("SELECT * FROM `top-athlete-459808-j9.name_age_dataset.name_age`"))
if tab2.button("refresh"):
    df = pd.DataFrame(run_query("SELECT * FROM `top-athlete-459808-j9.name_age_dataset.name_age`"))
tab2.write(df)

# Add the new vendor data to the existing data
name = tab1.text_input(label="Name",value=None)
age = tab1.number_input(label="age",min_value=0,value=None)
submit_button = tab1.button(label="Submit Details")
if submit_button:
    #insert = "
    #INSERT INTO `light-willow-459806-t7.sample_name_data.name_age` (Name, Age) VALUES ('India', '75')
    #"

    # Ejecutar la consulta
    #tab1.write("INSERT INTO `light-willow-459806-t7.sample_name_data.name_age` (Name, Age) VALUES ('{name}', {age})")
    #tab1.write("INSERT INTO `light-willow-459806-t7.sample_name_data.name_age` (Name, Age) VALUES ('India', '75')")
    
    #query_job_kai_insert =insert_query(f"""INSERT INTO `light-willow-459806-t7.sample_name_data.name_age` (Name, Age) VALUES ('India', '75')""")
    #query_job_kai_insert =run_query("select * from `light-willow-459806-t7.sample_name_data.name_age` where age > 20")
    #query_job_kai_insert =insert_query("insert into `top-athlete-459808-j9.name_age_dataset.name_age` values (:name,:age)",name,age)
    query_job_kai_insert =client.query(f"""insert into `top-athlete-459808-j9.name_age_dataset.name_age` values ('{name}',{age})""")
    tab1.write(query_job_kai_insert)
    tab1.success('Record added Successfully')
    # Update Google Sheets with the new vendor data
    



    #df = conn.read(worksheet="sample", ttl="0.5m")
    #st.write(df)
#tab3.write("Mean of ages")
tab3.metric("Mean Age",df.Age.mean())
tab3.metric("#Entries",df.shape[0])

rows2 = pd.DataFrame(run_query("SELECT * FROM `top-athlete-459808-j9.name_age_dataset.name_age`"))
st.write()
#rows = run_query("SELECT word FROM `bigquery-public-data.samples.shakespeare` LIMIT 10")

# Print results.
#st.write("Some wise words from Shakespeare:")
#for row in rows:
#    st.write("✍️ " + row['word'])
