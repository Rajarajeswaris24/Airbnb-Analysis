# import packages
import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import plotly.express as px
import re
import warnings
warnings.filterwarnings("ignore")

# csv file
df=pd.read_csv(r"C:\Users\balak\guvi\Airbnb analysis\airbnb_analysis_data.csv")

#streamlit  background color
page_bg_color='''
<style>
[data-testid="stAppViewContainer"]{
        background-color:#FFDAB9;
}
</style>'''

#streamlit button color
button_style = """
    <style>
        .stButton>button {
            background-color: #ffa089 ; 
            color: black; 
        }
        .stButton>button:hover {
            background-color: #ffddca; 
        }
    </style>    
"""
#streamlit settings
st.set_page_config(
    page_title="Airbnb Analysis",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="auto")


st.markdown(page_bg_color,unsafe_allow_html=True)  #calling background color
st.markdown(button_style, unsafe_allow_html=True)  #calling button color


st.title("Airbnb Analysis")

#menu
selected = option_menu(menu_title=None,options= ["Home", 'Property','Location','Analysis'],icons=["house", "houses","map", "bar-chart"],
          default_index=0,orientation='horizontal',
          styles={"container": { "background-color": "white", "size": "cover", "width": "100"},
            "icon": {"color": "brown", "font-size": "20px"},

            "nav-link": {"font-size": "20px", "text-align": "center", "margin": "-2px", "--hover-color": "#ffe5b4"},
            "nav-link-selected": {"background-color": "#E2838A"}})

# function minimum nights
def nights_min(min_nyt,country,properties):
    dp=df[['Name','Property_type','Country','Min_nights','Price']]
    d=dp[dp.Min_nights==min_nyt][dp.Country==country][dp.Property_type==properties]
    st.write("#### :red[ Hotel names with minimum nights:]")
    with st.expander("DataFrame"):
        st.write(d)
    fig_bar = px.bar(d,
                    title='Hotel Name and Price Vs Country Vs Property_type Vs Minimum_nights  ',
                    x="Name",
                    y="Price",
                    orientation='v',
                    color='Name',
                    color_discrete_sequence=px.colors.sequential.Inferno)
    st.plotly_chart(fig_bar,use_container_width=True)

# function maximum nights    
def  nights_max(max_nyt,country,properties):
    dp=df[['Name','Property_type','Country','Max_nights','Price']]
    d=dp[dp.Max_nights==max_nyt][dp.Country==country][dp.Property_type==properties]
    st.write("#### :red[ Hotel names with maximum nights:]")
    with st.expander("DataFrame"):
        st.write(d)
    fig_bar = px.bar(d,
                    title='Hotel Name and Price Vs Country Vs Property_type Vs  Maximun_nights ',
                    x="Name",
                    y="Price",
                    orientation='v',
                    color='Name',
                    color_discrete_sequence=px.colors.sequential.Inferno_r)
    st.plotly_chart(fig_bar,use_container_width=True)

# function availability 
def availability(country,properties,avail):
    dpp=df[['Name','Country','Property_type']]
    d=dpp[dpp.Country==country][dpp.Property_type==properties]
    
    if avail:   
        selected_column = df[df.Country==country][df.Property_type==properties][avail]
        merged_df = pd.concat([d, selected_column], axis=1)

        st.write(f"####  Hotel names with :red[**{avail}**] in each country ")
        with st.expander("DataFrame"):
            st.write(merged_df)
        merged_dff = pd.concat([d, selected_column], axis=1).head(20)
        fig1 = px.pie(merged_dff, values=avail,
                            names='Name',
                            title='Hotel Name Vs Country Vs Property_type Vs Availability',
                            color_discrete_sequence=px.colors.sequential.Aggrnyl_r,
                            hover_data=[avail],
                            labels={avail:'Availability'})
        st.plotly_chart(fig1,use_container_width=True)

