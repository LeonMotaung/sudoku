document.addEventListener('DOMContentLoaded', () => {
    const grid = document.getElementById('sudoku-grid');
    const solveButton = document.getElementById('solve-button');
    const clearButton = document.getElementById('clear-button');
    const uploadButton = document.getElementById('upload-button');
    const fileInput = document.getElementById('file-input');
    const fileName = document.getElementById('file-name');
    const scanButton = document.getElementById('scan-button');
    const solutionGrid = document.getElementById('solution-grid');

    // Create the input grid
    for (let i = 0; i < 9; i++) {
        for (let j = 0; j < 9; j++) {
            const cell = document.createElement('input');
            cell.type = 'text';
            cell.classList.add('w-10', 'h-10', 'text-center', 'text-2xl', 'border', 'border-gray-400');
            if ((j + 1) % 3 === 0 && j < 8) {
                cell.classList.add('border-r-2', 'border-gray-900');
            }
            if ((i + 1) % 3 === 0 && i < 8) {
                cell.classList.add('border-b-2', 'border-gray-900');
            }
            cell.maxLength = 1;
            grid.appendChild(cell);
        }
    }

    // Create the solution grid
    for (let i = 0; i < 9; i++) {
        for (let j = 0; j < 9; j++) {
            const cell = document.createElement('div');
            cell.classList.add('w-10', 'h-10', 'text-center', 'text-2xl', 'border', 'border-gray-400', 'flex', 'items-center', 'justify-center');
            if ((j + 1) % 3 === 0 && j < 8) {
                cell.classList.add('border-r-2', 'border-gray-900');
            }
            if ((i + 1) % 3 === 0 && i < 8) {
                cell.classList.add('border-b-2', 'border-gray-900');
            }
            solutionGrid.appendChild(cell);
        }
    }

    // Handle file upload
    uploadButton.addEventListener('click', () => {
        fileInput.click();
    });

    fileInput.addEventListener('change', () => {
        if (fileInput.files.length > 0) {
            fileName.textContent = fileInput.files[0].name;
        } else {
            fileName.textContent = 'No file chosen';
        }
    });

    // Solve the puzzle from manual input
    solveButton.addEventListener('click', async () => {
        const board = [];
        const cells = grid.children;
        for (let i = 0; i < 9; i++) {
            const row = [];
            for (let j = 0; j < 9; j++) {
                const value = cells[i * 9 + j].value;
                row.push(value === '' ? 0 : parseInt(value));
            }
            board.push(row);
        }

        const response = await fetch('/solve', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ board })
        });

        const data = await response.json();

        if (data.solution) {
            const solutionCells = solutionGrid.children;
            for (let i = 0; i < data.solution.length; i++) {
                for (let j = 0; j < data.solution[i].length; j++) {
                    solutionCells[i * 9 + j].textContent = data.solution[i][j];
                }
            }
        } else {
            alert(data.error);
        }
    });

    // Scan the puzzle from an image
    scanButton.addEventListener('click', async () => {
        if (!fileInput.files[0]) {
            alert('Please select an image file first.');
            return;
        }

        const formData = new FormData();
        formData.append('file', fileInput.files[0]);

        // Disable the button and show a "Scanning..." message
        scanButton.disabled = true;
        scanButton.textContent = 'Scanning...';

        try {
            const response = await fetch('/scan', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            if (data.board) {
                const cells = grid.children;
                for (let i = 0; i < data.board.length; i++) {
                    for (let j = 0; j < data.board[i].length; j++) {
                        const value = data.board[i][j];
                        cells[i * 9 + j].value = value === 0 ? '' : value;
                    }
                }
            }

            if (data.solution) {
                const solutionCells = solutionGrid.children;
                for (let i = 0; i < data.solution.length; i++) {
                    for (let j = 0; j < data.solution[i].length; j++) {
                        solutionCells[i * 9 + j].textContent = data.solution[i][j];
                    }
                }
            } else {
                if (data.error) {
                    alert(data.error);
                }
            }
        } catch (error) {
            alert('An error occurred while scanning the image.');
        } finally {
            // Re-enable the button and restore its original text
            scanButton.disabled = false;
            scanButton.textContent = 'Scan';
        }
    });

    // Clear the grid
    clearButton.addEventListener('click', () => {
        const cells = grid.children;
        for (let i = 0; i < cells.length; i++) {
            cells[i].value = '';
        }
        const solutionCells = solutionGrid.children;
        for (let i = 0; i < solutionCells.length; i++) {
            solutionCells[i].textContent = '';
        }
    });
});