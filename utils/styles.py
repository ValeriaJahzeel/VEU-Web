import streamlit as st

def apply_styles():
    st.markdown("""
    <style>
        .main-header {
            font-size: 2.5rem;
            font-weight: 700;
            color: white;
            background-color: #1A4E8C;
            padding: 1rem;
            border-radius: 0px;
            margin-bottom: 0;
            text-align: left;
        }
        .categories-header {
            font-size: 1.5rem;
            font-weight: 600;
            color: white;
            background-color: #1A4E8C;
            padding: 1rem;
            border-radius: 0px;
            margin-top: 0;
            margin-bottom: 1rem;
            text-align: left;
        }
        .sub-header {
            font-size: 1.8rem;
            font-weight: 600;
            margin-top: 1rem;
            margin-bottom: 1rem;
        }
        .category-card {
            background-color: #3E6FB9;
            color: white;
            padding: 1rem;
            border-radius: 5px;
            margin: 0.5rem 0;
            text-align: center;
        }
        .count-box {
            background-color: #2C5AA0;
            border-radius: 25px;
            padding: 0.3rem 1rem;
            margin: 0.5rem;
            display: inline-block;
            font-weight: bold;
        }
        .icon {
            font-size: 1.5rem;
            margin-right: 0.5rem;
        }
        .sidebar-section {
            margin-bottom: 1.5rem;
        }
        .filter-box {
            background-color: white;
            padding: 1rem;
            border-radius: 5px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
            margin-bottom: 1rem;
        }
        .stats-card {
            background-color: white;
            padding: 1rem;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
            margin-bottom: 1.5rem;
        }
        .chart-title {
            font-size: 1.2rem;
            font-weight: 500;
            margin-bottom: 0.5rem;
        }
        .stSelectbox div[data-baseweb="select"] {
            background-color: white;
        }
        div[data-testid="stVerticalBlock"] > div:has(>.main-header) {
            padding-bottom: 0 !important;
        }
        div[data-testid="stVerticalBlock"] > div:has(>.categories-header) {
            padding-top: 0 !important;
        }
        .reportes-section {
            margin-top: 2rem;
        }
        .map-container {
            padding: 0;
            margin: 0;
        }
    </style>
    """, unsafe_allow_html=True)