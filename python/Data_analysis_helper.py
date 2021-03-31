import pandas as pd
#import netCDF4 as nc4   
import numpy as np
import datetime as dt
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import copy
from scipy.signal import lfilter, butter
import matplotlib.image as mpimg
from matplotlib import rcParams
import scipy.stats as stats

numShuffles = 1000 
ncores = 4 #####
maxLag = 30

def report_length(table):
    for col in table.columns:
        var_series = table[col]
        print(col,var_series.first_valid_index(), var_series.last_valid_index())

######## subset the table by acquired stations and variables ######
def subset_single_var(table,var):
    col_lst=[]
    for col in table.columns:
        stn=col.split('_')[0]
        variable=col.split('_')[1]
        if variable==var:
            col_lst.append(col)
    subset_table=table[col_lst]
    return subset_table

def subset_table(table,dis_stn,met_stn,acq_vars):
    col_lst=[]
    
    for col in table.columns:
        stn = col.split('_')[0]
        var = col.split('_')[1]
        if acq_vars==[] or var in acq_vars:
            if var=='Discharge':
                if dis_stn==[] or stn in dis_stn: 
                    col_lst.append(col)
            else: 
                if met_stn==[] or stn in met_stn:
                    col_lst.append(col)
    
    subset_table=table[col_lst]
    
    return subset_table

###### read table from csv files #####
def read_table_csv(file_path,str_gauge,met_gauge,acq_vars):
    comp_table = pd.read_csv(file_path,header = 0,index_col = 'DateTime',
                             parse_dates = True,infer_datetime_format = True)
    table=subset_table(comp_table,str_gauge,met_gauge,acq_vars)
    return table
def uni_var(table):
    var=[]
    for col in table:
        if col.split('_')[1] not in var:
            var.append(col.split('_')[1])
    return var

###### read table from netcdf files #####
def read_table_filled_ncdf(n,variable_names_lst,folder_lst,path=''): # variable_names_lst=[] to get all the data
    folder=folder_lst[n-1]
    ws=folder.split('-')[1]
    File=ws+'_NetCDF.nc'
    ncdf = nc4.Dataset(path + File, 'r')
    for i,var in enumerate(variable_names_lst):
        indexUnique = pd.date_range(str(pd.to_datetime(ncdf.variables['Datetime'][:][0])), str(pd.to_datetime(ncdf.variables['Datetime'][:][-1])))  
        if ncdf.variables[var][:].shape[1]==1:
            var_df=pd.DataFrame(ncdf.variables[var][:], index=indexUnique, columns = [ncdf.variables[var].names])
        else:
            var_df=pd.DataFrame(ncdf.variables[var][:], index=indexUnique, columns = ncdf.variables[var].names)
        if i==0:
            former_df=var_df
        else:
            former_df=pd.concat([former_df,var_df],axis=1,join='outer')      
    ncdf.close()
    former_df.index.rename('DateTime',inplace = True)
    return former_df

def normalize_table(table):
    normalized_table = (table - table.mean(axis=0)) / table.std(axis=0)
    col_means = table.mean(axis=0)
    col_std = table.mean(axis=0)
    return normalized_table

###### trim table ########
def trim_long(table,var=''): # shortest source variables
    start_ind_lst=[]
    end_ind_lst=[]
    for i in np.arange(table.shape[1]):
        each_record=table.iloc[:,[i]]
        index_start=each_record.index.get_loc(each_record.first_valid_index())
        index_end=each_record.index.get_loc(each_record.last_valid_index())
        start_ind_lst.append(index_start)
        end_ind_lst.append(index_end)
        print(table.columns[i],'starts at',table.index[index_start],'ends at',table.index[index_end])
    
    start=max(start_ind_lst[0],np.min(start_ind_lst[1:])) # exclude discharge
    end=min(end_ind_lst[0],np.max(end_ind_lst[1:]))
    print(' ')
    print('The earliest starting date for met data is',table.index[start])
    print('The latest ending date for met data is',table.index[end])
    print(' ')
    
    trimmed_table=copy.deepcopy(table.iloc[start:end+1,:])
    print("Table start from",table.index[start], "to",table.index[end])
    return trimmed_table

def trim_short(table,var=''): # shortest source variables
    start_ind_lst=[]
    end_ind_lst=[]
    for i in np.arange(table.shape[1]):
        each_record=table.iloc[:,[i]]
        index_start=each_record.index.get_loc(each_record.first_valid_index())
        index_end=each_record.index.get_loc(each_record.last_valid_index())
        start_ind_lst.append(index_start)
        end_ind_lst.append(index_end)
        print(table.columns[i],'starts at',table.index[index_start],'ends at',table.index[index_end])
    
    start=np.max(start_ind_lst) # exclude discharge
    end=np.min(end_ind_lst)
    print('The lastest starting date is',table.index[start])
    print('The earliest ending date is',table.index[end])
    
    trimmed_table=copy.deepcopy(table.iloc[start:end+1,:])
    print("Table start from",table.index[start], "to",table.index[end])
    return trimmed_table

