# The function is to import the exam/assignment from LumiNUS to Google form

import pandas as pd
import regex as re


class lumi2google():
    def __init__(self, main_fp, csv_fp, write_fp, prefix):
        self.main_fp = main_fp
        self.csv_fp = csv_fp
        self.emails = []
        self.names = []

        self.main_table = pd.read_csv(self.main_fp)
        self.zoom_table = pd.read_excel(self.csv_fp)

        self.main_table_good_id = []
        self.zoom_table_good_id = []
        self.prefix = prefix
        self.write_fp = write_fp

        print('Init Done!')


    def pipeline(self):

        mark_list = []
        for i in range(len(self.main_table['Student Number'])):
            this_number = self.main_table['Student Number'][i]
            try:
                this_mark = self.zoom_table[self.zoom_table['Student Number'] == this_number]['Final Mark'].tolist()[0]
            except:
                this_mark = 0
            mark_list.append(this_mark)

        self.main_table[self.prefix] = pd.Series(mark_list).values
        print('Good')

        self.main_table.to_csv(self.write_fp)
        print('csv written to: {}'.format(self.write_fp))


if __name__ == '__main__':
    main_fp = 'data/cs3244-monitoring-oct.csv'
    # csv_fp = 'data/participants_83384276563.csv'
    csv_fp = 'data/scores-assign1.xlsx'
    prefix = 'assignment1'
    write_fp = 'data/score-{}.csv'.format(prefix)

    lumi2google = lumi2google(main_fp=main_fp, csv_fp=csv_fp, prefix=prefix, write_fp=write_fp)
    lumi2google.pipeline()

    print('Done')
