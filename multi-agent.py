import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
from groq import Groq
import threading
import json
import os
from datetime import datetime
import re
from typing import Dict, List, Optional
import hashlib
import base64

class ModernAIProcessor:
    def __init__(self):
        # Configuration
        self.config = {
            "api_key": "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",
            "model1": "gemma2-9b-it",  # تحلیل اولیه
            "model2": "meta-llama/llama-4-scout-17b-16e-instruct",  # پاسخ نهایی
            "temperature": 0.7,
            "max_tokens": 1024,
            "top_p": 0.9
        }
        
        # Initialize Groq client
        self.client = Groq(api_key=self.config["api_key"])
        
        # Processing state
        self.is_processing = False
        self.current_task = None
        
        # History
        self.history = []
        self.max_history = 50
        
        # Setup GUI
        self.setup_gui()
        
        # Load history
        self.load_history()
        
    def setup_gui(self):
        """Setup modern GUI with advanced features"""
        # Main window
        self.root = ttkb.Window(themename="cyborg")
        self.root.title("🤖 Modern AI Response Processor")
        self.root.geometry("1200x800")
        self.root.minsize(800, 600)
        
        # Configure grid weights
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        # Main container with padding
        self.main_container = ttk.Frame(self.root, padding=20)
        self.main_container.grid(row=0, column=0, sticky="nsew")
        self.main_container.grid_rowconfigure(1, weight=1)
        self.main_container.grid_columnconfigure(0, weight=1)
        
        # Header
        self.create_header()
        
        # Main content area
        self.create_main_content()
        
        # Footer with status
        self.create_footer()
        
        # Bind events
        self.bind_events()
        
    def create_header(self):
        """Create modern header with title and controls"""
        header_frame = ttk.Frame(self.main_container)
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        header_frame.grid_columnconfigure(1, weight=1)
        
        # Title with icon
        title_frame = ttk.Frame(header_frame)
        title_frame.grid(row=0, column=0, sticky="w")
        
        title_label = ttk.Label(
            title_frame, 
            text="🤖 AI Response Processor", 
            font=("Segoe UI", 24, "bold"),
            bootstyle="primary"
        )
        title_label.pack(side="left")
        
        subtitle_label = ttk.Label(
            title_frame,
            text="Advanced dual-model processing system",
            font=("Segoe UI", 10),
            bootstyle="secondary"
        )
        subtitle_label.pack(side="left", padx=(10, 0))
        
        # Control buttons
        controls_frame = ttk.Frame(header_frame)
        controls_frame.grid(row=0, column=1, sticky="e")
        
        ttk.Button(
            controls_frame,
            text="⚙️ Settings",
            command=self.open_settings,
            bootstyle="outline-secondary",
            width=12
        ).pack(side="right", padx=5)
        
        ttk.Button(
            controls_frame,
            text="📁 History",
            command=self.show_history,
            bootstyle="outline-info",
            width=12
        ).pack(side="right", padx=5)
        
        ttk.Button(
            controls_frame,
            text="💾 Save",
            command=self.save_results,
            bootstyle="outline-success",
            width=12
        ).pack(side="right", padx=5)
        
    def create_main_content(self):
        """Create main content area with modern layout"""
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.main_container)
        self.notebook.grid(row=1, column=0, sticky="nsew")
        
        # Main processing tab
        self.create_processing_tab()
        
        # Settings tab
        self.create_settings_tab()
        
    def create_processing_tab(self):
        """Create main processing interface"""
        # Main tab frame
        main_tab = ttk.Frame(self.notebook, padding=20)
        self.notebook.add(main_tab, text="🚀 Processing")
        
        # Configure grid
        main_tab.grid_rowconfigure(1, weight=1)
        main_tab.grid_rowconfigure(3, weight=1)
        main_tab.grid_rowconfigure(5, weight=1)
        main_tab.grid_columnconfigure(0, weight=1)
        
        # Input section
        self.create_input_section(main_tab)
        
        # Process button and progress
        self.create_process_section(main_tab)
        
        # Results sections
        self.create_results_sections(main_tab)
        
    def create_input_section(self, parent):
        """Create input section with modern styling"""
        # Input label with counter
        input_header = ttk.Frame(parent)
        input_header.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        input_header.grid_columnconfigure(1, weight=1)
        
        ttk.Label(
            input_header,
            text="📝 Your Input:",
            font=("Segoe UI", 14, "bold")
        ).grid(row=0, column=0, sticky="w")
        
        self.char_counter = ttk.Label(
            input_header,
            text="0 characters",
            font=("Segoe UI", 10),
            bootstyle="secondary"
        )
        self.char_counter.grid(row=0, column=1, sticky="e")
        
        # Input text area with frame
        input_frame = ttk.LabelFrame(parent, text="Enter your text here", padding=10)
        input_frame.grid(row=1, column=0, sticky="nsew", pady=(0, 15))
        input_frame.grid_rowconfigure(0, weight=1)
        input_frame.grid_columnconfigure(0, weight=1)
        
        # Text widget with scrollbar
        text_frame = ttk.Frame(input_frame)
        text_frame.grid(row=0, column=0, sticky="nsew")
        text_frame.grid_rowconfigure(0, weight=1)
        text_frame.grid_columnconfigure(0, weight=1)
        
        self.input_text = tk.Text(
            text_frame,
            wrap="word",
            font=("Consolas", 11),
            bg="#2b2b2b",
            fg="#ffffff",
            insertbackground="white",
            selectbackground="#404040",
            relief="flat",
            borderwidth=0
        )
        self.input_text.grid(row=0, column=0, sticky="nsew")
        
        input_scrollbar = ttk.Scrollbar(text_frame, orient="vertical", command=self.input_text.yview)
        input_scrollbar.grid(row=0, column=1, sticky="ns")
        self.input_text.config(yscrollcommand=input_scrollbar.set)
        
        # Input controls
        input_controls = ttk.Frame(input_frame)
        input_controls.grid(row=1, column=0, sticky="ew", pady=(10, 0))
        
        ttk.Button(
            input_controls,
            text="🗑️ Clear",
            command=self.clear_input,
            bootstyle="outline-danger",
            width=10
        ).pack(side="left")
        
        ttk.Button(
            input_controls,
            text="📋 Paste",
            command=self.paste_text,
            bootstyle="outline-secondary",
            width=10
        ).pack(side="left", padx=5)
        
        ttk.Button(
            input_controls,
            text="📁 Load File",
            command=self.load_file,
            bootstyle="outline-info",
            width=10
        ).pack(side="right")
        
    def create_process_section(self, parent):
        """Create processing controls section"""
        process_frame = ttk.Frame(parent)
        process_frame.grid(row=2, column=0, sticky="ew", pady=15)
        process_frame.grid_columnconfigure(1, weight=1)
        
        # Process button
        self.process_btn = ttk.Button(
            process_frame,
            text="🚀 Process Text",
            command=self.process_input,
            bootstyle="success",
            width=20
        )
        self.process_btn.grid(row=0, column=0, padx=(0, 20))
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            process_frame,
            variable=self.progress_var,
            mode="determinate",
            bootstyle="success-striped"
        )
        self.progress_bar.grid(row=0, column=1, sticky="ew")
        
        # Status label
        self.status_label = ttk.Label(
            process_frame,
            text="Ready to process",
            font=("Segoe UI", 10),
            bootstyle="secondary"
        )
        self.status_label.grid(row=1, column=0, columnspan=2, pady=(5, 0))
        
    def create_results_sections(self, parent):
        """Create results display sections"""
        # Results container
        results_container = ttk.Frame(parent)
        results_container.grid(row=3, column=0, sticky="nsew", pady=(15, 0))
        results_container.grid_rowconfigure(0, weight=1)
        results_container.grid_columnconfigure(0, weight=1)
        results_container.grid_columnconfigure(1, weight=1)
        
        # Model 1 results (Gemma - Analysis)
        self.create_result_section(
            results_container, 
            "🔍 Analysis (Gemma)", 
            0, 0, 
            "analysis_output"
        )
        
        # Model 2 results (LLaMA - Final Response)
        self.create_result_section(
            results_container, 
            "✨ Final Response (LLaMA)", 
            0, 1, 
            "final_output"
        )
        
    def create_result_section(self, parent, title, row, col, attr_name):
        """Create a result display section"""
        # Result frame
        result_frame = ttk.LabelFrame(parent, text=title, padding=10)
        result_frame.grid(row=row, column=col, sticky="nsew", padx=5)
        result_frame.grid_rowconfigure(0, weight=1)
        result_frame.grid_columnconfigure(0, weight=1)
        
        # Text widget with scrollbar
        text_frame = ttk.Frame(result_frame)
        text_frame.grid(row=0, column=0, sticky="nsew")
        text_frame.grid_rowconfigure(0, weight=1)
        text_frame.grid_columnconfigure(0, weight=1)
        
        text_widget = tk.Text(
            text_frame,
            wrap="word",
            font=("Segoe UI", 10),
            bg="#1a1a1a",
            fg="#ffffff",
            insertbackground="white",
            selectbackground="#404040",
            relief="flat",
            borderwidth=0,
            state="disabled"
        )
        text_widget.grid(row=0, column=0, sticky="nsew")
        
        scrollbar = ttk.Scrollbar(text_frame, orient="vertical", command=text_widget.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        text_widget.config(yscrollcommand=scrollbar.set)
        
        # Controls
        controls_frame = ttk.Frame(result_frame)
        controls_frame.grid(row=1, column=0, sticky="ew", pady=(10, 0))
        
        ttk.Button(
            controls_frame,
            text="📋 Copy",
            command=lambda: self.copy_text(text_widget),
            bootstyle="outline-primary",
            width=10
        ).pack(side="left")
        
        ttk.Button(
            controls_frame,
            text="💾 Save",
            command=lambda: self.save_text(text_widget),
            bootstyle="outline-success",
            width=10
        ).pack(side="left", padx=5)
        
        # Store reference
        setattr(self, attr_name, text_widget)
        
    def create_settings_tab(self):
        """Create settings tab"""
        settings_tab = ttk.Frame(self.notebook, padding=20)
        self.notebook.add(settings_tab, text="⚙️ Settings")
        
        # Model settings
        model_frame = ttk.LabelFrame(settings_tab, text="Model Configuration", padding=15)
        model_frame.pack(fill="x", pady=(0, 20))
        
        # Temperature setting
        ttk.Label(model_frame, text="Temperature (0.0-2.0):").grid(row=0, column=0, sticky="w", pady=5)
        self.temp_var = tk.DoubleVar(value=self.config["temperature"])
        temp_scale = ttk.Scale(
            model_frame, 
            from_=0.0, 
            to=2.0, 
            variable=self.temp_var, 
            orient="horizontal",
            length=200
        )
        temp_scale.grid(row=0, column=1, sticky="ew", padx=10)
        self.temp_label = ttk.Label(model_frame, text=f"{self.config['temperature']:.1f}")
        self.temp_label.grid(row=0, column=2)
        
        # Max tokens
        ttk.Label(model_frame, text="Max Tokens:").grid(row=1, column=0, sticky="w", pady=5)
        self.tokens_var = tk.IntVar(value=self.config["max_tokens"])
        tokens_spin = ttk.Spinbox(
            model_frame, 
            from_=100, 
            to=4000, 
            textvariable=self.tokens_var,
            width=10
        )
        tokens_spin.grid(row=1, column=1, sticky="w", padx=10)
        
        # Update temperature label
        self.temp_var.trace('w', lambda *args: self.temp_label.config(text=f"{self.temp_var.get():.1f}"))
        
        # API Settings
        api_frame = ttk.LabelFrame(settings_tab, text="API Configuration", padding=15)
        api_frame.pack(fill="x", pady=(0, 20))
        
        ttk.Label(api_frame, text="API Key:").grid(row=0, column=0, sticky="w", pady=5)
        self.api_key_var = tk.StringVar(value="*" * 20 + self.config["api_key"][-8:])
        api_entry = ttk.Entry(api_frame, textvariable=self.api_key_var, show="*", width=50)
        api_entry.grid(row=0, column=1, sticky="ew", padx=10)
        
        # Save settings button
        ttk.Button(
            settings_tab,
            text="💾 Save Settings",
            command=self.save_settings,
            bootstyle="success"
        ).pack(pady=20)
        
    def create_footer(self):
        """Create footer with status information"""
        footer_frame = ttk.Frame(self.main_container)
        footer_frame.grid(row=2, column=0, sticky="ew", pady=(20, 0))
        footer_frame.grid_columnconfigure(1, weight=1)
        
        # Connection status
        self.connection_status = ttk.Label(
            footer_frame,
            text="🟢 Connected",
            font=("Segoe UI", 9),
            bootstyle="success"
        )
        self.connection_status.grid(row=0, column=0, sticky="w")
        
        # Version info
        version_label = ttk.Label(
            footer_frame,
            text="v2.0 | Modern AI Processor",
            font=("Segoe UI", 9),
            bootstyle="secondary"
        )
        version_label.grid(row=0, column=1, sticky="e")
        
    def bind_events(self):
        """Bind keyboard and mouse events"""
        self.input_text.bind('<KeyRelease>', self.update_char_counter)
        self.input_text.bind('<Control-Return>', lambda e: self.process_input())
        
        # Bind window close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def update_char_counter(self, event=None):
        """Update character counter"""
        content = self.input_text.get("1.0", tk.END).strip()
        char_count = len(content)
        word_count = len(content.split()) if content else 0
        
        self.char_counter.config(text=f"{char_count} chars | {word_count} words")
        
    def clear_input(self):
        """Clear input text"""
        self.input_text.delete("1.0", tk.END)
        self.update_char_counter()
        
    def paste_text(self):
        """Paste text from clipboard"""
        try:
            clipboard_text = self.root.clipboard_get()
            self.input_text.insert(tk.INSERT, clipboard_text)
            self.update_char_counter()
        except tk.TclError:
            messagebox.showwarning("Warning", "Clipboard is empty or contains non-text data")
            
    def load_file(self):
        """Load text from file"""
        file_path = filedialog.askopenfilename(
            title="Select Text File",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    self.input_text.delete("1.0", tk.END)
                    self.input_text.insert("1.0", content)
                    self.update_char_counter()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load file: {str(e)}")
                
    def copy_text(self, text_widget):
        """Copy text from widget to clipboard"""
        content = text_widget.get("1.0", tk.END).strip()
        if content:
            self.root.clipboard_clear()
            self.root.clipboard_append(content)
            messagebox.showinfo("Success", "Text copied to clipboard!")
        else:
            messagebox.showwarning("Warning", "No text to copy")
            
    def save_text(self, text_widget):
        """Save text from widget to file"""
        content = text_widget.get("1.0", tk.END).strip()
        if not content:
            messagebox.showwarning("Warning", "No text to save")
            return
            
        file_path = filedialog.asksaveasfilename(
            title="Save Text",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(content)
                messagebox.showinfo("Success", "Text saved successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file: {str(e)}")
                
    def call_groq_model(self, model: str, messages: List[Dict], progress_callback=None) -> str:
        """Call Groq model with error handling"""
        try:
            if progress_callback:
                progress_callback(10, f"Connecting to {model}...")
                
            completion = self.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=self.config["temperature"],
                max_tokens=self.config["max_tokens"],
                top_p=self.config["top_p"],
                stream=False
            )
            
            if progress_callback:
                progress_callback(90, f"Processing response from {model}...")
                
            return completion.choices[0].message.content
            
        except Exception as e:
            error_msg = f"Error with {model}: {str(e)}"
            if progress_callback:
                progress_callback(0, error_msg)
            return error_msg
            
    def process_input(self):
        """Process input with modern UI feedback"""
        if self.is_processing:
            messagebox.showwarning("Warning", "Processing already in progress!")
            return
            
        user_input = self.input_text.get("1.0", tk.END).strip()
        if not user_input:
            messagebox.showwarning("Warning", "Please enter some text to process!")
            return
            
        # Validate input
        if len(user_input) < 10:
            messagebox.showwarning("Warning", "Please enter at least 10 characters!")
            return
            
        # Start processing
        self.is_processing = True
        self.process_btn.config(state="disabled", text="🔄 Processing...")
        self.progress_var.set(0)
        
        # Clear previous results
        self.clear_output(self.analysis_output)
        self.clear_output(self.final_output)
        
        # Start processing thread
        self.current_task = threading.Thread(target=self.run_models, args=(user_input,), daemon=True)
        self.current_task.start()
        
    def run_models(self, user_input: str):
        """Run both models sequentially with progress updates"""
        try:
            # Model 1: Gemma for analysis
            def update_progress_1(progress, status):
                self.root.after(0, lambda: self.update_ui_progress(progress, status))
                
            update_progress_1(5, "Starting analysis with Gemma...")
            
            model1_messages = [
                {
                    "role": "system", 
                    "content": "You are an expert analyst. Analyze the user's input thoroughly, identify key themes, extract important information, and provide structured insights that will help generate a comprehensive response."
                },
                {"role": "user", "content": user_input}
            ]
            
            model1_response = self.call_groq_model("gemma2-9b-it", model1_messages, update_progress_1)
            
            # Update UI with first model result
            self.root.after(0, lambda: self.update_output(self.analysis_output, model1_response))
            self.root.after(0, lambda: self.update_ui_progress(50, "Analysis complete. Generating final response..."))
            
            # Model 2: LLaMA for final response
            def update_progress_2(progress, status):
                final_progress = 50 + (progress * 0.5)
                self.root.after(0, lambda: self.update_ui_progress(final_progress, status))
                
            model2_messages = [
                {
                    "role": "system", 
                    "content": "You are a skilled communicator who creates comprehensive, well-structured responses. Based on the analysis provided, generate a detailed, helpful, and engaging final response to the user's original query."
                },
                {
                    "role": "user", 
                    "content": f"Original Query: {user_input}\n\nAnalysis: {model1_response}\n\nPlease provide a comprehensive final response based on this analysis."
                }
            ]
            
            model2_response = self.call_groq_model("meta-llama/llama-4-scout-17b-16e-instruct", model2_messages, update_progress_2)
            
            # Update UI with final result
            self.root.after(0, lambda: self.update_output(self.final_output, model2_response))
            self.root.after(0, lambda: self.complete_processing())
            
            # Save to history
            self.add_to_history(user_input, model1_response, model2_response)
            
        except Exception as e:
            error_msg = f"Processing error: {str(e)}"
            self.root.after(0, lambda: self.handle_processing_error(error_msg))
            
    def update_ui_progress(self, progress: float, status: str):
        """Update progress bar and status"""
        self.progress_var.set(progress)
        self.status_label.config(text=status)
        
    def update_output(self, text_widget, content: str):
        """Update output text widget"""
        text_widget.config(state="normal")
        text_widget.delete("1.0", tk.END)
        text_widget.insert("1.0", content)
        text_widget.config(state="disabled")
        
    def clear_output(self, text_widget):
        """Clear output text widget"""
        text_widget.config(state="normal")
        text_widget.delete("1.0", tk.END)
        text_widget.insert("1.0", "Processing...")
        text_widget.config(state="disabled")
        
    def complete_processing(self):
        """Complete processing and reset UI"""
        self.is_processing = False
        self.process_btn.config(state="normal", text="🚀 Process Text")
        self.progress_var.set(100)
        self.status_label.config(text="✅ Processing completed successfully!")
        
        # Auto-clear status after 3 seconds
        self.root.after(3000, lambda: self.status_label.config(text="Ready to process"))
        
    def handle_processing_error(self, error_msg: str):
        """Handle processing errors"""
        self.is_processing = False
        self.process_btn.config(state="normal", text="🚀 Process Text")
        self.progress_var.set(0)
        self.status_label.config(text="❌ Processing failed")
        
        messagebox.showerror("Processing Error", error_msg)
        
    def add_to_history(self, input_text: str, analysis: str, response: str):
        """Add result to history"""
        history_item = {
            "timestamp": datetime.now().isoformat(),
            "input": input_text[:100] + "..." if len(input_text) > 100 else input_text,
            "analysis": analysis,
            "response": response
        }
        
        self.history.insert(0, history_item)
        
        # Limit history size
        if len(self.history) > self.max_history:
            self.history = self.history[:self.max_history]
            
        self.save_history()
        
    def save_history(self):
        """Save history to file"""
        try:
            with open("ai_processor_history.json", "w", encoding="utf-8") as f:
                json.dump(self.history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Failed to save history: {e}")
            
    def load_history(self):
        """Load history from file"""
        try:
            if os.path.exists("ai_processor_history.json"):
                with open("ai_processor_history.json", "r", encoding="utf-8") as f:
                    self.history = json.load(f)
        except Exception as e:
            print(f"Failed to load history: {e}")
            self.history = []
            
    def show_history(self):
        """Show history window"""
        if not self.history:
            messagebox.showinfo("History", "No history available yet!")
            return
            
        # Create history window
        history_window = tk.Toplevel(self.root)
        history_window.title("📜 Processing History")
        history_window.geometry("800x600")
        history_window.transient(self.root)
        history_window.grab_set()
        
        # Configure grid
        history_window.grid_rowconfigure(0, weight=1)
        history_window.grid_columnconfigure(0, weight=1)
        
        # Main frame
        main_frame = ttk.Frame(history_window, padding=20)
        main_frame.grid(row=0, column=0, sticky="nsew")
        main_frame.grid_rowconfigure(1, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        
        # Title
        ttk.Label(
            main_frame, 
            text="📜 Processing History", 
            font=("Segoe UI", 16, "bold")
        ).grid(row=0, column=0, pady=(0, 15))
        
        # History list with scrollbar
        list_frame = ttk.Frame(main_frame)
        list_frame.grid(row=1, column=0, sticky="nsew")
        list_frame.grid_rowconfigure(0, weight=1)
        list_frame.grid_columnconfigure(0, weight=1)
        
        # Treeview for history
        columns = ("timestamp", "input_preview")
        history_tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=15)
        
        history_tree.heading("timestamp", text="Time")
        history_tree.heading("input_preview", text="Input Preview")
        
        history_tree.column("timestamp", width=150)
        history_tree.column("input_preview", width=500)
        
        # Populate history
        for i, item in enumerate(self.history):
            timestamp = datetime.fromisoformat(item["timestamp"]).strftime("%Y-%m-%d %H:%M")
            history_tree.insert("", "end", values=(timestamp, item["input"]))
        
        history_tree.grid(row=0, column=0, sticky="nsew")
        
        # Scrollbar for history
        history_scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=history_tree.yview)
        history_scrollbar.grid(row=0, column=1, sticky="ns")
        history_tree.config(yscrollcommand=history_scrollbar.set)
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, pady=(15, 0))
        
        def load_selected():
            selection = history_tree.selection()
            if selection:
                item_id = history_tree.index(selection[0])
                history_item = self.history[item_id]
                
                # Load to input
                self.input_text.delete("1.0", tk.END)
                self.input_text.insert("1.0", history_item["input"])
                self.update_char_counter()
                
                # Load results
                self.update_output(self.analysis_output, history_item["analysis"])
                self.update_output(self.final_output, history_item["response"])
                
                history_window.destroy()
                messagebox.showinfo("Success", "History item loaded successfully!")
            else:
                messagebox.showwarning("Warning", "Please select a history item first!")
        
        def clear_history():
            if messagebox.askyesno("Confirm", "Are you sure you want to clear all history?"):
                self.history = []
                self.save_history()
                history_window.destroy()
                messagebox.showinfo("Success", "History cleared successfully!")
        
        ttk.Button(
            button_frame, 
            text="📥 Load Selected", 
            command=load_selected,
            bootstyle="primary"
        ).pack(side="left", padx=5)
        
        ttk.Button(
            button_frame, 
            text="🗑️ Clear History", 
            command=clear_history,
            bootstyle="danger"
        ).pack(side="left", padx=5)
        
        ttk.Button(
            button_frame, 
            text="❌ Close", 
            command=history_window.destroy,
            bootstyle="secondary"
        ).pack(side="right", padx=5)
        
    def open_settings(self):
        """Open settings window"""
        self.notebook.select(1)  # Switch to settings tab
        
    def save_settings(self):
        """Save current settings"""
        try:
            # Update config
            self.config["temperature"] = self.temp_var.get()
            self.config["max_tokens"] = self.tokens_var.get()
            
            # Save to file
            config_file = "ai_processor_config.json"
            with open(config_file, "w") as f:
                # Don't save API key to file for security
                config_to_save = self.config.copy()
                del config_to_save["api_key"]
                json.dump(config_to_save, f, indent=2)
            
            messagebox.showinfo("Success", "Settings saved successfully!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save settings: {str(e)}")
            
    def load_settings(self):
        """Load settings from file"""
        try:
            config_file = "ai_processor_config.json"
            if os.path.exists(config_file):
                with open(config_file, "r") as f:
                    loaded_config = json.load(f)
                    self.config.update(loaded_config)
                    
                # Update UI
                self.temp_var.set(self.config["temperature"])
                self.tokens_var.set(self.config["max_tokens"])
                
        except Exception as e:
            print(f"Failed to load settings: {e}")
            
    def save_results(self):
        """Save current results to file"""
        analysis = self.analysis_output.get("1.0", tk.END).strip()
        response = self.final_output.get("1.0", tk.END).strip()
        
        if not analysis and not response:
            messagebox.showwarning("Warning", "No results to save!")
            return
            
        file_path = filedialog.asksaveasfilename(
            title="Save Results",
            defaultextension=".txt",
            filetypes=[
                ("Text files", "*.txt"),
                ("JSON files", "*.json"),
                ("All files", "*.*")
            ]
        )
        
        if file_path:
            try:
                if file_path.endswith('.json'):
                    # Save as JSON
                    results = {
                        "timestamp": datetime.now().isoformat(),
                        "input": self.input_text.get("1.0", tk.END).strip(),
                        "analysis": analysis,
                        "final_response": response
                    }
                    with open(file_path, 'w', encoding='utf-8') as f:
                        json.dump(results, f, ensure_ascii=False, indent=2)
                else:
                    # Save as text
                    content = f"""AI PROCESSING RESULTS
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

INPUT:
{self.input_text.get("1.0", tk.END).strip()}

ANALYSIS (Gemma):
{analysis}

FINAL RESPONSE (LLaMA):
{response}
"""
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                        
                messagebox.showinfo("Success", "Results saved successfully!")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save results: {str(e)}")
                
    def validate_input(self, text: str) -> bool:
        """Validate input text"""
        if not text.strip():
            return False
            
        # Check for minimum length
        if len(text.strip()) < 10:
            return False
            
        # Check for maximum length (to prevent API limits)
        if len(text) > 8000:
            messagebox.showwarning(
                "Warning", 
                "Input is too long. Please limit to 8000 characters."
            )
            return False
            
        return True
        
    def check_api_connection(self):
        """Check API connection status"""
        try:
            # Simple test call
            test_messages = [
                {"role": "user", "content": "Hello"}
            ]
            
            response = self.client.chat.completions.create(
                model="gemma2-9b-it",
                messages=test_messages,
                max_tokens=10,
                temperature=0.1
            )
            
            self.connection_status.config(text="🟢 Connected", bootstyle="success")
            return True
            
        except Exception as e:
            self.connection_status.config(text="🔴 Disconnected", bootstyle="danger")
            return False
            
    def on_closing(self):
        """Handle window closing"""
        if self.is_processing:
            if messagebox.askyesno("Confirm", "Processing is in progress. Are you sure you want to exit?"):
                self.root.destroy()
        else:
            self.root.destroy()
            
    def run(self):
        """Start the application"""
        # Load settings
        self.load_settings()
        
        # Check connection
        self.root.after(1000, self.check_api_connection)
        
        # Start main loop
        self.root.mainloop()


# Main execution
if __name__ == "__main__":
    try:
        app = ModernAIProcessor()
        app.run()
    except Exception as e:
        print(f"Application error: {e}")
        messagebox.showerror("Error", f"Failed to start application: {str(e)}")