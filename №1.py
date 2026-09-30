import math
import tkinter as tk
from tkinter import filedialog, messagebox

# --- Алгоритмы геометрических расчетов ---


def orientation(p, q, r):
    """Ориентация трех точек (векторное произведение)"""
    val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
    if abs(val) < 1e-9:
        return 0
    return 1 if val > 0 else 2


def on_segment(p, q, r):
    """Проверка нахождения точки r на отрезке pq"""
    if (
        r[0] <= max(p[0], q[0])
        and r[0] >= min(p[0], q[0])
        and r[1] <= max(p[1], q[1])
        and r[1] >= min(p[1], q[1])
    ):
        return True
    return False


def do_intersect(seg1, seg2):
    """Основной алгоритм проверки пересечения"""
    p1, q1 = seg1[0], seg1[1]
    p2, q2 = seg2[0], seg2[1]

    o1 = orientation(p1, q1, p2)
    o2 = orientation(p1, q1, q2)
    o3 = orientation(p2, q2, p1)
    o4 = orientation(p2, q2, q1)

    if o1 != o2 and o3 != o4:
        return True

    if o1 == 0 and on_segment(p1, q1, p2):
        return True
    if o2 == 0 and on_segment(p1, q1, q2):
        return True
    if o3 == 0 and on_segment(p2, q2, p1):
        return True
    if o4 == 0 and on_segment(p2, q2, q1):
        return True

    return False


