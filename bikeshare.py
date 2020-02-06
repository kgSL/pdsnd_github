import time as t
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
    print('\nHello friend! Let\'s explore some US bikeshare data!')
    while True:
        city = ''
        city = input('\nWhich city would you like to explore: Chicago, New York City, or Washington? ').lower()
        if city in ['chicago', 'washington', 'new york city']:
            break
        else:
            print('\nInvalid entry. Please enter city again.')
    while True:
        time = ''
        time = input('\nWould you like to filter the data by month, day, both, or none?: ').lower()
        if time in ['month', 'day', 'both', 'none']:
            break
        else:
            print('\nInvalid entry. Please enter time filter again.')
    while True:
        if time == 'month':
            month = input('\nWhich month? Please type January, February, March, April, May, or June: ').lower()
            print('\nPerfect! We\'ll look at bikeshare data for {} in the month of {}.'.format(city.title(), month.title()))
            day = 'all'
            if month in ['january', 'february', 'march', 'april', 'may', 'june']:
                break
            else:
                print('\nInvalid entry. Please enter month again.')
        elif time == 'day':
            day = input('\nWhich day? Please type Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday: ').lower()
            print('\nPerfect! We\'ll look at bikeshare data for {} on {} of every week.'.format(city.title(), day.title()))
            month = 'all'
            if day in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
                break
            else:
                print('\nInvalid entry. Please enter day again.')
        elif time == 'both':
            month = input('\nWhich month? Please type January, February, March, April, May, or June: ').lower()
            day = input('\nWhich day? Please type Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday: ').lower()
            print('\nPerfect! We\'ll look at bikeshare data for {} on {} of every week in {}.'.format(city.title(), day.title(), month.title())),
            if month in ['january', 'february', 'march', 'april', 'may', 'june'] and day in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
                break
            else:
                print('\nInvalid entry. Please enter month and day again.')
        elif time == 'none':
            day = 'all'
            month = 'all'
            print('\nPerfect! We\'ll look at all six months of bikeshare data for {}.'.format(city.title()))
            break
    print('-'*40)
    return city, month, day




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
    df = pd.read_csv(CITY_DATA[city.lower()])

    df['Start Time'] = pd.to_datetime(df['Start Time'])

    df['month'] = df['Start Time'].dt.month
    df['day'] = df['Start Time'].dt.weekday_name

    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        df = df[df['month'] == month]

    if day != 'all':
        df = df[df['day'] == day.title()]
        print(df.head())

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = t.time()

    print('\nThe most common month is: ', df.month.mode()[0])

    print('\nThe most common day is: ', df.day.mode()[0])

    df['Start Hour'] = pd.to_datetime(df['Start Time'], format='%I%p')
    print('\nThe most common start hour is: ', df['Start Hour'].mode()[0])

    print("\nThis took %s seconds." % (t.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = t.time()

    print('\nThe most common start station is: ', df['Start Station'].mode()[0])

    print('\nThe most common end station is: ', df['End Station'].mode()[0])

    temp = pd.DataFrame()
    #First concatenate the trips
    temp['Common Trip'] = df['Start Station'] + ' to ' + df['End Station']
    print('\nThe most common end station is: ', temp['Common Trip'].mode()[0])

    print("\nThis took %s seconds." % (t.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = t.time()

    print('\nTotal travel time (in seconds) was: ', int(np.sum(df['Trip Duration'])))

    print('\nAverage travel time (in seconds) was: ', int(np.mean(df['Trip Duration'])))

    print("\nThis took %s seconds." % (t.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = t.time()

    print(df['User Type'].value_counts())

    try:
        print(df['Gender'].value_counts())
    except KeyError:
        print('\nThis data does not include Gender segmentation\n')

    try:
        print('\nThe oldest passenger was born in: ', int(np.min(df['Birth Year'])))
        print('\nThe youngest passenger was born in: ', int(np.max(df['Birth Year'])))
        print('\nThe most common year of birth was: ', int(df['Birth Year'].mode()[0]))
    except KeyError:
        print('\nThis data does not include Birth Year segmentation\n')

    print("\nThis took %s seconds." % (t.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        a = 0
        #Loop asks the user if they'd like to see some raw data
        display_raw = input('\nWould you like to see five lines of raw data? Enter yes or no.\n').lower()
        while display_raw == 'yes':
            print(df.iloc[a:a+5])
            display_raw = input('\nWould you like to see five lines of raw data? Enter yes or no.\n').lower()
            a += 5
            if display_raw != 'yes':
                continue
        restart = input('\nWould you like to restart? Enter yes or no.\n').lower()
        if restart != 'yes':
            break


if __name__ == "__main__":
	main()
