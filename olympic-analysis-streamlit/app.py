import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import preprocess, helper

# Load data and preprocess
df = pd.read_csv('little_bit_sorted_for_analysis.csv')
df = preprocess.preprocess(df)
# Page configuration
st.set_page_config(
    page_title="Olympics Analysis",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS styling
st.markdown(
    """
    <style>
        .main-title {
            font-size: 48px;
            color: #1E90FF;
            text-align: center;
            margin-bottom: 30px;
        }
        .sub-title {
            font-size: 32px;
            color: #1E90FF;
            margin-bottom: 20px;
        }
        .header {
            font-size: 24px;
            color: #1E90FF;
        }
        .sidebar {
            background-color: #00FF00; /* Replace this color with your desired color, e.g., #00FF00 for green */
        }
        .footer {
            font-size: 14px;
            color: #888888;
            text-align: center;
            margin-top: 30px;
            position: absolute;
            bottom: 0;
            left: 50%;
            transform: translateX(-50%);
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Page title
st.markdown("<h1 class='main-title'>Olympics Analysis</h1>", unsafe_allow_html=True)

# Sidebar menu
st.sidebar.image("olympics.jpg", use_column_width=True)  # Add the image to the sidebar
st.sidebar.title("Menu")
user_menu = st.sidebar.radio("Select an option", ('Medal Tally', 'Overall Analysis', 'Country wise Analysis'))

# Medal Tally section
if user_menu == 'Medal Tally':
    st.sidebar.header("Medal Tally")
    years, countries = helper.country_year_list(df)

    selected_year = st.sidebar.selectbox("Select Year", years)
    selected_country = st.sidebar.selectbox("Select Country", countries)
    medal_tally = helper.fetch_medal_tally(df, selected_year, selected_country)

    # Page header
    st.markdown("<h2 class='sub-title'>Medal Tally</h2>", unsafe_allow_html=True)
    if selected_year == 'Overall' and selected_country == 'Overall':
        st.subheader('Overall Tally')
    elif selected_year != 'Overall' and selected_country == 'Overall':
        st.subheader(f"Medal Tally in {selected_year} Olympics")
    elif selected_year == 'Overall' and selected_country != 'Overall':
        st.subheader(f"{selected_country} Overall Performance")
    else:
        st.subheader(f"{selected_country} Performance in {selected_year} Olympics")

    st.table(medal_tally)

# Overall Analysis section
if user_menu == 'Overall Analysis':
    st.sidebar.header("Overall Analysis")

    # Top Statistics
    editions = df['year'].nunique()
    cities = df['city'].nunique()
    sports = df['discipline_title'].nunique()
    athletes = df['athlete_full_name'].nunique()
    nations = df['country_name'].nunique()

    # Page header
    st.markdown("<h2 class='sub-title'>Top Statistics</h2>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("<div class='header'>Editions</div>", unsafe_allow_html=True)
        st.title(editions)

    with col2:
        st.markdown("<div class='header'>Hosts</div>", unsafe_allow_html=True)
        st.title(cities)

    with col3:
        st.markdown("<div class='header'>Sports</div>", unsafe_allow_html=True)
        st.title(sports)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div class='header'>Winning Nations</div>", unsafe_allow_html=True)
        st.title(nations)

    with col2:
        st.markdown("<div class='header'>Winning Athletes</div>", unsafe_allow_html=True)
        st.title(athletes)

    # Winning Nations over the years
    nations_over_time = helper.data_over_time(df, "country_name")
    fig = px.line(nations_over_time, x="Edition", y="country_name")
    st.subheader("Winning Nations over the years")
    st.plotly_chart(fig)

    # Events over the years
    events_over_time = helper.data_over_time(df, "discipline_title")
    fig = px.line(events_over_time, x="Edition", y="discipline_title")
    st.subheader("Events over the years")
    st.plotly_chart(fig)

    # Winning Athletes over the years
    athletes_over_time = helper.data_over_time(df, "athlete_full_name")
    fig = px.line(athletes_over_time, x="Edition", y="athlete_full_name")
    st.subheader("Winning Athletes over the years")
    st.plotly_chart(fig)

    # Men vs Women vs Mixed participation over the years
    final = helper.men_vs_women_mixed(df)
    fig = px.line(final, x='year', y=['Male', 'Female', 'Mixed'])
    st.subheader("Men vs Women vs Mixed participation over the years")
    st.plotly_chart(fig)

    # No of events over time (Every Sport)
    fig, ax = plt.subplots(figsize=(20, 20))
    x = df.drop_duplicates(['year', 'discipline_title', 'event_title'])
    ax = sns.heatmap(x.pivot_table(index='discipline_title', columns='year', values='event_title', aggfunc='count').fillna(0).astype(int),
                     annot=True)
    st.subheader("No of events over time (Every Sport)")
    st.pyplot(fig)

    # Most successful Athletes
    sport_list = df['discipline_title'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')

    selected_sport = st.selectbox('Select a sport', sport_list)
    x = helper.most_succesful(df, selected_sport)
    st.subheader("Most Successful Athletes")
    st.table(x)

# Country wise Analysis section
if user_menu == 'Country wise Analysis':
    st.sidebar.header("Country wise Analysis")
    country_list = df['country_name'].unique().tolist()
    country_list.sort()

    selected_country = st.sidebar.selectbox("Select a country", country_list)

    # Medal tally over the years
    country_df = helper.yearwise_medal_tally(df, selected_country)
    fig = px.line(country_df, x='year', y='medal_type')
    st.header(f"{selected_country} Medal Tally over the years")
    st.plotly_chart(fig)

    # Exceles in following sports
    pt = helper.country_event_heatmap(df, selected_country)
    fig, ax = plt.subplots(figsize=(20, 20))
    ax = sns.heatmap(pt, annot=True)
    st.header(f"{selected_country} Excels in Following Sports")
    st.pyplot(fig)

    # Top 10 athletes of the selected country
    top10_df = helper.most_succesful_countrywise(df, selected_country)
    st.header(f"Top 10 Athletes of {selected_country}")
    st.table(top10_df)

# Footer
st.markdown("<p class='footer'>© Olympics Analysis</p>", unsafe_allow_html=True)
