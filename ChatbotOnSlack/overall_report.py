# import dependencies and map the folder
import os, xlsxwriter, pandas as pd, numpy as np, shlex, subprocess, requests

def complete_report(TSS, TSE):

    def date_filter(TSS,TSE):
        query_log_complete = pd.read_csv("./data/result.csv")
        query_count = query_log_complete.count()
        query_count = query_count[0]
        query_log_complete['time'] = pd.to_datetime(query_log_complete['time'], format='%d%m%Y', errors='ignore')
        query_log_complete['time']
        mask = (query_log_complete['time'] >= TSS) & (query_log_complete['time'] <= TSE)
        query_log= query_log_complete.loc[mask]
        return query_log
        # create excels sheet

    workbook = xlsxwriter.Workbook('./data/Tubclass_Report.xlsx')
    # Cell Formating to bold
    bold = workbook.add_format({'bold': True, 'border': 1, 'text_wrap': 1})
    size = workbook.add_format({'font_size': 12, 'border': 1, 'text_wrap': 1})
    border = workbook.add_format({'border': 1, 'text_wrap': 1, })
    dtype_num = workbook.add_format({'border': 1, 'num_format': '###'})
    align_center = workbook.add_format({'align': 'center', 'border': 1, 'text_wrap': 1})
    white_cell = workbook.add_format({'bold': True, 'font_color': 'colour'})
    # Merge Format For Merging cells
    merge_format_header = workbook.add_format(
        {'bold': 0, 'border': 1, 'align': 'center', 'valign': 'vcenter', 'fg_color': 'yellow', 'font_size': 18})
    merge_format_date = workbook.add_format({'bold': 0, 'border': 1, 'valign': 'vcenter', 'font_size': 12})

    def UWQS(TSS, TSE):
        query_log = date_filter(TSS, TSE)
        # general querry count
        query_count = query_log.count()
        query_count = query_count[0]
        # print(query_log)
        # we will create a pivot table to create bar graph
        # counting no. of product to decide no of columns required for pivot table
        product_freq = query_log["Category"].value_counts().rename_axis('products').reset_index(name='counts')
        all_product_count = product_freq.count()
        all_product_count = all_product_count[0]
        # adding a column just to make product count per user to add in pivot table
        # we do so in another dataframe so that the main dataframe is not altered
        query_log_changed = query_log
        query_log_changed["new_category"] = 1
        # creating pivot table
        user_wise_log = pd.pivot_table(query_log, values="new_category", index=["user_name"], columns=["Category"],
                                       aggfunc=np.sum).reset_index()
        # Converting all NAN values to zero
        user_wise_log = user_wise_log.fillna(0)
        # counting no of users
        # the very next line of code is not working
        # user_count = user_wise_log['user_name'].count()
        a = user_wise_log.count()
        user_count = a[0]
        # print(user_count)
        worksheetUWQS = workbook.add_worksheet("UWQS1")  # UWQR is user wise querry summary
        # pending setup the page for print: for that we will have to keep no. of columns as variable
        # pending set width of all the columns
        # writing intial format to excel, here to merging of columns needs to be extended upto products
        max_column = all_product_count + 1
        worksheetUWQS.merge_range(0, 0, 0, max_column, "Querry Summary Report", merge_format_header)
        worksheetUWQS.merge_range(1, 0, 1, max_column, "Start Date:   " + str(TSS), merge_format_date)
        worksheetUWQS.merge_range(2, 0, 2, max_column, "End Date:   " + str(TSE), merge_format_date)
        worksheetUWQS.merge_range(3, 0, 3, max_column, "Total No Of Querries:   " + str(query_count), merge_format_date)
        worksheetUWQS.merge_range(4, 0, 4, max_column, "Total No Of Products:   " + str(all_product_count),
                                  merge_format_date)
        worksheetUWQS.write(5, 0, "Sl.No.", bold)
        worksheetUWQS.write(5, 1, "User", bold)
        for product in range(2, all_product_count + 2):
            # print(product)
            product_new = product - 1
            # print(user_wise_log.columns[product_new])

            worksheetUWQS.write(5, product, user_wise_log.columns[product_new], bold)
        for row in range(user_count):
            worksheetUWQS.write(row + 6, 0, row + 1, align_center)
        # print(user_wise_log)
        for product in range(all_product_count + 1):
            # print(product)
            product_new = product + 1
            product_col = user_wise_log.columns[product]
            # print(product_col)
            product_name = user_wise_log[product_col]
            for row in range(user_count):
                worksheetUWQS.write(row + 6, product_new, product_name[row], align_center)

        # BarGraph
        chart1 = workbook.add_chart({'type': 'bar', 'subtype': 'stacked'})
        for bar in range(all_product_count):
            bar1 = bar + 1
            bar2 = bar + 2
            max_row = user_count + 6
            # Configure the first series.
            chart1.add_series({
                'name': ['UWQS1', 5, bar2],
                'categories': ['UWQS1', 6, 1, max_row, 1],
                'values': ['UWQS1', 6, bar2, max_row, bar2],
            })

        # Add a chart title and some axis labels.
        chart1.set_title({'name': 'User-wise query report'})
        chart1.set_x_axis({'name': 'No. of Queries'})
        chart1.set_y_axis({'name': 'Users'})

        # Set an Excel chart style.
        chart1.set_style(11)

        # Insert the chart into the worksheet (with an offset).
        worksheetUWQS.insert_chart('G1', chart1, {'x_offset': 0, 'y_offset': 0})

    UWQS(TSS, TSE)
    def QSR(TSS, TSE):
        query_log = date_filter(TSS, TSE)
        product_freq = query_log["Category"].value_counts().rename_axis('products').reset_index(name='counts')
        # print(product_freq.products[0])
        all_product_count = product_freq.count()
        all_product_count = all_product_count[0]
        # print(all_product_count)
        query_count = query_log.count()
        query_count = query_count[0]
        excel_len = query_count + 6
        worksheetQSR = workbook.add_worksheet("QRS1")
        worksheetQSR.set_landscape()
        worksheetQSR.print_area(0, 0, excel_len, 3)
        worksheetQSR.set_column('A:A', 16)
        worksheetQSR.set_column('B:B', 45)
        worksheetQSR.set_column('C:C', 30)
        worksheetQSR.set_column('D:D', 1)  # just to place the graph at this position
        worksheetQSR.merge_range('A1:C1', "Querry Summary Report", merge_format_header)
        worksheetQSR.merge_range('A2:C2', "Start Date:   " + str(TSS), merge_format_date)
        worksheetQSR.merge_range('A3:C3', "End Date:   " + str(TSE), merge_format_date)
        worksheetQSR.merge_range('A4:C4', "Total No Of Querries:   " + str(query_count), merge_format_date)
        worksheetQSR.merge_range('A5:C5', "Total No Of Products:   " + str(all_product_count), merge_format_date)
        worksheetQSR.write(5, 0, "Sl. No.", bold)
        worksheetQSR.write(5, 1, "Product", bold)
        worksheetQSR.write(5, 2, "Count", bold)
        for row in range(all_product_count):
            worksheetQSR.write(row + 6, 0, row + 1, align_center)
            worksheetQSR.write(row + 6, 1, product_freq.products[row], border)
            worksheetQSR.write(row + 6, 2, product_freq.counts[row], dtype_num)

        ##Whitening cells did not work
        # worksheetQSR.write('D1:Z1',"", white_cell)
        # for row in range(excel_len, excel_len+20):
        #    worksheetQSR.write(row,0,"", white_cell)
        #   worksheetQSR.write(row,1,"", white_cell)
        #   worksheetQSR.write(row,2,"", white_cell)

        ###################Creating Graph
        # Create a new chart object.
        chart1 = workbook.add_chart({'type': 'pie'})

        # Configure the series. Note the use of the list syntax to define ranges:
        product_count4graph = all_product_count + 5
        chart1.add_series({
            'name': 'Querry Summary Report',
            'categories': ['QRS1', 6, 1, product_count4graph, 1],
            'values': ['QRS1', 6, 2, product_count4graph, 2],
        })

        chart1.set_title({'name': 'Querry Summary Report'})  # Add a title.

        chart1.set_style(10)  # Set an Excel chart style. Colors with white outline and shadow.

        # Setting Dimantion of chart
        chart1.set_size({'width': 666, 'height': 450})
        # Insert the chart into the worksheet (with an offset).
        worksheetQSR.insert_chart('D1', chart1, {'x_offset': 0, 'y_offset': 0})

    QSR(TSS, TSE)

    def QSRlog(TSS, TSE):  # take TimeStampStart(TSS) and TimeStampEnd(TSE) as argument
        query_log = date_filter(TSS, TSE)
        print(query_log)
        query_count = query_log.count()
        query_count = query_count[0]
        excel_len = query_count + 5
        worksheetQSRlog = workbook.add_worksheet("Query Log")
        worksheetQSRlog.set_landscape()
        worksheetQSRlog.print_area(0, 0, excel_len, 5)
        worksheetQSRlog.set_column('A:A', 6)
        worksheetQSRlog.set_column('B:B', 20)
        worksheetQSRlog.set_column('C:C', 15)
        worksheetQSRlog.set_column('D:D', 30)
        worksheetQSRlog.set_column('E:E', 20)
        worksheetQSRlog.merge_range('A1:E1', "Querry Log", merge_format_header)
        worksheetQSRlog.merge_range('A2:E2', "Start Date:   " + str(TSS), merge_format_date)
        worksheetQSRlog.merge_range('A3:E3', "End Date:   " + str(TSE), merge_format_date)
        worksheetQSRlog.merge_range('A4:E4', "Total No Of Querries:   " + str(query_count), merge_format_date)
        worksheetQSRlog.write(4, 0, "Sl. No.", bold)
        worksheetQSRlog.write(4, 1, "Date", bold)
        worksheetQSRlog.write(4, 2, "User", bold)
        worksheetQSRlog.write(4, 3, "Querry", bold)
        worksheetQSRlog.write(4, 4, "Product", bold)
        # print(query_log)
        for row in range(query_count):
            worksheetQSRlog.write(row + 5, 0, row + 1, align_center)
            worksheetQSRlog.write(row + 5, 1, query_log.time[row], border)
            worksheetQSRlog.write(row + 5, 2, query_log.user_name[row], border)
            worksheetQSRlog.write(row + 5, 3, query_log.User_query[row], border)
            worksheetQSRlog.write(row + 5, 4, query_log.Category[row], border)
        ##Whitening cells did not work
        # worksheetQSRlog.write('F1:Z1',"", white_cel
        # for row in range(excel_len, excel_len+20):
        # worksheetQSRlog.write(row,0,"", white_cell)
        # worksheetQSRlog.write(row,1,"", white_cell)
        # worksheetQSRlog.write(row,2,"", white_cell)
        # worksheetQSRlog.write(row,3,"", white_cell)
        # worksheetQSRlog.write(row,4,"", white_cell)

    QSRlog(TSS, TSE)

    def QTL(TSS, TSE):
        query_log = date_filter(TSS, TSE)
        # general querry count
        query_count = query_log.count()
        query_count = query_count[0]
        # we will create a pivot table to create bar graph
        # counting no. of product to decide no of columns required for pivot table
        product_freq = query_log["Category"].value_counts().rename_axis('products').reset_index(name='counts')
        all_product_count = product_freq.count()
        all_product_count = all_product_count[0]
        # adding a column just to make product count per user to add in pivot table
        # we do so in another dataframe so that the main dataframe is not altered
        query_log_changed = query_log
        query_log_changed["new_category"] = 1
        # creating pivot table
        user_wise_log = pd.pivot_table(query_log, values="new_category", index=["time"], columns=["Category"],
                                       aggfunc=np.sum).reset_index()
        # Converting all NAN values to zero
        user_wise_log = user_wise_log.fillna(0)
        # counting no of users
        # the very next line of code is not working
        # user_count = user_wise_log['user_name'].count()
        a = user_wise_log.count()
        user_count = a[0]
        print(user_count)
        worksheetUWQS = workbook.add_worksheet("QTL")  # UWQR is user wise querry summary
        # pending setup the page for print: for that we will have to keep no. of columns as variable
        # pending set width of all the columns
        # writing intial format to excel, here to merging of columns needs to be extended upto products
        max_column = all_product_count + 1
        worksheetUWQS.merge_range(0, 0, 0, max_column, "Querry Summary Report", merge_format_header)
        worksheetUWQS.merge_range(1, 0, 1, max_column, "Start Date:   " + str(TSS), merge_format_date)
        worksheetUWQS.merge_range(2, 0, 2, max_column, "End Date:   " + str(TSE), merge_format_date)
        worksheetUWQS.merge_range(3, 0, 3, max_column, "Total No Of Querries:   " + str(query_count), merge_format_date)
        worksheetUWQS.merge_range(4, 0, 4, max_column, "Total No Of Products:   " + str(all_product_count),
                                  merge_format_date)
        worksheetUWQS.write(5, 0, "Sl.No.", bold)
        worksheetUWQS.write(5, 1, "User", bold)
        for product in range(2, all_product_count + 2):
            # print(product)
            product_new = product - 1
            # print(user_wise_log.columns[product_new])

            worksheetUWQS.write(5, product, user_wise_log.columns[product_new], bold)
        for row in range(user_count):
            worksheetUWQS.write(row + 6, 0, row + 1, align_center)
        # print(user_wise_log)
        for product in range(all_product_count + 1):
            # print(product)
            product_new = product + 1
            product_col = user_wise_log.columns[product]
            # print(product_col)
            product_name = user_wise_log[product_col]
            for row in range(user_count):
                worksheetUWQS.write(row + 6, product_new, product_name[row], align_center)

        # BarGraph
        chart1 = workbook.add_chart({'type': 'line'})
        for bar in range(all_product_count):
            colour = 10000000 + (bar*10000)
            col_hex = '{:06x}'.format(colour)
            col_hex = '#' + col_hex
            print(col_hex)
            bar1 = bar + 1
            bar2 = bar + 2
            max_row = user_count + 6
            # Configure the first series.
            chart1.add_series({
                'name': ['QTL', 5, bar2],
                'categories': ['QTL', 6, 1, max_row, 1],
                'values': ['QTL', 6, bar2, max_row, bar2],
                'line': {'color': col_hex}
            })

        # Add a chart title and some axis labels.
        chart1.set_title({'name': 'User-wise query report'})
        chart1.set_x_axis({'name': 'No. of Queries'})
        chart1.set_y_axis({'name': 'Users'})

        # Set an Excel chart style.
        chart1.set_style(11)

        # Insert the chart into the worksheet (with an offset).
        worksheetUWQS.insert_chart('G1', chart1, {'x_offset': 0, 'y_offset': 0})
        workbook.close()
    QTL(TSS, TSE)

