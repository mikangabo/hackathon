import pandas as pd
from tabulate import tabulate

 # #Renaming the columns
def col_names(df):
    df.rename(
        columns = {
            col: col.strip().upper().replace(' ','_') for col in df.columns
        }, inplace = True
    )
    return df
def household():

    houshold_df= pd.read_csv('household_internet_offers_v2.csv')
 
    # # converting KB into GB
    houshold_df['monthly_estimate_GB']=houshold_df['monthly_estimate_kb'].apply(lambda x: round(x / 1024 / 1024, 0))
    
    # #converting into integer
    houshold_df['monthly_estimate_GB'].astype('Int64')
    
    
    
    # # remove spaces
    houshold_df['recommended_plan'] = houshold_df['recommended_plan'].str.strip()
    
    # # creating column for the offer Gb
    houshold_df['monthly_Offer_GB']= houshold_df['recommended_plan'].str.extract('(\d+)')
    
    # # replace nan with 999 for unlimited bundle
    houshold_df['monthly_Offer_GB']= houshold_df['monthly_Offer_GB'].fillna(999)
    # create offername column
    houshold_df['Offer_Name']=houshold_df['recommended_plan'].str.split('(').str[0].str.strip()
    # # getting the min and max of each class
    min_max_df= houshold_df.groupby('Offer_Name')['monthly_estimate_GB'].agg(['min', 'max']).reset_index()
    # #convertint into integer
    min_max_df['min']=min_max_df['min'].astype('Int64')
    min_max_df['max']=min_max_df['max'].astype('Int64')
    
    # # addiing the interval on the dataframe
    min_max_df['Intervals']=min_max_df['min'].astype(str) + 'GB-'+min_max_df['max'].astype(str)+'GB'
    
    
    # # Merge DataFrame
    merged_df = houshold_df.merge(min_max_df[['Offer_Name', 'Intervals']], on='Offer_Name', how='left')
    houshold_df['Intervals'] = merged_df['Intervals']
    
    # #Renaming the column
    houshold_df=col_names(houshold_df)
    houshold_df['MONTHLY_ESTIMATE_GB']=houshold_df['MONTHLY_ESTIMATE_GB'].astype('Int64')
    # getting average
    average_df = houshold_df.groupby('INTERVALS')['MONTHLY_ESTIMATE_GB'].mean().reset_index()
    average_df  = average_df.rename(columns={'MONTHLY_ESTIMATE_GB': 'AVERAGE_MONTHLY_USAGE_GB'})
    # average_df = houshold_df.groupby('INTERVALS')['MONTHLY_ESTIMATE_GB'].mean().reset_index()
    average_df['AVERAGE_MONTHLY_USAGE_GB']=average_df['AVERAGE_MONTHLY_USAGE_GB'].astype('Int64')
    print("average_df")
    print(average_df.head())
    
    houshold_graph_df=houshold_df[['HOUSEHOLD_ID','RECOMMENDED_PLAN','OFFER_NAME','INTERVALS','MONTHLY_OFFER_GB']]
    
    household_plan_df=houshold_df[['HOUSEHOLD_ID','RECOMMENDED_PLAN','MONTHLY_ESTIMATE_GB','MONTHLY_OFFER_GB']]
    
    # # grouping the count of household by the offer names, data usage intervals, and provisionned offer
    HOUSEHOLD_ID_count_by_offer = houshold_graph_df.groupby([ 'OFFER_NAME','INTERVALS','MONTHLY_OFFER_GB'])['HOUSEHOLD_ID'].size().reset_index(name='count')
    #Renaming the column
    HOUSEHOLD_ID_count_by_offer = HOUSEHOLD_ID_count_by_offer.rename(columns={'INTERVALS': 'monthly_data_Usage_INTERVALS'})
    HOUSEHOLD_ID_count_by_offer=col_names(HOUSEHOLD_ID_count_by_offer)
    print(tabulate(HOUSEHOLD_ID_count_by_offer, headers='Mapped Offers', tablefmt='pretty'))
    return[HOUSEHOLD_ID_count_by_offer,average_df,household_plan_df]

# if __name__=='__main__':
#     household()