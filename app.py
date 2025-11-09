from flask import Flask, render_template, request, jsonify
from utilities import solve_sudoku
from vision import preprocess_image, find_grid, extract_grid, extract_digits
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/solve', methods=['POST'])
def solve():
    board = request.json['board']
    if solve_sudoku(board):
        return jsonify({'solution': board})
    else:
        return jsonify({'error': 'No solution exists'})

@app.route('/scan', methods=['POST'])
def scan():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
        
    upload_folder = 'uploads'
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)
        
    filepath = os.path.join(upload_folder, file.filename)
    file.save(filepath)
    
    try:
        original_image, processed_image = preprocess_image(filepath)
        corners = find_grid(processed_image)
        grid_image = extract_grid(original_image, corners)
        board = extract_digits(grid_image)
        
        print("Detected Board:", board)  # Add this line for debugging
        
        # Make a copy of the board to return to the user
        original_board = [row[:] for row in board]

        if solve_sudoku(board):
            return jsonify({'solution': board, 'board': original_board})
        else:
            return jsonify({'error': 'No solution exists for the detected board', 'board': original_board})
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500
        
    finally:
        if os.path.exists(filepath):
            os.remove(filepath)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)