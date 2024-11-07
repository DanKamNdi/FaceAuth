import tkinter as tk
from tkinter import font as tkfont, messagebox
import cv2
from PIL import Image, ImageTk
import threading
import queue
from deepface import DeepFace
import os
import time


class SecretGovApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold")
        self.normal_font = tkfont.Font(family='Helvetica', size=12)
        self.current_user = None

        # Set the application to full-screen mode
        self.attributes('-fullscreen', True)

        # Bind the Escape key to exit full-screen mode
        self.bind('<Escape>', self.exit_fullscreen)

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (LoginPage, RegistrationPage, AuthenticationPage, SecureAreaPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("LoginPage")

    def show_frame(self, page_name, user=None):
        for frame in self.frames.values():
            if hasattr(frame, 'stop_camera'):
                frame.stop_camera()

        frame = self.frames[page_name]
        if page_name == "SecureAreaPage" and user:
            self.current_user = user
            frame.update_welcome_message(user)
        frame.tkraise()
        if page_name in ["AuthenticationPage", "RegistrationPage"]:
            self.frames[page_name].start_camera()

    def exit_fullscreen(self, event=None):
        self.attributes('-fullscreen', False)


class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg='black')

        label = tk.Label(self, text="CLASSIFIED ACCESS", font=controller.title_font, fg="green", bg="black")
        label.pack(side="top", fill="x", pady=10)

        auth_button = tk.Button(self, text="INITIATE FACIAL SCAN",
                                command=lambda: controller.show_frame("AuthenticationPage"),
                                font=controller.normal_font, bg="green", fg="black")
        auth_button.pack(pady=20)

        reg_button = tk.Button(self, text="REGISTER NEW USER",
                               command=lambda: controller.show_frame("RegistrationPage"),
                               font=controller.normal_font, bg="blue", fg="white")
        reg_button.pack(pady=20)


class RegistrationPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg='black')

        self.label = tk.Label(self, text="REGISTER NEW USER", font=controller.title_font, fg="blue", bg="black")
        self.label.pack(side="top", fill="x", pady=10)

        self.name_label = tk.Label(self, text="Enter your name:", font=controller.normal_font, fg="white", bg="black")
        self.name_label.pack(pady=10)

        self.name_entry = tk.Entry(self, font=controller.normal_font)
        self.name_entry.pack(pady=10)

        self.camera_label = tk.Label(self, text="Initializing camera...", font=controller.normal_font, fg="yellow",
                                     bg="black")
        self.camera_label.pack(pady=20)

        self.register_button = tk.Button(self, text="CAPTURE AND REGISTER",
                                         command=self.register_face,
                                         font=controller.normal_font, bg="blue", fg="white")
        self.register_button.pack(pady=20)
        self.register_button.config(state=tk.DISABLED)

        self.back_button = tk.Button(self, text="BACK TO LOGIN",
                                     command=lambda: controller.show_frame("LoginPage"),
                                     font=controller.normal_font, bg="red", fg="white")
        self.back_button.pack(pady=20)

        self.camera = None
        self.frame_queue = queue.Queue(maxsize=1)
        self.running = False
        self.camera_ready = False

    def start_camera(self):
        self.camera = cv2.VideoCapture(0)
        self.running = True
        threading.Thread(target=self.update_camera, daemon=True).start()
        self.wait_for_camera()

    def wait_for_camera(self):
        if not self.camera_ready:
            self.controller.after(100, self.wait_for_camera)
        else:
            self.camera_label.config(text="Camera ready")
            self.register_button.config(state=tk.NORMAL)
            self.show_frame()

    def stop_camera(self):
        self.running = False
        self.camera_ready = False
        if self.camera is not None:
            self.camera.release()
            self.camera = None
        self.camera_label.config(text="Initializing camera...")
        self.register_button.config(state=tk.DISABLED)

    def update_camera(self):
        while self.running:
            if self.camera is not None:
                ret, frame = self.camera.read()
                if ret:
                    if self.frame_queue.full():
                        self.frame_queue.get()
                    self.frame_queue.put(frame)
                    if not self.camera_ready:
                        self.camera_ready = True
                    time.sleep(0.03)  # Limit to about 30 fps

    def show_frame(self):
        if not self.frame_queue.empty():
            frame = self.frame_queue.get()
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=img)
            self.camera_label.imgtk = imgtk
            self.camera_label.configure(image=imgtk)
        if self.running:
            self.controller.after(10, self.show_frame)

    def register_face(self):
        name = self.name_entry.get().strip()
        if name == "":
            messagebox.showerror("Error", "Please enter a valid name")
            return

        if not self.frame_queue.empty():
            frame = self.frame_queue.get()
            if not os.path.exists("registered_faces"):
                os.makedirs("registered_faces")

            file_path = f"registered_faces/{name}.jpg"
            cv2.imwrite(file_path, frame)

            try:
                # Extract face encodings
                DeepFace.represent(file_path, model_name="Facenet")
                messagebox.showinfo("Success", f"Face registered for {name}")
                self.stop_camera()
                self.controller.show_frame("LoginPage")
            except Exception as e:
                messagebox.showerror("Error", f"Registration failed: {str(e)}")
        else:
            messagebox.showerror("Error", "Kindly move closer to the camera such that your face covers majority of the camera frame.")


class AuthenticationPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg='black')

        self.label = tk.Label(self, text="SCANNING...", font=controller.title_font, fg="yellow", bg="black")
        self.label.pack(side="top", fill="x", pady=10)

        self.loader_label = tk.Label(self, text="⏳", font=("Arial", 48), fg="yellow", bg="black")
        self.loader_label.pack(pady=20)

        self.camera = None
        self.frame_queue = queue.Queue(maxsize=1)
        self.running = False

    def start_camera(self):
        self.camera = cv2.VideoCapture(0)
        self.running = True
        threading.Thread(target=self.update_camera, daemon=True).start()
        self.animate_loader()
        self.controller.after(2000, self.start_authentication)  # Start authentication after 2 seconds

    def animate_loader(self):
        if self.running:
            current_text = self.loader_label.cget("text")
            new_text = "⏳" if current_text == "⌛" else "⌛"
            self.loader_label.config(text=new_text)
            self.controller.after(500, self.animate_loader)

    def stop_camera(self):
        self.running = False
        if self.camera is not None:
            self.camera.release()
            self.camera = None

    def update_camera(self):
        while self.running:
            if self.camera is not None:
                ret, frame = self.camera.read()
                if ret:
                    self.frame_queue.put(frame)
                    time.sleep(0.03)  # Limit to about 30 fps

    def start_authentication(self):
        if not self.frame_queue.empty():
            frame = self.frame_queue.get()
            self.authenticate_face(frame)
        else:
            self.controller.after(100, self.start_authentication)

    def authenticate_face(self, frame):
        try:
            # Save the current frame temporarily
            temp_file = "temp_auth.jpg"
            cv2.imwrite(temp_file, frame)

            # Compare with registered faces
            result = DeepFace.find(img_path=temp_file, db_path="registered_faces", model_name="Facenet")

            if not result[0].empty:
                # Authentication successful
                self.auth_success(result[0].iloc[0]['identity'].split('/')[-1].split('.')[0])
            else:
                # Face not recognized
                self.auth_failure()

            # Remove temporary file
            os.remove(temp_file)

        except Exception as e:
            print(f"Authentication error: {str(e)}")
            self.auth_failure()

    def auth_success(self, name):
        self.stop_camera()
        self.label.config(text=f"ACCESS GRANTED: Welcome, {name}", fg="green")
        self.loader_label.config(text="✅")
        self.controller.after(1000, lambda: self.controller.show_frame("SecureAreaPage", user=name))

    def auth_failure(self):
        self.stop_camera()
        self.label.config(text="ACCESS DENIED", fg="red")
        self.loader_label.config(text="❌")
        self.controller.after(2000, lambda: self.controller.show_frame("LoginPage"))


class SecureAreaPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg='black')

        self.welcome_label = tk.Label(self, text="WELCOME AGENT!!\nTOP SECRET TERMINAL", font=controller.title_font,
                                      fg="red", bg="black")
        self.welcome_label.pack(side="top", fill="x", pady=10)

        self.info = tk.Text(self, height=10, width=50, font=controller.normal_font, bg="black", fg="green")
        self.info.pack(pady=20)
        self.info.insert(tk.END, "This terminal contains classified information.\n\nProceed with caution.")
        self.info.config(state=tk.DISABLED)

        button = tk.Button(self, text="LOG OUT",
                           command=self.logout,
                           font=controller.normal_font, bg="red", fg="white")
        button.pack(pady=20)

    def update_welcome_message(self, agent_name):
        # Extract only the agent name from the file path
        agent_name = os.path.splitext(os.path.basename(agent_name))[0]

        self.welcome_label.config(text=f"WELCOME AGENT {agent_name}!!\nTOP SECRET TERMINAL")
        self.info.config(state=tk.NORMAL)
        self.info.delete(1.0, tk.END)
        self.info.insert(tk.END,
                         f"Welcome, Agent {agent_name}.\n\nThis terminal contains classified information.\n\nProceed with caution.")
        self.info.config(state=tk.DISABLED)

    def logout(self):
        self.controller.current_user = None
        self.controller.show_frame("LoginPage")


if __name__ == "__main__":
    app = SecretGovApp()
    app.geometry("800x600")
    app.mainloop()
