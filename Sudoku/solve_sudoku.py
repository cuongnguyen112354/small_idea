class Prepare:
   def __init__(self, data: str):
      self.data = data
      self.char_need_get = {'0','1','2','3','4','5','6','7','8','9'}
      self.matrix = []
      self.matrix_result = []

   def clear(self):
      data_clear = self.data[:self.data.find('notes')]
      data_clear = data_clear.replace('null', '0')

      char_set = set()
      for char in data_clear:
         char_set.add(char)

      char_not_need = list(char_set - self.char_need_get)
      
      for char in char_not_need:
         data_clear = data_clear.replace(char, '')
      
      return data_clear

   def fill_data_into_matrix(self):
      data = self.clear()

      for i in range(18):
         start = i * 9
         end = start + 9

         if i < 9:
            self.matrix.append(list(data[start:end]))
         else:
            self.matrix_result.append(list(data[start:end]))

   def convert_elements_to_int(self):
      for i in range(len(self.matrix)):
         self.matrix[i] = list(map(int, self.matrix[i]))
         self.matrix_result[i] = list(map(int, self.matrix_result[i]))

   def print_matrix(self):
      print('~~~ Matrix ~~~')
      for i in self.matrix:
         print(i)

   def print_matrix_result(self):
      print('~~~ Matrix Result ~~~')
      for i in self.matrix_result:
         print(i)

   def run(self):
      self.fill_data_into_matrix()
      self.convert_elements_to_int()

import copy

