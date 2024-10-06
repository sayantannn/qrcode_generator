import docx
import pdfplumber
import pytesseract
from PIL import Image
from pdf2image import convert_from_path

# Helper function to read txt and docx files
def read_txt_file(file):
    try:
        content = file.read().decode("utf-8")
        # Clean up content (remove excessive line breaks and extra spaces)
        cleaned_text = ' '.join(content.split())
        cleaned_text = cleaned_text.replace(' .', '.')   # Fix spacing before periods
        cleaned_text = cleaned_text.replace(' ,', ',')   # Fix spacing before commas
        cleaned_text = cleaned_text.replace(' :', ':')   # Fix spacing before colons
        cleaned_text = cleaned_text.replace(' \n', '\n') # Clean up single newlines
        
        # Replace multiple spaces with a single space
        cleaned_text = ' '.join(cleaned_text.split())

        # Properly format paragraphs (double newlines to separate paragraphs)
        cleaned_text = cleaned_text.replace('\n\n\n', '\n\n')  # Replace excessive newlines with two newlines
        cleaned_text = cleaned_text.strip()  # Remove any leading/trailing spaces/newlines

        return cleaned_text
    except Exception as e:
        return f"Error reading .txt file: {str(e)}"

# Helper function to read .docx files
def read_docx_file(file):
    try:
        doc = docx.Document(file)
        full_text = [para.text.strip() for para in doc.paragraphs if para.text.strip()]  # Remove empty paragraphs
        cleaned_text = ' '.join(full_text)
        cleaned_text = cleaned_text.replace(' .', '.')   # Fix spacing before periods
        cleaned_text = cleaned_text.replace(' ,', ',')   # Fix spacing before commas
        cleaned_text = cleaned_text.replace(' :', ':')   # Fix spacing before colons
        cleaned_text = cleaned_text.replace(' \n', '\n') # Clean up single newlines
        
        # Replace multiple spaces with a single space
        cleaned_text = ' '.join(cleaned_text.split())

        # Properly format paragraphs (double newlines to separate paragraphs)
        cleaned_text = cleaned_text.replace('\n\n\n', '\n\n')  # Replace excessive newlines with two newlines
        cleaned_text = cleaned_text.strip()  # Remove any leading/trailing spaces/newlines

        return cleaned_text
    except Exception as e:
        return f"Error reading .docx file: {str(e)}"

# Helper function to read .pdf files (non-image PDFs)
def read_pdf_file(file):
    full_text = []
    try:
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    full_text.append(page_text.strip())  # Strip unnecessary spaces/newlines

        # Join all page text into a single string
        cleaned_text = ' '.join(full_text)
        
        # Fix common formatting issues
        cleaned_text = cleaned_text.replace(' .', '.')   # Fix spacing before periods
        cleaned_text = cleaned_text.replace(' ,', ',')   # Fix spacing before commas
        cleaned_text = cleaned_text.replace(' :', ':')   # Fix spacing before colons
        cleaned_text = cleaned_text.replace(' \n', '\n') # Clean up single newlines
        
        # Replace multiple spaces with a single space
        cleaned_text = ' '.join(cleaned_text.split())

        # Properly format paragraphs (double newlines to separate paragraphs)
        cleaned_text = cleaned_text.replace('\n\n\n', '\n\n')  # Replace excessive newlines with two newlines
        cleaned_text = cleaned_text.strip()  # Remove any leading/trailing spaces/newlines

        return cleaned_text
    except Exception as e:
        return f"Error reading .pdf file: {str(e)}"

# Helper function to perform OCR on image files
def read_image_file(file):
    try:
        image = Image.open(file)
        text = pytesseract.image_to_string(image)
        cleaned_text = ' '.join(text.split())
        cleaned_text = cleaned_text.replace(' .', '.')   # Fix spacing before periods
        cleaned_text = cleaned_text.replace(' ,', ',')   # Fix spacing before commas
        cleaned_text = cleaned_text.replace(' :', ':')   # Fix spacing before colons
        cleaned_text = cleaned_text.replace(' \n', '\n') # Clean up single newlines
        
        # Replace multiple spaces with a single space
        cleaned_text = ' '.join(cleaned_text.split())

        # Properly format paragraphs (double newlines to separate paragraphs)
        cleaned_text = cleaned_text.replace('\n\n\n', '\n\n')  # Replace excessive newlines with two newlines
        cleaned_text = cleaned_text.strip()  # Remove any leading/trailing spaces/newlines

        return cleaned_text
    except Exception as e:
        return f"Error reading image file: {str(e)}"

def read_image_pdf(file):
    text = ""
    try:
        images = convert_from_path(file)
        for image in images:
            ocr_text = pytesseract.image_to_string(image)
            text += ' '.join(ocr_text.split()) + "\n"
        return text.strip()  # Strip trailing newline
    except Exception as e:
        return f"Error reading scanned .pdf file: {str(e)}"
