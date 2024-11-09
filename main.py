import streamlit as st
### Page Setup
admim_page = st.Page(
    page="admin.py",
    title= "Admin Page",
    default=True,
)
sales_page = st.Page(
    page="exceldataset.py",
    title="Sales Page",
)
purchase_page = st.Page(
    page="purchase.py",
    title="Purchase Page",
)
marketing_page = st.Page(
    page="marketing.py",
    title="Marketing Page",
)

about_page = st.Page(
    page="about.py",
    title = "About Project",
)
##pg=st.navigation(pages=[admim_page,sales_page,purchase_page,marketing_page,about_page])
##pg.run()
pg=st.navigation(
    {
        "info":[admim_page],
        "Projects":[sales_page,purchase_page,marketing_page,about_page],
    }
)
pg.run()