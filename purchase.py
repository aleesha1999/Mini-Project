import time
import concurrent.futures
import streamlit as st
from streamlit.runtime.scriptrunner import add_script_run_ctx
import flet as ft
import plotly.express as px
import pandas as pd
import os
import warnings
import sys
warnings.filterwarnings('ignore')
st.set_page_config(page_title="Super Market Project ", page_icon=":bar_chart:",layout="wide")
st.title(" :bar_chart:  Super Market Project by Purchase  Fathimathu Aleesha")
st.markdown('<style> div.block.container {padding-top:1rem;} </style>',unsafe_allow_html=True)
fl = st.file_uploader("file_folder: Upload a File",type=(["csv","txt","xlsx","xls"]))
if fl is not None:
    filename = fl.name
    st.write(filename)
    df = pd.read_csv(filename,encoding="ANSI")
else:
    os.chdir(r"C:\My Laptop\Munna Notes\MCA\Sem 3\Study Materials\Mini Project\SalesPurchaseMarketing\pythonProject1")
    df = pd.read_csv("purchase1.csv",encoding="ANSI")
    # "ISO-8859-1"
    col1, col2 = st.columns((2))
    df["Order Date"] = pd.to_datetime(df["Order Date"])
    # Getting the MIn and Max Date
    startDate = pd.to_datetime(df["Order Date"]).min()
    endDate   = pd.to_datetime(df["Order Date"]).max()
    with col1:
        date1 = pd.to_datetime(st.date_input("Start Date ",startDate))
    with col2:
        date2 = pd.to_datetime(st.date_input("End Date",endDate))
    df = df[(df["Order Date"] >= date1) & (df["Order Date"] <= date2)].copy()
    # Side bar filter
    st.sidebar.header("Choose your filter:")
    region= st.sidebar.multiselect("Pick Your Region", df["Region"].unique())
    ##  create for region
    if not region:
        df2=df.copy()
    else:
        df2=df[df["Region"].isin(region)]
    ## create for State
    state=st.sidebar.multiselect("Pick the State",df2["State"].unique())
    if not state:
        df3=df2.copy()
    else:
        df3=df2[df2["State"].isin(state)]
    ## create for city
    city = st.sidebar.multiselect("Pick the City", df3["City"].unique())
    ## Filter based on Region , state and city
    if not region and not state and not city:
        filtered_df = df
    elif not state and not city:
        filtered_df = df[df["Region"].isin(region)]
    elif not region and not city:
        filtered_df = df[df["State"].isin(state)]
    elif state and city:
        filtered_df = df3[df["State"].isin(state) & df3["City"].isin(city)]
    elif region and city:
        filtered_df= df3[df3[df["Region"].isin(region) & df3["City"].isin(city)]]
    elif region and state:
        filtered_df = df3[df["Region"].isin (region) & df3["State"].isin(state)]
    elif city:
        filtered_df = df3[df3["City"].isin(city)]
    else:
        filtered_df = df3[df3["Region"].isin(region) & df3["state"],isin(state) & df3["City"].isin(city)]

        #  ok 08-10-2024
    category_df = filtered_df.groupby (by=["Category"], as_index = False )["Sales"].sum()
    with col1:
        st.subheader("Category Wise Purchase")
        fig=px.bar(category_df,x="Category",y="Sales", text= ['${:,.2f}'.format(x) for x in category_df["Sales"]],template= "seaborn")
        st.plotly_chart(fig,use_container_width=True,height =200)
        with col2:
         st.subheader("Category wise Purchase")
         fig=px.pie(filtered_df , values= "Sales" , names = "Region", hole =0.5)
         fig.update_traces(text = filtered_df ["Region"],textposition="outside")
         st.plotly_chart(fig,use_container_width=True)
         # Download data Codet
         cl1,cl2 = st.columns(2)
    with cl1:
        with st.expander("Category_View Data"):
             st.write(category_df.style.background_gradient(cmap="Blues"))
             csv = category_df.to_csv(index=False).encode('utf-8')
             st.download_button("Download Data",data= csv, file_name = "Category.csv",mime="text/csv",
                               help="Click Here to Download the data as a CSV file")
    with cl2:
        with st.expander("Region_View Data"):
            region = filtered_df.groupby (by="Region",as_index= False)["Sales"].sum()
            st.write(region.style.background_gradient(cmap="Oranges"))
            csv = region.to_csv(index=False).encode('utf-8')
            st.download_button("Download Data", data=csv, file_name="Region.csv", mime="text/csv",
                               help="Click Here to Download the data as a CSV file")
