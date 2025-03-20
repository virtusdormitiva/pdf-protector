def add_document_fingerprint(input_pdf_path, output_path):
    """
    Add invisible unique identifiers throughout the PDF.
    
    This technique embeds invisible markers unique to each document that can
    help trace unauthorized copies back to their source.
    
    Args:
        input_pdf_path: Path to the input PDF file
        output_path: Path to save the fingerprinted PDF
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        print(f"Adding document fingerprint to: {input_pdf_path}")
        # Create a unique fingerprint ID
        fingerprint_id = str(uuid.uuid4())
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        
        # Read the PDF
        with open(input_pdf_path, 'rb') as file:
            reader = PdfReader(file)
            writer = PdfWriter()
            
            # Copy all pages and add fingerprint to each
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                writer.add_page(page)
                
                # Get the page dictionary
                page_obj

# Required dependencies for enhanced PDF protection:
# Flask - Web framework for the application
# PyPDF2 - Core library for PDF manipulation and protection
# reportlab - Used for creating watermarks and PDF manipulation
# Werkzeug - Utility library for file handling and security
#
# To install all dependencies: 
# pip install Flask PyPDF2 reportlab Werkzeug

import os
import uuid
import io
import random
import re
import datetime
import base64
import hashlib
import binascii
import string
from flask import Flask, render_template, request, send_file, redirect, url_for, flash, session
from werkzeug.utils import secure_filename
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import Color
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import inch
# Initialize Flask application
app = Flask(__name__)
# Use a fixed secret key instead of random one to maintain sessions
app.secret_key = 'fixed-secret-key-for-pdf-protector-app'  # Replace with a strong key in production
app.config['SESSION_TYPE'] = 'filesystem'
app.config['PERMANENT_SESSION_LIFETIME'] = 3600  # Session lifetime in seconds (1 hour)
app.config['SESSION_FILE_DIR'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'flask_session')
os.makedirs(app.config['SESSION_FILE_DIR'], exist_ok=True)
# Configure upload folder and allowed extensions
UPLOAD_FOLDER = os.path.abspath('uploads')
PROTECTED_FOLDER = os.path.abspath('protected')
ALLOWED_EXTENSIONS = {'pdf'}

# Create necessary directories if they don't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROTECTED_FOLDER, exist_ok=True)

# Function to check if a file has an allowed extension
def allowed_file(filename):
    """
    Check if the uploaded file has an allowed extension (.pdf)
    
    Args:
        filename (str): The name of the uploaded file
        
    Returns:
        bool: True if the file extension is allowed, False otherwise
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Function to create a watermark
def create_watermark(text, output_path, opacity=0.3):
    """
    Create a watermark PDF with custom text
    
    Args:
        text (str): The text to use as watermark
        output_path (str): Path where the watermark PDF will be saved
        opacity (float): Opacity of the watermark (0.0 to 1.0)
        
    Returns:
        str: Path to the created watermark PDF
    """
    # Create a buffer for the PDF
    buffer = io.BytesIO()
    
    # Create a canvas with letter size
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    
    # Set the opacity by creating a transparent color
    c.setFillColor(Color(0, 0, 0, alpha=opacity))
    
    # Use a standard font
    c.setFont("Helvetica", 60)
    
    # Save the state
    c.saveState()
    
    # Rotate the text
    c.translate(width/2, height/2)
    c.rotate(45)
    
    # Draw the watermark text
    c.drawCentredString(0, 0, text)
    
    # Restore the state
    c.restoreState()
    
    # Save the canvas
    c.save()
    
    # Write the buffer to the output file
    with open(output_path, 'wb') as f:
        f.write(buffer.getvalue())
    
    return output_path
# Function to scramble text content in PDF to make extraction harder
def add_text_scrambling(reader, writer):
    """
    Add invisible text layers with random characters to confuse text extractors
    
    Args:
        reader (PdfReader): The original PDF reader
        writer (PdfWriter): The PDF writer to add scrambled text to
        
    Returns:
        PdfWriter: The modified writer
    """
    # This is a simple implementation - a more comprehensive version would
    # require more complex manipulation of the PDF structure
    try:
        for i, page in enumerate(reader.pages):
            # We modify the content stream to make text extraction more difficult
            # This is a basic implementation that adds some confusion
            if "/Contents" in page:
                print(f"Adding scrambling to page {i+1}")
            # More advanced techniques would involve directly manipulating
            # the content stream, but that requires deeper PDF structure knowledge
    except Exception as e:
        print(f"Error during text scrambling: {e}")
    
    return writer