# function amenities
def amenities(country,properties):
    unique_amenities = set()
    for amenities in df['Amenities']:
        unique_amenities.update(amenities.split(', '))

    selected_amenities = st.multiselect('Select amenities', sorted(unique_amenities),default=['TV','Air conditioning'],key='nr')

    pattern = ', '.join(selected_amenities)
    selected_amenities_list = pattern.split(',')
    if not selected_amenities:
            st.warning("Please select at least one amenity.")
    a=df[['Name','Property_type','Country','Country_code','Amenities','Price']]
    amen=a[a.Property_type==properties][a.Amenities.str.contains('|'.join(selected_amenities_list),case=False)]
    st.write("#### :red[ Count of amenities in each country:]")
    with st.expander("View table"):
        st.write(amen)

    amenity_counts = {}
    for amenity in selected_amenities_list:
        amenity_counts[amenity.strip()] = amen['Amenities'].str.contains(amenity.strip(), case=False).sum()

    fig_bar2 = px.bar(amen,
                    title='Amenities count Vs Country Vs Property_type',
                    x=list(amenity_counts.keys()),
                    y=list(amenity_counts.values()),
                    orientation='v',
                    color=list(amenity_counts.keys()),
                    color_discrete_sequence=px.colors.sequential.Inferno_r)
    fig_bar2.update_layout(
        xaxis=dict(title='Amenity'),
        yaxis=dict(title='Count')   
    )
    st.plotly_chart(fig_bar2,use_container_width=True)

l=df[['Name','Property_type','Room_type','Bed_type','Cancellation_policy','Country','Longitude','Latitude','Price']]

# function location avg price
def location_price():
    
    geo = l.groupby('Country')['Price'].mean().reset_index()
    
    st.write("#### :red[ Average Price in each country:]")
    fig_geo = px.scatter_geo(data_frame=geo,
                                       locations='Country',
                                       color= 'Price', 
                                       hover_data=['Price'],
                                       locationmode='country names',
                                       size='Price',
                                       title= 'Avg Price in each Country',
                                       projection='eckert4',
                                       color_continuous_scale='agsunset'
                            )

    st.plotly_chart(fig_geo,use_container_width=True)

# function location property type count
def location_property():
    
    properties=st.selectbox("Select property",df['Property_type'].unique(),key='map')     
    df_c = l[l['Property_type'] == properties]
    geo_p = df_c.groupby(['Country', 'Property_type']).size().reset_index(name='Count')
    st.write(f"#### Total count of :red[**{properties}**] in each country ")
    
    fig_ = px.choropleth(geo_p,
                    locations="Country", 
                    locationmode='country names',
                    color="Count",
                    hover_name="Country",
                    color_continuous_scale=px.colors.sequential.Viridis,
                    title="Total property_type count in each country")
    st.plotly_chart(fig_,use_container_width=True)

# function location room type count
def location_room():
    rooms=st.selectbox("Select room",df['Room_type'].unique()) 
    df_r = l[l['Room_type'] == rooms]
    geo_r = df_r.groupby(['Country', 'Room_type']).size().reset_index(name='Count')
    st.write(f"#### Total count of :red[**{rooms}**] in each country ")
    
    fig_ = px.choropleth(geo_r,
                    locations="Country", 
                    locationmode='country names',
                    color="Count",
                    hover_name="Country",
                    projection='azimuthal equal area',
                    color_continuous_scale=px.colors.sequential.Sunsetdark_r,
                    title="Total room_type count in each country")
    st.plotly_chart(fig_,use_container_width=True)

# function location bed type count
def location_bed():
    beds=st.selectbox("Select bed",df['Bed_type'].unique()) 
    df_b = l[l['Bed_type'] == beds]
    geo_b = df_b.groupby(['Country' ]).agg({'Longitude': 'first', 'Latitude': 'first', 'Bed_type': 'count'}).reset_index()
    st.write(f"#### Total count of :red[**{beds}**] in each country ")
    
    fig_4 = px.scatter_mapbox(geo_b, lat='Latitude', lon='Longitude', color='Bed_type', size='Bed_type',
                    color_continuous_scale= px.colors.sequential.Cividis,hover_name='Country', mapbox_style="carto-positron",
                    zoom=1)
    fig_4.update_layout(width=1150,height=800,title='Total bed_type count in each country')
    
    st.plotly_chart(fig_4) 

# function cancelation policy count 
def location_cancel():
    policy=st.selectbox("Select Cancellation_policy",df['Cancellation_policy'].unique()) 
    df_b = l[l['Cancellation_policy'] == policy]
    geo_b = df_b.groupby(['Country' ]).agg({'Longitude': 'first', 'Latitude': 'first', 'Cancellation_policy': 'count'}).reset_index()
    st.write(f"#### Total count of :red[**{policy}**] in each country ")
    
    fig5 = px.scatter_mapbox(geo_b, lat='Latitude', lon='Longitude', color='Cancellation_policy', size='Cancellation_policy',
                    color_continuous_scale= px.colors.sequential.Plotly3,hover_name='Country', mapbox_style="open-street-map",
                    zoom=1)
    fig5.update_layout(width=1150,height=800,title='Total Cancellation_policy count in each country')
    
    st.plotly_chart(fig5)  