### Time series analysis
    filtered_df["month_year"]=filtered_df["Order Date"].dt.to_period("M")
    st.subheader('Time Series Analysis')
    linechart = pd.DataFrame(filtered_df.groupby(filtered_df["month_year"].dt.strftime("%Y : %b"))["Sales"].sum()).reset_index()
    fig2=px.line(linechart, x="month_year",y="Sales",labels= {"Sales": "Amount"},height=500,width =1000,template="gridon")
    st.plotly_chart(fig2,use_container_width=True)
    ### Download time series data
    with st.expander("View Data of Time Series"):
        st.write(linechart.T.style.background_gradient(cmap="Blues"))
        csv=linechart.to_csv(index=False).encode("utf=8")
        st.download_button('Download Data',data=csv,file_name="TimeSeries.csv")
#### Create a tree based on Region , Category,sub-cateogory
    st.subheader("Hierarchical view of Sales using tree map")
    fig3 = px.treemap(filtered_df,path =["Region","Category","Sub-Category"],values= "Sales",
                      hover_data=["Sales"],color= "Sub-Category")
    fig3.update_layout(width = 800, height = 650)
    st.plotly_chart(fig3,use_container_width= True)

 ##  Segment wise Sales
    chart1, chart2  = st.columns((2))
    with chart1:
        st.subheader("Segment WIse Sales")
        fig = px.pie(filtered_df, values="Sales", names="Segment", template="plotly_dark")
        fig.update_traces(text=filtered_df["Segment"],textposition="inside")
        st.plotly_chart(fig,use_container_width=True)
    ##  Category wise Sales
    with chart2:
        st.subheader("Category Wise Sales")
        fig = px.pie(filtered_df, values="Sales", names="Category", template="gridon")
        fig.update_traces(text=filtered_df["Category"], textposition="inside")
        st.plotly_chart(fig, use_container_width=True)
    ### Show table data in month wise Sales Sammary
    import plotly.figure_factory as ff
    st.subheader(":point_right: Month wise Sub-Category Sales Summary")
    with st.expander("Summary Table"):
         df_sample = df[0:5] [["Region","State","City","Category","Sales","Profit","Quantity"]]
         fig = ff.create_table(df_sample,colorscale="Cividis")
         st.plotly_chart(fig, use_container_width=True)
###  SHow hcategory wise sales
         st.markdown("Month wise sub-Category Table")
         filtered_df["month"]=filtered_df["Order Date"].dt.month_name()
         sub_category_Year = pd.pivot_table(data=filtered_df,values="Sales",index=["Sub-Category"],columns="month")
         st.write(sub_category_Year.style.background_gradient(cmap="Blues"))

## Scatter polotter SHow the relatioship between Sales and Profit
data1 = px.scatter(filtered_df,x="Sales",y="Profit",size="Quantity")
data1['layout'].update(title="Relationship between Sales and Profit using Scatter Plot.",
                       titlefont= dict(size=20),xaxis = dict(title="Sales",titlefont=dict(size=19)),
                       yaxis=dict(title= "Profit",titlefont= dict(size=19)))
st.plotly_chart(data1,use_container_width=True)
## View Sacattered Plet Data in Table
with  st.expander("View Data"):
     st.write(filtered_df.iloc[:500,1:20:2].style.background_gradient(cmap="Oranges"))
## Download the data set
csv= df.to_csv(index=False).encode('utf-8')
st.download_button('Download Data',data = csv,file_name="Data.csv")










































