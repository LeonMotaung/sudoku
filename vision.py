import cv2
import numpy as np
from PIL import Image
import pytesseract

# If you're on Windows, you might need to set the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def preprocess_image(image_path):
    """
    Loads an image, preprocesses it for Sudoku grid detection.
    
    Args:
        image_path (str): The path to the image file.
        
    Returns:
        tuple: A tuple containing the original image and the processed image.
    """
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
    return img, thresh

def find_grid(processed_image):
    """
    Finds the Sudoku grid in the processed image.
    
    Args:
        processed_image (numpy.ndarray): The preprocessed image.
        
    Returns:
        numpy.ndarray: The corners of the detected grid.
    """
    contours, _ = cv2.findContours(processed_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Find the largest contour which should be the Sudoku grid
    largest_contour = max(contours, key=cv2.contourArea)
    
    # Get the corners of the contour
    epsilon = 0.02 * cv2.arcLength(largest_contour, True)
    corners = cv2.approxPolyDP(largest_contour, epsilon, True)
    
    return corners

def extract_grid(image, corners):
    """
    Extracts the Sudoku grid from the image using the detected corners.
    
    Args:
        image (numpy.ndarray): The original image.
        corners (numpy.ndarray): The corners of the Sudoku grid.
        
    Returns:
        numpy.ndarray: The warped and cropped image of the Sudoku grid.
    """
    # Order the corners
    corners = np.squeeze(corners)
    ordered_corners = np.zeros((4, 2), dtype="float32")
    
    s = corners.sum(axis=1)
    ordered_corners[0] = corners[np.argmin(s)]
    ordered_corners[2] = corners[np.argmax(s)]
    
    diff = np.diff(corners, axis=1)
    ordered_corners[1] = corners[np.argmin(diff)]
    ordered_corners[3] = corners[np.argmax(diff)]
    
    # Define the destination points for the perspective transform
    dst = np.array([
        [0, 0],
        [450 - 1, 0],
        [450 - 1, 450 - 1],
        [0, 450 - 1]], dtype="float32")
    
    # Get the perspective transform matrix and warp the image
    matrix = cv2.getPerspectiveTransform(ordered_corners, dst)
    warped = cv2.warpPerspective(image, matrix, (450, 450))
    
    return warped

def extract_digits(grid_image):
    """
    Extracts the digits from the Sudoku grid image.
    
    Args:
        grid_image (numpy.ndarray): The image of the Sudoku grid.
        
    Returns:
        list: A 9x9 list representing the Sudoku board.
    """
    board = np.zeros((9, 9), dtype=int)
    cell_size = grid_image.shape[0] // 9
    padding = 5  # Add some padding to avoid the grid lines
    
    for i in range(9):
        for j in range(9):
            # Crop a smaller region to avoid grid lines
            cell_image = grid_image[i * cell_size + padding:(i + 1) * cell_size - padding, 
                                    j * cell_size + padding:(j + 1) * cell_size - padding]
            
            # Preprocess the cell for digit recognition
            gray_cell = cv2.cvtColor(cell_image, cv2.COLOR_BGR2GRAY)
            
            # Thresholding
            thresh_cell = cv2.threshold(gray_cell, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
            
            # Find contours to see if there's something in the cell
            contours, _ = cv2.findContours(thresh_cell.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            if len(contours) > 0:
                # Check the area of the largest contour
                c = max(contours, key=cv2.contourArea)
                if cv2.contourArea(c) > 20: # Filter out noise
                    # Use Tesseract to recognize the digit
                    text = pytesseract.image_to_string(thresh_cell, config='--psm 10 --oem 3 -c tessedit_char_whitelist=123456789')
                    
                    if text.strip().isdigit():
                        board[i][j] = int(text.strip())
                
    return board.tolist()
