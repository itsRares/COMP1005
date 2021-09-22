from helpers import *
from community import *

#Resets the console and header
def resetHeader():
    os.system('clear')
    print("---=== Tesla Power Modelling System ===---")

#Main menu, User can select what section they would like
def menuModelling(house):
    resetHeader()

    option=True
    while option:
        print("""
        1. View Appliance Usage
        2. Search Appliance
        3. Add Appliances
        4. Go back
        """)
        option=input("What would you like to do? ")
        if option=="1":
            #Ensure there are appliances to plot
            if house.getAppliance() != []:
                viewAppQuestions(house) #Plot usage
            else:
                os.system('clear')
                print("No data found, Please add appliances then search!")
        elif option=="2":
            #Ensure there are appliances to plot
            if house.getAppliance() != []:
                searchAppliance(house) #Search appliances
            else:
                os.system('clear')
                print("No data found, Please add appliances then search!")
        elif option=="3":
            addAppliance(house) #Add new appliances
        elif option=="4":
            #Back to home
            os.system('clear')
            print("---=== Welcome to TESLA POWER ===---")
            option = None
        else:
            #Back to home
            os.system('clear')
            print("Invalid choice, What would you like to do? ")

#--------------------------- Search Appliance

#Search appliances
def searchAppliance(house):
    resetHeader()

    option=input("Input the name of the Appliance... ")
    #Check and see if appliance 
    if not house.containsAppliance(option):
        print("No appliances found.")

    input("\nPress enter to continue... ")   
    resetHeader()

#--------------------------- Add Appliance

#Add Appliance menu, User can select what section they would like
def addAppliance(house):
    resetHeader()

    option=True 
    while option:
        print("""
        How would you like to input data?
        1. File Input
        2. Input Appliance
        3. Go back
        """)
        option=input("What would you like to do? ")
        if option == "1":
            addApplianceFile(house) #Add Appliance via file input
            option = None
        elif option=="2":
            addApplianceInput(house) #Add Appliance manually
            option = None
        elif option=="3":
            #Back to main menu
            option = None
        else:
            #If invalid try again
            os.system('clear')
            print("Invalid choice, What would you like to do? ")

    input("\nPress enter to continue... ")
    resetHeader()

#Add Appliance via file input
def addApplianceFile(house):
    fileobj = fileInput() #Get file input, returns file obj

    #For each line
    for idx,line in enumerate(fileobj):
        line_s = line.strip() #Strip whitespace
        #Seperate by ':' and put into array - shorthand
        usages = [x for x in line_s.split(':')] 
        #If not the first index
        if idx != 0:
            #Seperate by ',' and put into array - shorthand
            activity = [x for x in usages[2].split(',')]
            #Create new appliance (name,usage,activity)
            appliance = Appliance(usages[0], usages[1], activity)
            #Add appliance to the household
            house.addAppliance(appliance)
            #Create delay - for design
            time.sleep(0.1)
        else:
            #Else change amount of residents in house
            #if idx == 0
            house.changeResidents(usages[1])

#Add Appliance manually
def addApplianceInput(house):
    resetHeader()

    #Input the name of the appliance
    print("1. Input the name of the Appliance... ")
    name=input("> ")

    #Input the usage
    print("2. Input the usage (W) of the Appliance")
    watt = numberInput()

    print("3. Input activity of appliance (0-1) seperated by commas x 24(hrs)")
    print("eg) 0,0,0,0,0.25,0,0,1,0,0,0.15,0,0,0,0.5,0,0,0,1,1,0,0,0,0")

    option=True
    while option:
        #Input the activity
        activity = input("> ")
        #Check to see if 24 values
        if activity.count(",") == 23:
            option = None
        else:
            print('Error: Please enter 24 comma seperated values')

        #Check to see if correct format (a float)
        activities = [x for x in activity.split(',')]
        for a in activities:
            try:
                float(a)
            except:
                print('Error: Not a number')
                option = True

    #Create new appliance (name,usage,activity)
    appliance = Appliance(name, watt, activities)
    #Add appliance to the household
    house.addAppliance(appliance)

#--------------------------- View Appliance

#View Appliance menu, User can select what section they would like
def viewAppQuestions(house):
    resetHeader()

    option=True
    while option:
        print("""
        1. Appliance Ratings
        2. All Appliance Usage plot
        3. Appliance Usage Plot
        4. Day General Usage vs Appliance Usage
        """)
        option=input("What would you like to do? ")
        if option=="1":
            applianceRating(house) #View list of appliance rating
            option = None
        elif option=="2":
            showAllUsage(house) #Show all appliance usage
            option = None
        elif option=="3":
            applianceUsage(house) #Show select appliance usage
            option = None
        elif option=="4":
            generalAppUsage(house) 
            option = None
        else:
            #Back to main menu
            os.system('clear')
            print("Invalid choice, What would you like to do? ")
    
    input("\nPress enter to continue... ") 
    resetHeader() 

#View list of appliance rating
def applianceRating(house):
    appliances = house.getAppliance() #Get all appliances

    #For each show the rating
    for a in appliances:
        a.showRating()

