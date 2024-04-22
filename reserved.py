import streamlit as st
import pandas as pd
import plotly.express as px
def main():
    st.set_page_config(layout="wide")  # Set page layout to wide
    # Custom CSS to set background color and plot text color
    st.markdown(
        """
        <style>
        body {
            background-color: #e6eaf0; /* Greyish blue background */
            color: black; /* Set text color to black */
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    st.title('Interactive Boxplot Dashboard')
    st.sidebar.title('Filters')
    # Read the CSV file
    # data = pd.read_csv('/Users/rosie.farkash/Downloads/reserve.csv')
    uploaded_file = st.sidebar.file_uploader("Upload CSV", type=["csv"])
    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file)
    else:
        st.sidebar.warning('Please upload a CSV file.')
        return
    # Filter by year
    year_filter = st.sidebar.selectbox('Filter by Year', ['All'] + sorted(data['YEAR_OF_ACCOUNT'].unique()))
    if year_filter != 'All':
        data = data[data['YEAR_OF_ACCOUNT'] == year_filter]
    # Filter by super_segment
    super_segment_filter = st.sidebar.selectbox('Filter by Super Segment', ['All'] + sorted(data['SUPER_SEGMENT'].astype(str).unique()))
    if super_segment_filter != 'All':
        data = data[data['SUPER_SEGMENT'].astype(str) == super_segment_filter]
    # Filter by Claim status
    claim_status_filter = st.sidebar.selectbox('Filter by Claim Status', ['All'] + sorted(data['CLAIM_STATUS'].unique()))
    if claim_status_filter != 'All':
        data = data[data['CLAIM_STATUS'] == claim_status_filter]
    # Slider filter for sum of reserve
    sum_reserve_filter = st.sidebar.slider('Filter by Sum of Reserve', min_value=float(data['SUM(RESERVE)'].min()), max_value=float(data['SUM(RESERVE)'].max()), value=(float(data['SUM(RESERVE)'].min()), float(data['SUM(RESERVE)'].max())))
    # Apply sum of reserve filter
    data = data[(data['SUM(RESERVE)'] >= sum_reserve_filter[0]) & (data['SUM(RESERVE)'] <= sum_reserve_filter[1])]
    # Boxplot
    fig = px.box(data, x='PERIL', y='INCURRED', color='PERIL', title='Boxplot of Incurred Values by Peril',
                 labels={'PERIL': 'Peril', 'INCURRED': 'Incurred Value'}, hover_data=['CLAIM_REFERENCE', 'CLAIM_COUNT', 'SUM(RESERVE)'])
    # Set initial plot to show all years
    fig.update_layout(xaxis={'tickangle': 45}, height=600, width=1000)  # Set boxplot size
    # Show the plot
    st.plotly_chart(fig, use_container_width=True)
    
    # Showing a table with total claim_count and sum(reserved) for each peril when a peril is selected
    selected_peril = st.selectbox('Select a Peril to Show Total Claim Count and Sum of Reserve', [''] + sorted(data['PERIL'].unique()))
    if selected_peril:
        peril_data = data[data['PERIL'] == selected_peril]
        summed_claim_count = peril_data['CLAIM_COUNT'].sum()
        summed_reserve = peril_data['SUM(RESERVE)'].sum()
        table_data = {'Claim Count Sum': [summed_claim_count], 'Sum of Reserve': [summed_reserve]}
        st.table(pd.DataFrame(table_data))
if __name__ == '__main__':
    main()













