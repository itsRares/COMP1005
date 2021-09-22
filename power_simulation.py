from helpers import *
from community import *

#Resets the console and header
def resetHeader():
    os.system('clear')
    print("---=== Tesla Power Simulation System ===---")

#Main menu, User can select what section they would like
def menuSimulation(house):
    resetHeader()

    option=True
    while option:
        print("""
        1. Create Simulation
        2. View Pre-set Simulation
        3. View Average Simulation
        4. Go back
        """)
        option=input("What would you like to do? ")
        if option=="1":
            createSimulation(house) #Create own simulation
        elif option=="2":
            presetSimulation(house) #View Preset Simulation
        elif option=="3":
            avgSimulation(house) #Create Average Simulation
        elif option=="4":
            #Back to home
            os.system('clear')
            print("---=== Welcome to TESLA POWER ===---")
            option = None
        else:
            #Back to home
            os.system('clear')
            print("Invalid choice, What would you like to do? ")

#Create own simulation
def createSimulation(house):
    resetHeader()
    suburb = []
    day = [1,2,3,4,5,6,7]

    #Check if file input or not
    print("Would you like to read a file in? y/n...")
    print("Read documentation for required format")
    response = input("> ")

    if response.upper() == "Y":
        fileobj = fileInput() #Get file input, returns file obj

        house = House("Nope","Nope")
        for idx,line in enumerate(fileobj):
            try:
                line_s = line.strip()  #Strip whitespace
                if idx % 8 == 0:
                    usages = [x for x in line_s.split('=')]
                    info = [x for x in usages[1].split(',')]
                    house = House(info[0], info[1])
                    suburb.append(house)
                else:
                    usages = [x for x in line_s.split(',')]
                    dateValid = validateDate(usages[0])
                    if dateValid:
                        house.addUsage(usages[0], usages[1])
            except: #Other errors
                print('Error adding simulation value') 
    else:
        #Else create simulation manually
        print("Lets create a houses for " + house.getSuburb() + " suburb")

        looping = True
        while looping:
            #Get house number
            print("1. What is the house number?... ")
            number = numberInput()
            tempHouse = House(number, suburb)

            print("Creating house ...")
            time.sleep(0.5)

            print("\nNow lets add a 8 day power usage")
            #Create 8 day usage
            for n in range(8):
                dateValid = False
                while not dateValid:
                    #Input the usage
                    print("2. Add day "+str(n+1)+" usage | format: <Date>,<totalUsage>")
                    print("eg) 16 02 2020 00:00:00,143732")
                    usage=input("> ")

                    #Seperate by ',' and put into array - shorthand
                    usages = [x for x in usage.split(',')] 
                    dateValid = validateDate(usages[0]) #Check if valid date

                #Add usage to house
                tempHouse.addUsage(usages[0], usages[1])
            
            suburb.append(tempHouse)

            #Check if more houses want to get added
            print("\nWould you like to add another house? y/n...")
            answer = input("> ")
            if answer.upper() == "N":
                looping = None

    output_file('output/createSimulation.html', mode='inline')

    #Plot
    plot = figure(title='Power Usage for Suburb', x_axis_label='Day', y_axis_label='Power Usage (kWh)')

    #Get color pallete
    colors = itertools.cycle(palette)

    #For each usage
    for idx,s in enumerate(suburb):
        print(s.getNumber())
        gen_usage = []
        pow_usage = s.getKwhUsage()

        #Loop through each usage
        for idx,usage in enumerate(pow_usage):
            if idx != 0:
                #Minus previous day and current day to get daily usage
                gen_usage.append(int(pow_usage[idx]) - int(pow_usage[idx-1]))

        #Create datasource
        source_usage = ColumnDataSource(data=dict(
            date=day,
            usage=gen_usage,
        ))

        color = next(colors) #Next color
        #Plot line
        plot.line('date', 'usage', line_width=2, line_color=color, legend_label='House '+s.getNumber()+'', source=source_usage)
        #Plot circle info dot
        plot.circle('date', 'usage', fill_color=color, line_color=color, size=8, source=source_usage)

    #No scientific numbers on Y column
    plot.left[0].formatter.use_scientific = False

    #When hover over circle show this
    hover = HoverTool(
        tooltips=[
            ('Day', '@date'), 
            ('Usage', '@usage kWh')
        ],
        formatters={
            '@date': 'datetime'
        }
    )

    plot.add_tools(hover)
    show(plot)

    input("\nPress enter to continue... ")   
    resetHeader()