def find_intersection_point(seg1, seg2):
    """Поиск точки пересечения через определители"""
    p1, q1 = seg1[0], seg1[1]
    p2, q2 = seg2[0], seg2[1]

    xdiff = (p1[0] - q1[0], p2[0] - q2[0])
    ydiff = (p1[1] - q1[1], p2[1] - q2[1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
        return None

    d = (det(p1, q1), det(p2, q2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return x, y


# --- Графический интерфейс пользователя ---


class IntersectApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Проверка отрезков")
        self.root.geometry("1000x650")
        self.segments_data = []

        # Левая панель
        self.left_panel = tk.Frame(root, width=350, bg="#f0f0f0")
        self.left_panel.pack(side=tk.LEFT, fill=tk.Y)
        self.left_panel.pack_propagate(False)

        self.btn_load = tk.Button(
            self.left_panel,
            text="📂 Выбрать файл",
            command=self.load_file,
            bg="#2196F3",
            fg="white",
            font=("Arial", 11, "bold"),
            pady=8,
        )
        self.btn_load.pack(fill=tk.X, padx=10, pady=10)

        # Контейнер списка кнопок
        self.frame_container = tk.Frame(self.left_panel)
        self.frame_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.canvas_list = tk.Canvas(self.frame_container, bg="#f0f0f0")
        self.scrollbar = tk.Scrollbar(
            self.frame_container, orient="vertical", command=self.canvas_list.yview
        )
        self.scrollable_frame = tk.Frame(self.canvas_list, bg="#f0f0f0")

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas_list.configure(
                scrollregion=self.canvas_list.bbox("all")
            ),
        )
        self.canvas_list.create_window(
            (0, 0), window=self.scrollable_frame, anchor="nw"
        )
        self.canvas_list.configure(yscrollcommand=self.scrollbar.set)
        self.canvas_list.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Правая панель
        self.right_panel = tk.Frame(root, bg="white")
        self.right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.status_label = tk.Label(
            self.right_panel,
            text="Выберите пару отрезков",
            font=("Arial", 13, "bold"),
            bg="#e0e0e0",
            pady=10,
        )
        self.status_label.pack(fill=tk.X)

        self.plot_canvas = tk.Canvas(self.right_panel, bg="#fafafa")
        self.plot_canvas.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

    def load_file(self):
        """Парсинг файла координат"""
        file_path = filedialog.askopenfilename(
            filetypes=[("Текстовые файлы", "*.txt *.csv"), ("Все файлы", "*.*")]
        )
        if not file_path:
            return

        for w in self.scrollable_frame.winfo_children():
            w.destroy()
        self.segments_data.clear()
        self.plot_canvas.delete("all")
        self.status_label.config(text="Файл загружен", bg="#e0e0e0")

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                lines = f.readlines()

            p_idx = 1
            for line in lines:
                line = line.strip()
                if not line:
                    continue

                coords = [float(x.strip()) for x in line.split(",") if x.strip()]
                if len(coords) < 8:
                    continue

                seg1 = ((coords[0], coords[1]), (coords[2], coords[3]))
                seg2 = ((coords[4], coords[5]), (coords[6], coords[7]))
                self.segments_data.append((seg1, seg2))

                txt = (
                    f"Пара №{p_idx}\n"
                    f"O1:({coords[0]},{coords[1]})-"
                    f"({coords[2]},{coords[3]})\n"
                    f"O2:({coords[4]},{coords[5]})-"
                    f"({coords[6]},{coords[7]})"
                )

                btn = tk.Button(
                    self.scrollable_frame,
                    text=txt,
                    justify=tk.LEFT,
                    anchor="w",
                    padx=10,
                    pady=5,
                    font=("Courier", 9),
                    bd=1,
                    relief=tk.GROOVE,
                    command=lambda i=len(self.segments_data) - 1: self.draw_pair(
                        i
                    ),
                )
                btn.pack(fill=tk.X, pady=3, padx=5)
                p_idx += 1

        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка файла:\n{str(e)}")

    def draw_pair(self, idx):
        """Отрисовка выбранных отрезков"""
        self.plot_canvas.delete("all")
        seg1, seg2 = self.segments_data[idx]

        intersects = do_intersect(seg1, seg2)
        color = "#4CAF50" if intersects else "#F44336"

        if intersects:
            self.status_label.config(
                text=f"Пара №{idx+1}: Пересекаются 🟢",
                bg="#E8F5E9",
                fg="#2E7D32",
            )
        else:
            self.status_label.config(
                text=f"Пара №{idx+1}: Не пересекаются 🔴",
                bg="#FFEBEE",
                fg="#C62828",
            )

        all_x = [seg1[0][0], seg1[1][0], seg2[0][0], seg2[1][0]]
        all_y = [seg1[0][1], seg1[1][1], seg2[0][1], seg2[1][1]]

        min_x, max_x = min(all_x), max(all_x)
        min_y, max_y = min(all_y), max(all_y)

        if max_x == min_x:
            max_x += 1
            min_x -= 1
        if max_y == min_y:
            max_y += 1
            min_y -= 1

        margin = 50
        w = self.plot_canvas.winfo_width() - 2 * margin
        h = self.plot_canvas.winfo_height() - 2 * margin

        if w <= 0:
            w = 500
        if h <= 0:
            h = 400

        def to_scr(x, y):
            sx = margin + ((x - min_x) / (max_x - min_x)) * w
            sy = margin + h - ((y - min_y) / (max_y - min_y)) * h
            return sx, sy

        s1_p1 = to_scr(*seg1[0])
        s1_p2 = to_scr(*seg1[1])
        s2_p1 = to_scr(*seg2[0])
        s2_p2 = to_scr(*seg2[1])

        self.plot_canvas.create_rectangle(
            margin, margin, margin + w, margin + h, outline="#e0e0e0", fill="#fafafa"
        )

        self.plot_canvas.create_line(
            s1_p1[0], s1_p1[1], s1_p2[0], s1_p2[1], fill=color, width=4
        )
        self.plot_canvas.create_line(
            s2_p1[0], s2_p1[1], s2_p2[0], s2_p2[1], fill=color, width=4
        )

        pts = [
            (seg1[0], "A1"),
            (seg1[1], "B1"),
            (seg2[0], "A2"),
            (seg2[1], "B2"),
        ]
        for pt, name in pts:
            sx, sy = to_scr(*pt)
            self.plot_canvas.create_oval(
                sx - 4, sy - 4, sx + 4, sy + 4, fill="#333", outline="white"
            )
            self.plot_canvas.create_text(
                sx,
                sy - 12,
                text=f"{name}({pt[0]},{pt[1]})",
                font=("Arial", 8),
                fill="#555",
            )

        if intersects:
            pt_i = find_intersection_point(seg1, seg2)
            if pt_i:
                ix, iy = to_scr(*pt_i)
                self.plot_canvas.create_oval(
                    ix - 6,
                    iy - 6,
                    ix + 6,
                    iy + 6,
                    fill="yellow",
                    outline="black",
                    width=2,
                )
                self.plot_canvas.create_text(
                    ix,
                    iy + 20,
                    text=f"X:({round(pt_i[0],2)},{round(pt_i[1],2)})",
                    font=("Arial", 8, "bold"),
                    fill="#1b5e20",
                )


if __name__ == "__main__":
    root = tk.Tk()
    app = IntersectApp(root)
    root.mainloop()
