import sys
import pandas as pd
from sqlalchemy import create_engine

def load_data(messages_filepath, categories_filepath):
    """
    Input: (path_to_messages_csv, path_to_categories_csv)
    Output: Dataframe merged from messages and categories. 
    
    """
    messages = pd.read_csv(messages_filepath)
    categories = pd.read_csv(categories_filepath)
    df = messages.merge(categories, on='id')
    
    return df

def clean_data(df):
    """
    Input: Dataframe from function load_data. 
    Output: cleaned data. 

    This function is used to drop duplicates, as well as 
    splitting categories and use either 0 or 1 to represent
    whether a specific message falls into that category. 
    
    """

    categories = df['categories'].str.split(';', expand=True)
    
    row = categories.iloc[0]
    category_colnames = [cat for cat in row]
    categories.columns = category_colnames
    
    for column in categories:
        # set each value to be the last character of the string
        categories[column] = categories[column].str[-1]
        # convert column from string to numeric
        categories[column] = categories[column].astype(int)
       
    df.drop(['categories'], inplace=True, axis=1)
    # concatenate the original dataframe with the new `categories` dataframe
    df = pd.concat([df, categories], axis=1)
    df.drop_duplicates(subset=['id'], inplace=True)
    
    return df


def save_data(df, database_filename):
    """
    Input: (dataframe from function "clean_data", output name of this function)
    Output: An SQLite database.     
    """

    engine = create_engine('sqlite:///{0}'.format(database_filename))
    df.to_sql('clean_all', engine, index=False)


def main():
    if len(sys.argv) == 4:

        messages_filepath, categories_filepath, database_filepath = sys.argv[1:]

        print('Loading data...\n    MESSAGES: {}\n    CATEGORIES: {}'
              .format(messages_filepath, categories_filepath))
        df = load_data(messages_filepath, categories_filepath)

        print('Cleaning data...')
        df = clean_data(df)
        
        print('Saving data...\n    DATABASE: {}'.format(database_filepath))
        save_data(df, database_filepath)
        
        print('Cleaned data saved to database!')
    
    else:
        print('Please provide the filepaths of the messages and categories '\
              'datasets as the first and second argument respectively, as '\
              'well as the filepath of the database to save the cleaned data '\
              'to as the third argument. \n\nExample: python process_data.py '\
              'disaster_messages.csv disaster_categories.csv '\
              'DisasterResponse.db')


if __name__ == '__main__':
    main()
