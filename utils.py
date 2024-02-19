import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def clean_participation_in_lectures(df, row_name, number_of_participants):
    df = df.iloc[:, 0:5]
    df.rename(columns={df.columns[0]: "what"}, inplace=True)

    # Set the 'what' column as the index to facilitate transposition
    df.set_index('what', inplace=True)

    # Transpose the DataFrame so that columns become rows
    df_t = df.T

    # Reset index to turn the index into a column
    df_t = df_t.reset_index()

    # Rename the columns for clarity
    df_t.columns = ['Percentage', row_name]

    # Convert the 'Value' column to numeric, removing the '%' and converting to float
    df_t[row_name] = df_t[row_name].astype(str).str.replace('%', '').astype(float)

    df_t['Percentage'] = df_t['Percentage'].astype(str)

    df_t['Lezioni frequentate'] = (df_t['Lezioni frequentate'] * number_of_participants).astype(int)

    return df_t


def plot_participation_in_lectures(df, x_column, y_column):
    """
    Create a bar chart using seaborn.

    :param df: pandas DataFrame containing the data
    :param x_column: Name or index of the column to use for the x-axis
    :param y_column: Name or index of the column to use for the y-axis
    """
    sns.barplot(x=df[x_column].values, y=df[y_column].values)
    # Set the title and labels of the plot
    plt.title('Bar Chart of Participation in Lectures')
    plt.xlabel(x_column if isinstance(x_column, str) else df.columns[x_column])
    plt.ylabel(y_column if isinstance(y_column, str) else df.columns[y_column])

    # Show the plot
    plt.show()


def split_mark_and_comment(column):
    """ it does the heavy lifting for the function extract_marks_and_comments:
     the columns contain marks and comments together. Let's split them
     e.g. column_A with value '3 - comment text'
     becomes column_A_marks: 3 and Column_A_Comment: 'comment text'
     """
    # Adjust the split to account for potential variability in spacing around the hyphen
    split_df = column.str.split(' ?- ?', n=1, expand=True)
    split_df.columns = [column.name + '_Mark', column.name + '_Comment']
    # Fill None values with an empty string or some default value in the '_Comment' column
    split_df[column.name + '_Comment'] = split_df[column.name + '_Comment'].fillna('')
    return split_df


def extract_marks_and_comments(loc_df):
    """ the columns contain marks and comments together.
    this function calls extract_marks_and_comments to  split these columns into separate columns for marks and comments
         e.g. column_A with value '3 - comment text'
         becomes column_A_marks: 3 and Column_A_Comment: 'comment text'
    then it clean the data removing invalid values
    """
    # Define a function that you want to apply to each column
    # Apply the function to each column that has a string data type
    for col in loc_df.columns:
        if pd.api.types.is_string_dtype(loc_df[col]):
            new_columns_df = split_mark_and_comment(loc_df[col])
            mark_column_name = new_columns_df.columns[0]
            new_columns_df[mark_column_name] = new_columns_df[mark_column_name].str.replace('-', '', regex=True)
            new_columns_df[mark_column_name] = new_columns_df[mark_column_name].str.replace('[^\d.]', '', regex=True)
            new_columns_df[mark_column_name] = pd.to_numeric(new_columns_df[mark_column_name], errors='coerce')
            loc_df = pd.concat([loc_df, new_columns_df], axis=1)
        # Drop original columns
        loc_df = loc_df.drop(columns=[col])
    return loc_df


def plot_chart_and_print_comments(local_df):
    """
    it produces the violin plots for each of the marks columns and also prints the comments (and their marks for each column)
    :param local_df: the data frame with stats - the columns of the df must have been already  split between marks and
    comments using the function  extract_marks_and_comments
    :return: it produces the plots
    """
    for i, mark_col in enumerate(local_df.columns[:-1]):  # Exclude the last column to avoid index out of range
        if pd.api.types.is_numeric_dtype(local_df[mark_col]):
            # Create two plots for the numeric column
            fig, axes = plt.subplots(1, 2, figsize=(12, 6))  # 1 row, 2 columns
            sns.violinplot(y=mark_col, data=local_df, ax=axes[0])
            print(mark_col)

            axes[0].set_title(mark_col.replace('_Mark', ''))
            sns.histplot(data=local_df, x=mark_col, kde=False, ax=axes[1])
            axes[1].set_title(mark_col.replace('_Mark', ''))

            # Calculate and sort the counts for each unique value
            value_counts = local_df[mark_col].value_counts().sort_values(ascending=False)  # Sort counts
            sorted_counts_str = value_counts.to_string()

            # Display sorted counts as legend
            plt.legend([f'Counts:\n{sorted_counts_str}'], loc='upper right')

            # Show the plots
            plt.tight_layout()
            plt.show()

            # Assuming the comment column directly follows the numeric column
            comment_col = local_df.columns[i + 1]  # Get the next column, assumed to be the comments column
            if not pd.api.types.is_numeric_dtype(local_df[comment_col]):
                print(f'Comments for {mark_col}:')
                print_comments_and_marks(local_df, comment_col, mark_col)
                print("\n---\n")  # Separator for readability


def print_comments_and_marks(local_df, comment_col, mark_col):
    """
    given a comment column and a mark column, it will print all the comments and their marks
    :param local_df: the dataframe
    :param comment_col: the column of the comments
    :param mark_col: the column of the marks
    :return: it prints comments and marks
    """
    # Replace empty strings with np.nan in the comment column
    local_df[comment_col] = local_df[comment_col].replace('', np.nan)
    # Drop rows with NaN in the comment column and find unique comments
    unique_comments = local_df[comment_col].dropna().unique()
    # For each unique comment, find and print the corresponding mark(s)
    for comment in unique_comments:
        # Find rows with the current unique comment
        corresponding_rows = local_df[local_df[comment_col] == comment]
        # Extract marks for these rows. Assuming mark_col holds the correct column name for marks
        marks = corresponding_rows[mark_col].unique()
        print(f"{', '.join(map(str, marks))}: {comment}")
        print("---")



def load_schede_data(full_stat_file, full_stats_headers_row, full_stats_last_relevant_data_row):
    """

    :param full_stat_file:
    :param full_stats_headers_row: the line containing the headings of the table
    :param full_stats_last_relevant_data_row: the last row of data
    :return: the dataframe with the stats
    """
    relevant_rows = list(range(full_stats_headers_row - 2, full_stats_last_relevant_data_row))
    # import specific rows from CSV into DataFrame
    df = pd.read_excel(full_stat_file, skiprows=lambda x: x not in relevant_rows, header=1)
    return df


def extract_data_from_stats_file(stat_file):
    """
    it extracts the number of participants and the stats of participation in the lectures from the stat file
    :param stat_file: the file containing the participation in the lectures
    :return: the number of participants and the stats of participation in %
    """
    headers_row = 49
    # the last row with marks data
    last_relevant_data_row = 50
    # specify rows to import
    relevant_rows = list(range(headers_row - 2, last_relevant_data_row))

    # import specific rows from CSV into DataFrame
    df = pd.read_excel(stat_file, skiprows=lambda x: x not in relevant_rows, header=1)

    # getting the number of participants
    part_df = pd.read_excel(stat_file, skiprows=lambda x: x not in [7, 8])
    number_of_participants = part_df.iloc[0, 1]

    df_t = clean_participation_in_lectures(df, 'Lezioni frequentate', number_of_participants)

    return df_t, number_of_participants
