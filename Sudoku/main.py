import subprocess
import os
from prepare_data import Prepare
from handle_data import Handle

def main(i, data, detail=False):
   problem = Prepare(data)
   problem.run()

   if detail:
      with open(f'answer{i+1}.txt', 'w') as f:
         for line in problem.matrix_result:
            f.write(f'{line}\n')

   solve_problem = Handle(problem.matrix)
   solve_problem.run()

   if solve_problem.isDone() == False:
      solve_problem.random_value()

   with open(f'output{i+1}.txt', 'w') as f:
      for line in solve_problem.data:
         f.write(f'{line}\n')

   if problem.matrix_result != solve_problem.data:
      return i+1

def assigment(n):
   completed = 0
   index = []
   for i in range(n):
      with open(f'answer{i+1}.txt', 'r') as f:
         result = f.read()

      with open(f'output{i+1}.txt', 'r') as f:
         data = f.read()

      if result == data:
         index.append(i+1)
         completed += 1

   return completed, index

def clear(n, detail=False):
   for i in range(1, n+1):
      os.remove(f'output{i}.txt')
      if detail:
         os.remove(f'answer{i}.txt')


n = int(input('Nhập n: '))

if n == 1:
   with open('input.txt', 'r') as f:
      data = f.read()

   not_complete = main(n-1, data)

   if not_complete:
      print('Not Complete!')
   else:
      print('Completed!!!')

   input('Press "Enter" to exit!!!')

   clear(n)

else:
   not_complete = []
   level = int(input('Nhập level: '))

   char = str(input('Bạn có muốn xem chi tiết không?\nw '))

   if char:
      detail = True
   else:
      detail = False

   for i in range(n):
      data = str(subprocess.check_output(f'curl -d REQUESTED_LEVEL={level} https://www.sudoku.net/api/getSudoku.php'))
      result = main(i, data, detail)
      if result:
         not_complete.append(result)

   lenght = len(not_complete)
   if lenght:
      print(f'Not Complete: {len(not_complete)}/{n} - Index: {not_complete}')
   else:
      print('Completed all!')

   if detail:
      completed = assigment(n)
      print(f'Completed: {completed[0]}/{n} - Index: {completed[1]}')

   input('Press "Enter" to exit!!!')

   clear(n, detail)

subprocess.run('cls', shell=True)