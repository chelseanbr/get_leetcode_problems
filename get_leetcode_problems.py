# Requests sends and recieves HTTP requests.
import requests
import json
import pandas as pd
import os

save_folder = 'problems/'
leetcode_api = 'https://leetcode.com/api/problems/'
leetcode_url_prefix = 'https://leetcode.com/problems/'

problem_types = ['algorithms', 'database']

cols_of_interest = ['stat.frontend_question_id', 'stat.question__title', 'acceptance_pct', 'difficulty.level', 'link']

if __name__ == "__main__":
    # Get problems & save to csv per problem type
    try:
        os.mkdir(save_folder)
        print('Created directory: {}'.format(save_folder))
    except FileExistsError:
        print('Will save to existing directory: {}'.format(save_folder))

    for problem_type in problem_types:
        print('\nGetting {} problems...'.format(problem_type))
        r = requests.get(leetcode_api + problem_type)
        probs = r.json()['stat_status_pairs']
        df = pd.json_normalize(probs)

        # Add Links
        df['link'] = df['stat.question__title_slug'].apply(lambda x: leetcode_url_prefix + x)

        # Add Acceptance Rate
        df['acceptance_pct'] = 100 * round(df['stat.total_acs'] / df['stat.total_submitted'], 3)

        # Remove "Paid-Only" problems
        df_free = df.loc[df['paid_only']==False].copy()

        # Sort by difficulty (asc), acceptance rate (desc)
        df_free = df_free[cols_of_interest].sort_values(by=['difficulty.level', 'acceptance_pct'], ascending=[True, False])

        df_free[cols_of_interest].to_csv(save_folder + problem_type + '.csv', index=False)
        print('\t--> Saved to {}{}.csv!'.format(save_folder, problem_type))