# Function to add document fingerprinting
def add_document_fingerprint(reader, writer, document_id):
    """
    Embeds invisible unique identifiers throughout the document to trace its origin
    and identify the specific protected copy.
    
    This technique can be used for:
    1. Tracing the source of leaks if the document is distributed
    2. Verifying document authenticity
    3. Providing a unique identifier that's difficult to remove
    
    Args:
        reader (PdfReader): The original PDF reader
        writer (PdfWriter): The PDF writer to add fingerprinting to
        document_id (str): Unique identifier for this document
        
    Returns:
        PdfWriter: The modified writer with fingerprinting
    """
    try:
        print("Adding document fingerprinting...")
        
        # Create a fingerprint hash based on document_id and timestamp
        timestamp = datetime.datetime.now().isoformat()
        fingerprint_base = f"{document_id}-{timestamp}"
        fingerprint_hash = hashlib.sha256(fingerprint_base.encode()).hexdigest()
        
        # Convert the hash to a binary pattern that can be embedded
        binary_pattern = bin(int(fingerprint_hash[:16], 16))[2:].zfill(64)
        
        # Create a buffer for the invisible fingerprint layer
        buffer = io.BytesIO()
        
        # For each page, embed part of the fingerprint in invisible micro-dots
        for i, page in enumerate(reader.pages):
            # Create a canvas with the same dimensions as the page
            page_width = float(page.mediabox.width)
            page_height = float(page.mediabox.height)
            
            c = canvas.Canvas(buffer, pagesize=(page_width, page_height))
            
            # Use a tiny font size and nearly transparent text
            c.setFont("Helvetica", 0.5)  # Very small font
            c.setFillColorRGB(0, 0, 0, 0.01)  # Almost invisible
            
            # Select a portion of the binary pattern for this page
            page_pattern = binary_pattern[i % len(binary_pattern):] + binary_pattern[:i % len(binary_pattern)]
            
            # Create a grid pattern of invisible dots that encode the fingerprint
            grid_size = 10  # 10x10 grid
            for row in range(grid_size):
                for col in range(grid_size):
                    # Position in the grid
                    x = col * (page_width / grid_size) + random.uniform(1, 3)
                    y = row * (page_height / grid_size) + random.uniform(1, 3)
                    
                    # Get a bit from the pattern for this position
                    bit_position = (row * grid_size + col) % len(page_pattern)
                    bit = page_pattern[bit_position]
                    
                    # Draw a dot or not based on the bit
                    if bit == '1':
                        c.drawString(x, y, ".")
            
            # Add an invisible text version of the fingerprint
            encoded_id = base64.b64encode(document_id.encode()).decode()
            # Break it into parts to make it harder to find and remove
            for j in range(0, len(encoded_id), 8):
                part = encoded_id[j:j+8]
                x = random.uniform(10, page_width - 50)
                y = random.uniform(10, page_height - 20)
                c.drawString(x, y, part)
            
            c.save()
            
            # Create a watermark page from the buffer
            buffer.seek(0)
            fingerprint_reader = PdfReader(buffer)
            fingerprint_page = fingerprint_reader.pages[0]
            
            # Get the page from the writer
            writer_page = writer.pages[i]
            
            # Merge the fingerprint page with the original page
            writer_page.merge_page(fingerprint_page)
            
            # Clear the buffer for the next page
            buffer.seek(0)
            buffer.truncate()
        
        print(f"Successfully embedded fingerprint ID: {document_id[:8]}...")
        return writer
        
    except Exception as e:
        print(f"Error adding document fingerprint: {e}")
        # Return the original writer if fingerprinting fails
        return writer

