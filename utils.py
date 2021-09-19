from typing import List

import pandas as pd

VAR = "totalTestResultsIncrease"


def five_day_change(df: pd.DataFrame):

    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values(by=['date'], ascending=False).reset_index(drop=True)

    covid_ind = df[df["date"] == "2020-03-11"].index[
        0]  # output the start index
    stop_ind = df[df['date'] == df['date'].max()].index[0]

    max_ind = 0
    max_increase_rate = 0
    min_ind = 0
    min_increase_rate = 0

    for i in range(covid_ind, max(stop_ind - 3, 3), -1):
        if df.iloc[i][VAR]:
            increase_rate = (df.iloc[i - 4][VAR] -
                             df.iloc[i][VAR]) / df.iloc[i][VAR]
            if increase_rate > max_increase_rate:
                max_ind = i
                max_increase_rate = increase_rate
            elif increase_rate < min_increase_rate:
                min_ind = i
                min_increase_rate = increase_rate

    return max_ind, max_increase_rate, min_ind, min_increase_rate


def print_format(state: str, direction: str, start_date: str, end_date: str,
                 ratio: float):
    print(
        f"State {state} experienced the highest {direction} among all between "
        f"{start_date} and "
        f"{end_date} "
        f"by {ratio * 100:.2f}%.")


def print_results(state_list: List[pd.DataFrame]):

    state_max_ind = 0
    max_ind = 0
    max_num = 0
    state_min_ind = 0
    min_ind = 0
    min_num = 0

    for i in range(len(state_list)):
        cur_max_ind, cur_max_num, cur_min_ind, cur_min_num = five_day_change(
            state_list[i])
        print_format(state_list[i]['state'].iloc[0], 'increase',
                     state_list[i].iloc[cur_max_ind]['date'].date(),
                     state_list[i].iloc[cur_max_ind - 4]['date'].date(),
                     cur_max_num)

        print_format(state_list[i]['state'].iloc[0], 'decrease',
                     state_list[i].iloc[cur_min_ind]['date'].date(),
                     state_list[i].iloc[cur_min_ind - 4]['date'].date(),
                     -cur_min_num)

        if cur_max_num > max_num:
            state_max_ind = i
            max_ind = cur_max_ind
            max_num = cur_max_num
        elif cur_min_num < min_num:
            state_min_ind = i
            min_ind = cur_min_ind
            min_num = cur_min_num

    print_format(state_list[state_max_ind]['state'].iloc[0], 'increase',
                 state_list[state_max_ind].iloc[max_ind]['date'].date(),
                 state_list[state_max_ind].iloc[max_ind - 4]['date'].date(),
                 max_num)

    print_format(state_list[state_min_ind]['state'].iloc[0], 'decrease',
                 state_list[state_min_ind].iloc[min_ind]['date'].date(),
                 state_list[state_min_ind].iloc[min_ind - 4]['date'].date(),
                 -min_num)
