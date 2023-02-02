import altair as alt
import pandas as pd
import streamlit as st

@st.experimental_memo()
def load_data():
    df = pd.read_csv('data/article_data_with_topics.csv')
    # df = df[df.extra_issue==False]
    # df['year_month'] = pd.to_datetime(df.month.astype(str) + '-' + df.year.astype(str))
    return df

df = load_data()

date_filter = st.select_slider(label='Years', options=sorted(df.year.unique()), value=(1971, 2021))
topic_filter = st.multiselect(label='Compare topics', options=sorted(df.topic_naive.unique()))

filtered_df = df[
    (df.topic_naive.isin(topic_filter))
    & (df.year >= date_filter[0])
    & (df.year <= date_filter[1])
    ]

chart = alt.Chart(filtered_df).mark_area(opacity=0.5).encode(
    x='year:N',
    y=alt.Y('count():Q'),
    color='topic_naive:N',
    row='topic_naive:N',
    tooltip=['year:N', 'topic_naive:N', 'count():Q'],
).properties(
    height=100
).interactive()

# Version with interactive legend
# selection = alt.selection_multi(fields=['topic_naive'], bind='legend')

# chart = alt.Chart(filtered_df).mark_area().encode(
#     # x=alt.X('yearmonth(year_month):T', axis=alt.Axis(domain=False, format='%Y', tickSize=0)),
#     x='year:N',
#     y=alt.Y('count():Q', stack=None),
#     color='topic_naive:N',
#     tooltip=['year:N', 'topic_naive:N', 'count():Q'],
#     opacity=alt.condition(selection, alt.value(0.5), alt.value(0.1))
# ).properties(
#     height=400
# ).add_selection(
#     selection
# ).interactive()

st.altair_chart(chart, use_container_width=True)