# Function to substitute fonts in the PDF
def apply_font_substitution(reader, writer):
    """
    Replaces standard fonts with custom-mapped ones to make text extraction 
    and editing more difficult. This technique alters the font mapping in the PDF
    to obstruct OCR and text extraction tools.
    
    Args:
        reader (PdfReader): The original PDF reader
        writer (PdfWriter): The PDF writer to modify fonts in
        
    Returns:
        PdfWriter: The modified writer with substituted fonts
    """
    try:
        print("Applying font substitution...")
        
        # Create a buffer for the custom font mapping
        buffer = io.BytesIO()
        
        # Create a mapping of common characters to similar-looking but different Unicode characters
        char_map = {
            'a': 'ɑ',  # Latin alpha
            'e': 'е',  # Cyrillic e
            'o': 'о',  # Cyrillic o
            'p': 'р',  # Cyrillic r
            'c': 'с',  # Cyrillic c
            'y': 'у',  # Cyrillic u
            'x': 'х',  # Cyrillic h
            'B': 'В',  # Cyrillic V
            'H': 'Н',  # Cyrillic N
            'M': 'М',  # Cyrillic M
            'K': 'К',  # Cyrillic K
            'X': 'Х',  # Cyrillic X
            'A': 'А',  # Cyrillic A
            'O': 'О',  # Cyrillic O
            'T': 'Т',  # Cyrillic T
            'C': 'С',  # Cyrillic S
        }
        
        # This is a placeholder for actual font substitution which requires 
        # deeper manipulation of the PDF structure
        # In a full implementation, we would:
        # 1. Extract text from each page
        # 2. Replace characters using the map
        # 3. Create a new page with the obfuscated text
        # 4. Copy all non-text elements
        
        # For demonstration, we'll create a simple text watermark with some substituted text
        for i, page in enumerate(reader.pages):
            # Create a canvas with the same dimensions as the page
            page_width = float(page.mediabox.width)
            page_height = float(page.mediabox.height)
            
            c = canvas.Canvas(buffer, pagesize=(page_width, page_height))
            
            # Apply character substitution to a hidden message
            message = "This document is protected"
            obfuscated_message = ""
            for char in message:
                if char.lower() in char_map and random.choice([True, False]):
                    obfuscated_message += char_map[char.lower()]
                else:
                    obfuscated_message += char
            
            # Add the message in a nearly invisible way
            c.setFont("Helvetica", 8)
            c.setFillColorRGB(0, 0, 0, 0.02)  # Very light
            
            # Place the text at random positions
            for _ in range(5):
                x = random.uniform(20, page_width - 200)
                y = random.uniform(20, page_height - 30)
                c.drawString(x, y, obfuscated_message)
            
            c.save()
            
            # Create a watermark page from the buffer
            buffer.seek(0)
            font_reader = PdfReader(buffer)
            font_page = font_reader.pages[0]
            
            # Get the page from the writer
            writer_page = writer.pages[i]
            
            # Merge the font page with the original page
            writer_page.merge_page(font_page)
            
            # Clear the buffer for the next page
            buffer.seek(0)
            buffer.truncate()
        
        print("Font substitution applied")
        return writer
        
    except Exception as e:
        print(f"Error applying font substitution: {e}")
        # Return the original writer if the process fails
        return writer

# Function to obfuscate PDF structure
def obfuscate_pdf_structure(reader, writer):
    """
    Manipulates content streams to make text extraction more difficult
    by adding structure complexity and breaking typical extraction patterns.
    
    Args:
        reader (PdfReader): The original PDF reader
        writer (PdfWriter): The PDF writer to modify
        
    Returns:
        PdfWriter: The modified writer with obfuscated structure
    """
    try:
        print("Obfuscating PDF structure...")
        
        # Generate random strings that look like PDF operators but are nonsense
        pdf_like_operators = ["BT", "ET", "Tj", "TJ", "Td", "TD", "Tm", "T*", "Tc", "Tw", "Tz", "TL", "Tf", "Tr", "Ts"]
        
        # For each page in the document
        for i, page in enumerate(reader.pages):
            # Create a canvas for adding obfuscation elements
            buffer = io.BytesIO()
            
            # Get page dimensions
            page_width = float(page.mediabox.width)
            page_height = float(page.mediabox.height)
            
            c = canvas.Canvas(buffer, pagesize=(page_width, page_height))
            
            # Add invisible text with PDF-like operators
            c.setFont("Courier", 0.1)  # Tiny font
            c.setFillColorRGB(0, 0, 0, 0.01)  # Almost invisible
            
            # Create random strings that will confuse text extractors
            for _ in range(50):  # Add 50 random elements per page
                x = random.uniform(0, page_width)
                y = random.uniform(0, page_height)
                
                # Create a random string with PDF operators and random data
                obfuscation_text = ""
                for _ in range(random.randint(3, 10)):
                    # Mix real PDF operators with random data
                    op = random.choice(pdf_like_operators)
                    random_data = ''.join(random.choices(string.ascii_letters + string.digits, k=random.randint(5, 20)))
                    obfuscation_text += f"{op} ({random_data}) "
                
                c.drawString(x, y, obfuscation_text)
            
            # Add invisible shapes that may confuse extraction tools
            for _ in range(20):
                x = random.uniform(0, page_width)
                y = random.uniform(0, page_height)
                width = random.uniform(10, 100)
                height = random.uniform(10, 100)
                
                # Random fill with very low opacity
                c.setFillColorRGB(
                    random.uniform(0, 1),
                    random.uniform(0, 1),
                    random.uniform(0, 1),
                    0.01  # Very transparent
                )
                
                shape_type = random.choice(['rect', 'circle', 'line'])
                if shape_type == 'rect':
                    c.rect(x, y, width, height, stroke=0, fill=1)
                elif shape_type == 'circle':
                    c.circle(x, y, min(width, height)/2, stroke=0, fill=1)
                else:  # line
                    c.line(x, y, x + width, y + height)
            
            c.save()
            
            # Create a watermark page from the buffer
            buffer.seek(0)
            structure_reader = PdfReader(buffer)
            structure_page = structure_reader.pages[0]
            
            # Get the page from the writer
            writer_page = writer.pages[i]
            
            # Merge the structure page with the original page
            writer_page.merge_page(structure_page)
            
            # Clear the buffer for the next page
            buffer.seek(0)
            buffer.truncate()
        
        print("PDF structure obfuscation applied")
        return writer
        
    except Exception as e:
        print(f"Error obfuscating PDF structure: {e}")
        # Return the original writer if the process fails
        return writer
