import sys
import streamlit as st
import mysql.connector
import pandas as pd
from datetime import datetime, timedelta, time
import plotly.graph_objs as go

sys.tracebacklimit = 0

st.set_page_config(layout="wide", page_title="co2 sensor", page_icon="🧊", initial_sidebar_state="auto",
                   menu_items=None)
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            .block-container {
                    padding-top: 0rem;
                    padding-bottom: 4rem;

                }
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
st.header('Sensors help your business do better.', divider='rainbow')

current_date = datetime.today()
future_date = current_date + timedelta(days=-8)
current_date_up = "%" + current_date.strftime('%Y-%m-%d') + "%"
future_date_up = "%" + future_date.strftime('%Y-%m-%d') + "%"
current_sensor_values = "%" + current_date.strftime('%Y-%m-%d') + "%"


def init_connection():
    try:
        return mysql.connector.connect(**st.secrets["mysql"])
    except mysql.connector.Error as err:
        raise Exception("Something went wrong (╯°益°)╯ ")


conn = init_connection()


def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()


def current_sensor():
    temp_nw = run_query("SELECT `metrics_t` FROM `temperature` WHERE `create_date` LIKE '%s';" %
                        current_sensor_values)
    humidity_nw = run_query("SELECT `metrics_hum` FROM `humidity` WHERE `create_date` LIKE '%s';" %
                            current_sensor_values)
    wea_pre_nw = run_query("SELECT `metrics_p` FROM `weather_pressure` WHERE `create_date` LIKE '%s';" %
                           current_sensor_values)
    co2_nw = run_query("SELECT `metrics_co2` FROM `co2` WHERE `create_date` LIKE '%s';" %
                       current_sensor_values)
    tvoc_nw = run_query("SELECT `metrics_tvoc` FROM `tvoc` WHERE `create_date` LIKE '%s';" %
                        current_sensor_values)
    status_device = run_query("SELECT `status_chek` FROM `status_device` WHERE `status_chek` = '1';")
    temp_status = run_query("SELECT `temperature_status` FROM `status_device` WHERE `temperature_status` = '1';")
    humidity_status = run_query("SELECT `temperature_status` FROM `status_device` WHERE `humidity_status` = '1';")
    weather_pressure_status = run_query("SELECT `temperature_status` FROM `status_device` WHERE "
                                        "`weather_pressure_status` = '1';")
    co2_status = run_query("SELECT `temperature_status` FROM `status_device` WHERE `co2_status` = '1';")
    tvoc_status = run_query("SELECT `temperature_status` FROM `status_device` WHERE `tvoc_status` = '1';")

    if status_device:

        if temp_nw or humidity_nw or wea_pre_nw or co2_nw or tvoc_nw:
            st.title('Current sensor values:')

            if temp_status:
                temp_now = [item[0] for item in temp_nw]
                try:
                    last_temp_now = temp_now[-1]
                    previous_temp_now = temp_now[-2]
                    delta_temp = last_temp_now - previous_temp_now
                    last_temp_now = str(last_temp_now) + " °C"
                    delta_temp = round(delta_temp, 2)
                    delta_temp = str(delta_temp) + " °C"
                except IndexError as e:
                    print(f"Temp___ERRORs {e}")
                    last_temp_now = "Wait..."
                    delta_temp = ""
            else:
                last_temp_now = "Receiving data..."
                delta_temp = ""

            if humidity_status:
                humidity_now = [item[0] for item in humidity_nw]
                try:
                    last_humidity_now = humidity_now[-1]
                    previous_humidity_now = humidity_now[-2]
                    delta_humidity_now = last_humidity_now - previous_humidity_now
                    last_humidity_now = str(last_humidity_now) + " %"
                    delta_humidity_now = round(delta_humidity_now)
                    delta_humidity_now = str(delta_humidity_now) + " %"
                except IndexError as e:
                    print(f"Humidity___ERRORs {e}")
                    last_humidity_now = "Wait..."
                    delta_humidity_now = ""
            else:
                last_humidity_now = "Receiving data..."
                delta_humidity_now = ""

            if weather_pressure_status:
                weather_pressure_now = [item[0] for item in wea_pre_nw]
                try:
                    last_weather_pressure_now = weather_pressure_now[-1]
                    previous_weather_pressure_now = weather_pressure_now[-2]
                    delta_weather_pressure_now = last_weather_pressure_now - previous_weather_pressure_now
                    last_weather_pressure_now = str(last_weather_pressure_now) + " mmhg"
                    delta_weather_pressure_now = round(delta_weather_pressure_now)
                    delta_weather_pressure_now = str(delta_weather_pressure_now) + " mmhg"
                except IndexError as e:
                    print(f"Weather_pressure___ERRORs {e}")
                    last_weather_pressure_now = "Wait..."
                    delta_weather_pressure_now = ""
            else:
                last_weather_pressure_now = "Receiving data..."
                delta_weather_pressure_now = ""

            if co2_status:
                co2_now = [item[0] for item in co2_nw]
                try:
                    last_co2_nw = co2_now[-1]
                    previous_co2_nw = co2_now[-2]
                    delta_co2_nw = last_co2_nw - previous_co2_nw
                    last_co2_nw = str(last_co2_nw) + " ppm"
                    delta_co2_nw = round(delta_co2_nw)
                    delta_co2_nw = str(delta_co2_nw) + " ppm"
                except IndexError as e:
                    print(f"CO_pressure___ERRORs {e}")
                    last_co2_nw = "Wait..."
                    delta_co2_nw = ""
            else:
                last_co2_nw = "Receiving data..."
                delta_co2_nw = ""

            if tvoc_status:
                tvoc_now = [item[0] for item in tvoc_nw]
                try:
                    last_tvoc_now = tvoc_now[-1]
                    previous_tvoc_now = tvoc_now[-2]
                    delta_tvoc_now = last_tvoc_now - previous_tvoc_now
                    last_tvoc_now = str(last_tvoc_now) + " ppb"
                    delta_tvoc_now = round(delta_tvoc_now)
                    delta_tvoc_now = str(delta_tvoc_now) + " ppb"
                except IndexError as e:
                    print(f"Tvoc_now___ERRORs{e}")
                    last_tvoc_now = "Wait..."
                    delta_tvoc_now = ""
            else:
                last_tvoc_now = "Receiving data..."
                delta_tvoc_now = ""

            col1, col2 = st.columns(2)
            col1.metric("CO2 (carbon dioxide concentrations)", f"{last_co2_nw}", f"{delta_co2_nw}", delta_color="inverse")
            col2.metric("TVOC (Total volatile organic compounds)", f"{last_tvoc_now}", f"{delta_tvoc_now}", delta_color="inverse")

            col1, col2 = st.columns(2)
            col1.metric("Temperature", f"{last_temp_now}", f"{delta_temp}")
            col2.metric("Humidity", f"{last_humidity_now}", f"{delta_humidity_now}")
            st.metric(label="Weather Pressure", value=f"{last_weather_pressure_now}")
        else:
            st.title('There is no data to display, please try later')
    else:
        st.header(

            ":orange[***The device is not connected.***]"

        )

    if st.button("Refresh", key='restart_current'):
        st.rerun()