#View Preset Simulation
def presetSimulation(house):
    print("what")
    print("Creating houses ...")
    suburbName = house.getSuburb()
    suburb = []

    #Creating houses
    h1 = House("10746", suburbName)
    h2 = House("4192", suburbName)
    h3 = House("5636", suburbName)
    h4 = House("7583", suburbName)
    h5 = House("2447", suburbName)

    suburb.append(h1)
    suburb.append(h2)
    suburb.append(h3)
    suburb.append(h4)
    suburb.append(h5)

    print("Adding usage ...")

    #Adding usages to house
    #House 10746
    h1.addUsage("09 02 2014 00:00:00", "0")
    h1.addUsage("10 02 2014 00:00:00", "11")
    h1.addUsage("11 02 2014 00:00:00", "16")
    h1.addUsage("12 02 2014 00:00:00", "22")
    h1.addUsage("13 02 2014 00:00:00", "27")
    h1.addUsage("14 02 2014 00:00:00", "32")
    h1.addUsage("15 02 2014 00:00:00", "43")
    h1.addUsage("16 02 2014 00:00:00", "51")

    #House 4192
    h2.addUsage("09 02 2014 00:00:00", "0")
    h2.addUsage("10 02 2014 00:00:00", "12")
    h2.addUsage("11 02 2014 00:00:00", "24")
    h2.addUsage("12 02 2014 00:00:00", "38")
    h2.addUsage("13 02 2014 00:00:00", "52")
    h2.addUsage("14 02 2014 00:00:00", "65")
    h2.addUsage("15 02 2014 00:00:00", "81")
    h2.addUsage("16 02 2014 00:00:00", "92")

    #House 5636
    h3.addUsage("09 02 2014 00:00:00", "0")
    h3.addUsage("10 02 2014 00:00:00", "8")
    h3.addUsage("11 02 2014 00:00:00", "14")
    h3.addUsage("12 02 2014 00:00:00", "21")
    h3.addUsage("13 02 2014 00:00:00", "27")
    h3.addUsage("14 02 2014 00:00:00", "32")
    h3.addUsage("15 02 2014 00:00:00", "35")
    h3.addUsage("16 02 2014 00:00:00", "41")

    #House 7583
    h4.addUsage("09 02 2014 00:00:00", "0")
    h4.addUsage("10 02 2014 00:00:00", "15")
    h4.addUsage("11 02 2014 00:00:00", "33")
    h4.addUsage("12 02 2014 00:00:00", "71")
    h4.addUsage("13 02 2014 00:00:00", "93")
    h4.addUsage("14 02 2014 00:00:00", "114")
    h4.addUsage("15 02 2014 00:00:00", "142")
    h4.addUsage("16 02 2014 00:00:00", "156")

    #House 2447
    h5.addUsage("09 02 2014 00:00:00", "0")
    h5.addUsage("10 02 2014 00:00:00", "11")
    h5.addUsage("11 02 2014 00:00:00", "22")
    h5.addUsage("12 02 2014 00:00:00", "36")
    h5.addUsage("13 02 2014 00:00:00", "46")
    h5.addUsage("14 02 2014 00:00:00", "56")
    h5.addUsage("15 02 2014 00:00:00", "68")
    h5.addUsage("16 02 2014 00:00:00", "82")

    output_file('output/presetSimulation.html', mode='inline')

    #Plot
    plot = figure(title='Power Usage for Households', x_axis_label='Day', 
        y_axis_label='Power Usage (kWh)', x_axis_type='datetime')

    colors = itertools.cycle(palette)

    #For each household
    for idx,s in enumerate(suburb):
        gen_usage = []
        pow_usage = s.getKwhUsage()
        
        #Loop through each usage
        for idx,usage in enumerate(pow_usage):
            if idx != 0:
                #Minus previous day and current day to get daily usage
                gen_usage.append(int(pow_usage[idx]) - int(pow_usage[idx-1]))

        #Create datasource
        source_usage = ColumnDataSource(data=dict(
            date=s.getDateUsage(),
            usage=gen_usage,
        ))

        color = next(colors) #Next color
        #Plot line
        plot.line('date', 'usage', line_width=2, line_color=color, legend_label='House '+s.getNumber()+'', source=source_usage)
        #Plot circle info dot
        plot.circle('date', 'usage', fill_color=color, line_color=color, size=8, source=source_usage)

    #No scientific numbers on Y column
    plot.left[0].formatter.use_scientific = False

    #When hover over circle show this
    hover = HoverTool(
        tooltips=[
            ('Day', '@date{%F'),
            ('Usage', '@usage kWh')
        ],
        formatters={
            '@date': 'datetime'
        }
    )

    plot.add_tools(hover)
    show(plot)

    input("\nPress enter to continue... ") 
    resetHeader()  