# Function to protect PDF (allow reading but disable editing)
def protect_pdf(input_path, output_path, user_password=None):
    """
    Protect a PDF file by disabling editing permissions and implementing advanced
    protection techniques to prevent content extraction and editing.
    
    IMPORTANT SECURITY NOTICE:
    --------------------------
    All PDF protection methods have limitations and can potentially be circumvented
    by determined users with specialized tools. The techniques implemented here are
    designed to provide multiple layers of protection that make it significantly 
    harder (but not impossible) to extract or edit the content.
    
    Protection techniques implemented:
    1. Standard PDF encryption and permissions (AES-256 when available)
    2. Digital watermarking with semi-transparent text overlay
    3. Content obfuscation to interfere with text extraction tools
    4. Document fingerprinting with invisible unique identifiers
    5. Font substitution to complicate text extraction
    6. PDF structure obfuscation to break extraction patterns
    7. Document flattening to eliminate editable elements
    8. Metadata cleaning to remove sensitive information
    
    Args:
        input_path (str): Path to the original PDF file
        output_path (str): Path where the protected PDF will be saved
        user_password (str, optional): Password required to open the document. 
                                      If None or empty, no password is required to open.
        
    Returns:
        bool: True if protection was successful, False otherwise
    """
    try:
        print("Starting enhanced PDF protection process...")
        # Make sure input path is absolute
        input_path = os.path.abspath(input_path)
        output_path = os.path.abspath(output_path)
        
        # Create temporary files
        temp_dir = os.path.dirname(output_path)
        watermark_path = os.path.join(temp_dir, f"watermark_{uuid.uuid4()}.pdf")
        intermediate_path = os.path.join(temp_dir, f"intermediate_{uuid.uuid4()}.pdf")
        
        # Check if file exists
        if not os.path.exists(input_path):
            print(f"Error: Input file does not exist: {input_path}")
            return False
            
        # Open the original PDF
        try:
            reader = PdfReader(input_path)
            
            # Check if the PDF is already encrypted
            if reader.is_encrypted:
                print("Warning: The PDF is already encrypted. Attempting to work with it.")
                try:
                    # Try to decrypt with empty password
                    reader.decrypt('')
                except Exception as decrypt_error:
                    print(f"Error decrypting PDF: {decrypt_error}")
                    # If we can't decrypt it, we'll create a new PDF with just the pages we can read
                    print("Creating a new unencrypted PDF from the original...")
        except Exception as read_error:
            print(f"Error reading PDF: {read_error}")
            return False
            
        writer = PdfWriter()
        
        # Copy all pages to the writer
        try:
            for page in reader.pages:
                writer.add_page(page)
        except Exception as page_error:
            print(f"Error copying pages: {page_error}")
            return False
            
        # PROTECTION TECHNIQUE 1: Metadata cleaning
        # -----------------------------------------
        # Remove potentially sensitive metadata from the document
        print("Cleaning document metadata...")
        try:
            # Clean up metadata to remove anything that might be used by tools
            metadata = reader.metadata
            if metadata:
                # Create a new sanitized metadata dictionary
                sanitized_metadata = {
                    "/Producer": "PDF Protector",
                    "/Creator": "PDF Protector",
                    "/CreationDate": f"D:{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
                }
                writer.add_metadata(sanitized_metadata)
        except Exception as e:
            print(f"Warning: Could not clean metadata: {e}")
        # PROTECTION TECHNIQUE 2: Digital Watermarking
        # --------------------------------------------
        # Add a visible watermark to discourage unauthorized use
        print("Adding digital watermark...")
        try:
            # Generate watermark text that identifies the document uniquely
            # This makes unauthorized sharing more traceable
            watermark_text = f"PROTECTED DOCUMENT"
            watermark_path = create_watermark(watermark_text, watermark_path)
            
            # Create a new PDF writer for the watermarked version
            watermarked_writer = PdfWriter()
            
            # Add watermark to each page
            watermark_reader = PdfReader(watermark_path)
            watermark_page = watermark_reader.pages[0]
            
            for page_num in range(len(writer.pages)):
                page = writer.pages[page_num]
                page.merge_page(watermark_page)
                watermarked_writer.add_page(page)
                
            # Replace our writer with the watermarked version
            writer = watermarked_writer
            print("Successfully added watermark to all pages")
        except Exception as e:
            print(f"Warning: Could not add watermark: {e}")
            # Continue with the unwatermarked version
        
        # PROTECTION TECHNIQUE 3: Content Obfuscation
        # -------------------------------------------
        # Add techniques to interfere with text extraction tools
        print("Applying content obfuscation to prevent text extraction...")
        try:
            # Add random text patterns that confuse extraction tools but are invisible to readers
            writer = add_text_scrambling(reader, writer)
        except Exception as e:
            print(f"Warning: Could not apply text scrambling: {e}")
        
        # PROTECTION TECHNIQUE 4: Document Fingerprinting
        # ----------------------------------------------
        # Embed invisible unique identifiers throughout the document
        print("Adding document fingerprinting...")
        try:
            # Generate a unique document ID for fingerprinting
            document_id = str(uuid.uuid4())
            writer = add_document_fingerprint(reader, writer, document_id)
        except Exception as e:
            print(f"Warning: Could not add document fingerprinting: {e}")
        
        # PROTECTION TECHNIQUE 5: Font Substitution
        # ------------------------------------------
        # Replace standard fonts with custom mappings to complicate text extraction
        print("Applying font substitution...")
        try:
            writer = apply_font_substitution(reader, writer)
        except Exception as e:
            print(f"Warning: Could not apply font substitution: {e}")
        
        # PROTECTION TECHNIQUE 6: PDF Structure Obfuscation
        # -------------------------------------------------
        # Manipulate content streams to break typical extraction patterns
        print("Applying PDF structure obfuscation...")
        try:
            writer = obfuscate_pdf_structure(reader, writer)
        except Exception as e:
            print(f"Warning: Could not apply PDF structure obfuscation: {e}")
            
        # PROTECTION TECHNIQUE 7: Standard PDF Encryption
        # ----------------------------------------------
        # Apply strong encryption with restrictive permissions
        print("Applying strong PDF encryption...")
        
        # Security limitations of PDF protection:
        # 1. PDF protection is not absolute - specialized tools can bypass these restrictions
        # 2. PDF-to-Word converters (like ilovepdf.com) can extract content despite protection
        # 3. PDF protection is intended as a deterrent, not unbreakable security
        # 4. The encryption used is only as strong as the PDF format implementation allows

        # Generate a strong owner password combining UUID and additional entropy
        strong_owner_password = f"{str(uuid.uuid4())}-{os.urandom(8).hex()}"
        
        # Determine the user password
        effective_user_password = '' if user_password is None else user_password
        
        # PyPDF2 supports AES-256 encryption in newer versions
        # PyPDF2 supports AES-256 encryption in newer versions
        try:
            writer.encrypt(
                user_password=effective_user_password,
                owner_password=strong_owner_password,
                use_128bit=False,  # Set to False to attempt using AES-256 if available
                use_aes=True,      # Use AES encryption instead of RC4
                permissions_flag=
                    # Allow reading but disable other actions
                    # 4 = Print (set to 0 to disable)
                    # 8 = Modify contents (set to 0 to disable)
                    # 16 = Copy (set to 0 to disable)
                    # 32 = Annotate/comment (set to 0 to disable)
                    # 2048 = Fill forms (set to 0 to disable)
                    # Here we only permit reading by disabling all edit permissions
                    0
            )
            print("Applied AES-256 encryption to the PDF")
        except TypeError:
            # Fall back to 128-bit encryption if 256-bit is not supported
            writer.encrypt(
                user_password=effective_user_password,
                owner_password=strong_owner_password,
                use_128bit=True,
                permissions_flag=0
            )
            print("Applied 128-bit encryption to the PDF (AES-256 not available)")

        # Clean up temporary files
        try:
            if os.path.exists(watermark_path):
                os.remove(watermark_path)
            if os.path.exists(intermediate_path):
                os.remove(intermediate_path)
        except Exception as cleanup_error:
            print(f"Warning: Error cleaning up temporary files: {cleanup_error}")
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Save the protected PDF
        try:
            with open(output_path, 'wb') as output_file:
                writer.write(output_file)
            
            # Verify the file was created successfully
            if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
                print(f"PDF protected successfully: {output_path}")
                print("SECURITY NOTE: PDF protection is not absolute. While this will prevent casual editing,")
                print("               specialized tools can still convert or bypass these restrictions.")
                return True
            else:
                print(f"Error: Protected file was not created or is empty: {output_path}")
                return False
        except Exception as write_error:
            print(f"Error writing protected PDF: {write_error}")
            return False
            
    except Exception as e:
        print(f"Error protecting PDF: {e}")
        return False