current_sensor()

st.title('Sensor values history:')
select_d = st.date_input("Choose a date:", format="MM.DD.YYYY")
select_date = "%" + select_d.strftime('%Y-%m-%d') + "%"
appointment = st.slider(
    "Schedule your appointment:",
    value=(time(00, 00), time(23, 59)))
st_interval = appointment[0].strftime('%H:%M')
end_interval = appointment[1].strftime('%H:%M')
select_dt_st = str(select_d.strftime('%Y-%m-%d ')) + str(appointment[0])
select_dt_end = str(select_d.strftime('%Y-%m-%d ')) + str(appointment[1])


def co2_sensor():
    temp_co2 = run_query("SELECT `metrics_co2`, `create_date` FROM `co2` WHERE create_date BETWEEN '%s' AND '%s';"
                         % (select_dt_st, select_dt_end))
    if temp_co2:
        try:
            res_co2 = []
            res_time_co2 = []
            try:
                for item in temp_co2:
                    res_co2 += item[0] if isinstance(item[0], tuple) else [item[0]]
                    res_time_co2 += item[1] if isinstance(item[1], tuple) else [item[1]]
            except IndexError as e:
                print(f"res_co2_or_res_time_co2_ {e}")
            d_t = []
            data_hour = []
            data_minutes = []
            data_seconds = []
            try:
                for res3_time in res_time_co2:
                    d_t += [res3_time.strftime('%H:%M:%S')]
                    data_hour += [res3_time.strftime('%H')]
                    data_minutes += [res3_time.strftime('%M')]
                    data_seconds += [res3_time.strftime('%S')]
            except IndexError as e:
                print(f"_time_operations_ERRORs {e}")

            hour_t_seconds = []
            try:
                for data_h in data_hour:
                    hour_t_seconds += [int(data_h) * 3600]
            except IndexError as e:
                print(f"hour_t_seconds_ERRORs {e}")
            data_t_seconds = []
            try:
                for data_m in data_minutes:
                    data_t_seconds += [int(data_m) * 60]
            except IndexError as e:
                print(f"data_t_seconds_ERRORs {e}")
            seconds_t_seconds = []
            try:
                for data_s in data_seconds:
                    seconds_t_seconds += [int(data_s) * 1]
            except IndexError as e:
                print(f"seconds_t_seconds {e}")
            try:
                longer = hour_t_seconds if len(hour_t_seconds) >= len(data_t_seconds) else data_t_seconds
                hour_and_minutes = ([x + y for x, y in zip(hour_t_seconds, data_t_seconds)] +
                                    longer[min(len(hour_t_seconds), len(data_t_seconds)):])

                longer1 = seconds_t_seconds if len(seconds_t_seconds) >= len(hour_and_minutes) else hour_and_minutes
                oll_seconds = ([x + y for x, y in zip(seconds_t_seconds, hour_and_minutes)] +
                               longer1[min(len(seconds_t_seconds), len(hour_and_minutes)):])

                shift_oll_sec = oll_seconds[0:]
                shift_oll_sec1 = oll_seconds[1:]

                interval_t = [a - b for a, b in zip(shift_oll_sec1, shift_oll_sec)]

                if not interval_t:
                    print("no data for calculation*")
                else:
                    temperature_duration = [a * b for a, b in zip(interval_t, res_co2)]

                    total_temperature_duration = round(sum(temperature_duration))

                    total_duration = round(sum(interval_t))

                    weighted_arithmetic_average = round((total_temperature_duration / total_duration), 2)

                    largest_element = max(res_co2, key=lambda x: x)

                    min_element = min(res_co2, key=lambda x: x)

                    data_table = [largest_element] + [min_element] + [weighted_arithmetic_average]

                    st.divider()

                    st.subheader("CO2 (carbon dioxide concentrations) indicators:")

                    df = pd.DataFrame([data_table], columns=['Max ppm', 'Min ppm', 'Average ppm'])

                    st.dataframe(df, hide_index=True)

                    t_p_d = len(res_co2)
                    id_tpd = []
                    for ind in range(t_p_d):
                        id_tpd += [[str(res_co2[ind])] + [d_t[ind]]]

                    on = st.toggle('CO2 per day. Time interval %s - %s' % (st_interval, end_interval), key='co2')
                    if on:
                        df2 = pd.DataFrame(id_tpd, columns=['CO2', 'Time period'])
                        st.dataframe(df2.style.highlight_max('CO2'), hide_index=True)

                    lis = len(d_t)
                    lst1 = [399] * lis
                    lst2 = [599] * lis
                    lst3 = [799] * lis
                    lst4 = [999] * lis
                    lst5 = [1499] * lis
                    lst6 = [2499] * lis
                    lst7 = [3999] * lis
                    lst8 = [4999] * lis
                    lst9 = [7999] * lis
                    lst10 = [10000] * lis

                    filtered_400 = filter(lambda score: 0 <= score <= 399, res_co2)
                    filtered_600 = filter(lambda score: 400 <= score <= 599, res_co2)
                    filtered_800 = filter(lambda score: 600 <= score <= 799, res_co2)
                    filtered_1000 = filter(lambda score: 800 <= score <= 999, res_co2)
                    filtered_1500 = filter(lambda score: 1000 <= score <= 1499, res_co2)
                    filtered_2500 = filter(lambda score: 1500 <= score <= 2499, res_co2)
                    filtered_4000 = filter(lambda score: 2500 <= score <= 3999, res_co2)
                    filtered_5000 = filter(lambda score: 4000 <= score <= 4999, res_co2)
                    filtered_8000 = filter(lambda score: 5000 <= score <= 7999, res_co2)
                    filtered_10000 = filter(lambda score: 8000 <= score <= 9999, res_co2)

                    bool_400 = False
                    bool_600 = False
                    bool_800 = False
                    bool_1000 = False
                    bool_1500 = False
                    bool_2500 = False
                    bool_4000 = False
                    bool_5000 = False
                    bool_8000 = False
                    bool_10000 = False

                    filtered_400_l = (len(list(filtered_400)))
                    if not filtered_400_l:
                        filtered_400_l = 'Null'
                    else:
                        bool_400 = True
                    filtered_600_l = (len(list(filtered_600)))
                    if not filtered_600_l:
                        filtered_600_l = 'Null'
                    else:
                        bool_600 = True
                    filtered_800_l = (len(list(filtered_800)))
                    if not filtered_800_l:
                        filtered_800_l = 'Null'
                    else:
                        bool_800 = True
                    filtered_1000_l = (len(list(filtered_1000)))
                    if not filtered_1000_l:
                        filtered_1000_l = 'Null'
                    else:
                        bool_1000 = True
                    filtered_1500_l = (len(list(filtered_1500)))
                    if not filtered_1500_l:
                        filtered_1500_l = 'Null'
                    else:
                        bool_1500 = True
                    filtered_2500_l = (len(list(filtered_2500)))
                    if not filtered_2500_l:
                        filtered_2500_l = 'Null'
                    else:
                        bool_2500 = True
                    filtered_4000_l = (len(list(filtered_4000)))
                    if not filtered_4000_l:
                        filtered_4000_l = 'Null'
                    else:
                        bool_4000 = True
                    filtered_5000_l = (len(list(filtered_5000)))
                    if not filtered_5000_l:
                        filtered_5000_l = 'Null'
                    else:
                        bool_5000 = True
                    filtered_8000_l = (len(list(filtered_8000)))
                    if not filtered_8000_l:
                        filtered_8000_l = 'Null'
                    else:
                        bool_8000 = True
                    filtered_10000_l = (len(list(filtered_10000)))
                    if not filtered_10000_l:
                        filtered_10000_l = 'Null'
                    else:
                        bool_10000 = True

                    dil_l = [filtered_400_l] + [filtered_600_l] + [filtered_800_l] + [filtered_1000_l] + [
                        filtered_1500_l] + [filtered_2500_l] + [filtered_4000_l] + [filtered_5000_l] + [
                                filtered_8000_l] + [
                                filtered_10000_l]

                    st.markdown("**Co2 level (according to ASHRAE CO2 Standards)**")

                    fig = go.Figure()
                    fig.add_trace(go.Scatter(x=d_t, y=lst1, fill='tonexty', fillcolor="rgba(0,252,23, 0.7)",
                                             mode='none', name='Excellent, 0 - 400 PPM', visible=bool_400,
                                             connectgaps=True,
                                             # override default markers+lines
                                             ))
                    fig.add_trace(go.Scatter(x=d_t, y=lst2, fill='tonexty', fillcolor='rgba(92,237,121, 0.7)',
                                             mode='none', name='Very Good, 400 - 600 PPM', visible=bool_600))
                    fig.add_trace(go.Scatter(x=d_t, y=lst3, fill='tonexty', fillcolor='rgba(181,235,73, 0.7)',
                                             mode='none', name='Good, 600 - 800 PPM', visible=bool_800))
                    fig.add_trace(go.Scatter(x=d_t, y=lst4, fill='tonexty', fillcolor='rgba(219,222,37, 0.7)',
                                             mode='none', name='Medium, 800 - 1000 PPM', visible=bool_1000))
                    fig.add_trace(go.Scatter(x=d_t, y=lst5, fill='tonexty', fillcolor='rgba(230,171,27, 0.7)',
                                             mode='none', name='Poor, 1000 - 1500 PPM', visible=bool_1500))
                    fig.add_trace(go.Scatter(x=d_t, y=lst6, fill='tonexty', fillcolor='rgba(203,131,26, 0.7)',
                                             mode='none', name='Inadequate, 1500 - 2500 PPM', visible=bool_2500))
                    fig.add_trace(go.Scatter(x=d_t, y=lst7, fill='tonexty', fillcolor='rgba(219,89,15, 0.7)',
                                             mode='none', name='Bad, 2500 - 4000 PPM', visible=bool_4000))
                    fig.add_trace(go.Scatter(x=d_t, y=lst8, fill='tonexty', fillcolor='rgba(226,38,11, 0.7)',
                                             mode='none', name='Very Bad, 4000 - 5000 PPM', visible=bool_5000))
                    fig.add_trace(go.Scatter(x=d_t, y=lst9, fill='tonexty', fillcolor='rgba(142,5,5, 0.7)',
                                             mode='none', name='Dangerous, 5000 - 8000 PPM', visible=bool_8000))
                    fig.add_trace(go.Scatter(x=d_t, y=lst10, fill='tonexty', fillcolor='rgba(105,7,7, 0.7)',
                                             mode='none', name='Very dangerous, 8000 - 10000 PPM', visible=bool_10000))
                    fig.add_trace(go.Scatter(x=d_t, y=res_co2,
                                             mode='lines', name='Index PPM',
                                             line=dict(width=2, color='rgb(122,122,122)')
                                             ))
                    config = {'displayModeBar': False}
                    fig.update_xaxes(tickangle=45)
                    fig.update_layout(xaxis_title="Time",
                                      legend=dict(font=dict(size=14),
                                                  bordercolor="Black",
                                                  borderwidth=0.3,
                                                  yanchor="top",
                                                  y=15,
                                                  xanchor="left",
                                                  x=0.01))
                    st.plotly_chart(fig, use_container_width=True, config=config)

                    labels = ['Excellent', 'Very Good', 'Good', 'Medium', 'Poor', 'Inadequate', 'Bad', 'Very Bad',
                              'Dangerous', 'Very dangerous']
                    colors = ['rgba(0,252,23, 0.8)', 'rgba(92,237,121, 0.8)', 'rgba(181,235,73, 0.8)',
                              'rgba(219,222,37, 0.8)', 'rgba(230,171,27, 0.8)', 'rgba(203,131,26, 0.8)',
                              'rgba(219,89,15, 0.8)', 'rgba(226,38,11, 0.8)', 'rgba(142,5,5, 0.8)',
                              'rgba(105,7,7, 0.8)']

                    fig2 = go.Figure(data=[go.Pie(labels=labels, values=dil_l, name="CO2",
                                                  marker=dict(colors=colors, line=dict(color='#000000', width=2)))])
                    fig2.update_traces(hole=.4, hoverinfo="label+percent+name")

                    fig2.update_layout(
                        title_text="PPM indicators in percent %",
                        uniformtext_minsize=10, uniformtext_mode='hide',
                        legend=dict(font=dict(size=12)),
                        margin=dict(
                            l=0,
                            r=0,
                            b=0,
                            t=50,
                            pad=0
                        ),
                        annotations=[dict(text='PPM', x=0.50, y=0.5, font_size=20, showarrow=False)])
                    st.plotly_chart(fig2, use_container_width=True, config=config)

            except IndexError as e:
                print(f"data_for_statistics {e}")
                st.subheader('Something went wrong (:!')
                st.write("Please try again later")

        except IndexError as e:
            print(f"OLL__temperature_sensor_ERRORs {e}")

    else:
        print('Wait...')


