def report():
    

    #import modules
    import numpy as np
    import pandas  # for dataframes
    import matplotlib.pyplot as plt # for plotting graphs
    import seaborn as sns # for plotting graphs

    from matplotlib.backends.backend_pdf import PdfPages # saving multiple plots to a pdf


    # In[99]:


    data = pandas.read_csv('telecom_churn.csv')

    churn = data.groupby('Churn')
    churn.mean()




    data.Churn.value_counts()

    # In[106]:


    #default churn rate
    labels = 'Churn', 'Stay'
    sizes = [data.Churn[data['Churn'] == 1].count(), data.Churn[data['Churn'] == 0].count()]
    explode = (0.1, 0)


    # In[107]:


    fig, ax = plt.subplots(figsize=(5, 5))
    ax.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%', shadow=True)
    ax.axis('equal')

    plt.title("Proportion of customer churned and retained")
    plt.savefig('proportions.pdf')



    # In[108]:


    features = ['Churn','AccountWeeks','ContractRenewal','DataPlan', 'DataUsage','CustServCalls','DayMins','DayCalls','MonthlyCharge','OverageFee','RoamMins']
    fig = plt.subplots(figsize=(15,20))

    with PdfPages('plots.pdf') as pdf:   
        for i, j in enumerate(features):
            plt.subplot(6, 2, i+1)
            plt.subplots_adjust(hspace = 1.0)
            sns.countplot(x=j, data = data)
            plt.xticks(rotation=90)
            #fig_name = "plot" + str(i)
            #plt.savefig(fig_name)
            plt.title("Customers")
        pdf.savefig()


    # In[122]:


    #plotting correlation matrix
    with PdfPages('correlation_matrix.pdf') as pdf:  
        fig = plt.figure(figsize=(19, 15))
        plt.matshow(data.corr(), fignum=fig.number)
        plt.xticks(range(data.shape[1]), data.columns, fontsize=14, rotation=45)
        plt.yticks(range(data.shape[1]), data.columns, fontsize=14)
        cb = plt.colorbar()
        cb.ax.tick_params(labelsize=14)
        plt.title('Correlation Matrix', fontsize=16)
        pdf.savefig()


    # In[109]:


    #Let's look at the relationship between variables

    df_hue = data.copy()
    df_hue["Churn"] = np.where(df_hue["Churn"] == 0, "S", "C")
    df_new = df_hue[["Churn","AccountWeeks", "DataUsage", "CustServCalls", "DayMins", "DayCalls", "MonthlyCharge", "OverageFee", "RoamMins"]]


    # In[123]:


    #A master view at all the numerical variables
    sns.pairplot(df_new, hue="Churn", palette="husl")
    plt.savefig('density_graph.pdf')


    # In[111]:


    # A closer look at the relations based on the continuous data attributes

    with PdfPages('boxplots.pdf') as pdf:   
        fig, axarr = plt.subplots(3, 2, figsize=(20, 16))
        fig.tight_layout(pad=6.0) #space between subplots

        sns.set(palette='pastel',) #setting the color/style of our plots

        #Customer Service Calls
        sns.boxplot(y = "CustServCalls", x = "Churn", hue = "Churn", data = data, ax = axarr[0][0]).set_title("Customer Service Call Distribution \n In Customer Attrition")
        #plt.savefig("boxplot_CustServCalls.png")
        
        #Monthly Charge
        sns.boxplot(y = "MonthlyCharge", x = "Churn", hue = "Churn", data = data, ax = axarr[0][1]).set_title("Monthly Charge Distribution \n In Customer Attrition")
        #plt.savefig("boxplot_MonthlyCharge.png")
        
        #Data Usage
        sns.boxplot(y = "DataUsage", x = "Churn", hue = "Churn", data = data, ax = axarr[1][0]).set_title("\nData Usage Distribution \n In Customer Attrition")
        #plt.savefig("boxplot_DataUsage.png")
        
        #Roam Mins
        sns.boxplot(y = "RoamMins", x = "Churn", hue = "Churn", data = data, ax = axarr[1][1]).set_title("\nRoam Mins Distribution \n In Customer Attrition")
        #plt.savefig("boxplot_RoamMins.png")
        
        #Day Mins
        sns.boxplot(y = "DayMins", x = "Churn", hue = "Churn", data = data, ax = axarr[2][0]).set_title("\nDay Mins Distribution \n In Customer Attrition")
        #plt.savefig("boxplot_DayMins.png")
        
        #Overage Fee
        sns.boxplot(y = "OverageFee", x = "Churn", hue = "Churn", data = data, ax = axarr[2][1]).set_title("Overage Fee Distribution \n In Customer Attrition")
        #plt.savefig("boxplot_OverageFee")
        
        pdf.savefig()


    # In[112]:


    #Let's quickly look at the histogram of categorical varaibles

    with PdfPages('histograms.pdf') as pdf:    
        fig, axarr = plt.subplots(1, 2, figsize=(12, 6))
        sns.countplot(x='DataPlan', hue = 'Churn',data = df_hue, ax=axarr[0], palette="pastel")
        #plt.savefig("histogram_DataPlan")

        sns.countplot(x='ContractRenewal', hue = 'Churn',data = df_hue, ax=axarr[1], palette="pastel")
        plt.savefig("histogram_ContractRenewal")
        pdf.savefig()


    # In[113]:


    #Let's do a quick check to see if all the 0 in DataUsage is due to the O in DataPlan
    #in percentage

    noplan_percentage = (len(data[data["DataPlan"]==0])/len(data)) *100
    nousage_percentage = (len(data[data["DataUsage"]==0])/len(data))*100

    print("The percentage for people with 0 data usage is " + str(round(nousage_percentage, 2)) + " percent")
    print("The percentage for people with no data plan is " + str(round(noplan_percentage, 2)) + " percent")

    #in absolute number 
    nousage = len(data[data["DataUsage"]==0])
    noplan = len(data[data["DataPlan"]==0])

    print(str(nousage) + " numbers of people have 0 data usage.")
    print(str(noplan) + " numbers of people have 0 data plan.")
    print("\nRemark: 598 people who did not purchase a data plan were also using data. Let's check the roaming data.")

    #for the people who didn't have a data plan but still have data usage, to they belong to roaming?
    #Roaming info

    roam = len(data[data["RoamMins"]!=0])
    print("\n" + str(roam) + " numbers of people used roaming.")
    print("\nRemark: Seems like almost everyone uses Roaming and it does not relates to wheather you use data.")


    # In[117]:


    #using a pie chart to visualize the relationship between the three variables

    group_names=['no DataPlan', 'DataPlan']
    group_size=[2411, (3333-2411)]

    subgroup1_names=['no DataUse','DataUse']
    subgroup1_size=[1813, (3333-1813)]

    subgroup2_names=['no Roam', 'Roaming']
    subgroup2_size=[(3333-3315), 3315]

    a, b, c=[plt.cm.Blues, plt.cm.Reds, plt.cm.Greens]
    
    with PdfPages('DataPlan_DataUsage_Roam.pdf') as pdf:    
        # First Ring (Outside)
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.axis('equal')
        mypie, _ = ax.pie(group_size, radius=1.0, labels=group_names, colors=[b(0.3), a(0.3)])
        plt.setp( mypie, width=0.3, edgecolor='white')

        # Second Ring (Inside)
        mypie2, _ = ax.pie(subgroup1_size, radius=1.0-0.3, labels=subgroup1_names, labeldistance=0.7, colors=[a(0.2), b(0.2)])
        plt.setp( mypie2, width=0.4, edgecolor='white')
        plt.margins(0,0)

        # Third Ring (Most Inner)
        mypie3, _ = ax.pie(subgroup2_size, radius=1.0-0.3-0.3, labels=subgroup2_names, labeldistance=0.7, colors=[a(0.1), b(0.1)])
        plt.setp( mypie3, width=0.4, edgecolor='white')
        plt.margins(0,0)

        ax.set(title='DataPlan vs. DataUsage vs. Roam\n')
        pdf.savefig()


    # In[118]:


    #categorical variables exploration

    with PdfPages('categorical_variables_exploration.pdf') as pdf:   
        fig, axs = plt.subplots(3, 2, figsize=(18,10)) 
        explode = (0, 0.1)
        labels=['Churn', 'Not Churn']

        #data plan 
        has_plan=[len(data[(data["DataPlan"]==1) & (data["Churn"]==1)]), len(data[(data["DataPlan"]==1) & (data["Churn"]==0)])]
        axs[0, 0].pie(has_plan, explode=explode, labels=labels, autopct='%1.1f%%', shadow=True)
        #plt.savefig("PieChart_DataPlan_1")
        axs[0, 0].set_title("Customers with a Data Plan")

        no_plan = [len(data[(data["DataPlan"]==0) & (data["Churn"]==1)]), len(data[(data["DataPlan"]==0) & (data["Churn"]==0)])]       
        axs[0, 1].pie(no_plan, explode=explode, labels=labels, autopct='%1.1f%%', shadow=True)
        #plt.savefig("PieChart_DataPlan_0")
        axs[0, 1].set_title("Customers without a Data Plan")

        #Contract Renewal 
        has_ContractRenewal=[len(data[(data["ContractRenewal"]==1) & (data["Churn"]==1)]), len(data[(data["DataPlan"]==1) & (data["Churn"]==0)])]
        axs[1, 0].pie(has_ContractRenewal, explode=explode, labels=labels, autopct='%1.1f%%', shadow=True)
        #plt.savefig("PieChart_ContractRenewal_1")
        axs[1, 0].set_title("Customers who recently renewed contracts")

        no_ContractRenewal = [len(data[(data["ContractRenewal"]==0) & (data["Churn"]==1)]), len(data[(data["DataPlan"]==0) & (data["Churn"]==0)])]
        axs[1, 1].pie(no_ContractRenewal, explode=explode, labels=labels, autopct='%1.1f%%', shadow=True)
        #plt.savefig("PieChart_ContractRenewal_0")
        axs[1, 1].set_title("Customers who didn't renewed contracts")

        #Datausage    
        has_Datausage=[len(data[(data["DataUsage"]!=0) & (data["Churn"]==1)]), len(data[(data["DataUsage"]!=0) & (data["Churn"]==0)])]
        axs[2, 0].pie(has_Datausage, explode=explode, labels=labels, autopct='%1.1f%%', shadow=True)
        #plt.savefig("PieChart_DataUsage_1")
        axs[2, 0].set_title("Customers who has data usage")

        no_Datausage = [len(data[(data["DataUsage"]==0) & (data["Churn"]==1)]), len(data[(data["DataUsage"]==0) & (data["Churn"]==0)])]
        axs[2, 1].pie(no_Datausage, explode=explode, labels=labels, autopct='%1.1f%%', shadow=True)
        #plt.savefig("PieChart_DataUsage_0")
        axs[2, 1].set_title("Customers who has 0 data usage")

        #plt.show()
        pdf.savefig()