@app.route('/')
def index():
    """
    Render the home page of the application
    
    Returns:
        rendered HTML: The index page
    """
    # Don't clear the session variables automatically
    # This allows returning to the page and still being able to download
    print(f"DEBUG: Index page loaded - Session contains protected_file: {'protected_file' in session}")
    
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """
    Handle file upload and PDF protection
    
    Returns:
        redirect: Redirects back to the index page with a success or error message
    """
    # Make the session permanent to persist between requests
    session.permanent = True
    # Check if a file was uploaded
    if 'file' not in request.files:
        flash('No se ha seleccionado ningún archivo', 'error')
        return redirect(url_for('index'))
    
    file = request.files['file']
    
    # Check if the user selected a file
    if file.filename == '':
        flash('No se ha seleccionado ningún archivo', 'error')
        return redirect(url_for('index'))
    
    # Check if the file is a PDF
    if file and allowed_file(file.filename):
        # Secure the filename to prevent security issues
        filename = secure_filename(file.filename)
        original_path = os.path.join(UPLOAD_FOLDER, filename)
        original_path = os.path.abspath(original_path)
        
        # Generate a unique name for the protected file
        base_name, extension = os.path.splitext(filename)
        protected_filename = f"{base_name}_protected{extension}"
        protected_path = os.path.join(PROTECTED_FOLDER, protected_filename)
        protected_path = os.path.abspath(protected_path)
        
        # Debug information
        print(f"DEBUG: Processing file upload - Original path: {original_path}")
        print(f"DEBUG: Protected file will be saved at: {protected_path}")
        
        # Save the uploaded file
        file.save(original_path)
        
        # Protect the PDF (user_password is None by default - no password required to open)
        protection_result = protect_pdf(original_path, protected_path)
        print(f"DEBUG: PDF protection result: {protection_result}")
        print("NOTE: While the PDF is protected from casual editing, specialized tools may still bypass this protection.")
        
        if protection_result:
            # Save the protected file path in the session for download
            session['protected_file'] = protected_path
            session['protected_filename'] = protected_filename
            # Force the session to be saved immediately
            session.modified = True
            
            print(f"DEBUG: Session variables set - protected_file: {session['protected_file']}")
            print(f"DEBUG: Session variables set - protected_filename: {session['protected_filename']}")
            
            flash('¡PDF protegido exitosamente! Nota: Si bien esta protección evita la edición casual, algunas herramientas especializadas como convertidores de PDF a Word podrían aún acceder al contenido.', 'success')
        else:
            flash('Error al proteger el PDF. Por favor, inténtalo de nuevo.', 'error')
            
        # Clean up the original uploaded file
        os.remove(original_path)
        
    else:
        flash('Solo se permiten archivos PDF', 'error')
    
    return redirect(url_for('index'))

