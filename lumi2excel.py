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

        list_student_number = []
        list_total_mark = []
        list_comment = []
        list_moderation = []
        for row in self.zoom_table.iterrows():
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

        df = pd.DataFrame.from_dict(data)
        df.to_excel('data/assignment1_grade.xlsx')
        print('Done!')


if __name__ == '__main__':
    csv_fp = 'data/Assignment #1-1632548825555.xlsx'
    lumi2excel = lumi2excel(csv_fp=csv_fp)
    
    lumi2excel.pipeline()

    print('Done')
