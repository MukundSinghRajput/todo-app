from typing import List, Optional

class BTodo:
    def __init__(self, file: str) -> None:
            self.file = file

    def add(self, todo: str) -> None:
            with open(self.file, "a") as f:
                f.write(todo + '\n')

    def read(self) -> List[str]:
            with open(self.file, "r") as f:
                return [x.strip() for x in f]

    def delete(self, line_number: int) -> Optional[str]:
            todos = self.read()
            if 0 < line_number <= len(todos):
                removed_todo = todos.pop(line_number - 1)
                with open(self.file, "w") as f:
                    for todo in todos:
                        f.write(todo + '\n')
                return removed_todo
            else:
                return None

    def edit(self, line_number:int, todo:str) -> Optional[bool]:
            todos = self.read()
            if 0 < line_number <= len(todos):
                todos[line_number-1] = todo
                with open(self.file, "w") as f:
                    for todo in todos:
                        f.write(todo + '\n')
                return True
            else:
                None