def upload_report(keys):
    cha = keys['channel_report']
    chai = keys['slack_bot_token']
    chaii = 'Please find the report attached'
    xls_name = "./data/Tubclass_Report.xlsx"
    try:
        command_line = 'curl -F file=@%s -F "initial_comment=%s" -F channels=%s -H "Authorization: Bearer %s" https://slack.com/api/files.upload'%(
            xls_name, chaii, cha, chai)
        args = shlex.split(command_line)
        subprocess.Popen(args)
        print(args)
    except (
            AssertionError, AttributeError, EOFError, FloatingPointError, GeneratorExit, ImportError, IndexError,
            KeyError,
            KeyboardInterrupt, MemoryError, NameError, NotImplementedError, OSError, OverflowError, ReferenceError,
            RuntimeError, StopIteration, SyntaxError, IndentationError, TabError, SystemError, SystemExit,
            TypeError,
            UnboundLocalError, UnicodeError, UnicodeEncodeError, UnicodeDecodeError, UnicodeTranslateError,
            ValueError,
            ZeroDivisionError):
        headers = {
            'Authorization': keys['slack_bot_token']
        }
        print(headers)
        files = {
            'file': ('C:\\Users\\z003ww7c.AD001\\PycharmProjects\\SlackIntegration\\data\\result.csv',
                     open('C:\\Users\\z003ww7c.AD001\\PycharmProjects\\SlackIntegration\\data\\result.csv', 'rb')),
            'initial_comment': 'Please find the report attached',
            'channels': keys['channel_report'],
        }
        url = 'https://slack.com/api/files.upload'
        requests.post(url, headers=headers, files=files)
