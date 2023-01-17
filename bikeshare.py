import time
import pandas as pd
import numpy as np


CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}

Cities = ['chicago', 'new york city', 'washington']
Months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
Days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bike share data!')

    while True:
        city = input('Would you like to see data for Chicago, New York City , or Washington? \n> ')
        city = city.lower()
        if city in Cities:
            break
        else:
            print("Invalid input. Please enter a valid input.")
    while True:
        month = input('Please enter a month: January, February, March, April, May, or June?'
                      ' or just say \'all\' to see all months. \n> ')
        month = month.lower()
        if month in Months:
            break
        else:
            print("Invalid input. Please enter a valid input.")

    while True:
        day = input('Please enter a day: Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday?'
                    ' or just say \'all\' to see all days. \n> ')
        day = day.lower()
        if day in Days:
            break
        else:
            print("Invalid input. Please enter a valid input.")

    print('-' * 40)
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

    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month

    df['week_day'] = df['Start Time'].dt.day_name()

    if month != 'all':
        month = Months.index(month) + 1
        df = df[df['month'] == month]
    if day != 'all':
        df = df[df['week_day'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    common_month = df['month'].mode()[0]
    print('Most Frequent Month is :', common_month)
    common_week_day = df['week_day'].mode()[0]
    print('Most Frequent Day is :', common_week_day)
    df['hour'] = df['Start Time'].dt.hour
    common_start_hour = df['hour'].mode()[0]
    print('Most Frequent Start Hour is :', common_start_hour)

    print("\nThis took %s seconds." % round(time.time() - start_time, 3))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    most_commonly_start_stat = df['Start Station'].mode()[0]
    print('Most Commonly used Start Station is:', most_commonly_start_stat)
    most_commonly_end_stat = df['End Station'].mode()[0]
    print('Most Commonly used End Station is:', most_commonly_end_stat)

    commonly_start_to_end_stat = df[['Start Station', 'End Station']].mode().loc[0]
    print('Most Frequent Combination of Start Station and End Station trip : {}, {}'
          .format(commonly_start_to_end_stat[0], commonly_start_to_end_stat[1]))
    print("\nThis took %s seconds." % round(time.time() - start_time, 3))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    total_time = df['Trip Duration'].sum()
    print('Total Travel Time: ', total_time)
    mean_time = df['Trip Duration'].mean()
    print('Mean Travel Time: ', mean_time)
    print("\nThis took %s seconds." % round(time.time() - start_time, 3))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bike share users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    user_types = df['User Type'].value_counts()
    print(user_types)

    while True:
        if 'Gender' in df.columns or 'Birth Year' in df.columns:
            gender_types = df['Gender'].value_counts()
            print(gender_types)
            birth_year = df['Birth Year']
            common_year = birth_year.mode()[0]
            print("The most common birth year:", common_year)
            most_recent = birth_year.max()
            print("The most recent birth year:", most_recent)
            earliest_year = birth_year.min()
            print("The earliest birth year:", earliest_year)
            break
        else:
            print('Gender Stats can\'t be determined')
            break

    print("\nThis took %s seconds." % round(time.time() - start_time, 3))
    print('-' * 40)

    view_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no\n')
    start_loc = 0
    keep_asking = True
    while keep_asking:
        print(df.iloc[start_loc:start_loc + 5])
        start_loc += 5
        view_display = input("Do you wish to continue?: ").lower()
        if view_display == "no":
            keep_asking = False

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
    main()