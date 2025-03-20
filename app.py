import os
import uuid
from flask import Flask, render_template, request, send_file, redirect, url_for, flash, session
from werkzeug.utils import secure_filename
from PyPDF2 import PdfReader, PdfWriter

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

# Function to protect PDF (allow reading but disable editing)
def protect_pdf(input_path, output_path):
    """
    Protect a PDF file by disabling editing permissions but allowing reading
    
    Args:
        input_path (str): Path to the original PDF file
        output_path (str): Path where the protected PDF will be saved
        
    Returns:
        bool: True if protection was successful, False otherwise
    """
    try:
        # Make sure input path is absolute
        input_path = os.path.abspath(input_path)
        output_path = os.path.abspath(output_path)
        
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

        # Set up encryption with permissions
        # '/R=4' means revision 4 of the standard security handler
        # No user password (empty string), so anyone can open and read
        writer.encrypt(
            user_password='',  # No password to open the document
            owner_password=str(uuid.uuid4()),  # Random password that only the owner knows
            use_128bit=True,
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

        # Make sure the output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Save the protected PDF
        try:
            with open(output_path, 'wb') as output_file:
                writer.write(output_file)
            
            # Verify the file was created successfully
            if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
                print(f"PDF protected successfully: {output_path}")
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
        
        # Protect the PDF
        protection_result = protect_pdf(original_path, protected_path)
        print(f"DEBUG: PDF protection result: {protection_result}")
        
        if protection_result:
            # Save the protected file path in the session for download
            session['protected_file'] = protected_path
            session['protected_filename'] = protected_filename
            # Force the session to be saved immediately
            session.modified = True
            
            print(f"DEBUG: Session variables set - protected_file: {session['protected_file']}")
            print(f"DEBUG: Session variables set - protected_filename: {session['protected_filename']}")
            
            flash('¡PDF protegido exitosamente!', 'success')
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