co2_sensor()


def tvoc_sensor():
    temp_tvoc = run_query(
        "SELECT `metrics_tvoc`, `create_date` FROM `tvoc` "
        "WHERE create_date BETWEEN '%s' AND '%s';" % (select_dt_st, select_dt_end))
    if temp_tvoc:
        try:
            res_tvoc = []
            res_time_tvoc = []
            try:
                for item in temp_tvoc:
                    res_tvoc += item[0] if isinstance(item[0], tuple) else [item[0]]
                    res_time_tvoc += item[1] if isinstance(item[1], tuple) else [item[1]]
            except IndexError as e:
                print(f"res_tvoc_or_res_time_tvoc_ERRORs {e}")
            d_t = []
            data_hour = []
            data_minutes = []
            data_seconds = []
            try:
                for res3_time in res_time_tvoc:
                    d_t += [res3_time.strftime('%H:%M:%S')]
                    data_hour += [res3_time.strftime('%H')]
                    data_minutes += [res3_time.strftime('%M')]
                    data_seconds += [res3_time.strftime('%S')]
            except IndexError as e:
                print(f"_time_operations_ERRORs {e}")

            hour_t_seconds = []
            try:
                for data_h in data_hour:
                    hour_t_seconds += [int(data_h) * 3600]
            except IndexError as e:
                print(f"hour_t_seconds_ERRORs {e}")
            data_t_seconds = []
            try:
                for data_m in data_minutes:
                    data_t_seconds += [int(data_m) * 60]
            except IndexError as e:
                print(f"data_t_seconds_ERRORs {e}")
            seconds_t_seconds = []
            try:
                for data_s in data_seconds:
                    seconds_t_seconds += [int(data_s) * 1]
            except IndexError as e:
                print(f"seconds_t_seconds {e}")
            try:
                longer = hour_t_seconds if len(hour_t_seconds) >= len(data_t_seconds) else data_t_seconds
                hour_and_minutes = ([x + y for x, y in zip(hour_t_seconds, data_t_seconds)] +
                                    longer[min(len(hour_t_seconds), len(data_t_seconds)):])

                longer1 = seconds_t_seconds if len(seconds_t_seconds) >= len(hour_and_minutes) else hour_and_minutes
                oll_seconds = ([x + y for x, y in zip(seconds_t_seconds, hour_and_minutes)] +
                               longer1[min(len(seconds_t_seconds), len(hour_and_minutes)):])

                shift_oll_sec = oll_seconds[0:]
                shift_oll_sec1 = oll_seconds[1:]

                interval_t = [a - b for a, b in zip(shift_oll_sec1, shift_oll_sec)]

                if not interval_t:
                    print("no data for calculation*")
                else:
                    temperature_duration = [a * b for a, b in zip(interval_t, res_tvoc)]

                    total_temperature_duration = round(sum(temperature_duration))

                    total_duration = round(sum(interval_t))

                    weighted_arithmetic_average = round((total_temperature_duration / total_duration), 2)

                    largest_element = max(res_tvoc, key=lambda x: x)

                    min_element = min(res_tvoc, key=lambda x: x)

                    data_table = [largest_element] + [min_element] + [weighted_arithmetic_average]

                    st.divider()

                    st.subheader("TVOC indicators:")

                    agree = st.checkbox(
                        'What is TVOC? End how TVOC affects indoor air quality: effects on wellbeing and health')
                    if agree:
                        st.write(
                            'When we think of air quality, people mostly think of the outside world, smog from cars and industry or the fresh air of woods. However, 90% of our daily life is spent indoors: our home, workplace, public buildings and schools. Indoor quality is one of the most important components of well-being, feeling comfortable in a room.  Besides, bad air quality has implications on your productivity and may even harm your health. The Volatile organic components (VOC) may be the least known.')
                        st.subheader('TVOCS affects the wellbeing, feeling comfortable and health')
                        st.write(
                            'TVOCs affect your sense off wellbeing and if you feel comfortable inside a building. Some VOC’s are even bad for health. Some VOCs are more harmful than others. If a TVOC is harmful also depend on factors as level of exposure and length of time being exposed. Besides, some people -especially children and elderly people- have a higher sensibility then others. Immediate symptoms that some people have experienced soon after exposure to VOCs are eye and respiratory tract irritation, headaches, dizziness, visual disorders and memory impairment. An example: some people get immediately a headache from being in a room which is just painted. Others may find the smell just uncomfortable.')
                        st.markdown("""
                        ***TVOCs can cause:***
                        * Headaches
                        * Dizziness 
                        * Nausea
                        * Eye, nose, and throat irritation
                        * Coordination loss
                        * Fatigue
                        * Some VOC’s (as toluene) cause irritation at normal levels, eg allergic skin reactions
                        * Bad odor and stale air are uncomfortable and affect people’s feeling of cleanliness
                        * Some VOC’s as formaldehyde can cause cancer. VOC’s for a long-term exposure in large doses can damage liver, nervous system and kidneys 
                                    """)
                        st.subheader('What is TVOC?')
                        st.write(
                            'What is TVOC? TVOC means Total Volatile Organic compounds. Volatile organic compounds are organic chemicals that become a gas at room temperature. There are thousands of VOCs and a multiple of VOC’s are at the same time present. Therefore, the Total VOC is used at most times: measuring the concentration of the total of VOC’s This is easier and less expensive then measuring individual VOC’s.')
                        st.markdown("""
                        ***Some examples of VOC’s are:***
                        * Benzene
                        * Ethylene glycol
                        * Formaldehyde
                        * Methylene chloride
                        * Tetrachloroethylene
                        * Toluene                
                        """)
                        st.subheader('Where do you find VOC’s?')
                        st.markdown("""
                        VOC’s come from many sources, even yourself can be a polluter!

                        * Products
                        * Outside world


                        VOC in Products


                        Many VOC’s come from:



                        * Cleaners and disinfectants
                        * Pesticides
                        * Air fresheners
                        * Paints and solvents
                        * Glue
                        * New furniture and carpets
                        * Construction materials
                        * Electronic devices
                        * Plywood

                        So, some VOC’s may come from everyday life, especially found in sprays and aerosols from cleaners and such. Besides, new construction and renovation may cause significant health concerns. Construction materials, but also the new furniture, carpets and plywood may increase the indoor concentration of VOC’s due to off-gassing. Until the off-gassing has declined, those new products may cause serious threats to your well-being. You can be a polluter yourself, however often far less dangerous then products do.

                        VOC in the outside world

                        Vehicle exhaust and indusstry pollution may also cause bad indoor air quality when the polluted air can enter the building due to open windows or air condition that doesn’t work properly. Especially when the building stands in congested or industrial areas.



                        """)

                    df = pd.DataFrame([data_table], columns=['Max ppb', 'Min ppb', 'Average ppb'])

                    st.dataframe(df, hide_index=True)

                    t_p_d = len(res_tvoc)
                    id_tpd = []
                    for ind in range(t_p_d):
                        id_tpd += [[str(res_tvoc[ind])] + [d_t[ind]]]

                    on = st.toggle('TVOC per day. Time interval %s - %s' % (st_interval, end_interval), key='tvoc')
                    if on:
                        df2 = pd.DataFrame(id_tpd, columns=['TVOC', 'Time period'])
                        st.dataframe(df2.style.highlight_max('TVOC'), hide_index=True)

                    lis = len(d_t)
                    lst1 = [220] * lis
                    lst2 = [660] * lis
                    lst3 = [1430] * lis
                    lst4 = [2200] * lis
                    lst5 = [3300] * lis
                    lst6 = [5500] * lis

                    filtered_220 = filter(lambda score: 0 <= score <= 220, res_tvoc)
                    filtered_660 = filter(lambda score: 221 <= score <= 660, res_tvoc)
                    filtered_1430 = filter(lambda score: 661 <= score <= 1430, res_tvoc)
                    filtered_2200 = filter(lambda score: 1431 <= score <= 2200, res_tvoc)
                    filtered_3300 = filter(lambda score: 2201 <= score <= 3300, res_tvoc)
                    filtered_5500 = filter(lambda score: 3301 <= score <= 5500, res_tvoc)

                    bool_220 = True
                    bool_660 = False
                    bool_1430 = False
                    bool_2200 = False
                    bool_3300 = False
                    bool_5500 = False

                    filtered_220_l = (len(list(filtered_220)))
                    if not filtered_220_l:
                        filtered_220_l = 'Null'
                    else:
                        bool_220 = True
                    filtered_660_l = (len(list(filtered_660)))
                    if not filtered_660_l:
                        filtered_660_l = 'Null'
                    else:
                        bool_660 = True
                    filtered_1430_l = (len(list(filtered_1430)))
                    if not filtered_1430_l:
                        filtered_1430_l = 'Null'
                    else:
                        bool_1430 = True
                    filtered_2200_l = (len(list(filtered_2200)))
                    if not filtered_2200_l:
                        filtered_2200_l = 'Null'
                    else:
                        bool_2200 = True
                    filtered_3300_l = (len(list(filtered_3300)))
                    if not filtered_3300_l:
                        filtered_3300_l = 'Null'
                    else:
                        bool_3300 = True
                    filtered_5500_l = (len(list(filtered_5500)))
                    if not filtered_5500_l:
                        filtered_5500_l = 'Null'
                    else:
                        bool_5500 = True

                    dil_l = [filtered_220_l] + [filtered_660_l] + [filtered_1430_l] + [filtered_2200_l] + [
                        filtered_3300_l] + [filtered_5500_l]

                    st.markdown("**TVOC level (ISO 13199:2012)**")

                    fig = go.Figure()
                    fig.add_trace(go.Scatter(x=d_t, y=lst1, fill='tonexty', fillcolor="rgba(80,164,108, 0.7)",
                                             mode='none', name='Good, 0 - 220 ppb', visible=bool_220,
                                             ))
                    fig.add_trace(go.Scatter(x=d_t, y=lst2, fill='tonexty', fillcolor='rgba(243,205,81, 0.7)',
                                             mode='none', name='Moderate, 221 - 660 ppb', visible=bool_660))
                    fig.add_trace(go.Scatter(x=d_t, y=lst3, fill='tonexty', fillcolor='rgba(236,160,103, 0.7)',
                                             mode='none', name='Poor, 661 - 1430 ppb', visible=bool_1430))
                    fig.add_trace(go.Scatter(x=d_t, y=lst4, fill='tonexty', fillcolor='rgba(254,84,78, 0.7)',
                                             mode='none', name='High, 1431 - 2200 ppb', visible=bool_2200))
                    fig.add_trace(go.Scatter(x=d_t, y=lst5, fill='tonexty', fillcolor='rgba(110,70,241, 0.7)',
                                             mode='none', name='Very High, 2201 - 3300 ppb', visible=bool_3300))
                    fig.add_trace(go.Scatter(x=d_t, y=lst6, fill='tonexty', fillcolor='rgba(117,56,133, 0.7)',
                                             mode='none', name='Unhealthy, 3301 - 5500 ppb', visible=bool_5500))
                    fig.add_trace(go.Scatter(x=d_t, y=res_tvoc,
                                             mode='lines', name='Index PPB',
                                             line=dict(width=2, color='rgb(122,122,122)')
                                             ))
                    config = {'displayModeBar': False}
                    fig.update_xaxes(tickangle=45)
                    fig.update_layout(xaxis_title="Time",
                                      legend=dict(font=dict(size=14),
                                                  bordercolor="Black",
                                                  borderwidth=0.3,
                                                  yanchor="top",
                                                  y=15,
                                                  xanchor="left",
                                                  x=0.01))
                    st.plotly_chart(fig, use_container_width=True, config=config)

                    labels = ['Good', 'Moderate', 'Poor', 'High', 'Very High', 'Unhealthy']
                    colors = ['rgba(80,164,108, 0.8)', 'rgba(243,205,81, 0.8)', 'rgba(236,160,103, 0.8)',
                              'rgba(254,84,78, 0.8)', 'rgba(110,70,241, 0.8)', 'rgba(117,56,133, 0.8)']

                    fig2 = go.Figure(data=[go.Pie(labels=labels, values=dil_l, name="TVOC",
                                                  marker=dict(colors=colors, line=dict(color='#000000', width=2)))])
                    fig2.update_traces(hole=.4, hoverinfo="label+percent+name")

                    fig2.update_layout(
                        title_text="TVOC indicators in percent %",
                        uniformtext_minsize=10, uniformtext_mode='hide',
                        legend=dict(font=dict(size=12)),
                        margin=dict(
                            l=0,
                            r=0,
                            b=0,
                            t=50,
                            pad=0
                        ),
                        annotations=[dict(text='TVOC', x=0.50, y=0.5, font_size=20, showarrow=False)])
                    st.plotly_chart(fig2, use_container_width=True, config=config)

            except IndexError as e:
                print(f"data_for_statistics {e}")
                st.subheader('Something went wrong (:!')
                st.write("Please try again later")

        except IndexError as e:
            print(f"OLL__tvoc_sensor_ERRORs {e}")

    else:
        print('Wait...')