# function price analysis
def price_analysis():
        l=df[['Name','Property_type','Room_type','Bed_type','Country','Longitude','Latitude','Price']]  
        cola,colb=st.columns(2)
        with cola:
            country=st.selectbox("Select Country",df['Country'].unique())
        with colb:
             filtered_df = df[df['Country'] == country]

             types_in_country = filtered_df['Property_type'].unique()

             properties=st.selectbox("Select property",types_in_country)  
        grouped_data = filtered_df[filtered_df['Property_type'] == properties].groupby(['Country', 'Property_type']).agg({'Price': 'mean', 'Security_deposit': 'mean', 'Cleaning_fee': 'mean'}).reset_index()
        
        #melt data each single columns into rows
        melted_data = pd.melt(grouped_data, id_vars=['Country', 'Property_type'], var_name='Feature', value_name='Value')


        st.write("#### :red[ Price analysis for each country and property type:]")
        with st.expander("DataFrame"):
            st.write(melted_data)
        fig = px.pie(melted_data, values='Value',
                                    names='Feature',
                                    title='Price analysis Vs country and property type',
                                    color_discrete_sequence=px.colors.sequential.Teal,
                                    hover_data=['Value'],
                                    labels={'Vlaue':'Average'},hole=0.5)
        st.plotly_chart(fig,use_container_width=True)

# function room analysis
def room_analysis():
        colaa,colbb,colcc,coldd=st.columns(4)
        with colaa:
            country=st.selectbox("Select Country",df['Country'].unique(),key=24)
        with colbb:
             filtered_df = df[df['Country'] == country]

    
             pf = filtered_df['Property_type'].unique()
             properties=st.selectbox("Select property",pf,key=7)  
        with colcc:
            filtered_pr = filtered_df[filtered_df['Property_type'] == properties]
            ro=filtered_pr['Room_type'].unique()
            rooms=st.selectbox("Select Room",ro)
        with coldd:
            filtered_bed = filtered_pr[filtered_pr['Room_type'] ==rooms ]
            bt=filtered_bed['Bed_type'].unique()
            beds=st.selectbox("Select Bed",bt)
       
        
        group_df = filtered_bed[filtered_bed['Bed_type'] == beds].groupby(['Country', 'Property_type','Room_type','Bed_type']).agg({'Total_bedrooms': 'max', 'Total_beds': 'max', 'Bathrooms': 'mean'}).reset_index()
        
        #melt data each single columns into rows
        melted_df = pd.melt(group_df, id_vars=['Country', 'Property_type','Room_type','Bed_type'], var_name='Feature', value_name='Value')
        st.write("#### :red[ Room analysis for each country , property type , room type and bed type:]")
        with st.expander("View"):
            st.write(melted_df)
        fig = px.sunburst(melted_df, path=['Country','Property_type','Room_type','Bed_type','Feature'], values='Value',
                color='Value', hover_data=['Value'],color_continuous_scale=px.colors.sequential.Redor,title='Maximum bedrooms, beds,bathrooms  in each country')
        st.plotly_chart(fig,use_container_width=True)

# function accomodate analysis
def accomodates_analysis():
        coun,prop=st.columns(2)
        with coun:
            country=st.multiselect("Select Country",df['Country'].unique(),default=['United States','Australia'])
            coun_df=df[df["Country"].isin(country)]
        with prop:
            properties=st.multiselect("Select Property",df['Property_type'].unique(),default=['House','Apartment'])
            dff=coun_df[coun_df["Property_type"].isin(properties)]
        group_df = dff.groupby(['Country', 'Property_type','Room_type']).agg({'Accomodates': 'max',  'Guests_included': 'max'}).reset_index()
        st.write("#### :red[ Accomodates analysis for each country and property type:]")
        with st.expander("DataFrame"):
            st.write(group_df)
        fig = px.sunburst(group_df, path=['Country','Property_type','Room_type'], values='Accomodates',
                    color='Accomodates', hover_data=['Accomodates','Guests_included'],color_continuous_scale=px.colors.sequential.Redor_r,title='Accomodates analysis in each country')
           
        st.plotly_chart(fig,use_container_width=True)

