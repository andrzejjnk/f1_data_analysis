import pandas as pd
import streamlit as st
from st_on_hover_tabs import on_hover_tabs
from utils.lib import *

st.set_page_config(page_title="F1 Analysis", page_icon=":racing_car:", layout="wide")
st.markdown('<style>' + open('app_utils/style.css').read() + '</style>', unsafe_allow_html=True)

# Set the background image
# background_image = """
# <style>
# [data-testid="stAppViewContainer"] > .main {
#     background-image: url("");
#     background-size: 100vw 100vh;  # This sets the size to cover 100% of the viewport width and height
#     background-position: center;  
#     background-repeat: no-repeat;
# }
# </style>
# """

with st.sidebar:
    tabs = on_hover_tabs(tabName=['Overview', 'Standings', 'Race', 'Sprint', 'Qualifications', 'Sprint Qualifications', 'FP1', 'FP2', 'FP3'],
                         iconName=['dashboard', 'dashboard', 'dashboard', 'dashboard', 'dashboard', 'dashboard', 'dashboard', 'dashboard', 'dashboard'], default_choice=0)
    

if tabs== 'Overview':
    # st.markdown(background_image, unsafe_allow_html=True)
    st.title("Overview")
    st.write("This application is dedicated to visualization of data from the hybrid era with ground effect of Formula 1 from 2022 to 2024.")
    st.write("The hybrid era in Formula 1 is a period during which cars are equipped with hybrid engines, combining an internal combustion engine with an electric motor. Analyzing data from this period can provide valuable insights into the performance of individual teams, drivers, and the technology used during this time.")


elif tabs == 'Standings':
    st.title("Standings")

    options = ["Standings", "Compare drivers per year"]
    years = [2022, 2023, 2024]
    
    st.session_state.select_option = st.selectbox("Select option:", options, key="standings_plot_option")
    st.session_state.year = st.selectbox("Select year:", years, key="select_year_standings")

    drivers_to_compare = get_drivers_per_year_from_races(st.session_state.year)['Driver'].tolist()
    drivers_to_compare.insert(0, "All")
    if st.session_state.select_option == options[1]:
        st.session_state.selected_drivers = st.multiselect("Select drivers:", drivers_to_compare, default="All", key="select_drivers_standings")
        if not st.session_state.selected_drivers:
            st.session_state.selected_drivers = ["All"]

    st.session_state.generate_button = st.button("Show", key="standings_generate_chart_button")
    first_call = True
    if st.session_state.generate_button or first_call: 
        if st.session_state.select_option == options[0]:
            races_df = get_driver_points_per_season_with_race_results(st.session_state.year)
            sprints_df = get_driver_points_per_season_with_sprint_results(st.session_state.year)
            standings_df = merge_race_and_sprint_data(races_df, sprints_df)
            st.dataframe(standings_df, hide_index=True, use_container_width=True)

        elif st.session_state.select_option == options[1]:
            if "All" in st.session_state.selected_drivers:
                fig = plot_drivers_points_specified_year_standings(st.session_state.year)
            else:
                fig = plot_drivers_points_specified_year_standings(st.session_state.year, st.session_state.selected_drivers)
            st.plotly_chart(fig)
        first_call = False


