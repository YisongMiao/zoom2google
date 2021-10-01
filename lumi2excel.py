import pandas as pd
import regex as re


class lumi2excel():
    def __init__(self, csv_fp):
        self.csv_fp = csv_fp
        self.zoom_table = pd.read_excel(self.csv_fp)
        print('init')


    def pipeline(self):
        count = 0
        comments_col_names = ['Q{} Comment'.format(i) for i in [1, 2, 3, 4, 5, 7, 8, 10, 11, 12, 13, 14, 16, 17, 18, 19]]

        question_col_names = ['Q{} Answer'.format(i) for i in [1, 3, 5, 7, 9, 11, 13, 15]]

        question_to_be_marked = ['Q{} Mark'.format(i) for i in range(1, 20)]
        score_dict = dict()
        for q in question_to_be_marked:
            score_dict[q] = list()


        list_student_number = []
        list_total_mark = []
        list_comment = []
        list_moderation = []


        for row in self.zoom_table.iterrows():

            code = ''

            count += 1
            print(count)
            student_number = row[1]['Student Number']
            total_marks = row[1]['Total Marks']
            s = ''
            for comment in comments_col_names:
                comment_content = row[1][comment]
                if pd.isna(comment_content):
                    continue
                s += '#{}: {}'.format(comment, comment_content)

            # for code_name in question_col_names:
            #     code_in_question = row[1][code_name]
            #     if pd.isna(code_in_question):
            #         continue
            #     code += code_in_question
            #     code += '\n\n'

            for q in score_dict:
                score = row[1][q]
                if pd.isna(score):
                    score = 0
                    print(student_number)
                    print('Error: Score cannot be invalid.')
                score_dict[q].append(score)

            fp = 'data/assign1/{}.py'.format(student_number)
            with open(fp, 'w') as f:
                # print(code)
                f.write(code)

            list_student_number.append(student_number)
            list_total_mark.append(total_marks)
            list_comment.append(s)
            list_moderation.append('')



        data = {
                'STUDENT_NUMBER': list_student_number,
                'MARKS': list_total_mark,
                'MODERATION': None,
                'REMARKS': list_comment,
        }

        for i in range(1, 20):
            data['Q{}'.format(i)] = score_dict['Q{} Mark'.format(i)]

        df = pd.DataFrame.from_dict(data)
        df.to_excel('data/assignment1_grade.xlsx')
        print('Done!')


if __name__ == '__main__':
    csv_fp = 'data/Assignment #1-1632929272037.xlsx'
    lumi2excel = lumi2excel(csv_fp=csv_fp)
    
    lumi2excel.pipeline()

    # Not in use. Do it in excel. We still export in scale of 0 - 1.
    # score_table = {
    #     1: 3,
    #     2: 2,
    #     3: 3,
    #     4: 2,
    #     5: 3,
    #     6: 2,
    #     7: 3,
    #     8: 2,
    #     9: 3,
    #     10: 2,
    #     11: 3,
    #     12: 2,
    #     13: 3,
    #     14: 2,
    #     15: 3,
    #     16: 5,
    #     17: 5,
    #     18: 5,
    #     19: 5
    # }

    print('Done')