def avgSimulation(house):
    #Info in docs
    print("This simulation is based on CSIRO data. Information\ncan be found in the user guide.")

    #24hrs
    hours = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24]
    #CSIRO Victoria Average May
    vicAvg = [0.521,0.474,0.434,0.409,0.401,0.457,0.616,0.762,0.737,0.660,0.619,
              0.601,0.6,0.594,0.595,0.605,0.710,0.970,1.149,1.137,1.085,1.001,0.819,0.626]

    #Plot
    plot = figure(title='Average Power Usage in May for Suburb', x_axis_label='Hour',
                  y_axis_label='Power Usage (kWh)')

    #Create datasource
    source_usage = ColumnDataSource(data=dict(
        hour=hours,
        usage=vicAvg,
    ))

    #Create temp datasource to hold original values
    source_usage2 = ColumnDataSource(data=dict(
        hour=hours,
        usage=vicAvg,
    ))

    #Plot line
    plot.line('hour', 'usage', line_width=2, line_color='green', legend_label='Power Usage', source=source_usage)
    #Plot circle info dot
    plot.circle('hour', 'usage', fill_color="green", line_color='green', size=8, source=source_usage)
    #No scientific numbers on Y column
    plot.left[0].formatter.use_scientific = False

    #Add household slider
    households = Slider(start=1, end=10000, value=1, step=1, title="Households")

    #Create some JS for when updated
    #This times the temp value (olddata) with the amount of households (A)
    #Alongside adding randomness to each value as this is an average and wont be perfect
    callback = CustomJS(args=dict(source=source_usage, helper=source_usage2, house=households),
                    code="""
    const olddata = helper.data
    const data = source.data;
    const A = house.value;
    const x = data['hour']
    const y = data['usage']
    const oldy = olddata['usage']
    const randomness = [1.15, 1.1, 1.09, 1.085, 1.08, 1.075, 1.07, 1.065, 1.06, 1.035, 1.005];
    for (var i = 0; i < x.length; i++) {
        const randomDivide = randomness[Math.floor(Math.random() * randomness.length)];
        y[i] = (oldy[i]/randomDivide) * A
    }
    source.change.emit();
    """)

    #Callback
    households.js_on_change('value', callback)

    #Layout of webpage
    layout = row(
        plot,
        column(households),
    )

    #When hover over circle show this
    hover = HoverTool(
        tooltips=[
            ('Hour', '@hour'), 
            ('Usage', '@usage{(0.00)} kWh')
        ]
    )

    plot.add_tools(hover)
    output_file('output/avgSimulation.html', mode='inline')

    show(layout)

    input("\nPress enter to continue... ") 
    resetHeader() 
