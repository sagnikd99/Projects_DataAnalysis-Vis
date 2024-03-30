#!/usr/bin/env python
# coding: utf-8

# # Uber Ride Analysis 

# ## 1. Importing the Libraries:

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import chart_studio.plotly as py
import plotly.graph_objs as go
import plotly.express as px

from plotly.offline import download_plotlyjs , init_notebook_mode, plot, iplot
import folium
from folium.plugins import HeatMap
import os


# ## 2. Loading the Data:

# In[2]:


os.listdir(r'C:\Users\AAA\Downloads\Uber\Datasets')


# In[3]:


uber_15 = pd.read_csv(r'C:\Users\AAA\Downloads\Uber\Datasets/uber-raw-data-janjune-15_sample.csv')


# ## 3. Exploratory Data Analysis:

# In[4]:


uber_15.shape


# In[5]:


uber_15.info()


# In[6]:


uber_15.dtypes.unique()


# In[7]:


uber_15.columns


# In[8]:


uber_15.head(10)


# ## 4. Data Cleaning:

# In[9]:


uber_15.duplicated().sum()


# In[10]:


uber_15.drop_duplicates(inplace=True)


# In[11]:


uber_15.dtypes


# In[12]:


uber_15.isnull().sum()


# In[13]:


#converting datatype
type(uber_15['Pickup_date'][0])


# In[14]:


uber_15['Pickup_date'] = pd.to_datetime(uber_15['Pickup_date'], errors='coerce')


# ### Summary and Distribution of Numerical Attribute:

# In[15]:


uber_15.describe()


# ## 5. Analysing months having the maximum Uber Pickups:
# 

# In[16]:


uber_15


# In[17]:


uber_15['Month'] = uber_15['Pickup_date'].dt.month_name()


# In[18]:


uber_15['Month'].value_counts()


# In[19]:


uber_15['Month'].value_counts().plot(kind='bar')


# In[20]:


uber_15['Weekday'] = uber_15['Pickup_date'].dt.day_name()
uber_15['Day'] = uber_15['Pickup_date'].dt.day
uber_15['Hour'] = uber_15['Pickup_date'].dt.hour
uber_15['Minute'] = uber_15['Pickup_date'].dt.minute


# In[21]:


uber_15.head(5)


# In[22]:


pivot = pd.crosstab(index=uber_15['Month'], columns=uber_15['Weekday'])


# In[23]:


pivot


# In[24]:


pivot.plot(kind='bar',figsize=(6,6))


# ### Observations:
# 
# 1. Saturdays and Sundays consistently show higher pickups across all months, while Mondays generally exhibit lower pickups suggesting a slower start to the week.
# 2. May and June consistently stand out with the highest pickups across weekdays, suggesting potential seasonal trends or activities during these months.
# 4. February and January typically show lower pickups compared to other months, possibly due to post-holiday or seasonal factors.
# 5. In April, Thursdays notably exhibit the highest pickups compared to other weekdays, indicating potential weekday-specific activity during that month.
# 6. June demonstrates relatively consistent pickup figures across weekdays, suggesting stable consumer behavior throughout the month.

# ## 6. Analysing Hourly Rush for the WeekDays

# In[25]:


summary = uber_15.groupby(['Weekday' , 'Hour'], as_index=False).size()


# In[26]:


summary


# In[27]:


plt.figure(figsize=(7,7))
sns.pointplot(x='Hour', y='size', hue='Weekday', data=summary)


# ### Observations:
# 
# 1. Saturdays register the highest rush at around midnight due to the onset of weekend.
# 2. The weekdays register similar rush at morning owing to office rush.
# 3. Sunday rush starts dropping after 5pm, even though similar growth of rush like Saturday before evening.

# ## 7. Analysing the Base Number having the most number of active vehicles

# In[28]:


os.listdir(r'C:\Users\AAA\Downloads\Uber\Datasets')


# In[29]:


uber_foil = pd.read_csv(r'C:\Users\AAA\Downloads\Uber\Datasets/Uber-Jan-Feb-FOIL.csv')


# In[30]:


uber_foil


# In[31]:


uber_foil.shape


# In[32]:


get_ipython().system('pip install chart_studio')
get_ipython().system('pip install plotly')


# In[33]:


import chart_studio.plotly as py
import plotly.graph_objs as go
import plotly.express as px

from plotly.offline import download_plotlyjs , init_notebook_mode, plot, iplot 


# In[34]:


init_notebook_mode(connected=True)


# In[35]:


px.box(x='dispatching_base_number', y='active_vehicles', data_frame=uber_foil)


# ### Observations:
# 
# 1. The Base Number: B02764 records the highest number of active vehicles with Inter Quartile Range of 474 which is approx 166% more than the Base number with lowest number of active vehicles - B02512.

# In[36]:


os.listdir(r'C:\Users\AAA\Downloads\Uber\Datasets')


# In[37]:


files = os.listdir(r'C:\Users\AAA\Downloads\Uber\Datasets')[-8:]


# In[38]:


files.remove('uber-raw-data-janjune-15.csv')


# In[39]:


files.remove('uber-raw-data-janjune-15_sample.csv')


# In[40]:


files


# In[41]:


final = pd.DataFrame()

path = r'C:\Users\AAA\Downloads\Uber\Datasets'

for file in files:
    current_df = pd.read_csv(path+'/'+file)
    final = pd.concat([current_df, final])


# In[42]:


final


# In[43]:


final.duplicated().sum()


# In[44]:


final.drop_duplicates(inplace=True)


# In[45]:


final.isnull().sum()


# In[46]:


final.head(4)


# In[ ]:





# ## 8. Spatial Analysis to find rush of Uber Pickups

# In[47]:


rush_uber = final.groupby(['Lat', 'Lon'], as_index=False).size()


# In[48]:


rush_uber.head(6)


# In[49]:


get_ipython().system('pip install folium')


# In[50]:


import folium


# In[51]:


basemap = folium.Map()


# In[52]:


basemap


# In[53]:


from folium.plugins import HeatMap


# In[54]:


HeatMap(rush_uber).add_to(basemap)


# In[55]:


basemap


# ### Observations:
# 
# 1. New York, Brooklyn, Hampstead registers the highest activity understandably.
# 2. The rush drops around the coastal lines of Statent Island and pockets of low rush around Natural Reserves/Outdoor Park and Recreation areas.

# ## Examine rush on Hour and Weekday

# In[56]:


final.head(5)


# In[57]:


final['Date/Time'] = pd.to_datetime(final['Date/Time'], format="%m/%d/%Y %H:%M:%S")


# In[58]:


final['Day'] = final['Date/Time'].dt.day
final['Hour'] = final['Date/Time'].dt.hour


# In[59]:


final.head(4)


# In[60]:


pivot = final.groupby(['Day', 'Hour']).size().unstack()


# In[61]:


pivot


# In[62]:


pivot.style.background_gradient()


# ### Observations:
# 
# 1. There's low correlation between days of the month and hours of the day. Just to note, 30th of the month has relatively higher activity throughout the entire day.

# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




