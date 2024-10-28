import flet as ft
from backend.todo import BTodo

class Task(ft.Row):
    def __init__(self, text: str, todo: BTodo, task_number: int, on_delete=None):
        super().__init__()
        self.todos = todo
        self.task_number = task_number
        self.on_delete = on_delete
        
        self.checkbox = ft.Checkbox(
            value=False,
            check_color=ft.colors.BLACK,
        )
        
        self.text_view = ft.Text(
            text,
            size=16,
            color=ft.colors.WHITE,
            weight=ft.FontWeight.W_400,
        )
        
        self.text_edit = ft.TextField(
            text,
            visible=False,
            border_color=ft.colors.GREEN_400,
            focused_border_color=ft.colors.GREEN_200,
            text_style=ft.TextStyle(color=ft.colors.WHITE),
            content_padding=ft.padding.all(10),
        )
        
        self.delete_button = ft.IconButton(
            icon=ft.icons.DELETE_OUTLINE,
            icon_color=ft.colors.GREEN_400,
            icon_size=20,
            tooltip="Delete task",
            on_click=self.delete,
        )
        
        self.edit_button = ft.IconButton(
            icon=ft.icons.EDIT_OUTLINED,
            icon_color=ft.colors.GREEN_400,
            icon_size=20,
            tooltip="Edit task",
            on_click=self.edit,
        )
        
        self.save_button = ft.IconButton(
            visible=False,
            icon=ft.icons.SAVE_OUTLINED,
            icon_color=ft.colors.GREEN_400,
            icon_size=20,
            tooltip="Save changes",
            on_click=self.save,
        )
        
        self.controls = [
            self.checkbox,
            ft.Container(width=20),
            self.text_view,
            self.text_edit,
            ft.Container(expand=True),
            self.edit_button,
            self.save_button,
            self.delete_button,
        ]
        
        self.alignment = ft.MainAxisAlignment.START
        self.vertical_alignment = ft.CrossAxisAlignment.CENTER
        
        self.border = ft.border.all(1, ft.colors.GREEN_900)
        self.border_radius = 8
        self.padding = ft.padding.all(12)
        
    def edit(self, e):
        self.edit_button.visible = False
        self.save_button.visible = True
        self.text_view.visible = False
        self.text_edit.visible = True
        self.update()
        
    def save(self, e):
        if self.text_edit.value:
            self.todos.edit(self.task_number, self.text_edit.value)
            self.text_view.value = self.text_edit.value
            self.edit_button.visible = True
            self.save_button.visible = False
            self.text_view.visible = True
            self.text_edit.visible = False
            self.update()
        
    def delete(self, e):
        if self.on_delete:
            self.on_delete(self)
        self.todos.delete(self.task_number)
        self.visible = False
        self.update()

def main(page: ft.Page):
    todo = BTodo("todo.txt")
    page.title = "ToDo"
    page.bgcolor = ft.colors.BLACK
    page.padding = 40
    page.window_width = 800
    page.window_min_width = 600
    page.window_height = 800
    
    def add_task(e):
        if new_task.value:
            todo.add(new_task.value)
            task = Task(
                text=new_task.value,
                todo=todo,
                task_number=len(tasks_container.controls) + 1,
                on_delete=lambda x: tasks_container.controls.remove(x),
            )
            tasks_container.controls.append(task)
            new_task.value = ""
            page.update()
    
    title = ft.Text(
        "ToDo",
        size=44,
        weight=ft.FontWeight.BOLD,
        color=ft.colors.GREEN_400,
        text_align=ft.TextAlign.CENTER,
    )
    
    new_task = ft.TextField(
        hint_text="Enter your todo here",
        hint_style=ft.TextStyle(color=ft.colors.GREEN_200),
        border_color=ft.colors.GREEN_400,
        focused_border_color=ft.colors.GREEN_200,
        text_style=ft.TextStyle(color=ft.colors.WHITE),
        content_padding=ft.padding.all(15),
        expand=True,
        on_submit=add_task,
    )
    
    add_button = ft.ElevatedButton(
        text="Add Task",
        style=ft.ButtonStyle(
            color=ft.colors.BLACK,
            bgcolor=ft.colors.GREEN_400,
            padding=ft.padding.all(15),
        ),
        on_click=add_task,
        height=50,
    )

    tasks_container = ft.Column(
        spacing=10,
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )
    
    for i, x in enumerate(todo.read(), 1):
        task = Task(
            text=x,
            todo=todo,
            task_number=i,
            on_delete=lambda x: tasks_container.controls.remove(x),
        )
        tasks_container.controls.append(task)
    
    page.add(
        ft.Column(
            [
                ft.Container(
                    content=title,
                    alignment=ft.alignment.center,
                    margin=ft.margin.only(bottom=30),
                ),
                ft.Container(
                    content=ft.Row(
                        [
                            new_task,
                            ft.Container(width=10),
                            add_button,
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    margin=ft.margin.only(bottom=30),
                ),
                ft.Container(
                    content=tasks_container,
                    border=ft.border.all(1, ft.colors.GREEN_900),
                    border_radius=10,
                    padding=10,
                    expand=True,
                ),
            ],
            expand=True,
        ),
    )

ft.app(target=main)