elif tabs == 'Race':
    st.title("Race")
    
    options = ["Race Results per race", "Race Results per driver", "Compare points from races in a specified year", "Compare positions in a specified year", "Compare positions in a specified race"]
    years = [2022, 2023, 2024]
    st.session_state.select_option = st.selectbox("Select option:", options, key="race_results_plot_option")
    if not st.session_state.select_option == options[4]:
        st.session_state.year = st.selectbox("Select year:", years, key="select_year_race_results")
    drivers_to_compare = get_drivers_per_year_from_races(st.session_state.year)['Driver'].tolist()
    drivers_to_compare.insert(0, "All")

    if st.session_state.select_option == options[0]:
        st.session_state.country = st.selectbox("Select race:", list(race_orders[int(st.session_state.year)].values()), key="select_countries_race_results")
    elif st.session_state.select_option == options[4]:
        st.session_state.country = st.selectbox("Select race:", unique_races, key="select_countries_race_results")
    
    if not st.session_state.select_option == options[0] and not st.session_state.select_option == options[1]:
        st.session_state.selected_drivers = st.multiselect("Select drivers:", drivers_to_compare, default="All", key="select_drivers_race_results")
        if not st.session_state.selected_drivers:
            st.session_state.selected_drivers = ["All"]
    elif st.session_state.select_option == options[1]:
        st.session_state.selected_drivers = st.selectbox("Select drivers:", drivers_to_compare[1: ], key="select_drivers_race_results")
        if not st.session_state.selected_drivers:
            st.session_state.selected_drivers = ["All"]

    st.session_state.generate_button = st.button("Show", key="race_result_generate_chart_button")
    first_call = True
    if st.session_state.generate_button or first_call: 
        if st.session_state.select_option == options[0]:
            race_result_year_country_df = get_race_result_data_race_year(st.session_state.country, st.session_state.year)
            race_result_year_country_df['Year'] = race_result_year_country_df['Year'].astype(str)
            st.dataframe(race_result_year_country_df, hide_index=True, use_container_width=True)

        if st.session_state.select_option == options[1]:
            race_result_year_driver_df = get_driver_results_per_year(st.session_state.year, st.session_state.selected_drivers)
            race_result_year_driver_df['Year'] = race_result_year_driver_df['Year'].astype(str)
            st.dataframe(race_result_year_driver_df, hide_index=True, use_container_width=True)

        elif st.session_state.select_option == options[2]:
            if "All" in st.session_state.selected_drivers:
                fig = plot_drivers_points_specified_year(st.session_state.year)
            else:
                fig = plot_drivers_points_specified_year(st.session_state.year, st.session_state.selected_drivers)
            st.plotly_chart(fig)

        elif st.session_state.select_option == options[3]:
            if "All" in st.session_state.selected_drivers:
                fig = plot_comparision_between_drivers_specified_year(st.session_state.year)
            else:
                fig = plot_comparision_between_drivers_specified_year(st.session_state.year, st.session_state.selected_drivers)
            st.plotly_chart(fig)

        elif st.session_state.select_option == options[4]:
            if "All" in st.session_state.selected_drivers:
                fig = plot_comparision_between_drivers_specified_country(st.session_state.country, drivers_to_compare[1: ])
            else:
                fig = plot_comparision_between_drivers_specified_country(st.session_state.country, st.session_state.selected_drivers)
            st.plotly_chart(fig)
        first_call = False


