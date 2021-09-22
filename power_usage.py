#
# Student Name: Rares Popa
# Student ID  : 19159700
#
# power_usage.py: Calculates and plots power usage
#

from helpers import *

#Resets the console and header
def resetHeader():
    os.system('clear')
    print("---=== Tesla Power Usage System ===---")

#Main menu, User can select what section they would like
def menuUsage(house):
    resetHeader()

    option=True
    while option:
        print("""
        1. View Power Usage
        2. Add Power Usage
        3. Go back
        """)
        option=input("What would you like to do? ") #Input
        if option=="1":
            #Ensure there are usages to plot
            if house.getDateUsage() != []:
                viewQuestions(house) #Plot usage
            else:
                os.system('clear')
                print("No data found, Please add power usage then view it!")
        elif option=="2":
            addUsage(house) #Add Power Usage
        elif option=="3":
            #Back to home
            os.system('clear')
            print("---=== Welcome to TESLA POWER ===---")
            option = None
        else:
            #If invalid try again
            os.system('clear')
            print("Invalid choice, What would you like to do? ")

#Add Power Usage by a file
def addUsage(house):
    fileobj = fileInput() #Get file input, returns file object

    #Loop through each time
    for line in fileobj:
        try:
            line_s = line.strip() #Strip whitespace
            #Seperate date and usage and put in array
            usages = [x for x in line_s.split(',')]
            #Add usage to the household
            house.addUsage(usages[0], usages[1]) 
        except: #Other errors
            print('Error adding usage value') 

    input("\nPress enter to continue... ")   
    resetHeader()

#Menu to ask user what they want to plot
def viewQuestions(house):
    resetHeader()

    option=True
    while option:
        print("""
        1. General Usage 
        2. Cumulative Usage
        3. Solar Generation (Bonus)
        """)
        option=input("What would you like to do? ") #Input
        if option=="1":
            generalUsage(house) #Daily general usage
            option = None
        elif option=="2":
            cumulUsage(house) #Cumulative usage
            option = None
        elif option=="3":
            solarGen(house) #Solar generation
            option = None
        else:
            #If invalid try again
            os.system('clear')
            print("Invalid choice, What would you like to do? ")

    input("\nPress enter to continue... ")   
    resetHeader()

#Daily general usage
def generalUsage(house):
    pow_date = house.getDateUsage() #Get household usage dates
    pow_usage = house.getKwhUsage() #Get household usage 
    gen_usage = []

    #Loop through each usage
    for idx,usage in enumerate(pow_usage):
        if idx != 0: #If not first usage
            #Minus previous day and current day to get daily usage
            gen_usage.append(int(pow_usage[idx]) - int(pow_usage[idx-1]))

    output_file('output/generalUsage.html', mode='inline')
    
    #Plot, datetime type
    plot = figure(title='General Power Usage for household', x_axis_label='Date',
                  y_axis_label='Power Usage (kWh)', x_axis_type='datetime')

    #Create datasource
    source_usage = ColumnDataSource(data=dict(
        date=pow_date,
        usage=gen_usage,
    ))
    
    #Plot line
    plot.line('date', 'usage', line_width=2, line_color='green', legend_label='Power Usage', source=source_usage)
    #Plot circle info dot
    plot.circle('date', 'usage', fill_color="green", line_color='green', size=8, source=source_usage)
    #No scientific numbers on Y column
    plot.left[0].formatter.use_scientific = False

    #When hover over circle show this
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
    show(plot)

#Cumulative usage
def cumulUsage(house):
    pow_date = house.getDateUsage() #Get household usage dates
    pow_usage = house.getKwhUsage() #Get household usage 

    output_file('output/cumulUsage.html', mode='inline')
    
    #Plot, datetime type
    plot = figure(title='Cumulative Power Usage for household', x_axis_label='Date',
                  y_axis_label='Power Usage (kWh)', x_axis_type='datetime')

    #Create datasource
    source_usage = ColumnDataSource(data=dict(
        date=pow_date,
        usage=pow_usage,
    ))
    
    #Plot line
    plot.line('date', 'usage', line_width=2, line_color='green', legend_label='Power Usage', source=source_usage)
    #Plot circle info dot
    plot.circle('date', 'usage', fill_color="green", line_color='green', size=8, source=source_usage)
    #No scientific numbers on Y column
    plot.left[0].formatter.use_scientific = False
    
    #When hover over circle show this
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
    show(plot)

#Cumulative usage
def solarGen(house):
    if house.getKwhSolar() == []:
        print("Input the solar generation file")
        fileobj = fileInput() #Get file input, returns file object

        #Loop through each time
        for line in fileobj:
            try:
                line_s = line.strip() #Strip whitespace
                #Seperate date and usage and put in array
                usages = [x for x in line_s.split(',')]
                #Add usage to the household
                house.addSolar(usages[0], usages[1]) 
            except: #Other errors
                print('Error adding solar value') 

    solar_date = house.getDateSolar() #Get household solar dates
    solar_usage = house.getKwhSolar() #Get household solar 

    pow_date = house.getDateUsage() #Get household usage dates
    pow_usage = house.getKwhUsage() #Get household usage 
    gen_usage = [] 

    output_file('output/solarGen.html', mode='inline')

    #Create datasource - Solar
    source = ColumnDataSource(data=dict(
        date=solar_date, 
        usage=solar_usage
    ))

    #Loop through each usage
    for idx,usage in enumerate(pow_usage):
        if idx != 0: #If not first usage
            #Minus previous day and current day to get daily usage
            gen_usage.append(int(pow_usage[idx]) - int(pow_usage[idx-1]))

    #Create datasource - household
    source_usage = ColumnDataSource(data=dict(
        date=pow_date,
        usage=gen_usage,
    ))
    
    #Plot, datetime type
    plot = figure(title='Solar Generation for household', x_axis_label='Date',
                  y_axis_label='Solar Generation (kWh)', x_axis_type='datetime')
    
    #Plot line
    plot.vbar(x='date', top='usage', width=60000000, color=(88, 175, 219), source=source)
    #Plot line
    plot.line('date', 'usage', line_width=2, line_color='green', legend_label='Power Usage', source=source_usage)
    #Plot circle info dot
    plot.circle('date', 'usage', fill_color="green", line_color='green', size=8, source=source_usage)
    #No scientific numbers on Y column
    plot.left[0].formatter.use_scientific = False

    labels = LabelSet(x='date', y='usage', text='usage', level='glyph', x_offset=-13.5, y_offset=0, source=source, render_mode='canvas')

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