#Show all appliance usage
def showAllUsage(house):
    #24hrs
    hours = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24]
    #Get household appliances
    appliances = house.getAppliance()
    appUsage = []

    output_file('output/appGeneral.html', mode='inline')

    #Plot
    plot = figure(title='Appliance Power Usage for household', x_axis_label='Hour',
                  y_axis_label='Power Usage (W)')

    #Get color pallete
    colors = itertools.cycle(palette)

    #For each appliance
    for idx,a in enumerate(appliances):
        tempList = []
        nameList = []

        activity = a.getActivity() #Get actvity of appliance
        watt = a.getUsage() #Get usage of appliance
        for act in activity:
            #Calc hourly usage (watt * usage)
            nameList.append(a.getName())
            tempList.append(float(act) * float(watt))
        
        #Create datasource
        source_usage = ColumnDataSource(data=dict(
            name=nameList,
            hour=hours,
            usage=tempList,
        ))

        color = next(colors) #Next color
        #Plot line
        plot.line('hour', 'usage', line_width=2, line_color=color, source=source_usage)
        #Plot circle info dot
        plot.circle('hour', 'usage', fill_color=color, line_color=color, size=8, source=source_usage)

    #No scientific numbers on Y column
    plot.left[0].formatter.use_scientific = False

    #When hover over circle show this
    hover = HoverTool(
        tooltips=[
            ('Name', '@name'),
            ('Hour', '@hour'),
            ('Usage', '@usage W')
        ]
    )

    plot.add_tools(hover)
    show(plot)  

#Show select appliance usage
def applianceUsage(house):
    resetHeader()

    #Check if appliance exists
    option=input("Input the name of the Appliance... ")
    appliance = house.containsAppliance(option)

    if not appliance:
        print("No appliances found.")
    else:
        #24hrs
        hours = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24]
        tempList = []

        watt = appliance.getUsage() #Get actvity of appliance
        activity = appliance.getActivity() #Get usage of appliance

        #Calc hourly usage (watt * usage)
        for act in activity:
            tempList.append(float(act) * float(watt))

        output_file('output/appSingle.html', mode='inline')

        plot = figure(title=appliance.getName() + ' Power Usage for household', x_axis_label='Hour',
                  y_axis_label='Power Usage (W)')

        #Create datasource
        source_usage = ColumnDataSource(data=dict(
            hour=hours,
            usage=tempList,
        ))

        #Colors
        colors = itertools.cycle(palette)
        color = next(colors)

        #Plot line
        plot.line('hour', 'usage', line_width=2, line_color=color, legend_label=''+appliance.getName()+'', source=source_usage)
        #Plot circle info dot
        plot.circle('hour', 'usage', fill_color=color, line_color=color, size=8, source=source_usage)

        #No scientific numbers on Y column
        plot.left[0].formatter.use_scientific = False

        #When hover over circle show this
        hover = HoverTool(
            tooltips=[
                ('Hour', '@hour'),
                ('Usage', '@usage W')
            ]
        )

        plot.add_tools(hover)
        show(plot)

def generalAppUsage(house):
    daily_date = []
    daily_usage = []
    gen_usage = [] 

    print("Add single day usage data...")
    fileobj = fileInput() #Get file input, returns file object

    #Loop through each time
    for line in fileobj:
        try:
            line_s = line.strip() #Strip whitespace
            #Seperate date and usage and put in array
            usages = [x for x in line_s.split(',')]
            #Add usage to the household
            datetime_object = datetime.strptime(usages[0], '%d %m %Y %H:%M:%S') 
            daily_date.append(datetime_object)
            daily_usage.append(usages[1]) 
        except: #Other errors
            print('Error adding daily value') 

    appliances = house.getAppliance()
    appUsage = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

    #For each appliance
    for a in appliances:
        activity = a.getActivity() #Get actvity of appliance
        watt = a.getUsage() #Get usage of appliance
        for idx,act in enumerate(activity):
            #Calc hourly usage (watt * usage)
            appUsage[idx] += float(act) * float(watt)

    for idx,usage in enumerate(appUsage):
        #Calc w to kWh
        appUsage[idx] = float((usage * 1.0) / 1000.0)

    output_file('output/generalAppUsage.html', mode='inline')

    #Loop through each usage
    for idx,usage in enumerate(daily_usage):
        if idx != 0: #If not first usage
            #Minus previous day and current day to get daily usage
            gen_usage.append(int(daily_usage[idx]) - int(daily_usage[idx-1]))

    newDate = []
    #Panda used to create hourly data range
    datelist = pd.date_range('2020-05-27', periods=24, freq='H')

    #Create datasource - Daily
    source = ColumnDataSource(data=dict(
        date=datelist, 
        usage=appUsage
    ))

    #Create datasource - appliance
    source_usage = ColumnDataSource(data=dict(
        date=daily_date,
        usage=gen_usage,
    ))
    
    #Plot, datetime type
    plot = figure(title='Day General Usage vs Appliance Usage', x_axis_label='Date',
                  y_axis_label='Power Consumption (kWh)', x_axis_type='datetime')
    
    #Plot line
    plot.vbar(x='date', top='usage', width=3000000, legend_label='Appliance Usage', color=(88, 175, 219), source=source)
    #Plot line
    plot.line('date', 'usage', line_width=2, line_color='green', legend_label='Power Usage', source=source_usage)
    #Plot circle info dot
    plot.circle('date', 'usage', fill_color="green", line_color='green', size=8, source=source_usage)
    #No scientific numbers on Y column
    plot.left[0].formatter.use_scientific = False

    labels = LabelSet(x='date', y='usage', text='usage', level='glyph', x_offset=-13.5, y_offset=0, source=source, render_mode='canvas', text_font_size="7pt")

    #Start at 0
    plot.y_range.start = 0
    plot.xgrid.grid_line_color = None

    hover = HoverTool(
        tooltips=[
            ('Date', '@date{%F}'), 
            ('Usage', '@usage kWh')
        ],
        formatters={
            '@date': 'datetime'
        }
    )
    
    plot.add_tools(hover)
    plot.add_layout(labels)
    show(plot)