tvoc_sensor()


def temperature_sensor():
    temp_oll = run_query("SELECT `metrics_t`, `create_date` FROM `temperature` WHERE create_date BETWEEN '%s' AND '%s';"
                         % (select_dt_st, select_dt_end))
    if temp_oll:
        try:
            res_t = []
            res_time = []
            try:
                for item in temp_oll:
                    res_t += item[0] if isinstance(item[0], tuple) else [item[0]]
                    res_time += item[1] if isinstance(item[1], tuple) else [item[1]]
            except IndexError as e:
                print(f"res_t_or_res_time_ERRORs {e}")
            d_t = []
            data_hour = []
            data_minutes = []
            data_seconds = []
            try:
                for res3_time in res_time:
                    d_t += [res3_time.strftime('%H:%M:%S')]
                    data_hour += [res3_time.strftime('%H')]
                    data_minutes += [res3_time.strftime('%M')]
                    data_seconds += [res3_time.strftime('%S')]
            except IndexError as e:
                print(f"_time_operations_ERRORs {e}")

            hour_t_seconds = []
            try:
                for data_h in data_hour:
                    hour_t_seconds += [int(data_h) * 3600]
            except IndexError as e:
                print(f"hour_t_seconds_ERRORs {e}")
            data_t_seconds = []
            try:
                for data_m in data_minutes:
                    data_t_seconds += [int(data_m) * 60]
            except IndexError as e:
                print(f"data_t_seconds_ERRORs {e}")
            seconds_t_seconds = []
            try:
                for data_s in data_seconds:
                    seconds_t_seconds += [int(data_s) * 1]
            except IndexError as e:
                print(f"seconds_t_seconds {e}")
            try:
                longer = hour_t_seconds if len(hour_t_seconds) >= len(data_t_seconds) else data_t_seconds
                hour_and_minutes = ([x + y for x, y in zip(hour_t_seconds, data_t_seconds)] +
                                    longer[min(len(hour_t_seconds), len(data_t_seconds)):])

                longer1 = seconds_t_seconds if len(seconds_t_seconds) >= len(hour_and_minutes) else hour_and_minutes
                oll_seconds = ([x + y for x, y in zip(seconds_t_seconds, hour_and_minutes)] +
                               longer1[min(len(seconds_t_seconds), len(hour_and_minutes)):])

                shift_oll_sec = oll_seconds[0:]
                shift_oll_sec1 = oll_seconds[1:]

                interval_t = [a - b for a, b in zip(shift_oll_sec1, shift_oll_sec)]

                if not interval_t:
                    print("no data for calculation*")
                else:
                    temperature_duration = [a * b for a, b in zip(interval_t, res_t)]

                    total_temperature_duration = round(sum(temperature_duration))

                    total_duration = round(sum(interval_t))

                    weighted_arithmetic_average = round((total_temperature_duration / total_duration), 2)

                    largest_element = max(res_t, key=lambda x: x)

                    min_element = min(res_t, key=lambda x: x)

                    def tem_average(tem_av):
                        return sum(tem_av) / len(tem_av)

                    lst = res_t
                    average_t = tem_average(lst)
                    average_t = round(average_t, 2)

                    data_table = [largest_element] + [min_element] + [average_t] + [weighted_arithmetic_average]

                    st.divider()

                    st.subheader("Temperature indicators:")

                    df = pd.DataFrame([data_table], columns=['Max °C', 'Min °C', 'Average °C', 'Average °C feeling'])

                    st.dataframe(df, hide_index=True)

                    t_p_d = len(res_t)
                    id_tpd = []
                    for ind in range(t_p_d):
                        id_tpd += [[str(res_t[ind])] + [d_t[ind]]]

                    on = st.toggle('Temperature per day. Time interval %s - %s' % (st_interval, end_interval),
                                   key='temperature')
                    if on:
                        df2 = pd.DataFrame(id_tpd, columns=['Temperature', 'Time period'])
                        st.dataframe(df2.style.highlight_max('Temperature'), hide_index=True)

                    bool_t_p49 = False
                    bool_t_p42 = False
                    bool_t_p35 = False
                    bool_t_p28 = False
                    bool_t_p21 = False
                    bool_t_p14 = True
                    bool_t_p7 = True
                    bool_t_z0 = True
                    bool_t_m7 = False
                    bool_t_m14 = False
                    bool_t_m21 = False

                    ar_list = len(d_t)

                    art_p49 = [60] * ar_list
                    art_p42 = [48.99] * ar_list
                    art_p35 = [41.99] * ar_list
                    art_p28 = [34.99] * ar_list
                    art_p21 = [27.99] * ar_list
                    art_p14 = [20.99] * ar_list
                    art_p7 = [13.99] * ar_list
                    art_z0 = [6.99] * ar_list
                    art_m7 = [-7] * ar_list
                    art_m14 = [-14] * ar_list
                    art_m21 = [-30] * ar_list

                    fil_t_p49 = filter(lambda score: 49.00 <= score <= 60.00, res_t)
                    fil_t_p42 = filter(lambda score: 43.00 <= score <= 48.99, res_t)
                    fil_t_p35 = filter(lambda score: 35.00 <= score <= 41.99, res_t)
                    fil_t_p28 = filter(lambda score: 28.00 <= score <= 34.99, res_t)
                    fil_t_p21 = filter(lambda score: 21.00 <= score <= 27.99, res_t)
                    fil_t_p14 = filter(lambda score: 14.00 <= score <= 20.99, res_t)
                    fil_t_p7 = filter(lambda score: 7.00 <= score <= 13.99, res_t)
                    fil_t_z0 = filter(lambda score: 0.00 <= score <= 6.99, res_t)
                    fil_t_m7 = filter(lambda score: -0.01 >= score >= -7, res_t)
                    fil_t_m14 = filter(lambda score: -7.01 >= score >= -14, res_t)
                    fil_t_m21 = filter(lambda score: -14.01 >= score >= -30, res_t)

                    len_f_p49 = (len(list(fil_t_p49)))
                    if not len_f_p49:
                        len_f_p49 = 'Null'
                    else:
                        bool_t_p49 = True
                    len_f_p42 = (len(list(fil_t_p42)))
                    if not len_f_p42:
                        len_f_p42 = 'Null'
                    else:
                        bool_t_p42 = True
                    len_f_p35 = (len(list(fil_t_p35)))
                    if not len_f_p35:
                        len_f_p35 = 'Null'
                    else:
                        bool_t_p35 = True
                    len_f_p28 = (len(list(fil_t_p28)))
                    if not len_f_p28:
                        len_f_p28 = 'Null'
                    else:
                        bool_t_p28 = True
                    len_f_p21 = (len(list(fil_t_p21)))
                    if not len_f_p21:
                        len_f_p21 = 'Null'
                    else:
                        bool_t_p21 = True
                    len_f_p14 = (len(list(fil_t_p14)))
                    if not len_f_p14:
                        len_f_p14 = 'Null'
                    else:
                        bool_t_p14 = True
                    len_f_p7 = (len(list(fil_t_p7)))
                    if not len_f_p7:
                        len_f_p7 = 'Null'
                    else:
                        bool_t_p7 = True
                    len_f_z0 = (len(list(fil_t_z0)))
                    if not len_f_z0:
                        len_f_z0 = 'Null'
                    else:
                        bool_t_z0 = True
                    len_f_m7 = (len(list(fil_t_m7)))
                    if not len_f_m7:
                        len_f_m7 = 'Null'
                    else:
                        bool_t_m7 = True
                    len_f_m14 = (len(list(fil_t_m14)))
                    if not len_f_m14:
                        len_f_m14 = 'Null'
                    else:
                        bool_t_m14 = True
                    len_f_m21 = (len(list(fil_t_m21)))
                    if not len_f_m21:
                        len_f_m21 = 'Null'
                    else:
                        bool_t_m21 = True

                    dil_2l3 = [len_f_p49] + [len_f_p42] + [len_f_p35] + [len_f_p28] + [len_f_p21] + [
                        len_f_p14] + [len_f_p7] + [len_f_z0] + [len_f_m7] + [len_f_m14] + [len_f_m21]

                    fig4 = go.Figure()

                    fig4.add_trace(go.Scatter(x=d_t, y=art_m21,
                                              fill='tonexty',
                                              fillcolor="rgba(69,9,232, 0.6)",
                                              mode='none',
                                              name='(-14) ÷ (-21) C°',
                                              visible=bool_t_m21))
                    fig4.add_trace(go.Scatter(x=d_t, y=art_m14,
                                              fill='tonexty',
                                              fillcolor="rgba(51,127,214, 0.6)",
                                              mode='none',
                                              name='(-7) ÷ (-14) C°',
                                              visible=bool_t_m14))
                    fig4.add_trace(go.Scatter(x=d_t, y=art_m7,
                                              fill='tonexty',
                                              fillcolor="rgba(69,174,186, 0.6)",
                                              mode='none',
                                              name='0 ÷ (-7) C°',
                                              visible=bool_t_m7))
                    fig4.add_trace(go.Scatter(x=d_t, y=art_z0,
                                              fill='tonexty',
                                              fillcolor="rgba(133,242,239, 0.6)",
                                              mode='none',
                                              name='0 ÷ 7 C°',
                                              visible=bool_t_z0))

                    fig4.add_trace(go.Scatter(x=d_t, y=art_p7,
                                              fill='tonexty',
                                              fillcolor="rgba(78,230,182, 0.6)",
                                              mode='none',
                                              name='7 ÷ 14 C°',
                                              visible=bool_t_p7))

                    fig4.add_trace(go.Scatter(x=d_t, y=art_p14,
                                              fill='tonexty',
                                              fillcolor="rgba(5,252,145, 0.6)",
                                              mode='none',
                                              name='14 ÷ 21 C°',
                                              visible=bool_t_p14))
                    fig4.add_trace(go.Scatter(x=d_t, y=art_p21,
                                              fill='tonexty',
                                              fillcolor="rgba(37,181,29, 0.6)",
                                              mode='none',
                                              name='21 ÷ 28 C°',
                                              visible=bool_t_p21))
                    fig4.add_trace(go.Scatter(x=d_t, y=art_p28,
                                              fill='tonexty',
                                              fillcolor="rgba(255,255,0, 0.6)",
                                              mode='none',
                                              name='28 ÷ 35 C°',
                                              visible=bool_t_p28))
                    fig4.add_trace(go.Scatter(x=d_t, y=art_p35,
                                              fill='tonexty',
                                              fillcolor="rgba(255,192,0, 0.6)",
                                              mode='none',
                                              name='35 ÷ 42 C°',
                                              visible=bool_t_p35))
                    fig4.add_trace(go.Scatter(x=d_t, y=art_p42,
                                              fill='tonexty',
                                              fillcolor="rgba(255,0,0, 0.6)",
                                              mode='none',
                                              name='42 ÷ 49 C°',
                                              visible=bool_t_p42))
                    fig4.add_trace(go.Scatter(x=d_t, y=art_p49,
                                              fill='tonexty',
                                              fillcolor="rgba(192,0,0, 0.6)",
                                              mode='none',
                                              name='49 ÷ 80 C°',
                                              visible=bool_t_p49))

                    fig4.add_trace(go.Scatter(x=d_t, y=res_t,
                                              mode='lines', name='Temperature C°',
                                              line=dict(width=2, color='rgb(122,122,122)')))
                    config = {'displayModeBar': False}
                    fig4.update_xaxes(tickangle=45)
                    fig4.update_layout(xaxis_title="Time",
                                       legend=dict(font=dict(size=14),
                                                   bordercolor="Black",
                                                   borderwidth=0.3,
                                                   yanchor="top",
                                                   y=15,
                                                   xanchor="left",
                                                   x=0.01))
                    st.plotly_chart(fig4, use_container_width=True, config=config)

            except IndexError as e:
                print(f"data_for_statistics {e}")
                st.subheader('Something went wrong (:!')
                st.write("Please try again later")

        except IndexError as e:
            print(f"OLL__temperature_sensor_ERRORs {e}")

    else:
        print('Wait...')