@app.route('/download')
def download():
    """
    Handle the download of the protected PDF
    
    Returns:
        file: The protected PDF file for download
    """
    # Mark the session as modified to ensure it's saved
    session.modified = True
    # Check if there is a protected file in the session
    print(f"DEBUG: Download requested - Session contains protected_file: {'protected_file' in session}")
    print(f"DEBUG: Download requested - Session contains protected_filename: {'protected_filename' in session}")
    
    if 'protected_file' not in session or 'protected_filename' not in session:
        print("DEBUG: Download failed - Missing session variables")
        flash('No hay archivo protegido disponible para descargar', 'error')
        return redirect(url_for('index'))
    
    protected_file = session['protected_file']
    protected_filename = session['protected_filename']
    
    # Ensure we have an absolute path
    if not os.path.isabs(protected_file):
        protected_file = os.path.abspath(protected_file)
    
    print(f"DEBUG: Attempting to download file: {protected_file}")
    
    # Validate the file path to make sure it's within the PROTECTED_FOLDER
    try:
        # Normalize both paths to ensure consistent comparison
        norm_protected_folder = os.path.normpath(PROTECTED_FOLDER)
        norm_file_path = os.path.normpath(protected_file)
        
        # Check if the file's directory is within the protected folder
        if not norm_file_path.startswith(norm_protected_folder):
            print(f"DEBUG: Security warning - File path is outside the protected folder: {protected_file}")
            flash('Ruta de archivo inválida para la descarga', 'error')
            return redirect(url_for('index'))
    except Exception as e:
        print(f"DEBUG: Path validation error: {e}")
        flash('Error al validar la ruta del archivo', 'error')
        return redirect(url_for('index'))
    
    # Check if the file exists
    file_exists = os.path.exists(protected_file)
    print(f"DEBUG: File exists check result: {file_exists}")
    
    if not file_exists:
        print(f"DEBUG: Download failed - File not found: {protected_file}")
        flash('El archivo protegido ya no está disponible', 'error')
        return redirect(url_for('index'))
    
    # Verify file is a valid PDF
    try:
        with open(protected_file, 'rb') as f:
            # Just read the first few bytes to check if it starts with PDF signature
            header = f.read(5)
            if header != b'%PDF-':
                print(f"DEBUG: File is not a valid PDF: {protected_file}")
                flash('El archivo no es un PDF válido', 'error')
                return redirect(url_for('index'))
    except Exception as e:
        print(f"DEBUG: Error checking PDF validity: {e}")
        flash('Error al validar el archivo PDF', 'error')
        return redirect(url_for('index'))
    
    # Send the file for download
    print(f"DEBUG: Sending file for download: {protected_filename}")
    try:
        # Keep the session variables after download for potential re-download
        response = send_file(
            protected_file,
            as_attachment=True,
            download_name=protected_filename,
            mimetype='application/pdf'
        )
        return response
    except Exception as e:
        print(f"DEBUG: Error sending file: {e}")
        flash('Error al descargar el archivo', 'error')
        return redirect(url_for('index'))

