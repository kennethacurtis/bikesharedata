import pandas as pd
import numpy as np
from datetime import datetime

# uses whole prompt window to display data
pd.set_option('display.height', 1000)
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

# SettingWithCopyWarning -- see docs: http://pandas.pydata.org/pandas-docs/stable/indexing.html#returning-a-view-versus-a-copy
# and https://stackoverflow.com/questions/20625582/how-to-deal-with-settingwithcopywarning-in-pandas/40214434
pd.options.mode.chained_assignment = None

def get_city():
    '''Asks the user which city data they want to explore, returns the data

    Args:
        none.
    Returns:
        Data based on the users input, city_data
    '''
    try:
        city = input('\nHello! Let\'s explore some US bikeshare data!\n'
                     'Would you like to see data for Chicago, New York City, or Washington?\n')
        print('Getting data....')
        # read data and assign to city_data
        city_data = pd.read_csv("%s.csv" % city.lower().replace(' ', '_'))
        print('Converting time....')
        city_data['Start Time'] = pd.to_datetime(city_data['Start Time'])
        city_data['End Time'] = pd.to_datetime(city_data['End Time'])
        print('Converting days of week....')
        city_data['day_of_week'] = city_data['Start Time'].dt.weekday_name
        print('Converting months....')
        city_data['month'] = city_data['Start Time'].dt.strftime('%B')
        print('Converting hours....')
        city_data['hour'] = city_data['Start Time'].dt.strftime('%H %p')
        print('Done!')
        return city_data
    except:
        print('\nThat is not a valid city, try again\n')
        get_city()

def get_month(city_data):
    '''Asks the user which month they want to filter and returns that data
    Args:
        city_data -- data of chosen city
    Returns:
        filtered data
    '''
    month = input('\nWhich month? January, February, March, April, May, or June?\n')
    # returns data that equals the users input, converts input to datetime
    return city_data[city_data['Start Time'].dt.month == datetime.strptime(month, '%B').month]

def get_day(city_data):
    '''Asks the user which day they would like to filter and returns that data
    Args:
        city_data -- data of chosen city
    Returns:
        data based on filter
    '''
    # account for user error
    try:
        day = input('\nWhich day? Please enter your response like so: Monday, Tuesday...ect\n')
        # uses day_of_week column to return data
        return city_data[city_data['day_of_week'] == day]
    except:
        print('\nData for this day does not exist in the month you selected, try another')
        get_day(city_data)


def get_day_in_month(city_data):
    '''If the user wants to filter by day, asks for month, then day in month
    Args:
        city_data -- data of chosen city
    Returns:
        data based on filter
    '''
    month = input('\nFirst, lets select the month. January, February, March, April, May, or June?\n')
    month_data = city_data[city_data['Start Time'].dt.month == datetime.strptime(month, '%B').month]
    day = input('\nWhich day in your selected month? Please enter your response like so: Monday, Tuesday...ect\n')
    return city_data[city_data['day_of_week'] == day]


def get_time_period():
    '''Asks the user for a time period and returns the specified filter.
    Args:
        none.
    Returns:
        user input
    '''
    time_period = input('\nWould you like to filter the data by month, day, or not at'
                        ' all? Type "none" for no time filter.\n')
    if time_period == "month":
        return "month"
    elif time_period == "day":
        return "day"
    elif time_period == "none":
        return "nofilter"
    else:
        print("\nThat is not a valid filter\n")
        get_time_period()

def popular_month(city_data):
    '''Gets most occuring month in data and returns a string that includes that month
    Args:
        city_data -- data of chosen city
    Returns:
        (str) Tells user the popular month
    '''
    try:
        # stores a list of counts of the months in data to month_list
        month_list = city_data['month'].value_counts().index.tolist()
        pop_month = str(month_list[0])
        return '\nThe most popular month for the selected city is ' + pop_month
    except:
        print('\nno')

def popular_day(city_data):
    '''Gets most occuring day in data and returns a string that includes that day
    Args:
        city_data -- data of chosen city
    Returns:
        (str) Tells user the popular day
    '''
    day_list = city_data['day_of_week'].value_counts().index.tolist()
    pop_day = str(day_list[0])
    return '\nThe most popular day for the selected city is ' + pop_day

def popular_hour(city_data):
    '''Gets most occuring hour in data and returns a string that includes that hour
    Args:
        city_data -- data of chosen city
    Returns:
        (str) Tells user the popular hour
    '''
    hour_list = city_data['hour'].value_counts().index.tolist()
    pop_hour = str(hour_list[0])
    return '\nThe most popular hour (based on the 24hr clock) for the selected city is ' + pop_hour

def seconds_converter(seconds):
    '''Used for trip_duration(city_data), converts seconds into (hours minutes seconds)
    Args:
        seconds -- amount of seconds
    Returns:
        (str) Tells user the amount of time
    '''
    # divmod docs: https://docs.python.org/2/library/functions.html#divmod
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return '%d Days %02d Minutes and %02d seconds' % (h, m, s)

def trip_duration(city_data):
    '''Calculates the sum and mean of the duration of the trips and returns string
    Args:
        city_data -- data of chosen city
    Returns:
        (str) Tells user the sum and mean of the duration of trips
    '''
    calc_mean = round(city_data['Trip Duration'].mean())
    calc_duration = city_data['Trip Duration'].sum()
    mean = seconds_converter(calc_mean)
    total = seconds_converter(calc_duration)
    return '\nThe total trip duration for your selected city is {} and the average trip duration is {}'.format(total,mean)