temperature_sensor()


def humidity_sensor():
    humidity_oll = run_query(
        "SELECT `metrics_hum`, `create_date` FROM `humidity` "
        "WHERE create_date BETWEEN '%s' AND '%s';" % (select_dt_st, select_dt_end))
    if humidity_oll:
        try:
            res_h = []
            res_hime_h = []
            try:
                for item in humidity_oll:
                    res_h += item[0] if isinstance(item[0], tuple) else [item[0]]
                    res_hime_h += item[1] if isinstance(item[1], tuple) else [item[1]]
            except IndexError as e:
                print(f"res_h_or_res_hime_h_ERRORs {e}")
            d_t = []
            data_hour = []
            data_minutes = []
            data_seconds = []
            try:
                for res3_time in res_hime_h:
                    d_t += [res3_time.strftime('%H:%M:%S')]
                    data_hour += [res3_time.strftime('%H')]
                    data_minutes += [res3_time.strftime('%M')]
                    data_seconds += [res3_time.strftime('%S')]
            except IndexError as e:
                print(f"_time_operations_ERRORs {e}")

            hour_t_seconds = []
            try:
                for data_h in data_hour:
                    hour_t_seconds += [int(data_h) * 3600]
            except IndexError as e:
                print(f"hour_t_seconds_ERRORs {e}")
            data_t_seconds = []
            try:
                for data_m in data_minutes:
                    data_t_seconds += [int(data_m) * 60]
            except IndexError as e:
                print(f"data_t_seconds_ERRORs {e}")
            seconds_t_seconds = []
            try:
                for data_s in data_seconds:
                    seconds_t_seconds += [int(data_s) * 1]
            except IndexError as e:
                print(f"seconds_t_seconds {e}")
            try:
                longer = hour_t_seconds if len(hour_t_seconds) >= len(data_t_seconds) else data_t_seconds
                hour_and_minutes = ([x + y for x, y in zip(hour_t_seconds, data_t_seconds)] +
                                    longer[min(len(hour_t_seconds), len(data_t_seconds)):])

                longer1 = seconds_t_seconds if len(seconds_t_seconds) >= len(hour_and_minutes) else hour_and_minutes
                oll_seconds = ([x + y for x, y in zip(seconds_t_seconds, hour_and_minutes)] +
                               longer1[min(len(seconds_t_seconds), len(hour_and_minutes)):])

                shift_oll_sec = oll_seconds[0:]
                shift_oll_sec1 = oll_seconds[1:]

                interval_t = [a - b for a, b in zip(shift_oll_sec1, shift_oll_sec)]

                if not interval_t:
                    print("no data for calculation*")
                else:
                    temperature_duration = [a * b for a, b in zip(interval_t, res_h)]

                    total_temperature_duration = round(sum(temperature_duration))

                    total_duration = round(sum(interval_t))

                    weighted_arithmetic_average = round((total_temperature_duration / total_duration), 2)

                    largest_element = max(res_h, key=lambda x: x)

                    min_element = min(res_h, key=lambda x: x)

                    def tem_average(tem_av):
                        return sum(tem_av) / len(tem_av)

                    lst = res_h
                    average_t = tem_average(lst)
                    average_t = round(average_t, 2)

                    data_table = [largest_element] + [min_element] + [average_t] + [weighted_arithmetic_average]

                    st.divider()

                    st.subheader("Humidity indicators:")

                    df_h = pd.DataFrame([data_table], columns=['Max %', 'Min %', 'Average %', 'Average % feeling'])

                    st.dataframe(df_h, hide_index=True)

                    t_p_d = len(res_h)
                    id_tpd = []
                    for ind in range(t_p_d):
                        id_tpd += [[str(res_h[ind])] + [d_t[ind]]]

                    on_h = st.toggle('Humidity per day. Time interval %s - %s' % (st_interval, end_interval),
                                     key='humidity')
                    if on_h:
                        df2_h = pd.DataFrame(id_tpd, columns=['Humidity', 'Time period'])
                        st.dataframe(df2_h.style.highlight_max('Humidity'), hide_index=True)

                    bool_h1 = True
                    bool_h2 = True
                    bool_h3 = True

                    ar_list = len(res_h)

                    art_h_1 = [39] * ar_list
                    art_h_2 = [69] * ar_list
                    art_h_3 = [100] * ar_list

                    fil_h_1 = filter(lambda score: 0 <= score <= 39, res_h)
                    fil_h_2 = filter(lambda score: 40 <= score <= 69, res_h)
                    fil_h_3 = filter(lambda score: 70 <= score <= 100, res_h)

                    len_f_h1 = (len(list(fil_h_1)))
                    if not len_f_h1:
                        len_f_h1 = 'Null'
                    else:
                        bool_h1 = True
                    len_f_h2 = (len(list(fil_h_2)))
                    if not len_f_h2:
                        len_f_h2 = 'Null'
                    else:
                        bool_h2 = True
                    len_f_h3 = (len(list(fil_h_3)))
                    if not len_f_h3:
                        len_f_h3 = 'Null'
                    else:
                        bool_h3 = True

                    st.markdown("**Humidity level**")

                    fig = go.Figure()
                    fig.add_trace(go.Scatter(x=d_t, y=art_h_1, fill='tonexty', fillcolor="rgba(194,5,65, 0.7)",
                                             mode='none', name='To dry, 0% - 39%', visible=bool_h1,
                                             ))
                    fig.add_trace(go.Scatter(x=d_t, y=art_h_2, fill='tonexty', fillcolor='rgba(32,146,158, 0.7)',
                                             mode='none', name='Optimal 40% - 69%', visible=bool_h2))
                    fig.add_trace(go.Scatter(x=d_t, y=art_h_3, fill='tonexty', fillcolor='rgba(1,58,250, 0.7)',
                                             mode='none', name='Too humid 70% - 100%', visible=bool_h3))
                    fig.add_trace(go.Scatter(x=d_t, y=res_h,
                                             mode='lines', name='Humidity %',
                                             line=dict(width=2, color='rgb(255,255,255)')
                                             ))
                    config = {'displayModeBar': False}
                    fig.update_xaxes(tickangle=45)
                    fig.update_layout(xaxis_title="Time", yaxis_title="Humidity %",
                                      legend=dict(font=dict(size=14),
                                                  bordercolor="Black",
                                                  borderwidth=0.3,
                                                  yanchor="top",
                                                  y=15,
                                                  xanchor="left",
                                                  x=0.01))
                    st.plotly_chart(fig, use_container_width=True, config=config)

            except IndexError as e:
                print(f"data_for_statistics {e}")
                st.subheader('Something went wrong (:!')
                st.write("Please try again later")

        except IndexError as e:
            print(f"OLL__humidity_sensor_ERRORs {e}")

    else:
        print('Wait...')


