import pandas as pd
import streamlit as st
import plotly.express as px


# SETTINGS #

st.set_page_config(page_title='My first Streamlit app', 
	page_icon="🚙", 
	layout = "wide")

# @st.cache decorator tells Streamlit to run the function and store the result in a local cache
# Streamlit will skip the function if none of the components of the cached function changed
@st.cache 
def load_data(link): 
	df = pd.read_csv(link)
	df.replace({'continent': {' US.':'US', ' Europe.': 'Europe', ' Japan.': 'Japan'}}, inplace=True)
	df.rename(columns={'mpg': 'miles-per-gallon', 
                   'cubicinches': 'cubic(in)',
                   'hp':'horsepower', 
                   'weightlbs':'weight(lbs)'}, inplace=True)
	return df 


# DATA #
url = 'https://raw.githubusercontent.com/murpi/wilddata/master/quests/cars.csv'
df = load_data(url)

# SIDE BAR # 
st.sidebar.title('Filters')
st.sidebar.write('--------')
region = st.sidebar.multiselect('Region', df.continent.unique(), ['US', 'Japan', 'Europe']) ## name, choices, default choice
year = st.sidebar.slider('Year', min(df.year), max(df.year), (1975, 1980))
st.sidebar.write('--------')
show = st.sidebar.checkbox('Show Data')

# MAIN PAGE # 
st.title('Automotive industry in the 70s and 80s')
st.title("")

data = df[(df.continent.isin(region) & df.year.between(year[0], year[1]))]

### FIG 1 ###
col1, col2, col3 = st.columns([1,0.1,3])
with col1:
	st.title('') 
	st.markdown('') 
	st.markdown("""Between 1971 & 1983, the U.S. was the world leader in car manufacturing. 
		Europe held the second place until being overtaken by Japan in 1978. 
		Japan lost its rank briefly in 1980, but swiftly recover. 
		Since 1981, the first place in production was switched between the Japan and the U.S.
	""")
with col3:	

	st.markdown("**Histogram of car production overtime**")
	fig1 = px.histogram(data, x=data.year, color=data.continent)
	fig1.update_layout(margin=dict(l=20, r=0, b=20, t=20), 
		bargap=0.2,
		xaxis_title = None, 
		yaxis_title = None, 
		legend=dict(yanchor='top', y=0.99, xanchor='right', x=0.99))
	st.plotly_chart(fig1, user_container_width=True)


### FIG 2 ###
st.title('')
st.write('_Please select features to be displayed on x axis and y axis_')
col1, col2 = st.columns(2)
with col1:
	feat1 = st.selectbox('x axis', (df.columns.drop(['year','continent'])))
with col2: 
	feat2 = st.selectbox('y axis', (df.columns.drop(['year','continent', feat1])))


col1, col2 = st.columns([3, 1])
with col1: 
	fig2 = px.scatter(x=data[feat1], y=data[feat2], color=data.continent) 
	fig2.update_layout(margin=dict(l=0, r=0, b=20, t=20), 
		showlegend=False,
		xaxis_title = str(feat1), 
		yaxis_title = str(feat2))
	st.plotly_chart(fig2, user_container_width=True)
with col2:
	st.title('') 
	st.markdown('')
	st.markdown("""Globally, cars were made lighter weight over time to be more energy efficient. But Americans tended to focus on producing bigger cars with more power (high horsepower), which consequently more energy consuming. 
			Quite the opposite with the rest of the world.  
	""")


if show: 
	st.title("")
	st.markdown("_Data used in charts_")
	st.dataframe(data)