######### DOY #########
def generate_anomaly_table(table): # edits are necessary from original version
    annual_table=copy.deepcopy(table)
    anomaly_table=copy.deepcopy(table)
    #print('There are',len(pd.Series([str(t).split('-',1)[-1].split(' ')[0] for t in annual_table.index]).unique()), "date groups")
    annual_table.index=[str(t).split('-',1)[-1].split(' ')[0] for t in annual_table.index] # only keep the month and day information
    annual_table = annual_table.groupby(annual_table.index).apply(lambda g: g.mean(skipna=True))
    #print("The shape of annual table is", annual_table.shape)
    #annual_table.plot()
    for index in anomaly_table.index:
        date=str(index).split('-',1)[-1].split(' ')[0]
        cor_row=annual_table.loc[date,:]
        anomaly_table.loc[index,:]=anomaly_table.loc[index,:]-cor_row
    sns.set_context("talk", font_scale=0.6)
    #anomaly_table.plot(figsize=(15,8))
    return anomaly_table

####### MA 30 extrated ########
def generate_anomaly_table2(table): # the one-year annual data is smoothed on a window size of 30 days 
    annual_table=copy.deepcopy(table)
    anomaly_table=copy.deepcopy(table)
    #print('There are',len(pd.Series([str(t).split('-',1)[-1].split(' ')[0] for t in annual_table.index]).unique()), "date groups")
    annual_table.index=[str(t).split('-',1)[-1].split(' ')[0] for t in annual_table.index] 
    # only keep the month and day information
    annual_table = annual_table.groupby(annual_table.index).apply(lambda g: g.mean(skipna=True))
    annual_table=annual_table.rolling(window=30,min_periods=1).mean() ############## get smoother annual series
    #annual_table.plot()
    for index in anomaly_table.index:
        date=str(index).split('-',1)[-1].split(' ')[0]
        cor_row=annual_table.loc[date,:]
        anomaly_table.loc[index,:]=anomaly_table.loc[index,:]-cor_row
    #anomaly_table.plot(figsize=(20,5))
    return anomaly_table


######## do TE analysis ########
def TE_analysis(table):
    numVr = table.shape[1] 
    data=copy.deepcopy(table)
    SourN = np.arange(2,numVr+1)  # 2,3,...numVr, the index number of source variables
    SinN = np.array([1]) # 1 the index number of discharge
    if data.columns[0].split('_')[1]!='Discharge':
        print('Warning: the sink variable is not discharge')
    LabelC = np.r_[np.array(['DateTime']),np.array(data.columns)] # an array of ['Datetime', 'stn1_discharge','stn2_Precipitation',..] (the column names) 
    data.insert(0, 'DateTime', data.index.astype(str)) # insert the datetime column at the beginning
    DataM=data.values
    sf = [-1,0,-1] # ??
    Imat,Icritmat,Tfirstmat,Tbiggestmat,Tcube_store,Tcritcube_store = TEpython_ParallelNAN.RunNewTE2VarsPar(
        DataMatrix=DataM,ncores=ncores,LabelCell=LabelC, 
        shift=sf, SinkNodes=SinN,SourceNodes=SourN, 
        maxLag=maxLag,numShuffles=numShuffles)
    return Imat,Icritmat,Tfirstmat,Tbiggestmat,Tcube_store,Tcritcube_store

def lineplot_TE(table,Tcube_store,Tcritcube_store,figure_size,agg_length,file_nm):
    n = Tcube_store.shape[1]
    sns.set(rc={'figure.figsize':figure_size}, font='Arial')
    sns.set_context("talk", font_scale=1.0)
    AboveCritic = np.nan*np.ones([n,maxLag])
    LagTime = np.nan*np.ones([n])
    for i in np.arange(n):
        plt.subplot((int(n/3)+1), 3, i+1)
        plt.plot(np.arange(maxLag), Tcube_store[0,i,:].reshape(maxLag), color='green', marker='o', linewidth=2, markersize=5)
        plt.xlabel('Lag, days')
        plt.ylabel('TE')    
        plt.plot(np.arange(maxLag), Tcritcube_store[0,i,:].reshape(maxLag), color = 'black', linewidth=2, linestyle='dashed')
        plt.suptitle('Sink =' + table.columns[0] + ', Record Length=' + str(round(table.shape[0]/365,2))+' years'  )
        plt.title((table.columns[i+1])+", AggregationDays="+str(agg_length))
        AboveCritic[i,:] = (Tcube_store[0,i,:] - Tcritcube_store[0,i,:]).reshape(maxLag)
        plt.subplots_adjust(top=0.92, bottom=0.08, left=0.10, right=0.95, hspace=0.5,wspace=0.35)
    plt.savefig(file_nm,dpi = 100)
    plt.close()