humidity_sensor()


def weather_pressure_s():
    wp_oll = run_query(
        "SELECT `metrics_p`, `create_date` FROM `weather_pressure` "
        "WHERE create_date BETWEEN '%s' AND '%s';" % (select_dt_st, select_dt_end))
    if wp_oll:
        try:
            res_wp = []
            res_time_wp = []
            try:
                for item in wp_oll:
                    res_wp += item[0] if isinstance(item[0], tuple) else [item[0]]
                    res_time_wp += item[1] if isinstance(item[1], tuple) else [item[1]]
            except IndexError as e:
                print(f"res_wp_or_res_wps {e}")
            d_t = []
            data_hour = []
            data_minutes = []
            data_seconds = []
            try:
                for res3_time in res_time_wp:
                    d_t += [res3_time.strftime('%H:%M:%S')]
                    data_hour += [res3_time.strftime('%H')]
                    data_minutes += [res3_time.strftime('%M')]
                    data_seconds += [res3_time.strftime('%S')]
            except IndexError as e:
                print(f"_time_operations_ERRORs {e}")

            hour_t_seconds = []
            try:
                for data_h in data_hour:
                    hour_t_seconds += [int(data_h) * 3600]
            except IndexError as e:
                print(f"hour_t_seconds_ERRORs {e}")
            data_t_seconds = []
            try:
                for data_m in data_minutes:
                    data_t_seconds += [int(data_m) * 60]
            except IndexError as e:
                print(f"data_t_seconds_ERRORs {e}")
            seconds_t_seconds = []
            try:
                for data_s in data_seconds:
                    seconds_t_seconds += [int(data_s) * 1]
            except IndexError as e:
                print(f"seconds_t_seconds {e}")
            try:
                longer = hour_t_seconds if len(hour_t_seconds) >= len(data_t_seconds) else data_t_seconds
                hour_and_minutes = ([x + y for x, y in zip(hour_t_seconds, data_t_seconds)] +
                                    longer[min(len(hour_t_seconds), len(data_t_seconds)):])

                longer1 = seconds_t_seconds if len(seconds_t_seconds) >= len(hour_and_minutes) else hour_and_minutes
                oll_seconds = ([x + y for x, y in zip(seconds_t_seconds, hour_and_minutes)] +
                               longer1[min(len(seconds_t_seconds), len(hour_and_minutes)):])

                shift_oll_sec = oll_seconds[0:]
                shift_oll_sec1 = oll_seconds[1:]

                interval_t = [a - b for a, b in zip(shift_oll_sec1, shift_oll_sec)]

                if not interval_t:
                    print("no data for calculation*")
                else:
                    temperature_duration = [a * b for a, b in zip(interval_t, res_wp)]

                    total_temperature_duration = round(sum(temperature_duration))

                    total_duration = round(sum(interval_t))

                    weighted_arithmetic_average = round((total_temperature_duration / total_duration), 2)

                    largest_element = max(res_wp, key=lambda x: x)

                    min_element = min(res_wp, key=lambda x: x)

                    data_table = [largest_element] + [min_element] + [weighted_arithmetic_average]

                    st.divider()

                    st.subheader("Weather Pressure:")

                    df_wp = pd.DataFrame([data_table], columns=['Max Mmhg', 'Min Mmhg', 'Average Mmhg'])

                    st.dataframe(df_wp, hide_index=True)

                    t_p_d = len(res_wp)
                    id_tpd = []
                    for ind in range(t_p_d):
                        id_tpd += [[str(res_wp[ind])] + [d_t[ind]]]

                    on_h = st.toggle('Weather Pressure per day. Time interval %s - %s' % (st_interval, end_interval),
                                     key='weather_pressure')
                    if on_h:
                        df2_h = pd.DataFrame(id_tpd, columns=['Weather Pressure', 'Time period'])
                        st.dataframe(df2_h.style.highlight_max('Weather Pressure'), hide_index=True)

                    chart_data_h = pd.DataFrame(
                        {
                            "Weather Pressure": res_wp,
                            "Time": d_t,
                        }
                    )
                    st.bar_chart(chart_data_h, x="Time", y="Weather Pressure", color="Weather Pressure")



            except IndexError as e:
                print(f"data_for_statistics {e}")
                st.subheader('Something went wrong (:!')
                st.write("Please try again later")

        except IndexError as e:
            print(f"OLL__weather_pressure_s_ERRORs {e}")

    else:
        print('Wait...')


weather_pressure_s()

if st.button("Refresh", key='restart_history'):
    st.rerun()
