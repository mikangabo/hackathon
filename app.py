import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import streamlit as st
from tables import household

# Suppress warnings
import warnings
warnings.filterwarnings("ignore", message="missing ScriptRunContext")

# Load data once
@st.cache_data
def load_data():
    # return pd.read_csv('household_internet_offers.csv', index_col=None)
    return pd.read_csv('household_internet_offers_v2.csv', index_col=None)

# Plan name mapping
plan_name_mapping = {
    'Unlimited Family Internet': 'Unlimited',
    'Family Internet (150GB/month)': 'Family (150GB/month)',
    'Premium Family Internet (300GB/month)': 'Premium (300GB/month)', 
    'Standard Home Internet (30GB/month)': 'Standard (30GB/month)',
    'Basic Home Internet (15GB/month)': 'Basic (15GB/month)'
}

def show_donut_chart(df):
    """Show plan distribution donut chart"""
    plan_counts = df['recommended_plan'].value_counts().reset_index()
    plan_counts.columns = ['Plan', 'Count']
    plan_counts['Plan'] = plan_counts['Plan'].map(plan_name_mapping)

    fig = px.pie(
    plan_counts,
    values='Count', 
    names='Plan',
    color_discrete_sequence=px.colors.qualitative.Pastel,
    hole=0.4,
    height=400
).update_layout(
    legend=dict(
        title='Plans',  # Legend title
        orientation='h',  # 'h' for horizontal, 'v' for vertical
        yanchor='bottom',  # Anchor point for y position
        y=-0.2,  # Position below the chart (negative moves it down)
        xanchor='center',  # Anchor point for x position
        x=0.5  # Center the legend
    )
)

    fig.update_traces(
        textposition='inside', 
        textfont=dict(family="Calibri", size=14, color="black", weight="bold"),
        textinfo='percent+label',
        textfont_size=12,
        marker=dict(line=dict(color='#FFFFFF', width=1)),
        pull=[0.1 if i == plan_counts['Count'].idxmax() else 0 
              for i in range(len(plan_counts))]
    )

    # fig.update_layout(
    #     showlegend=True,
    #     margin=dict(l=20, r=20, t=40, b=20),
    #     title_x=0.5
    # )

    st.plotly_chart(fig, use_container_width=True)
    
    with st.expander("View Plan Distribution Data"):
        st.dataframe(plan_counts.sort_values('Count', ascending=False))

household_data=household()


def plot_household_ranges(household_data):
    """
    Creates a range bar chart showing monthly data usage by offer name
    Args:
        household_data: List containing [HOUSEHOLD_ID_count_by_offer, houshold_df] from household()
    """
    # Extract the DataFrames
    # household_count_df, houshold_df = household_data
    _, average_df, _ = household_data
    
    fig = px.bar(
    x=average_df['INTERVALS'],
    y=average_df['AVERAGE_MONTHLY_USAGE_GB'],
    title="",
    text_auto=True,  # Add data labels
    color_discrete_sequence=["#FFCC00"]  # Change bar color to yellow
    )
 
# Remove y-axis but keep data labels
    fig.update_layout(
    xaxis=dict(showgrid=False),  # Remove gridlines on x-axis
    yaxis=dict(
        showgrid=False,        # Remove y-axis gridlines
        showticklabels=False,  # Hide y-axis labels
        title=None             # Remove y-axis title
    ),
    # plot_bgcolor="white"  # Optional: Make background white for a cleaner look
    )
    # Make data labels bold
    fig.update_traces(
        textfont=dict(family="Calibri", size=14, color="white", weight="bold")
    )
 
# Display the chart in Streamlit
    st.plotly_chart(fig, use_container_width=True)

def main():
    # Page config
    st.set_page_config(
        layout="wide",
        page_title="Internet Plan Analytics",
        page_icon="📶"
    )

    # Custom CSS
    st.markdown("""
    <style>
        [data-testid="stSidebar"] {
            background-color: black;
            width: 250px !important;
            padding: 15px 10px;
            border-right: 1px solid #e0e0e0;
        }
        .stButton>button {
            background-color: #ff8f00;
            color: white;
        }
        h1, h2, h3 {
            color: #333;
        }
    </style>
    """, unsafe_allow_html=True)

    # Load data
    df = load_data()
    # results=household()
    with st.sidebar:
        try:
            st.image("third_logo.png", width=150)
        except:
            st.warning("Logo image not found")
        
        st.title("Internet Plans")
        st.markdown("---")

    # Main content
    # st.title("Internet Plan Analytics Dashboard")
    
    col1, col2 = st.columns(2)
    # Add custom styling to make the gap yellow
    st.markdown("""
    <style>
        [data-testid="column"] {
            border-right: 3px solid #FFCC00;
        }
        [data-testid="column"]:last-child {
            border-right: none;
        }
    </style>
    """, unsafe_allow_html=True)
    
    with col1:
        st.header("Offer Distribution")
        show_donut_chart(df)
    
    with col2:
        st.header("Average Monthly Data Usage Across Different Usage Intervals")
        plot_household_ranges(household_data)

    col3,col4=st.columns(2)
    with col3:
            st.header("Household Overview")
        # with st.expander("Household Overview"):
            st.dataframe(household_data[2])
        # st.table(household_data[2])
    with col4:
            st.header("Offer Plan Mapping Overview")
        #householdid,recommendedplan,intervals,monthlyestimateGB
        # with st.expander("View Offer Plan Mapping Overview"):
            st.dataframe(household_data[0])
        
            # st.table(household_data[2])
if __name__ == '__main__':
    main()