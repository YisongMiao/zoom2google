import pandas as pd
import regex as re


class csv2google():
    def __init__(self, main_fp, csv_fp, prefix, write_fp):
        self.main_fp = main_fp
        self.csv_fp = csv_fp
        self.emails = []
        self.names = []

        self.main_table = pd.read_csv(self.main_fp)
        self.zoom_table = pd.read_csv(self.csv_fp)

        self.main_table_good_id = []
        self.zoom_table_good_id = []
        self.prefix = prefix
        self.write_fp = write_fp

        print('init done!')

    def email_exact_match(self):
        '''
        Objective: match the email e1234567@u.nus.edu.
        Some are using "friendly email", then we need to map their name
        '''
        main_table_email = self.main_table['Email'].tolist()
        zoom_table_email = self.zoom_table['User Email'].tolist()
        intersect = list(set(main_table_email).intersection(zoom_table_email)) # 148 out of 262
        self.emails += intersect
        print('email exact match done: {}'.format(len(self.emails)))

    def name_exact_match(self):
        '''
        Objective: Exact match student name.
        '''
        # iterrows of zoom_table_email.
        # if email in.. pass
        # else match the name ...

        main_table_name = self.main_table['Name'].tolist()
        main_table_name = [item.lower() for item in main_table_name]
        zoom_table_name = self.zoom_table['Name (Original Name)'].tolist()
        zoom_table_name = [item.lower() for item in zoom_table_name]
        intersect = list(set(main_table_name).intersection(zoom_table_name))
        self.names += intersect

        print('name exact match done: {}'.format(len(self.names)))

    def name_partial_match(self):
        '''
        Objective: given that exact match can not be found, we need to do partial match.

        '''
        # _____ Counting the number of NOT FOUND by exact match _____
        count = 0
        not_found_id_list_zoom = []
        not_found_id_list_main = []

        for row in self.zoom_table.iterrows():
            if row[1]['Name (Original Name)'].lower() not in self.names and row[1]['User Email'] not in self.emails:
                count += 1
                not_found_id_list_zoom.append(row[0])
            else:
                self.zoom_table_good_id.append(row[0])

        for row in self.main_table.iterrows():
            if row[1]['Name'].lower() not in self.names and row[1]['Email'] not in self.emails:
                not_found_id_list_main.append(row[0])
            else:
                self.main_table_good_id.append(row[0])

        print('# of not found (of exact match) is: {}'.format(count))
        # some quick statistics:
        # w01b: exact match: 50 are not found out of 261
        # w02a: exact match: 52 are not found out of 274

        # _____ Now doing the partial match: _____
        print('ok')

        partial_match_tuples = []
        for id_main in not_found_id_list_main:
            name = self.main_table['Name'][id_main]
            name_tokens = [item.lower() for item in name.split(' ')]
            for id_zoom in not_found_id_list_zoom:
                name_zoom = self.zoom_table['Name (Original Name)'][id_zoom]
                name_tokens_zoom = [item.lower() for item in name_zoom.split(' ')]
                if len(list(set(name_tokens).intersection(set(name_tokens_zoom)))) >= 2:
                    partial_match_tuples.append((id_main, id_zoom, name, name_zoom))
                    break
        # print(partial_match_tuples)
        # print(len(partial_match_tuples))
        # Quick stats:
        # w01a: 28 are partially matched. Acc: 100% according to authors manual evaluation.
        # Hence we just add the partial_match_tuples to
        self.main_table_good_id += [t[0] for t in partial_match_tuples]
        self.zoom_table_good_id += [t[1] for t in partial_match_tuples]

    def result(self):
        '''
        Objective: (1) generate a new csv, where the weekly column is updated;
        (2) output the non-matched lines in zoom.csv, for manually update later.
        '''
        for index in self.main_table_good_id:
            self.main_table[self.prefix][index] = 1

        count = 0
        for row in self.zoom_table.iterrows():
            if row[0] not in self.zoom_table_good_id:
                print(row)
                count += 1

        the_sum = self.main_table[self.prefix].sum()
        print('Total attendance tracked automatically: {}'.format(the_sum)) # quick stat: 246
        print('Zoom total number (including instructors): {}'.format(len(self.zoom_table['Name (Original Name)'].tolist()))) # quick stat: 262
        print('Zoom not matched (need manual input): {}'.format(count)) # quick stat: 22

        self.main_table.to_csv(self.write_fp)
        print('csv written to: {}'.format(self.write_fp))


    def pipeline(self):
        self.email_exact_match()
        self.name_exact_match()
        self.name_partial_match()
        self.result()


if __name__ == '__main__':
    main_fp = 'data/cs3244-monitoring-clean.csv'
    # csv_fp = 'data/participants_83384276563.csv'
    csv_fp = 'data/participants_81945523458.csv'
    prefix = 'W02a'
    write_fp = 'data/{}.csv'.format(prefix)

    csv2google = csv2google(main_fp=main_fp, csv_fp=csv_fp, prefix=prefix, write_fp=write_fp)
    csv2google.pipeline()

    print('Done')
