                                      # Graph Traversing #
from tkinter import *
import time

class InteractiveGraph:
    def __init__(self, root):
        self.root = root
        self.canvas = Canvas(root, width=600, height=600, bg="#1e1f29")
        self.canvas.pack()

        self.node_radius = 20
        self.nodes = {}
        self.node_positions = {}
        self.edges = {}
        self.adj = {}

        self.node_count = 0
        self.selected_node = None

        self.status = Label(root, text="Click to add nodes. Then click two nodes to add edge.", font=("Helvetica", 14), fg="#f0f0f5", bg="#2e2f3e")
        self.status.pack(fill=X)

        self.canvas.bind("<Button-1>", self.on_canvas_click)

        btn_frame = Frame(root, bg="#2e2f3e")
        btn_frame.pack(pady=10, fill=X)

        self.bfs_btn = Button(btn_frame, text="BFS", command=self.bfs_traversal, state=DISABLED, bg="#4caf50", fg="white", width=10, font=("Helvetica", 12, "bold"), relief=FLAT)
        self.bfs_btn.pack(side=LEFT, padx=8)

        self.dfs_btn = Button(btn_frame, text="DFS", command=self.dfs_traversal, state=DISABLED, bg="#2196f3", fg="white", width=10, font=("Helvetica", 12, "bold"), relief=FLAT)
        self.dfs_btn.pack(side=LEFT, padx=8)

        self.reset_btn = Button(btn_frame, text="Reset", command=self.reset_graph, width=10, font=("Helvetica", 12, "bold"), relief=FLAT, bg="#f44336", fg="white")
        self.reset_btn.pack(side=LEFT, padx=8)

    def on_canvas_click(self, event):
        x, y = event.x, event.y
        clicked_node = self.get_node_at_pos(x, y)
        if clicked_node is None:
            self.create_node(x, y)
        else:
            if self.selected_node is None:
                self.selected_node = clicked_node
                self.status.config(text=f"Selected node {self.selected_node} for edge start. Click another node to connect.")
                self.canvas.itemconfig(self.nodes[self.selected_node][0], outline="#ff5252", width=4)
            else:
                if clicked_node != self.selected_node:
                    self.create_edge(self.selected_node, clicked_node)
                    self.status.config(text=f"Edge created between {self.selected_node} and {clicked_node}.")
                    self.canvas.itemconfig(self.nodes[self.selected_node][0], outline="white", width=2)
                    self.selected_node = None
                    self.bfs_btn.config(state=NORMAL)
                    self.dfs_btn.config(state=NORMAL)
                else:
                    self.canvas.itemconfig(self.nodes[self.selected_node][0], outline="white", width=2)
                    self.selected_node = None
                    self.status.config(text="Edge creation cancelled. Select a node or click empty space to add node.")

    def create_node(self, x, y):
        circle = self.canvas.create_oval(
            x - self.node_radius, y - self.node_radius,
            x + self.node_radius, y + self.node_radius,
            fill="#394263", outline="white", width=2
        )
        text = self.canvas.create_text(x, y, text=str(self.node_count), font=("Helvetica", 14, "bold"), fill="#c0c0c5")
        self.nodes[self.node_count] = (circle, x, y, text)
        self.node_positions[self.node_count] = (x, y)
        self.adj[self.node_count] = []
        self.node_count += 1
        self.status.config(text="Node created. Click empty space to add more nodes or click node to create edge.")

    def get_node_at_pos(self, x, y):
        for node_id, (circle, cx, cy, text) in self.nodes.items():
            dist_sq = (x - cx) ** 2 + (y - cy) ** 2
            if dist_sq <= self.node_radius ** 2:
                return node_id
        return None

    def create_edge(self, src, dst):
        x1, y1 = self.node_positions[src]
        x2, y2 = self.node_positions[dst]
        ctrl_x = (x1 + x2) / 2
        ctrl_y = (y1 + y2) / 2 - 40

        line_id = self.canvas.create_line(x1, y1, ctrl_x, ctrl_y, x2, y2, smooth=True, width=3, fill="#a8a8b3")
        self.edges[(src, dst)] = line_id
        self.edges[(dst, src)] = line_id

        self.adj[src].append(dst)
        self.adj[dst].append(src)

    def highlight_node(self, node, color):
        circle, x, y, text = self.nodes[node]
        self.canvas.itemconfig(circle, fill=color)

    def highlight_edge(self, src, dst, color):
        line_id = self.edges.get((src, dst))
        if line_id:
            self.canvas.itemconfig(line_id, fill=color)

    def reset_colors(self):
        for node in self.nodes:
            self.highlight_node(node, "#394263")
        for edge in self.edges.values():
            self.canvas.itemconfig(edge, fill="#a8a8b3")

    def bfs_traversal(self):
        if self.node_count == 0:
            self.status.config(text="No nodes to traverse!")
            return
        self.reset_colors()
        start = 0
        visited = set()
        queue = [start]
        visited.add(start)
        self.status.config(text="Running BFS traversal...")

        while queue:
            current = queue.pop(0)
            self.highlight_node(current, "#ff5252")
            self.root.update()
            time.sleep(0.6)

            for neighbor in self.adj[current]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
                    self.highlight_edge(current, neighbor, "#ff5252")
                    self.root.update()
                    time.sleep(0.4)
        self.status.config(text="BFS traversal complete!")

    def dfs_traversal(self):
        if self.node_count == 0:
            self.status.config(text="No nodes to traverse!")
            return
        self.reset_colors()
        start = 0
        visited = set()
        stack = [start]
        self.status.config(text="Running DFS traversal...")

        while stack:
            current = stack.pop()
            if current not in visited:
                visited.add(current)
                self.highlight_node(current, "#2196f3")
                self.root.update()
                time.sleep(0.6)

                for neighbor in reversed(self.adj[current]):
                    if neighbor not in visited:
                        stack.append(neighbor)
                        self.highlight_edge(current, neighbor, "#2196f3")
                        self.root.update()
                        time.sleep(0.4)
        self.status.config(text="DFS traversal complete!")

    def reset_graph(self):
        self.canvas.delete("all")
        self.nodes.clear()
        self.node_positions.clear()
        self.edges.clear()
        self.adj.clear()
        self.node_count = 0
        self.selected_node = None
        self.status.config(text="Graph cleared. Click to add nodes.")
        self.bfs_btn.config(state=DISABLED)
        self.dfs_btn.config(state=DISABLED)

if __name__ == "__main__":
    root = Tk()
    root.title("Interactive Graph Drawing and Traversal")
    root.geometry("620x700")
    root.configure(bg="#2e2f3e")
    app = InteractiveGraph(root)
    root.mainloop()
