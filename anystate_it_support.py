import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import datetime
import os
import getpass
import boto3
import threading

class ChatMessage:
    def __init__(self, sender_name, message, is_user=False):
        self.sender_name = sender_name
        self.message = message
        self.timestamp = datetime.datetime.now().strftime("%I:%M %p")
        self.is_user = is_user

class CallbackDialog(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title("Request Callback")
        self.geometry("350x150")
        self.resizable(False, False)
        self.phone_number = None
        self.result = False
        
        # Center window
        self.transient(parent)
        self.grab_set()
        
        # Create widgets
        tk.Label(self, text="Please enter your phone number for a callback:").pack(pady=(10, 5))
        self.phone_entry = tk.Entry(self, width=30)
        self.phone_entry.pack(pady=5)
        
        # Buttons
        button_frame = tk.Frame(self)
        button_frame.pack(pady=10, side=tk.BOTTOM, fill=tk.X)
        
        tk.Button(button_frame, text="Cancel", width=10, command=self.cancel).pack(side=tk.RIGHT, padx=5)
        tk.Button(button_frame, text="Request", width=10, command=self.request).pack(side=tk.RIGHT, padx=5)
        
        # Wait for window to be closed
        self.wait_window()
    
    def request(self):
        if not self.phone_entry.get().strip():
            messagebox.showwarning("Invalid Input", "Please enter a valid phone number.")
            return
        
        self.phone_number = self.phone_entry.get().strip()
        self.result = True
        self.destroy()
    
    def cancel(self):
        self.destroy()

class AnyStateITSupport:
    def __init__(self, root):
        self.root = root
        self.root.title("AnyState IT Support")
        self.root.geometry("400x600")
        self.root.minsize(400, 500)
        
        # User info
        self.current_user = self.get_current_user()
        self.is_connected_to_live_agent = False
        
        # Initialize AWS Connect client (in production)
        # self.connect_client = boto3.client('connect')
        # self.participant_client = boto3.client('connectparticipant')
        
        # Create UI
        self.create_ui()
        
        # Add welcome message
        self.add_system_message("Welcome to AnyState IT Support. How can I help you today?")
    
    def get_current_user(self):
        # In a real Windows app, this would use Windows authentication
        # For this demo, we'll use the system username
        return getpass.getuser()
    
    def create_ui(self):
        # Main layout
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        
        # Header
        header_frame = tk.Frame(self.root, bg="#003366", padx=10, pady=10)
        header_frame.grid(row=0, column=0, sticky="ew")
        
        tk.Label(header_frame, text="AnyState IT Support", fg="white", bg="#003366", 
                 font=("Arial", 14, "bold")).pack(anchor="w")
        self.user_label = tk.Label(header_frame, text=f"Welcome, {self.current_user}", 
                                  fg="white", bg="#003366", font=("Arial", 10))
        self.user_label.pack(anchor="w", pady=(5, 0))
        
        # Chat area
        chat_frame = tk.Frame(self.root)
        chat_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        chat_frame.grid_columnconfigure(0, weight=1)
        chat_frame.grid_rowconfigure(0, weight=1)
        
        # Create canvas and scrollbar for chat messages
        self.chat_canvas = tk.Canvas(chat_frame, highlightthickness=0)
        scrollbar = ttk.Scrollbar(chat_frame, orient="vertical", command=self.chat_canvas.yview)
        self.chat_canvas.configure(yscrollcommand=scrollbar.set)
        
        self.chat_canvas.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        
        # Frame for messages inside canvas
        self.messages_frame = tk.Frame(self.chat_canvas)
        self.messages_frame.grid_columnconfigure(0, weight=1)
        
        # Create window in canvas for messages
        self.messages_window = self.chat_canvas.create_window((0, 0), window=self.messages_frame, anchor="nw", width=self.chat_canvas.winfo_width())
        
        # Input area
        input_frame = tk.Frame(self.root, padx=10, pady=10)
        input_frame.grid(row=2, column=0, sticky="ew")
        input_frame.grid_columnconfigure(0, weight=1)
        
        self.message_input = tk.Text(input_frame, height=3, width=30, wrap="word")
        self.message_input.grid(row=0, column=0, sticky="ew", padx=(0, 5))
        self.message_input.bind("<Return>", self.on_enter_key)
        
        send_button = tk.Button(input_frame, text="Send", bg="#0078D7", fg="white", 
                               command=self.send_message, width=10)
        send_button.grid(row=0, column=1, sticky="ns")
        
        # Buttons for live agent and callback
        buttons_frame = tk.Frame(input_frame)
        buttons_frame.grid(row=1, column=0, columnspan=2, sticky="w", pady=(10, 0))
        
        self.live_agent_button = tk.Button(buttons_frame, text="Request Live Agent", 
                                         bg="#0078D7", fg="white", command=self.connect_to_live_agent)
        self.live_agent_button.pack(side=tk.LEFT, padx=(0, 10))
        
        callback_button = tk.Button(buttons_frame, text="Request Callback", 
                                   bg="#0078D7", fg="white", command=self.request_callback)
        callback_button.pack(side=tk.LEFT)
        
        # Configure canvas resize
        self.chat_canvas.bind('<Configure>', self.on_canvas_configure)
        self.messages_frame.bind('<Configure>', self.on_frame_configure)
    
    def on_canvas_configure(self, event):
        self.chat_canvas.itemconfig(self.messages_window, width=event.width)
    
    def on_frame_configure(self, event):
        self.chat_canvas.configure(scrollregion=self.chat_canvas.bbox("all"))
    
    def on_enter_key(self, event):
        # Send message on Enter key, allow Shift+Enter for new line
        if not event.state & 0x1:  # Shift not pressed
            self.send_message()
            return "break"  # Prevent default behavior
    
    def send_message(self):
        message = self.message_input.get("1.0", "end-1c").strip()
        if not message:
            return
        
        # Add user message to chat
        self.add_user_message(message)
        
        # Clear input
        self.message_input.delete("1.0", tk.END)
        
        # Process message
        if self.is_connected_to_live_agent:
            self.send_message_to_live_agent(message)
        else:
            self.process_with_ai(message)
    
    def add_message_bubble(self, message_obj):
        # Create frame for message
        frame = tk.Frame(self.messages_frame, padx=5, pady=5)
        frame.grid(row=len(frame.master.winfo_children()), column=0, sticky="ew", pady=5)
        
        # Set alignment and colors based on sender
        if message_obj.is_user:
            frame.grid_configure(sticky="e")
            bubble_color = "#DCF8C6"  # Light green for user
            text_anchor = "e"
        else:
            frame.grid_configure(sticky="w")
            bubble_color = "#F0F0F0"  # Light gray for system
            text_anchor = "w"
        
        # Create message bubble
        bubble = tk.Frame(frame, bg=bubble_color, padx=10, pady=5)
        bubble.pack(fill="x")
        
        # Add sender name
        sender_label = tk.Label(bubble, text=message_obj.sender_name, font=("Arial", 9, "bold"),
                              bg=bubble_color, anchor=text_anchor)
        sender_label.pack(fill="x")
        
        # Add message text
        message_label = tk.Label(bubble, text=message_obj.message, wraplength=250, 
                               justify=tk.LEFT, bg=bubble_color, anchor="w")
        message_label.pack(fill="x")
        
        # Add timestamp
        time_label = tk.Label(bubble, text=message_obj.timestamp, font=("Arial", 7),
                            bg=bubble_color, fg="gray")
        time_label.pack(anchor="e")
        
        # Scroll to bottom
        self.root.update_idletasks()
        self.chat_canvas.yview_moveto(1.0)
    
    def add_user_message(self, message):
        msg = ChatMessage(self.current_user, message, is_user=True)
        self.add_message_bubble(msg)
    
    def add_system_message(self, message):
        msg = ChatMessage("IT Support", message, is_user=False)
        self.add_message_bubble(msg)
    
    def process_with_ai(self, message):
        # Simulate AI processing
        # In a real implementation, this would call Amazon Lex or another AI service
        message_lower = message.lower()
        
        if "password reset" in message_lower:
            response = "To reset your password, please visit the self-service portal at https://reset.anystate.gov or call the IT helpdesk at 555-123-4567."
        elif "software" in message_lower or "install" in message_lower:
            response = "For software installation requests, please use the Software Request form in the Employee Portal. An IT technician will review and process your request."
        elif "vpn" in message_lower or "remote" in message_lower:
            response = "For VPN access or remote connectivity issues, please ensure you're using the latest AnyState VPN client. For installation instructions, visit https://vpn.anystate.gov"
        else:
            response = "I'm not sure I understand your question. Would you like to speak with a live IT support agent?"
        
        # Add AI response to chat
        self.add_system_message(response)
    
    def connect_to_live_agent(self):
        try:
            # In a real implementation, this would initiate a chat with Amazon Connect
            self.add_system_message("Connecting you to a live agent. Please wait a moment...")
            
            # Simulate connection delay
            def delayed_connection():
                # In production, this would be an async call to Amazon Connect
                self.is_connected_to_live_agent = True
                self.add_system_message("You are now connected with a live agent. Please note that live agent support is available Monday to Friday, 9 AM to 5 PM.")
                self.live_agent_button.config(state=tk.DISABLED)
            
            # Simulate delay with threading
            threading.Timer(1.5, delayed_connection).start()
            
        except Exception as ex:
            self.add_system_message(f"Error connecting to live agent: {str(ex)}")
            self.is_connected_to_live_agent = False
    
    def send_message_to_live_agent(self, message):
        # In a real implementation, this would send the message to Amazon Connect
        # For this demo, we'll simulate a response
        
        # Simulate agent typing delay
        self.add_system_message("Agent is typing...")
        
        # In production, this would be handled by the actual agent response
        def delayed_response():
            self.add_system_message("Thank you for your message. An IT support specialist will assist you shortly.")
        
        threading.Timer(2.0, delayed_response).start()
    
    def request_callback(self):
        dialog = CallbackDialog(self.root)
        if dialog.result:
            phone_number = dialog.phone_number
            
            # In a real implementation, this would schedule a callback via Amazon Connect
            self.add_system_message(f"A callback has been scheduled to {phone_number}. An IT support specialist will call you shortly during business hours (Monday to Friday, 9 AM to 5 PM).")

if __name__ == "__main__":
    root = tk.Tk()
    app = AnyStateITSupport(root)
    root.mainloop()