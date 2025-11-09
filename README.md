# Sudoku Solver with Image Recognition

A **web-based Sudoku solver** built with **Flask**, **OpenCV**, and **Tesseract OCR**.  
Upload a photo of a Sudoku puzzle or input it manually, and the system will automatically detect the numbers, solve the puzzle, and display the solution.

---

## Screenshot

![Sudoku Solver Screenshot](Screenshot 2025-11-09 211538.png)

---

## Features

- **Manual Sudoku Entry**
  - Input Sudoku numbers directly via the web interface.
  - Instantly solves the puzzle using a backtracking algorithm.

- **Image-based Sudoku Detection**
  - Upload an image of a Sudoku puzzle.
  - Automatic grid detection and perspective correction using OpenCV.
  - Digit recognition from cells using Tesseract OCR.

- **Automatic Solver**
  - Returns the solved Sudoku board or an error if no solution exists.
  - Displays both the original detected board and the solved board.

- **User-friendly Interface**
  - Interactive web interface built with HTML and JavaScript.
  - Easy workflow with step-by-step guidance.

---

## Technologies Used

- **Python** – Core programming language  
- **Flask** – Web framework  
- **OpenCV** – Image processing and computer vision  
- **Tesseract OCR** – Optical character recognition for digit detection  
- **HTML / JavaScript** – Frontend interface  

---

## Installation

1. **Clone the repository**

```bash
git clone https://github.com/LeonMotaung/sudoku.git
cd sudoku