# function host verification
def host_veri(country,properties):
    unique_verify = set()
    for ho_ve in df['Host_verification']:
        unique_verify.update(ho_ve.split(','))

    selected_verify = st.multiselect('Select Verification', sorted(unique_verify),default=['email','phone'],key='nr')
    
    pattern = ', '.join(selected_verify)
    selected_verify_list = pattern.split(',')
    if not selected_verify:
            st.warning("Please select at least one verification.")
    a=df[['Name','Property_type','Country','Country_code','Host_verification','Price']]
    amen=a[a.Country==country][a.Property_type==properties][a.Host_verification.str.contains('|'.join(selected_verify_list),case=False)]
    st.write("#### :red[ Count of host verification for each country and property type:]")
    with st.expander("DataFrame"):
        st.write(amen)

    verify_counts = {}
    for verify in selected_verify_list:
        verify_counts[verify.strip()] = amen['Host_verification'].str.contains(verify.strip(), case=False).sum()

    fig_bar2 = px.bar(amen,
                    title='Host Verification count Vs Country Vs Property_type',
                    x=list(verify_counts.keys()),
                    y=list(verify_counts.values()),
                    orientation='v',
                    color=list(verify_counts.keys()),
                    color_discrete_sequence=px.colors.sequential.Burg)
    fig_bar2.update_layout(
        xaxis=dict(title='Host_verification'),
        yaxis=dict(title='Count')
    )
    st.plotly_chart(fig_bar2,use_container_width=True)
    

# function host analysis
def host_analysis():
    c1,c2=st.columns(2)
    with c1:
        country= st.selectbox("Select the Country",df["Country"].unique())

        df1_a= df[df["Country"] == country]
        df1_a.reset_index(drop= True, inplace= True)
    with c2:

        property_ty_a= st.selectbox("Select the Property Type",df1_a["Property_type"].unique())
        df2_a= df1_a[df1_a["Property_type"] == property_ty_a]
        df2_a.reset_index(drop= True, inplace= True)
    host_veri(country,property_ty_a)    # calling host verification function

    host=st.sidebar.multiselect("Choose neighorbood",df['Host_neighbourhood'].unique(),default=['Not Specified','Waikiki'])
    coln,colr=st.columns(2)
    with coln:
        df1_a= df[df["Host_neighbourhood"] .isin(host)]
        nei_df = df1_a.groupby(['Country', 'Host_neighbourhood']).size().reset_index(name='Count')
        st.write("#### :red[ Total count of host neighbourhood:]")
        with st.expander("Dataframe"):
            st.write(nei_df)
        fig_nei= px.sunburst(nei_df, path=["Country","Host_neighbourhood"], values="Count",color="Count",width=600,height=500,title="Host_neighbourhood",color_continuous_scale= px.colors.sequential.haline_r)
        st.plotly_chart(fig_nei,use_container_width=True)

    with colr:
        response_time_counts = df.groupby(['Country', 'Host_response_time']).size().reset_index(name='Count')
        st.write("#### :red[ Total count of host response time:]")
        with st.expander("Table"):
            st.write(response_time_counts)
        df_a_sunb_30= px.sunburst(response_time_counts, path=["Country","Host_response_time"], values="Count",color="Count",width=600,height=500,title="Host_response_time",color_continuous_scale= px.colors.sequential.Mint)
        st.plotly_chart(df_a_sunb_30,use_container_width=True)


    host_df=df[['Host_id','Host_name','Country']]
    name_df = host_df.groupby(['Country', 'Host_name','Host_id']).size().reset_index(name='Count')
    n=name_df.sort_values(by="Count",ascending=False)
    st.write("#### :red[ Top 20 Host listings:]")
    with st.expander("View listings"):
        st.write(n)
    n=name_df.sort_values(by="Count",ascending=False).head(20)
    fig1 = px.bar(n, x='Host_name',y='Count',orientation='v',
                color='Country',
                        
                        title='Top 20 Host listings ',
                        color_discrete_sequence=px.colors.sequential.Sunsetdark)
                            
    st.plotly_chart(fig1,use_container_width=True)


