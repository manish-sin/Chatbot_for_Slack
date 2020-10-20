import pandas as pd
import numpy as np
import logging

module_logger = logging.getLogger('slackapp.charts')
#Date Filter
# def date_filter(TSS,TSE):
#     query_log_complete = pd.read_csv("result_old.csv")
#     query_count = query_log_complete.count()
#     query_count = query_count[0]
#     query_log_complete['time'] = pd.to_datetime(query_log_complete['time'], format='%d%m%Y', errors='ignore')
#     query_log_complete['time']
#     mask = (query_log_complete['time'] >= TSS) & (query_log_complete['time'] <= TSE)
#     query_log= query_log_complete.loc[mask]
#     return query_log
def report_fromslack_to_html(TSS, TSE):
    def date_convert(input_date):
        x = input_date.split('-')
        x[2] =int(x[2])
        x[1] =int(x[1])
        x[0] =int(x[0])
        date= x[2]*10000+x[1]*100+x[0]
        return date

    def date_format(input_date):
        x = input_date.split('-')
        date= x[2]+"-"+x[1]+"-"+x[0]
        return date


    def date_filter(TSS,TSE):
        query_log_complete = pd.read_csv("./data/result.csv")
        query_count = query_log_complete.count()
        query_count = query_count[0]
        query_log_complete['Date'] = query_log_complete.apply(lambda row: date_convert(row.time), axis = 1)
        query_log = query_log_complete.loc[query_log_complete['Date'] >= date_convert(TSS)]
        query_log = query_log.drop(['Date'], axis=1)
        query_log['time'] = query_log_complete.apply(lambda row: date_format(row.time), axis = 1)
        return query_log


    #Query Summary Report
    query_log = date_filter(TSS,TSE)
    product_freq = query_log["Category"].value_counts().rename_axis('products').reset_index(name='counts')
    module_logger.info(product_freq.shape)
    QSRcounts = product_freq.counts.tolist()
    prod_count = product_freq.count()
    prod_count = int(prod_count[0])
    # print(prod_count)

    QSRproducts = product_freq.products.tolist()

    #user wise summary report
    query_log = date_filter(TSS,TSE)
    query_log["new_category"] = 1
    user_wise_log = pd.pivot_table(query_log, values="new_category", index=["user_name"],columns=["Category"], aggfunc= np.sum).reset_index()
    user_wise_log=user_wise_log.fillna(0)
    module_logger.info(user_wise_log.shape)

    #print(user_wise_log)
    user_count = user_wise_log.count()
    user_count = int(user_count[0])
    USRproducts = list(user_wise_log.columns)
    USRproducts = USRproducts[1:]
    USRcount = []
    Prod_count = []
    Prod_count.append(prod_count)
    #print(row_col_count)
    #print(type(row_col_count))
    for user in range(prod_count+1):
        #print(user)
        #print(list(user_wise_log.iloc[user]))
        a = list(user_wise_log[user_wise_log.columns[user]])  # df.iloc[]

        USRcount.append(a)
    USRusers = list(user_wise_log.user_name)



    #Time line of search related to product
    # Time line of search related to product
    query_log = date_filter(TSS, TSE)
    query_log["new_category"] = 1
    date_wise_log = pd.pivot_table(query_log, values="new_category", index=["time"], columns=["Category"],
                                   aggfunc=np.sum).reset_index()
    date_wise_log = date_wise_log.fillna(0)
    module_logger.info(date_wise_log.shape)
    #print(date_wise_log)
    entry_count = date_wise_log.count()
    entry_count = int(entry_count[0])
    Entry_count = []
    Entry_count.append(entry_count)
    PQTLproducts = list(date_wise_log.columns)
    # print(PQTLproducts)
    PQTLproducts = PQTLproducts[1:]
    PQLTcount = []
    # print(PQTLproducts)
    # print(USRproducts)
    for time in range(prod_count+1):
        #print(time)

        a = list(date_wise_log[date_wise_log.columns[time]])
        PQLTcount.append(a)

    # print(PQLTtime)
    PQLTtime = list(date_wise_log.time)


    # colors=[]
    # for color in range(prod_count):
    #     i = hex (123123123)
    #     i = '#'+ i
    #     colo


    List_count = []
    list_count = 2*(prod_count)+6
    List_count.append(list_count)


    #print(USRusers)
    lis = []
    lis.append(List_count)
    lis.append(QSRcounts)# to be used for querry summary report, it sends count of querry against each product
    #lis.append(QSRproducts)# it sends list of category of products
    lis.append(QSRproducts)
    lis.append(USRusers)
    lis.append(Prod_count)
    lis.append(PQLTtime)
    lis.append(PQTLproducts)
    for user in range(1,prod_count+1):
        lis.append(USRcount[user])
    #lis.append(PQTLproducts)
    #lis.append(PQLTtime)
    #lis.append(Entry_count)
    #lis.append(PQLTtime)

    for time in range(1,prod_count+1):
        lis.append(PQLTcount[time])

    return lis
# print(lis)