def popular_stations(city_data):
    '''Calculates the popular start and end stations
    Args:
        city_data -- data of chosen city
    Returns:
        (str) Tells user the most popular start and end stations
    '''
    start_station = city_data['Start Station'].value_counts().index.tolist()
    pop_start = str(start_station[0])
    end_station = city_data['End Station'].value_counts().index.tolist()
    pop_end = str(end_station[0])
    return '\nThe most popular start station is {} and the most popular end station is {}'.format(pop_start,pop_end)

def popular_trip(city_data):
    '''Takes columns Start Station and End Station and counts occurences
    Args:
        city_data -- data of chosen city
    Returns:
        (str) Tells user most popular strip between stations
    '''
    # using size() of Start Station and End Station and stores number in start_end_size
    start_end_size = city_data.groupby(['Start Station', 'End Station']).size().reset_index(name='start_end_size')
    # sorts size() number in order from biggest to smallest
    sort = start_end_size.sort_values('start_end_size', ascending = False).drop_duplicates(['Start Station', 'End Station'])
    start = sort['Start Station'].iloc[0]
    end = sort['End Station'].iloc[1]
    return '\nThe most popular trip for your selected city was between {} and {} station'.format(start,end)

def users(city_data):
    '''Calculates number of user type
    Args:
        city_data -- data of chosen city
    Returns:
        (str) Tells user counts of users type
    '''
    print('\nFor your selected city...')
    #loops over User Type and count occurence
    for  val, cnt in city_data['User Type'].value_counts().iteritems():
        print('\nThere are {} {}s'.format(cnt, val))
    return '......'

def gender(city_data):
    '''Calculates number of gender types
    Args:
        city_data -- data of chosen city
    Returns:
        (str) Tells user counts of gender types
    '''
    try:
        for val, cnt in city_data['Gender'].value_counts().iteritems():
            print('\nThere are {} {}s'.format(cnt, val))
        return '......'
    except:
        return '\nThis city does not have Gender data'

def birth_years(city_data):
    '''Calculates the most recent, earliest, and most popular birth years
    Args:
        city_data -- data of chosen city
    Returns:
        (str) Tells user birth year information
    '''
    try:
        most_recent = str(int(city_data['Birth Year'].max()))
        most_early = str(int(city_data['Birth Year'].min()))
        birth_year_list = city_data['Birth Year'].value_counts().index.tolist()
        most_pop = str(round(birth_year_list[0]))
        return 'The most recent birth year is {}, the earliest is {}, and the most popular is {}'.format(most_recent,most_early,most_pop)
    except:
        return 'This city does not have Birth Year Data'

def restart():
    '''asks user if they would like to restart the program
    Args:
        none.
    Returns:
        none.
    '''
    restart = input('Would you like to restart? Type \'yes\' or \'no\'.')
    if restart.lower() == 'yes':
        statistics(dispatcher)
    else:
        quit()

def display_data_all(city_data):
    '''Displays the selected city data, diplays in increments of five
    Args:
        city_data -- data of chosen city
    Returns:
        data set
    '''
    user_ind_data = input('Would you like to view individual trip data?'
                    'Type \'yes\' or \'no\'. ')
    x=0
    y=5
    if user_ind_data == 'yes':
        print(city_data.iloc[x:y])
        while x < len(city_data.index):
            display = input('Would you like to view the next 5 lines of data?'
                            'Type \'yes\' or \'no\'. ')
            if display == 'yes':
                x = x + 5
                y = y + 5
                print(city_data.iloc[x:y])
            else:
                restart()
    else:
        restart()

def display_data_filtered(filtered_data):
    '''Displays the selected city data and filtered data, diplays in increments of five
    Args:
        filtered_data -- filtered data based on user input
    Returns:
        data set
    '''
    x=0
    y=5
    user_ind_data = input('\nWould you like to view individual trip data?'
                            'Type \'yes\' or \'no\'. ')
    if user_ind_data == 'yes':
        print(filtered_data.iloc[x:y])
        while x < len(filtered_data.index):
            next_rows = input('\nWould you like to view the next five rows?'
                                    'Type \'yes\' or \'no\'. ')
            if next_rows == 'yes':
                x = x + 5
                y = y + 5
                print(filtered_data.iloc[x:y])
            else:
                restart()
    else:
        restart()

# dictionary of all statistical functions
dispatcher = {'noFilter':  [popular_month, popular_day, popular_hour, trip_duration, popular_trip,
                        users, gender, birth_years],
              'monthFilter': [popular_day, popular_hour, trip_duration, popular_trip, users, gender,
                        birth_years],
              'dayFilter':   [popular_hour, trip_duration, popular_trip, users, gender, birth_years,]}

def statistics(dispatcher):
    '''Loops through and uses dictionary of statistical functions
    Args:
        dispatcher -- dictionary of functions
    Returns:
        (str) print statements that tell user data information
    '''
    city_data = get_city()
    data_filter = get_time_period()
    if data_filter == 'day':
        filtered_data = get_day_in_month(city_data)
        for f in dispatcher['dayFilter']:
            print(f(filtered_data))
        display_data_filtered(filtered_data)
    elif data_filter == 'month':
        filtered_data = get_month(city_data)
        for f in dispatcher['monthFilter']:
            print(f(filtered_data))
        display_data_filtered(filtered_data)
    else:
        for f in dispatcher['noFilter']:
            print(f(city_data))
        display_data_all(city_data)

statistics(dispatcher)