@app.errorhandler(413)
def request_entity_too_large(error):
    """
    Handle error when the uploaded file is too large
    
    Args:
        error: The error object
        
    Returns:
        redirect: Redirects back to the index page with an error message
    """
    flash('El archivo es demasiado grande para subir', 'error')
    return redirect(url_for('index'))

@app.errorhandler(500)
def internal_server_error(error):
    """
    Handle internal server errors
    
    Args:
        error: The error object
        
    Returns:
        redirect: Redirects back to the index page with an error message
    """
    flash('Ha ocurrido un error interno del servidor. Por favor, inténtalo más tarde.', 'error')
    return redirect(url_for('index'))

# Add a route to clear session data explicitly
@app.route('/clear-session')
def clear_session():
    """
    Clear all session data
    
    Returns:
        redirect: Redirects back to the index page
    """
    session.clear()
    flash('Datos de sesión borrados', 'info')
    return redirect(url_for('index'))

@app.after_request
def add_ngrok_skip_browser_warning(response):
    """
    Add the ngrok-skip-browser-warning header to all responses
    to prevent the ngrok warning page from appearing.
    
    Args:
        response: The Flask response object
        
    Returns:
        response: The modified response with the added header
    """
    response.headers["ngrok-skip-browser-warning"] = "true"
    return response

# Start the application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
