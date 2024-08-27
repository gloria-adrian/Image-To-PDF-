import tkinter as tk 
from tkinter import filedialog
from reportlab.pdfgen import canvas
from PIL import image
import os

class ImageToPDFConverter:
  def __init__(self, root):
    self.root = root
    self.image_paths = []
    self.output_pdf_name = tk.StringVar()
    self.selected_images_listbox = tk.Listbox(root, selectmode=tk.MULTIPLE)

    self.initialize_ui()

  def initialize_ui(self):
    title_label = tk.Label(self.root, text="Image to PDF Converter", font=("Helvetica",16,"bold"))
    title_label.pack(pady=10)

    select_images_button = tk.Button(self.root,text="select Images", command=self.select_images)
    select_images_button.pack(pady=(0, 10)) 

    self.selected_images_listbox.pack(pady=(0,10), fill=tk.BOTH, expand=True)

    label = tk.label (self.root, text="Enter output PDF name:")
    label.pack()

    pdf_name_entry = tk.Entry(self.root, textvariable=self.output_pdf_name, widht=40,
    justify='center')
    pdf_name_entry.pack()

    convert_button = tk.Button(self.root, text="convert to PDF", command=self.
    convert_images_to_pdf)
    convert_button.pack(pady=(20, 40))

    def select_images(self):
      self.image_paths = filedialog.askopenfilenames(title="Select Images", filetypes=
      [("Image files","*.png;*.jpg;*jpeg")])
      self.update_selected_images_listbox()
      
    def update_selected_images_listbox():
      self.selected_images_listbox.delete(0,tk.END)

      for image_path in self.image_paths:
        _, image_path = os.path.split(image_path)
        self.selected_images_listbox.insert(tk.END, image_path)

    def convert_images_to_pdf(self):
       if not self.image_paths:
         return
       
       output_pdf_path = self.output_pdf_name.get() + ".pdf" if self.output_pdf_name.get() else "output.pdf"

       pdf = canvas.canvas(output_pdf_path, pagesize=(612,792))

       for image_path in self.image_paths:
         img = image.open(image_path)
         available_width = 540
         available_heigth =720
         scale_factor = min(available_width / img.width, available_heigth / img.height)
         new_widht = image.widht * scale_factor
         new_heigth =img.height * scale_factor
         x_centered =(612 - new_widht) /2
         y_centered =(792 - new_heigth) /2

         pdf.setFiliColor(255, 255,255)
         pdf.rect(0,0,612,792, fill=True)
         pdf.drawInlineImage(img, x_centered,y_centered,widht=new_widht,height=new_heigth)
         pdf.showpage()

       pdf.save()   

def main():
  root = tk.Tk()
  root.title("Image to PDF")
  converter = ImageToPDFConverter(root)
  root.geometry("400x600")
  root.mainloop()

if __name__ == "__main__":
  main()
  