elif tabs == 'Sprint':
    st.title("Sprint")

    options = ["Sprint Results per sprint", "Sprint Results per driver", "Compare points from sprints in a specified year", "Compare positions in a specified year", "Compare positions in a specified sprint"]
    years = [2022, 2023, 2024]
    st.session_state.select_option = st.selectbox("Select option:", options, key="sprint_results_plot_option")
    if not st.session_state.select_option == options[4]:
        st.session_state.year = st.selectbox("Select year:", years, key="select_year_sprint_results")
    drivers_to_compare = get_drivers_per_year_from_sprints(st.session_state.year)['Driver'].tolist()
    drivers_to_compare.insert(0, "All")
    
    if st.session_state.select_option == options[0]:
        st.session_state.country = st.selectbox("Select sprint:", list(sprint_orders[int(st.session_state.year)].values()), key="select_countries_sprint_results")
    elif st.session_state.select_option == options[4]:
        st.session_state.country = st.selectbox("Select sprint:", unique_sprints, key="select_countries_sprint_results")

    if not st.session_state.select_option == options[0] and not st.session_state.select_option == options[1]:
        st.session_state.selected_drivers = st.multiselect("Select drivers:", drivers_to_compare, default="All", key="select_drivers_sprint_results")
        if not st.session_state.selected_drivers:
            st.session_state.selected_drivers = ["All"]
    elif st.session_state.select_option == options[1]:
        st.session_state.selected_drivers = st.selectbox("Select drivers:", drivers_to_compare[1: ], key="select_drivers_sprint_results")
        if not st.session_state.selected_drivers:
            st.session_state.selected_drivers = ["All"]

    st.session_state.generate_button = st.button("Show", key="sprint_result_generate_chart_button")
    first_call = True
    if st.session_state.generate_button or first_call: 
        if st.session_state.select_option == options[0]:
            sprint_result_year_country_df = get_sprint_result_data_sprint_year(st.session_state.country, st.session_state.year)
            sprint_result_year_country_df['Year'] = sprint_result_year_country_df['Year'].astype(str)
            st.dataframe(sprint_result_year_country_df, hide_index=True, use_container_width=True)

        if st.session_state.select_option == options[1]:
            sprint_result_year_driver_df = get_driver_results_per_year_sprints(st.session_state.year, st.session_state.selected_drivers)
            sprint_result_year_driver_df['Year'] = sprint_result_year_driver_df['Year'].astype(str)
            st.dataframe(sprint_result_year_driver_df, hide_index=True, use_container_width=True)

        elif st.session_state.select_option == options[2]:
            if "All" in st.session_state.selected_drivers:
                fig = plot_drivers_points_specified_year_sprints(st.session_state.year)
            else:
                fig = plot_drivers_points_specified_year_sprints(st.session_state.year, st.session_state.selected_drivers)
            st.plotly_chart(fig)

        elif st.session_state.select_option == options[3]:
            if "All" in st.session_state.selected_drivers:
                fig = plot_comparision_between_drivers_specified_year_sprints(st.session_state.year)
            else:
                fig = plot_comparision_between_drivers_specified_year_sprints(st.session_state.year, st.session_state.selected_drivers)
            st.plotly_chart(fig)

        elif st.session_state.select_option == options[4]:
            if "All" in st.session_state.selected_drivers:
                fig = plot_comparision_between_drivers_specified_country_sprints(st.session_state.country, drivers_to_compare[1: ])
            else:
                fig = plot_comparision_between_drivers_specified_country_sprints(st.session_state.country, st.session_state.selected_drivers)
            st.plotly_chart(fig)
        first_call = False


elif tabs == 'Qualifications':
    st.title("Qualifications")

    options = ["Qualifying Results per race", "Qualifying Results per driver", "Gaps to the leader"]
    years = [2022, 2023, 2024]
    st.session_state.select_option = st.selectbox("Select option:", options, key="qualifications_results_plot_option")
    st.session_state.year = st.selectbox("Select year:", years, key="select_year_qualifications_results")
    drivers_to_compare = get_drivers_per_year_from_qualifications(st.session_state.year)['Driver'].tolist()
    drivers_to_compare.insert(0, "All")
    
    if st.session_state.select_option == options[0] or st.session_state.select_option[2]:
        st.session_state.country = st.selectbox("Select qualifications:", list(race_orders[int(st.session_state.year)].values()), key="select_countries_qualifications_results")

    if st.session_state.select_option == options[2]:
        st.session_state.quali_session = st.selectbox("Select session:", ['Q1', 'Q2', 'Q3'], key="select_session_qualifications_results")

    if not st.session_state.select_option == options[0] and not st.session_state.select_option == options[1] and not st.session_state.select_option == options[2]:
        st.session_state.selected_drivers = st.multiselect("Select drivers:", drivers_to_compare, default="All", key="select_drivers_qualifications_results")
        if not st.session_state.selected_drivers:
            st.session_state.selected_drivers = ["All"]
    elif st.session_state.select_option == options[1] and not st.session_state.select_option == options[2]:
        st.session_state.selected_drivers = st.selectbox("Select drivers:", drivers_to_compare[1: ], key="select_drivers_qualifications_results")
        if not st.session_state.selected_drivers:
            st.session_state.selected_drivers = ["All"]


    st.session_state.generate_button = st.button("Show", key="qualifications_result_generate_chart_button")
    first_call = True
    if st.session_state.generate_button or first_call: 
        if st.session_state.select_option == options[0]:
            qualifications_result_year_country_df = get_qualifications_data_race_year(st.session_state.country, st.session_state.year)
            qualifications_result_year_country_df['Year'] = qualifications_result_year_country_df['Year'].astype(str)
            st.dataframe(qualifications_result_year_country_df, hide_index=True, use_container_width=True)

        if st.session_state.select_option == options[1]:
            qualifications_result_year_driver_df = get_driver_results_per_year_qualifications(st.session_state.year, st.session_state.selected_drivers)
            qualifications_result_year_driver_df['Year'] = qualifications_result_year_driver_df['Year'].astype(str)
            st.dataframe(qualifications_result_year_driver_df, hide_index=True, use_container_width=True)

        if st.session_state.select_option == options[2]:
            quali_df = get_qualifications_data_race_year(st.session_state.country, st.session_state.year)
            time_deltas_df = calculate_time_delta(quali_df)
            fig = plot_time_gap_per_session(time_deltas_df, st.session_state.quali_session)
            st.plotly_chart(fig)
        first_call = False


