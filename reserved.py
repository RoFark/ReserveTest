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
            background-color: #E6EAF0; /* Greyish blue background */
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
    # Calculate sum of reserve, average days to settle, and claim count per peril
    avg_days_per_peril = data.groupby('PERIL').agg({'DAYS_TO_SETTLE': 'mean', 'SUM(RESERVE)': 'sum', 'CLAIM_COUNT': 'sum'}).reset_index()
    avg_days_per_peril.columns = ['PERIL', 'AVG_DAYS_TO_SETTLE', 'SUM_OF_RESERVE', 'CLAIM_COUNT']
    # Select multiple perils to show
    selected_perils = st.sidebar.multiselect('Select Perils', sorted(data['PERIL'].unique()))
    # Display table with sum of reserve, average days to settle, and claim count for selected perils
    if selected_perils:
        avg_days_per_peril_filtered = avg_days_per_peril[avg_days_per_peril['PERIL'].isin(selected_perils)]
        st.write(avg_days_per_peril_filtered)
    # Slider filter for average days to settle per peril
    avg_days_range = (avg_days_per_peril['AVG_DAYS_TO_SETTLE'].min(), avg_days_per_peril['AVG_DAYS_TO_SETTLE'].max())
    selected_avg_days = st.sidebar.slider('Filter by Average Days to Settle', min_value=avg_days_range[0], max_value=avg_days_range[1], value=avg_days_range)
    # Apply average days to settle filter
    data = data[data['DAYS_TO_SETTLE'] >= selected_avg_days[0]]
    data = data[data['DAYS_TO_SETTLE'] <= selected_avg_days[1]]
    # Slider filter for sum of reserve
    sum_reserve_range = (avg_days_per_peril['SUM_OF_RESERVE'].min(), avg_days_per_peril['SUM_OF_RESERVE'].max())
    selected_sum_reserve = st.sidebar.slider('Filter by Sum of Reserve', min_value=sum_reserve_range[0], max_value=sum_reserve_range[1], value=sum_reserve_range)
    # Apply sum of reserve filter
    data = data[data['SUM(RESERVE)'] >= selected_sum_reserve[0]]
    data = data[data['SUM(RESERVE)'] <= selected_sum_reserve[1]]
    # Boxplot
    fig = px.box(data, x='PERIL', y='INCURRED', color='PERIL', title='Boxplot of Incurred Values by Peril',
                 labels={'PERIL': 'Peril', 'INCURRED': 'Incurred Value'}, hover_data=['CLAIM_REFERENCE', 'CLAIM_COUNT', 'SUM(RESERVE)'])
    # Set initial plot to show all years
    fig.update_layout(xaxis={'tickangle': 45}, height=600, width=1000)  # Set boxplot size
    # Show the plot
    st.plotly_chart(fig, use_container_width=True)
if __name__ == '__main__':
    main()
