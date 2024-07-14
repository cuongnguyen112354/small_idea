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