elif tabs == 'Sprint Qualifications':
    st.title("Sprint Qualifications")


    options = ["Sprint Qualifying Results per race", "Sprint Qualifying Results per driver", "Gaps to the leader"]
    years = [2023, 2024]
    st.session_state.select_option = st.selectbox("Select option:", options, key="sprint_qualifications_results_plot_option")
    st.session_state.year = st.selectbox("Select year:", years, key="select_year_sprint_qualifications_results")
    drivers_to_compare = get_drivers_per_year_from_sprint_qualifications(st.session_state.year)['Driver'].tolist()
    drivers_to_compare.insert(0, "All")
    
    if st.session_state.select_option == options[0] or st.session_state.select_option == options[2]:
        st.session_state.country = st.selectbox("Select sprint qualifications:", list(sprint_orders[int(st.session_state.year)].values()), key="select_countries_sprint_qualifications_results")

    if st.session_state.select_option == options[2]:
        st.session_state.quali_session = st.selectbox("Select session:", ['Q1', 'Q2', 'Q3'], key="select_session_sprint_qualifications_results")

    if not st.session_state.select_option == options[0] and not st.session_state.select_option == options[1] and not st.session_state.select_option == options[2]:
        st.session_state.selected_drivers = st.multiselect("Select drivers:", drivers_to_compare, default="All", key="select_drivers_sprint_qualifications_results")
        if not st.session_state.selected_drivers:
            st.session_state.selected_drivers = ["All"]
    elif st.session_state.select_option == options[1] and not st.session_state.select_option == options[2]:
        st.session_state.selected_drivers = st.selectbox("Select drivers:", drivers_to_compare[1: ], key="select_drivers_sprint_qualifications_results")
        if not st.session_state.selected_drivers:
            st.session_state.selected_drivers = ["All"]

    st.session_state.generate_button = st.button("Show", key="sprint_qualifications_result_generate_chart_button")
    first_call = True
    if st.session_state.generate_button or first_call: 
        if st.session_state.select_option == options[0]:
            sprint_qualifications_result_year_country_df = get_sprint_qualifications_data_sprint_year(st.session_state.country, st.session_state.year)
            sprint_qualifications_result_year_country_df['Year'] = sprint_qualifications_result_year_country_df['Year'].astype(str)
            st.dataframe(sprint_qualifications_result_year_country_df, hide_index=True, use_container_width=True)

        if st.session_state.select_option == options[1]:
            sprint_qualifications_result_year_driver_df = get_driver_results_per_year_sprint_qualifications(st.session_state.year, st.session_state.selected_drivers)
            sprint_qualifications_result_year_driver_df['Year'] = sprint_qualifications_result_year_driver_df['Year'].astype(str)
            st.dataframe(sprint_qualifications_result_year_driver_df, hide_index=True, use_container_width=True)

        if st.session_state.select_option == options[2]:
            sprint_quali_df = get_sprint_qualifications_data_sprint_year(st.session_state.country, st.session_state.year)
            time_deltas_df = calculate_time_delta(sprint_quali_df)
            fig = plot_time_gap_per_session(time_deltas_df, st.session_state.quali_session)
            st.plotly_chart(fig)
        first_call = False