# function review analysis
def review_analysis():
        country_b=st.sidebar.selectbox("Select Country",df['Country'].unique())

        r_df=df[['Name','Country','Property_type','No_of_reviews','Review_scores']]
        num_df=r_df[r_df['Country']==country_b]
        prope=st.sidebar.selectbox("Select Country",num_df['Property_type'].unique())
        dff=num_df[num_df['Property_type']==prope]
        review=dff.sort_values(by='No_of_reviews',ascending=False)
        
        st.write("#### :red[ Hotel names with maximum number of reviews for each country and property type:]")
        with st.expander("View table"):
            st.write(review)
        review=dff.sort_values(by='No_of_reviews',ascending=False).head(15)
        fig1 = px.bar(review,x='Name', y='No_of_reviews',orientation='v',
                color='No_of_reviews',
                        
                        title='Top 15 Hotel name vs country vs property type vs no.of reviews',
                        color_continuous_scale=px.colors.sequential.Sunsetdark)
                            
        st.plotly_chart(fig1,use_container_width=True)
    

        rating=dff.sort_values(by='Review_scores',ascending=False)
        st.write("#### :red[ Hotel names with maximum  review score for each country and property type:]")
        with st.expander("View table"):
            st.write(rating)
        rating=dff.sort_values(by='Review_scores',ascending=False).head(15)
        fig_bar = px.bar(rating,
                title='Top 15 Hotel name vs country vs property type vs reviews-scores',
                x="Name",
                y="Review_scores",
                orientation='v',
                color='Review_scores',
                color_continuous_scale=px.colors.sequential.Sunset)
        st.plotly_chart(fig_bar,use_container_width=True)

#streamlit page
#home page
if selected == 'Home':
    col1,col2=st.columns(2)
    with col1:
        st.image(r"C:\Users\balak\guvi\Airbnb analysis\airbnb.jpg")

    with col2:
        st.header("About Airbnb")
        st.write("")
        st.write('''***Airbnb is an online marketplace that connects people who want to rent out
                their property with people who are looking for accommodations,
                typically for short stays. Airbnb offers hosts a relatively easy way to
                earn some income from their property.Guests often find that Airbnb rentals
                are cheaper and homier than hotels.***''')
        st.write("")
        st.write('''***Airbnb Inc (Airbnb) operates an online platform for hospitality services.
                    The company provides a mobile application (app) that enables users to list,
                    discover, and book unique accommodations across the world.
                    The app allows hosts to list their properties for lease,
                    and enables guests to rent or lease on a short-term basis,
                    which includes vacation rentals, apartment rentals, homestays, castles,
                    tree houses and hotel rooms. The company has presence in China, India, Japan,
                    Australia, Canada, Austria, Germany, Switzerland, Belgium, Denmark, France, Italy,
                    Norway, Portugal, Russia, Spain, Sweden, the UK, and others.
                    Airbnb is headquartered in San Francisco, California, the US.***''')
        
        st.header("Background of Airbnb")
        st.write("")
        st.write('''***Airbnb was born in 2007 when two Hosts welcomed three guests to their
                San Francisco home, and has since grown to over 4 million Hosts who have
                    welcomed over 1.5 billion guest arrivals in almost every country across the globe.***''')
    
# property page
if selected=='Property':
    
    Features=st.selectbox("Select Features",("Number of nights","Availability","Amenities"))
    
    country=st.sidebar.selectbox("Select Country",df['Country'].unique())
    df_c=df[df['Country']==country]
    
    properties=st.sidebar.selectbox("Select property",df_c['Property_type'].unique())

    if Features=="Number of nights":
        min_nyt=st.select_slider("Select minimum nights",sorted(df['Min_nights'].unique()),value=2)
        try:
            nights_min(min_nyt,country,properties)
        except:
            st.warning("Filter Other range")
        
        max_nyt=st.select_slider("Select maximum nights",sorted(df['Max_nights'].unique()),value=30)
        
        try:
            nights_max(max_nyt,country,properties)
        except:
            st.warning("Filter Other range")

    if Features=="Availability":
        avail=st.selectbox("Select Availability",df.columns[32:36])
        availability(country,properties,avail)
        
    if Features=="Amenities":
        amenities(country,properties)

# location page
if selected=='Location':
        location_price()
        location_property()
        location_room() 
        location_bed()
        location_cancel()

        
# analysis page
if selected=='Analysis':
    insights=st.selectbox("Choose Insights",("Price Analysis","Room Analysis","Accomodates Analysis","Host Analysis","Review Analysis"))

    if insights=='Price Analysis':
        price_analysis()        

    if insights=='Room Analysis':
        room_analysis()

    if insights=='Accomodates Analysis':
       accomodates_analysis() 

    if insights=='Host Analysis':
        host_analysis()
        
    if insights=='Review Analysis':
        review_analysis()



        