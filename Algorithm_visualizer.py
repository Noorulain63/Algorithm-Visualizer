import flet
from flet import Page, RadioGroup, Radio, Column, Button, TextField, Text, Slider, Row, Container, Colors, padding
import random

# Sorting Algorithms
def bubble_sort(arr):
    steps = []
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
            steps.append(arr[:])  # Record the array state at this step
    return steps, "O(n)", "O(n^2)"

# selection sort
def selection_sort(arr):
    steps = []
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
        steps.append(arr[:])
    return steps, "O(n^2)", "O(n^2)"

#insertion sort
def insertion_sort(arr):
    steps = []
    n = len(arr)
    for i in range(1, n):
        key = arr[i]
        j = i - 1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
        steps.append(arr[:])
    return steps, "O(n)", "O(n^2)"

def generate_bars(arr):
    """Generate bar representation of the array."""
    max_value = max(arr)
    bars = [
        Container(
            bgcolor=Colors.RED_200,
            border_radius=5,
            border=1,
            border_color=Colors.BLACK,
            padding=padding.all(5),
            width=30,
            height=(value / max_value) * 200,  # Scale the height based on the max value
        )
        for index, value in enumerate(arr)
    ]
    return bars


def visualize_sorting(page: Page, steps, best_complexity, worst_complexity):
    """Visualize the sorting steps with color-shifting threads and borders."""
    try:
        for step in steps:
            row = Row(
                controls=generate_bars(step),
                alignment="center",
            )
            page.add(row)
        page.add(Text(f"Best Case Time Complexity: {best_complexity}", size=16, weight="bold"))
        page.add(Text(f"Worst Case Time Complexity: {worst_complexity}", size=16, weight="bold"))
        page.update()
    except Exception as e:
        page.add(Text(f"An error occurred: {e}", color=Colors.RED, size=16, weight="bold"))
        page.update()