class Handle:
   def __init__(self, data: list):
      self.data = data
   
   # input: row, col --> output: tất cả các giá trị có thể của ô đó
   def get_the_possible_values_of_index(self, row, col):
      values = [1, 2, 3, 4, 5, 6, 7, 8, 9]

      for value_row in self.data[row]:
         if value_row != 0 and value_row in values:
            values.remove(value_row)

      for value_col in [row[col] for row in self.data]:
         if value_col != 0 and value_col in values:
            values.remove(value_col)

      row_start = (row // 3) * 3
      col_start = (col // 3) * 3
      for row in range(row_start, row_start + 3):
         for col in range(col_start, col_start + 3):
            if self.data[row][col] != 0 and self.data[row][col] in values:
               values.remove(self.data[row][col])
      
      return values
   # Fill tất cả các giá trị cho 1 ô, cho tất cả các ô
   def fill_value_into_matrix(self):
      # Duyệt qua từng ô và gán các giá trị có thể cho nó (if == 0)
      for row in range(9):
         for col in range(9):
            if self.data[row][col] == 0:
               self.data[row][col] = self.get_the_possible_values_of_index(row, col)

   # Output: If ô này là note --> True, else --> False
   def isNote(self, value):
      if isinstance(value, list):
         return True
      return False

   # Update giá trị cho ô được chỉ định
   def update_value_for_index(self, row, col, value):
      self.data[row][col] = value
      self.update_note_affected(row, col, value)

   # Lấy ma trận nhỏ tại [row][col] --> {'row': [...], 'col': [...]}
   def get_small_matrix_of_index(self, row, col):
      row_start = (row // 3) * 3 # Lọc lấy dòng cần thiết
      col_start = (col // 3) * 3

      index = {
         'row': [],
         'col': []
      }

      for i in range(3):
         index['row'].append(row_start+i)
         index['col'].append(col_start+i)

      return index

   # Update lại note bị ảnh hưởng bởi ô được fill giá trị
   def update_note_affected(self, row, col, value):
      small_matrix = self.get_small_matrix_of_index(row, col)
      # Duyệt và xoá value note trong matrix nhỏ
      for rowL in small_matrix['row']:
         for colL in small_matrix['col']:
            data = self.data[rowL][colL]
            if self.isNote(data) and value in data:
               self.remove_note(rowL, colL, value)
      # Duyệt xoá value note của dòng (không xét lại matrix nhỏ)
      for i, values in enumerate(self.data[row]):
         if self.isNote(values) and value in values and i != small_matrix['col']:
            self.remove_note(row, i, value)
      # Duyệt xoá value note của cột (không xét lại matrix nhỏ)
      for i, values in enumerate([row[col] for row in self.data]):
         if self.isNote(values) and value in values and i != small_matrix['row']:
            self.remove_note(i, col, value)

   # Xoá value note tại vị trí chỉ định [row][col]
   def remove_note(self, row, col, value):
      self.data[row][col].remove(value)
      values = self.data[row][col]
      # Nếu còn 1 note, update luôn giá trị cho ô đó
      if len(values) == 1:
         self.update_value_for_index(row, col, values[0])

   # Scan và fill giá trị cho ô chỉ có thể là một giá trị duy nhất
   def fill_only_value_in_index(self):
      for row in range(9):
         for col in range(9):
            values = self.data[row][col]
            if self.isNote(values) and len(values) == 1:
               self.update_value_for_index(row, col, values[0])
               
   # Trả về những số có num lần xuất hiện
   def appears_times_in_small_matrix(self, matrix, appears_times=1):
      string = ''
      for row in matrix['row']:
         for col in matrix['col']:
            value = self.data[row][col]
            if self.isNote(value):
               for val in value:
                  string = string + str(val)

      result = []
      for i in set(string):
         if string.count(i) == appears_times and i not in ['[',']',',']:
            result.append(int(i))

      return result

   def update_only_value_in_small_matrix(self, matrix, values):
      for row in matrix['row']:
         for col in matrix['col']:
            data = self.data[row][col]
            if self.isNote(data):
               for value in values:
                  if value in data:
                     self.update_value_for_index(row, col, value)
      self.scan_4_matrix_affected(matrix)

   def scan_4_matrix_affected(self, matrix):
      def get_index_4_small_matrix_affected(row, col):
         matrix_affected = {
            'horizontal': [],
            'straight': []
         }

         for i in range(0, 9, 3):
            index_h = [row, i]
            index_s = [i, col]
            if i != col:
               matrix_affected['horizontal'].append(index_h)
            if i != row:
               matrix_affected['straight'].append(index_s)
            
         return matrix_affected

      matrix_affected = get_index_4_small_matrix_affected(matrix['row'][0], matrix['col'][0])
      
      for i in range(2):
         horizontal_matrix = self.get_small_matrix_of_index(matrix_affected['horizontal'][i][0],matrix_affected['horizontal'][i][1])
         straight_matrix = self.get_small_matrix_of_index(matrix_affected['straight'][i][0],matrix_affected['straight'][i][1])

         values = self.appears_times_in_small_matrix(horizontal_matrix)
         if len(values) > 0:
            self.update_only_value_in_small_matrix(horizontal_matrix, values)

         values = self.appears_times_in_small_matrix(straight_matrix)
         if len(values) > 0:
            self.update_only_value_in_small_matrix(straight_matrix, values)

   def fill_only_value_in_small_matrix(self):
      for rowSM in range(0,9,3):
         for colSM in range(0,9,3):
            small_matrix = self.get_small_matrix_of_index(rowSM, colSM)
            values = self.appears_times_in_small_matrix(small_matrix)
            if len(values) > 0:
               self.update_only_value_in_small_matrix(small_matrix, values)

   # Nhận vào 1 value, check xem phải nằm cùng 1 dòng or cột
   def is_a_row_or_col(self, matrix, value):
      def isRow(index):
         if index[0][0] == index[1][0]:
            return True
         return False

      def isCol(index):
         if index[0][1] == index[1][1]:
            return True
         return False

      index = []
      for row in matrix['row']:
         for col in matrix['col']:
            values = self.data[row][col]
            if self.isNote(values) and value in values:
               index.append([row, col])

      if len(index) != 2:
         return -1
      if isRow(index):
         return ['R' ,index[0][0]]
      elif isCol(index):
         return ['C', index[0][1]]
      return -1

   def update_small_matrix_row_or_col_affected(self, matrix, index, value):
      if index[0] == 'R':
         for col in range(9):
            if col in matrix['col']:
               continue
            values = self.data[index[1]][col]
            if self.isNote(values) and value in values:
               self.remove_note(index[1], col, value)
            if (col + 1) % 3 == 0:
               small_matrix = self.get_small_matrix_of_index(index[1], col)
               values = self.appears_times_in_small_matrix(small_matrix)
               if len(values) > 0:
                  self.update_only_value_in_small_matrix(small_matrix, values)
      else:
         for row in range(9):
            if row in matrix['row']:
               continue
            values = self.data[row][index[1]]
            if self.isNote(values) and value in values:
               self.remove_note(row, index[1], value)
            if (row + 1) % 3 == 0:
               small_matrix = self.get_small_matrix_of_index(row, index[1])
               values = self.appears_times_in_small_matrix(small_matrix)
               if len(values) > 0:
                  self.update_only_value_in_small_matrix(small_matrix, values)

   def fill_two_value_in_small_matrix(self):
      for rowSM in range(0,9,3):
         for colSM in range(0,9,3):
            small_matrix = self.get_small_matrix_of_index(rowSM, colSM)
            values = self.appears_times_in_small_matrix(small_matrix, 2)
            if len(values) > 0:
               for value in values:
                  index = self.is_a_row_or_col(small_matrix, value)
                  if index != -1:
                     self.update_small_matrix_row_or_col_affected(small_matrix, index, value)

   def isDone(self):
      for row in self.data:
         string = str(row)
         for value in range(1,9):
            if string.count(str(value)) != 1:
               return False
         for value in row:
            if self.isNote(value):
               return False
            
      for col in range(9):
         string = str([row[col] for row in self.data])
         for value in range(1,9):
            if string.count(str(value)) != 1:
               return False
         
      for row in range(0, 9, 3):
         for col in range(0, 9, 3):
            small_matrix = self.get_small_matrix_of_index(row, col)
            values = []
            for i in small_matrix['row']:
               for j in small_matrix['col']:
                  value = self.data[i][j]
                  if value in values:
                     return False
                  values.append(value)

      return True

   def random_value(self):
      def test(row, col, value):
         try:
            self.update_value_for_index(row, col, value)
            self.run()
         except:
            return False
         else:
            return True

      backup_data = copy.deepcopy(self.data)

      for row in range(9):
         for col in range(9):
            values = backup_data[row][col]
            if self.isNote(values) and len(values) == 3:
               for value in values:
                  if test(row, col, value) and self.isDone():
                     return
                  self.data = copy.deepcopy(backup_data)

   def print_matrix(self):
      for row in range(9):
         print(self.data[row])

   def run(self):
      self.fill_value_into_matrix()
      self.fill_only_value_in_index()
      self.fill_only_value_in_small_matrix()
      self.fill_two_value_in_small_matrix()