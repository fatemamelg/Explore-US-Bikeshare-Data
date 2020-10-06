import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

    city = str(input('Choose a city you want to analyze (Chicago, New York City, Washington): '))

    while city.lower() != 'chicago' and city.lower() != 'new york city' and city.lower() != 'washington': 
        city = str(input('Please choose either Chicago, New York City or Washington: '))

    # TO DO: get user input for month (all, january, february, ... , june)
    month = str(input('Choose name of the month to filter by or "all" to apply no month filter: '))

    while month.lower() not in ['all', 'january', 'february', 'march', 'april', 'may', 'june']: 
        month = str(input('Please choose name of the month from january to june to filter by or "all" to apply no month filter: '))


    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day = str(input('Choose name of the day to filter by or "all" to apply no day filter: '))

    while day.lower() not in ['all', 'saturday', 'sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday']: 
        day = str(input('Please choose a valid day to filter by or "all" to apply no month filter: '))

    print('-'*40)
    return city.lower(), month.lower(), day.lower()


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])

    df['Start Time'] = pd.to_datetime(df['Start Time'])

    df['month'] = df['Start Time'].dt.month
    df['hour'] = df['Start Time'].dt.hour
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month)
        df = df[df['month'] == month]

    # filter by day
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    if month.lower() == 'all':
        common_month = df['month'].mode()[0]
        print('* The most frequent month: ', common_month)

    # TO DO: display the most common day of week
    if day.lower() == 'all':
        common_day = df['day_of_week'].mode()[0]
        print('* The most frequent day: ', common_day)

    # TO DO: display the most common start hour
    common_hour = df['hour'].mode()[0]
    print('* The most frequent hour: ', common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    common_start = df['Start Station'].mode()[0]
    print('* The most commonly used start station: ', common_start
          , 'with count: ', len(df[df['Start Station'] == common_start]))

    # TO DO: display most commonly used end station
    common_end = df['End Station'].mode()[0]
    print('* The most commonly used end station: ', common_end
          , 'with count: ', len(df[df['Start Station'] == common_end]))

    # TO DO: display most frequent combination of start station and end station trip
    common_start_end = df.groupby(['Start Station', 'End Station']).size().nlargest(1)
    print('* The most frequent combination of start station and end station trip:\n', common_start_end)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('* Total travel time: ', total_travel_time)

    # TO DO: display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('* Mean travel time: ', mean_travel_time)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df['User Type'].value_counts()
    print('* Counts of user types:\n', user_types)

    if city.lower() != 'washington':
        # TO DO: Display counts of gender
        gender = df['Gender'].value_counts()
        print('* Counts of gender:\n', gender)
    
        # TO DO: Display earliest, most recent, and most common year of birth
        early_age = df['Birth Year'].min()
        recent = df['Birth Year'].max()
        common_birth_year = df['Birth Year'].mode()[0]
        print('* The earliest birth year: ', early_age, '\n* The most recent birth year: ', recent,
              '\n* The most common birth year: ', common_birth_year)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
        


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)

        # Ask user to check raw data
        check_raw = input('\nWould you like to see 5 lines of raw data ? Enter yes or no.\n')
        while (check_raw.lower() != 'yes' and check_raw.lower() != 'no'):
            check_raw = input('\nWould you like to see 5 lines of raw data ? Enter yes or no.\n')

        if (check_raw.lower() == 'yes'):
            print(df.head(5))

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()