elif tabs == 'FP1':
    st.title("Practice 1")

    options = ["Practice 1 Results per race", "Practice 1 Results per driver", "Gaps to the leader"]
    years = [2022, 2023, 2024]
    st.session_state.select_option = st.selectbox("Select option:", options, key="practice1_results_plot_option")
    st.session_state.year = st.selectbox("Select year:", years, key="select_year_practice1_results")
    drivers_to_compare = get_drivers_per_year_from_practice1_data(st.session_state.year)['Driver'].tolist()
    drivers_to_compare.insert(0, "All")
    
    if st.session_state.select_option == options[0] or st.session_state.select_option == options[2]:
        st.session_state.country = st.selectbox("Select practice 1:", list(practice1_orders[int(st.session_state.year)].values()), key="select_countries_practice1_results")

    if not st.session_state.select_option == options[0] and not st.session_state.select_option == options[1] and not st.session_state.select_option == options[2]:
        st.session_state.selected_drivers = st.multiselect("Select drivers:", drivers_to_compare, default="All", key="select_drivers_practice1_results")
        if not st.session_state.selected_drivers:
            st.session_state.selected_drivers = ["All"]
    elif st.session_state.select_option == options[1] and not st.session_state.select_option == options[2]:
        st.session_state.selected_drivers = st.selectbox("Select drivers:", drivers_to_compare[1: ], key="select_drivers_practice1_results")
        if not st.session_state.selected_drivers:
            st.session_state.selected_drivers = ["All"]

    st.session_state.generate_button = st.button("Show", key="practice1_result_generate_chart_button")
    first_call = True
    if st.session_state.generate_button or first_call: 
        if st.session_state.select_option == options[0]:
            practice1_result_year_country_df = get_practice1_data_data_race_year(st.session_state.country, st.session_state.year)
            practice1_result_year_country_df['Year'] = practice1_result_year_country_df['Year'].astype(str)
            st.dataframe(practice1_result_year_country_df, hide_index=True, use_container_width=True)

        if st.session_state.select_option == options[1]:
            practice1_result_year_driver_df = get_driver_results_per_year_practice1_data(st.session_state.year, st.session_state.selected_drivers)
            practice1_result_year_driver_df['Year'] = practice1_result_year_driver_df['Year'].astype(str)
            st.dataframe(practice1_result_year_driver_df, hide_index=True, use_container_width=True)

        if st.session_state.select_option == options[2]:
            practice1_result_year_country_df = get_practice1_data_data_race_year(st.session_state.country, st.session_state.year)
            fig = plot_time_gap_practice_session(practice1_result_year_country_df, 'FP1')
            st.plotly_chart(fig)
        first_call = False