def TE_heatmap(table,fig_size=(15,15),title="None",font_scale=0.7,legend_scale=0.3,vmin=None, vmax=None):
    sns.set(rc={'figure.figsize':fig_size}, font='Arial')
    sns.set_context("talk", font_scale=font_scale)
    ax = sns.heatmap(table,cbar_kws={"shrink": legend_scale},cmap='viridis',square = True,vmin=vmin, vmax=vmax)
    plt.title(title)
    ax.set_yticklabels(table.index,rotation=0)
    maxLag=table.shape[1]+2
    ax.set_xticks(range(0,maxLag,2))
    ax.set_xticklabels(range(0,maxLag,2),rotation=0)  

def leave_one_record_for_each_var(table,var_lst):
    sum_TE_df=table.sum(axis=1,skipna=False)
    var_d={}
    for record in sum_TE_df.index:
        var=record.split('_')[1]
        if var in var_lst:
            if var not in var_d.keys():
                if not np.isnan(sum_TE_df[record]):
                    var_d[var]=[record,sum_TE_df[record]]
            elif sum_TE_df[record]!=None and sum_TE_df[record]>var_d[var][1]:
                var_d[var]=[record,sum_TE_df[record]]    
    length=table.shape[1]*len(var_lst)
    if len(var_lst)!=len(var_d.keys()): # don't have all the variables in var_lst
        return np.nan 
    else:        
        left_ones=[]
        for var in var_lst:
            left_ones.append(var_d[var][0])   
        return left_ones#table.loc[left_ones,:], table.loc[left_ones,:].values.reshape(length)


class HiddenPrints:
    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._original_stdout
        
    
def identify_longest_record_without_nan(flagtable,colname='KettlePonds_SoilMoisture_508'):   
    max_l=0 # longest record length initialized as 0 days
    with HiddenPrints():
        trimmed_table=trim_short(flagtable[[colname]]) # trim table to start and end with non_nan values
    lst=[trimmed_table.index[0],trimmed_table.index[-1]] # a list of time nodes
    time_range=[] # a list of time ranges without missing values
    longest_tr=None # the longest time range without missing values
    mark_na=0 
    position=0
    
    for i in range(trimmed_table.shape[0]):
        date=trimmed_table.index[i]
        value=trimmed_table.iloc[i,0]
        if value==0 and mark_na==0: # mark the series of nan values begin
            mark_na=1
            position+=1
            lst.insert(position,trimmed_table.index[i-1])
            time_range.append((lst[position-1],lst[position]))
            if max_l==0 or lst[position]-lst[position-1]>max_l:
                longest_tr=(lst[position-1],lst[position])
                max_l=lst[position]-lst[position-1]
            
        elif value!=0 and mark_na==1: # mark the series of nan values end
            mark_na=0
            position+=1
            lst.insert(position,trimmed_table.index[i]) 
    time_range.append((lst[position],lst[position+1]))
    if max_l==0 or lst[position+1]-lst[position]>max_l:
        longest_tr=(lst[position],lst[position+1])
        max_l=lst[position+1]-lst[position]   
    return time_range,longest_tr

def leave_longest_record_without_nan(table,flagtable,colname):
    tr_lst,longest_tr=identify_longest_record_without_nan(flagtable,colname=colname)
    longest_rl_values=table.loc[pd.date_range(longest_tr[0],longest_tr[1]),colname]
    table[colname]=[np.nan]*table.shape[0] # set to nan
    table[colname]=longest_rl_values # replace with longest non-nan values

def replace_with_continuous_records(table,flagtable,main_str):
    ## Identify longest discharge time range without NAN values
    dis_tr_lst,dis_longest_tr=identify_longest_record_without_nan(flagtable,main_str+'_Discharge')
    ## Trim the table and flagtable using the time range above
    table=table.loc[pd.date_range(dis_longest_tr[0],dis_longest_tr[-1]),:]
    flagtable=flagtable.loc[pd.date_range(dis_longest_tr[0],dis_longest_tr[-1]),:]
    print("The longest continuous discharge time range is from",dis_longest_tr[0], "to",dis_longest_tr[1])

    ## replace each column with the longest record without nan values
    newtable=copy.deepcopy(table)
    for col in newtable.columns:
        leave_longest_record_without_nan(newtable,flagtable,col)
    return newtable