# Main Application
def main(page: Page):
    try:
        page.title = "Algorithm Visualizer"
        page.vertical_alignment = "start"
        page.scroll = "auto"
        page.padding = padding.all(20)

        # Initialize the array and variables
        array = []
        algorithm_steps = []
        current_step_index = 0
        selected_algorithm = "Bubble Sort"
        best_complexity = ""
        worst_complexity = ""

        # UI Components
        array_input = TextField(label="Enter Array (comma-separated)", width=400)
        array_size_slider = Slider(
            min=5, max=30, value=10, label="Array Size: {value}", on_change=lambda e: generate_array(None)
        )
        algorithm_selector = RadioGroup(
            content=Column(
                [
                    Radio(value="Bubble Sort", label="Bubble Sort"),
                    Radio(value="Selection Sort", label="Selection Sort"),
                    Radio(value="Insertion Sort", label="Insertion Sort"),
                ]
            ),
            value="Bubble Sort",
        )
        graph_canvas = Row(alignment="center", spacing=2)
        array_text_display = Text(value="Generated Array: []", size=14, color=Colors.WHITE)  # Dark Blue Color
        graph_step_label = Text(value="Step: 0", size=14)

        def draw_graph(data):
            """
            Update the graph visualization based on the array data.

            :param data: List of integers to visualize
            """
            graph_canvas.controls.clear()
            max_value = max(data) if data else 1
            for value in data:
                bar_height = (value / max_value) * 200  # Scale bar height
                bar = Column(
                    [
                        Text(str(value), size=12, color=Colors.WHITE, weight="bold"),  # White numbers on top
                        Container(
                            bgcolor=Colors.GREEN,
                            width=20,
                            height=bar_height,
                            border_radius=5,
                            margin=padding.only(right=5),
                        ),
                    ],
                    horizontal_alignment="center",
                )
                graph_canvas.controls.append(bar)
            page.update()

        # Generate Random Array
        def generate_array(e):
            """
            Generate a random array and display it on the graph.

            :param e: Event trigger
            """
            nonlocal array
            try:
                array_size = int(array_size_slider.value)
                if array_size < 5 or array_size > 30:
                    page.snack_bar = Text("Array size out of bounds!", color=Colors.RED)
                    page.snack_bar.open = True
                    return
                array = [random.randint(1, 100) for _ in range(array_size)]
                draw_graph(array)
                array_text_display.value = f"Generated Array: {array}"  # Dark Blue Text Display
                page.update()
            except Exception as ex:
                page.snack_bar = Text(f"Error: {ex}", color=Colors.RED)
                page.snack_bar.open = True
                page.update()
        # Update Sorting Algorithm
        def update_algorithm(e):
            """
            Update the selected algorithm.

            :param e: Event trigger
            """
            nonlocal selected_algorithm
            selected_algorithm = algorithm_selector.value

        # Sort and Visualize
        def sort_and_visualize(e):
            """
            Perform the selected sorting algorithm and visualize each step.

            :param e: Event trigger
            """
            nonlocal algorithm_steps, current_step_index, best_complexity, worst_complexity
            if array_input.value.strip():
                try:
                    array[:] = list(map(int, array_input.value.split(",")))
                    array_text_display.value = f"Entered Array: {array}"
                except ValueError:
                    page.snack_bar = Text("Invalid array input. Use only integers.", color=Colors.RED)
                    page.snack_bar.open = True
                    page.update()
                    return
            if selected_algorithm == "Bubble Sort":
                algorithm_steps, best_complexity, worst_complexity = bubble_sort(array[:])
            elif selected_algorithm == "Selection Sort":
                algorithm_steps, best_complexity, worst_complexity = selection_sort(array[:])
            elif selected_algorithm == "Insertion Sort":
                algorithm_steps, best_complexity, worst_complexity = insertion_sort(array[:])
            current_step_index = 0
            graph_step_label.value = f"Step: {current_step_index}/{len(algorithm_steps)}"
            show_graph_page()

        # Graph Page Navigation
        def show_graph_page():
            page.clean()

            def back_to_main(e):
                show_main_page()

            def next_step(e):
                nonlocal current_step_index
                if current_step_index < len(algorithm_steps):
                    draw_graph(algorithm_steps[current_step_index])
                    graph_step_label.value = f"Step: {current_step_index + 1}/{len(algorithm_steps)}"
                    current_step_index += 1
                page.update()

            def auto_sort(e):
                nonlocal current_step_index
                import time
                while current_step_index < len(algorithm_steps):
                    if current_step_index < len(algorithm_steps):
                        draw_graph(algorithm_steps[current_step_index])
                        graph_step_label.value = f"Step: {current_step_index + 1}/{len(algorithm_steps)}"
                        current_step_index += 1
                        page.update()
                        time.sleep(0.4)  # Delay between steps

            page.add(
                Column(
                    [
                        Button("Back", on_click=back_to_main),
                        graph_step_label,
                        graph_canvas,
                        Button("Next Step", on_click=next_step),
                        Button("Auto Sort", on_click=auto_sort),  # Added Auto Sort button
                        Text(f"Best Case Time Complexity: {best_complexity}", size=16, weight="bold"),
                        Text(f"Worst Case Time Complexity: {worst_complexity}", size=16, weight="bold"),
                    ],
                    horizontal_alignment="center",
                    alignment="center",
                )
            )
            draw_graph(array)

        # Main Page Layout
        def show_main_page():
            page.clean()
            page.add(
                Column(
                    [
                        Text("Algorithm Visualizer", size=24, weight="bold"),
                        array_input,
                        Text("Array Size"),
                        array_size_slider,
                        array_text_display,
                        Text("Choose Algorithm"),
                        algorithm_selector,
                        Button("Generate Random Array", on_click=generate_array),
                        Button("Visualize Sorting", on_click=sort_and_visualize),
                        graph_canvas,
                    ],
                    horizontal_alignment="center",
                    alignment="center",
                )
            )
            generate_array(None)

        algorithm_selector.on_change = update_algorithm
        show_main_page()
    except Exception as e:
        page.add(Text(f"An error occurred: {e}", color=Colors.RED, size=16, weight="bold"))
        page.update()


flet.app(target=main)