elif tabs == 'FP2':
    st.title("Practice 2")

    options = ["Practice 2 Results per race", "Practice 2 Results per driver", "Gaps to the leader"]
    years = [2022, 2023, 2024]
    st.session_state.select_option = st.selectbox("Select option:", options, key="practice2_results_plot_option")
    st.session_state.year = st.selectbox("Select year:", years, key="select_year_practice2_results")
    drivers_to_compare = get_drivers_per_year_from_practice2_data(st.session_state.year)['Driver'].tolist()
    drivers_to_compare.insert(0, "All")
    
    if st.session_state.select_option == options[0] or st.session_state.select_option == options[2]:
        st.session_state.country = st.selectbox("Select practice 2:", list(practice2_orders[int(st.session_state.year)].values()), key="select_countries_practice2_results")

    if not st.session_state.select_option == options[0] and not st.session_state.select_option == options[1] and not st.session_state.select_option == options[2]:
        st.session_state.selected_drivers = st.multiselect("Select drivers:", drivers_to_compare, default="All", key="select_drivers_practice2_results")
        if not st.session_state.selected_drivers:
            st.session_state.selected_drivers = ["All"]
    elif st.session_state.select_option == options[1] and not st.session_state.select_option == options[2]:
        st.session_state.selected_drivers = st.selectbox("Select drivers:", drivers_to_compare[1: ], key="select_drivers_practice2_results")
        if not st.session_state.selected_drivers:
            st.session_state.selected_drivers = ["All"]

    st.session_state.generate_button = st.button("Show", key="practice2_result_generate_chart_button")
    first_call = True
    if st.session_state.generate_button or first_call: 
        if st.session_state.select_option == options[0]:
            practice2_result_year_country_df = get_practice2_data_data_race_year(st.session_state.country, st.session_state.year)
            practice2_result_year_country_df['Year'] = practice2_result_year_country_df['Year'].astype(str)
            st.dataframe(practice2_result_year_country_df, hide_index=True, use_container_width=True)

        if st.session_state.select_option == options[1]:
            practice2_result_year_driver_df = get_driver_results_per_year_practice2_data(st.session_state.year, st.session_state.selected_drivers)
            practice2_result_year_driver_df['Year'] = practice2_result_year_driver_df['Year'].astype(str)
            st.dataframe(practice2_result_year_driver_df, hide_index=True, use_container_width=True)

        if st.session_state.select_option == options[2]:
            practice2_result_year_country_df = get_practice2_data_data_race_year(st.session_state.country, st.session_state.year)
            fig = plot_time_gap_practice_session(practice2_result_year_country_df, 'FP2')
            st.plotly_chart(fig)
        first_call = False


elif tabs == 'FP3':
    st.title("Practice 3")

    options = ["Practice 3 Results per race", "Practice 3 Results per driver", "Gaps to the leader"]
    years = [2022, 2023, 2024]
    st.session_state.select_option = st.selectbox("Select option:", options, key="practice3_results_plot_option")
    st.session_state.year = st.selectbox("Select year:", years, key="select_year_practice3_results")
    drivers_to_compare = get_drivers_per_year_from_practice3_data(st.session_state.year)['Driver'].tolist()
    drivers_to_compare.insert(0, "All")
    
    if st.session_state.select_option == options[0] or st.session_state.select_option == options[2]:
        st.session_state.country = st.selectbox("Select practice 3:", list(practice3_orders[int(st.session_state.year)].values()), key="select_countries_practice3_results")

    if not st.session_state.select_option == options[0] and not st.session_state.select_option == options[1] and not st.session_state.select_option == options[2]:
        st.session_state.selected_drivers = st.multiselect("Select drivers:", drivers_to_compare, default="All", key="select_drivers_practice3_results")
        if not st.session_state.selected_drivers:
            st.session_state.selected_drivers = ["All"]
    elif st.session_state.select_option == options[1] and not st.session_state.select_option == options[2]:
        st.session_state.selected_drivers = st.selectbox("Select drivers:", drivers_to_compare[1: ], key="select_drivers_practice3_results")
        if not st.session_state.selected_drivers:
            st.session_state.selected_drivers = ["All"]

    st.session_state.generate_button = st.button("Show", key="practice3_result_generate_chart_button")
    first_call = True
    if st.session_state.generate_button or first_call: 
        if st.session_state.select_option == options[0]:
            practice3_result_year_country_df = get_practice3_data_data_race_year(st.session_state.country, st.session_state.year)
            practice3_result_year_country_df['Year'] = practice3_result_year_country_df['Year'].astype(str)
            st.dataframe(practice3_result_year_country_df, hide_index=True, use_container_width=True)

        if st.session_state.select_option == options[1]:
            practice3_result_year_driver_df = get_driver_results_per_year_practice3_data(st.session_state.year, st.session_state.selected_drivers)
            practice3_result_year_driver_df['Year'] = practice3_result_year_driver_df['Year'].astype(str)
            st.dataframe(practice3_result_year_driver_df, hide_index=True, use_container_width=True)

        if st.session_state.select_option == options[2]:
            practice3_result_year_country_df = get_practice3_data_data_race_year(st.session_state.country, st.session_state.year)
            fig = plot_time_gap_practice_session(practice3_result_year_country_df, 'FP3')
            st.plotly_chart(fig)
        first_call = False