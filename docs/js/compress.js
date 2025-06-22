// File upload and compression handling
class FileCompressor {
    constructor() {
        this.dropZone = document.getElementById('dropZone');
        this.fileInput = document.getElementById('fileInput');
        this.historyTable = document.getElementById('historyTable').querySelector('tbody');
        this.loadCompressionHistory();
    }

    handleFiles(files, operation) {
        if (!checkCompressionLimit()) {
            return;
        }

        Array.from(files).forEach(file => {
            if (this.isValidFile(file)) {
                if (operation === 'compress') {
                    this.compressFile(file);
                } else if (operation === 'decompress') {
                    this.decompressFile(file);
                }
            } else {
                showToast('Invalid file type. Please upload a valid file.', 'error');
            }
        });
    }

    isValidFile(file) {
        const validTypes = ['image/jpeg', 'image/png', 'text/plain', 'application/pdf'];
        return validTypes.includes(file.type);
    }

    async compressFile(file) {
        try {
            this.showUploadingState(file.name);

            const formData = new FormData();
            formData.append('file', file);
            formData.append('algorithm', 'auto');

            const response = await fetch('/api/compress', {
                method: 'POST',
                body: formData
            });

            const result = await response.json();

            if (!response.ok) {
                throw new Error(result.error || 'Compression failed');
            }

            if (result.success) {
                // Add to history
                const historyEntry = {
                    fileName: file.name,
                    originalSize: result.original_size,
                    compressedSize: result.compressed_size,
                    ratio: result.compression_ratio,
                    compressedFilename: result.output_filename,
                    timestamp: new Date().toISOString()
                };
                this.addToHistory(historyEntry);
                
                // Show success message
                this.hideUploadingState();
                showToast(`File compressed successfully! Compression ratio: ${result.compression_ratio.toFixed(2)}%`, 'success');
                
                // Enable download button
                const downloadBtn = document.querySelector(`button[onclick="fileCompressor.downloadFile('${result.output_filename}')"]`);
                if (downloadBtn) {
                    downloadBtn.disabled = false;
                }
            } else {
                throw new Error(result.error || 'Compression failed');
            }

        } catch (error) {
            console.error('Compression error:', error);
            this.hideUploadingState();
            showToast(error.message || 'Compression failed', 'error');
        }
    }

    async decompressFile(file) {
        try {
            this.showUploadingState(file.name);

            const formData = new FormData();
            formData.append('file', file);
            formData.append('algorithm', 'auto');

            const response = await fetch('/api/decompress', {
                method: 'POST',
                body: formData
            });

            const result = await response.json();

            if (!response.ok) {
                throw new Error(result.error || 'Decompression failed');
            }

            if (result.success) {
                this.hideUploadingState();
                showToast('File decompressed successfully!', 'success');
                
                // Enable download button
                const downloadBtn = document.querySelector(`button[onclick="fileCompressor.downloadFile('${result.output_filename}')"]`);
                if (downloadBtn) {
                    downloadBtn.disabled = false;
                }
            } else {
                throw new Error(result.error || 'Decompression failed');
            }

        } catch (error) {
            console.error('Decompression error:', error);
            this.hideUploadingState();
            showToast(error.message || 'Decompression failed', 'error');
        }
    }

    showUploadingState(fileName) {
        this.dropZone.classList.add('uploading');
        this.dropZone.innerHTML = `
            <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
            <p class="mt-2">${translations[getCurrentLanguage()].compressing} ${fileName}...</p>
        `;
    }

    hideUploadingState() {
        this.dropZone.classList.remove('uploading');
        this.dropZone.innerHTML = `
            <!-- <img src="assets/mascot.svg" alt="Mascot" class="mascot mb-3"> -->
            <h3>${translations[getCurrentLanguage()].dragDrop}</h3>
            <p>${translations[getCurrentLanguage()].or}</p>
            <input type="file" id="fileInput" class="d-none" accept=".jpg,.jpeg,.png,.txt,.pdf">
            <button class="btn btn-primary" onclick="document.getElementById('fileInput').click()">
                ${translations[getCurrentLanguage()].chooseFiles}
            </button>
        `;
    }

    addToHistory(entry) {
        const history = this.getCompressionHistory();
        history.unshift(entry);
        if (history.length > 10) {
            history.pop();
        }
        localStorage.setItem('compressionHistory', JSON.stringify(history));
        this.updateHistoryTable();
    }

    getCompressionHistory() {
        const history = localStorage.getItem('compressionHistory');
        return history ? JSON.parse(history) : [];
    }

    loadCompressionHistory() {
        this.updateHistoryTable();
    }

    updateHistoryTable() {
        const history = this.getCompressionHistory();
        this.historyTable.innerHTML = '';

        history.forEach(entry => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${entry.fileName}</td>
                <td>${this.formatFileSize(entry.originalSize)}</td>
                <td>${this.formatFileSize(entry.compressedSize)}</td>
                <td>${entry.ratio.toFixed(1)}%</td>
                <td>
                    <button class="btn btn-sm btn-download" onclick="fileCompressor.downloadFile('${entry.compressedFilename}')">
                        Download
                    </button>
                </td>
            `;
            this.historyTable.appendChild(row);
        });
    }

    async downloadFile(filename) {
        try {
            console.log(`Attempting to download file: ${filename}`);
            const response = await fetch(`/api/download/${filename}`);
            
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || 'Download failed');
            }

            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = filename;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            a.remove();

            showToast('File downloaded successfully!', 'success');
        } catch (error) {
            console.error('Download error:', error);
            showToast(error.message || 'Download failed', 'error');
        }
    }

    formatFileSize(bytes) {
        if (bytes === 0) return '0 B';
        const k = 1024;
        const sizes = ['B', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }
}

// Helper function to get current language
function getCurrentLanguage() {
    return localStorage.getItem('preferredLanguage') || 'id';
}

// Placeholder for compression limit check
function checkCompressionLimit() {
    // For now, always allow compression. 
    // This function will be properly implemented with authentication logic.
    return true;
}

// Initialize file compressor
const fileCompressor = new FileCompressor();

// Compression-specific functionality

// Compression type selection handler
document.getElementById('compressionType').addEventListener('change', function(event) {
    const selectedType = event.target.value;
    updateCompressionUI(selectedType);
});

// Update UI based on compression type
function updateCompressionUI(compressionType) {
    const fileInput = document.getElementById('fileInput');
    const operationRadios = document.querySelectorAll('input[name="operation"]');
    
    // Update accepted file types based on compression type
    switch (compressionType) {
        case COMPRESSION_TYPES.HUFFMAN:
            fileInput.accept = '.png,.jpg,.jpeg';
            break;
        case COMPRESSION_TYPES.RLE:
            fileInput.accept = '.txt,.pdf';
            break;
        default:
            fileInput.accept = '.png,.jpg,.jpeg,.txt,.pdf';
    }
    
    // Update operation radio buttons - Always enable them
    operationRadios.forEach(radio => {
        radio.disabled = false; // Set to always be enabled
    });
}

// Get recommended compression type for file
function getRecommendedCompressionType(file) {
    const ext = '.' + file.name.split('.').pop().toLowerCase();
    
    if (['.png', '.jpg', '.jpeg'].includes(ext)) {
        return COMPRESSION_TYPES.HUFFMAN;
    } else if (['.txt', '.pdf'].includes(ext)) {
        return COMPRESSION_TYPES.RLE;
    }
    
    return COMPRESSION_TYPES.AUTO;
}

// Validate compression settings
function validateCompressionSettings(file, compressionType, operation) {
    const ext = '.' + file.name.split('.').pop().toLowerCase();
    
    // Check if file type is supported for the selected compression type
    if (compressionType === COMPRESSION_TYPES.HUFFMAN && !['.png', '.jpg', '.jpeg'].includes(ext)) {
        showToast('Huffman compression only supports image files', 'warning');
        return false;
    }
    
    if (compressionType === COMPRESSION_TYPES.RLE && !['.txt', '.pdf'].includes(ext)) {
        showToast('RLE compression only supports text and PDF files', 'warning');
        return false;
    }
    
    // Check if operation is valid for the file
    if (operation === 'decompress') {
        if (!file.name.startsWith('compressed_') && !file.name.startsWith('decompressed_')) {
            showToast('This file does not appear to be a compressed file', 'warning');
            return false;
        }
    }
    
    return true;
}

// Show compression progress
function showCompressionProgress(file, compressionType) {
    const progressContainer = document.createElement('div');
    progressContainer.className = 'compression-progress mt-3';
    progressContainer.innerHTML = `
        <div class="progress">
            <div class="progress-bar progress-bar-striped progress-bar-animated" 
                 role="progressbar" 
                 style="width: 0%">
            </div>
        </div>
        <small class="text-muted mt-2 d-block">
            Compressing ${file.name} using ${compressionType}...
        </small>
    `;
    
    const form = document.getElementById('uploadForm');
    form.appendChild(progressContainer);
    
    return progressContainer;
}

// Update compression progress
function updateCompressionProgress(container, progress) {
    const progressBar = container.querySelector('.progress-bar');
    progressBar.style.width = `${progress}%`;
}

// Remove compression progress
function removeCompressionProgress(container) {
    container.remove();
}

// Show compression results
function showCompressionResults(result) {
    const resultsContainer = document.createElement('div');
    resultsContainer.className = 'compression-results mt-4';
    resultsContainer.innerHTML = `
        <div class="card">
            <div class="card-body">
                <h5 class="card-title">Compression Results</h5>
                <div class="compression-stats">
                    <div class="stat-card">
                        <div class="stat-value">${formatSize(result.original_size)}</div>
                        <div class="stat-label">Original Size</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value">${formatSize(result.compressed_size)}</div>
                        <div class="stat-label">Compressed Size</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value">${result.compression_ratio.toFixed(2)}%</div>
                        <div class="stat-label">Compression Ratio</div>
                    </div>
                </div>
                <div class="text-center mt-3">
                    <button class="btn btn-primary" onclick="downloadFile('${result.output_filename}')">
                        Download Compressed File
                    </button>
                </div>
            </div>
        </div>
    `;
    
    const form = document.getElementById('uploadForm');
    form.appendChild(resultsContainer);
    
    // Remove results after 5 seconds
    setTimeout(() => {
        resultsContainer.remove();
    }, 5000);
}

// Initialize compression module
function initializeCompression() {
    // Set initial compression type
    const compressionType = document.getElementById('compressionType').value;
    updateCompressionUI(compressionType);
    
    // Add event listeners for operation radio buttons
    const operationRadios = document.querySelectorAll('input[name="operation"]');
    operationRadios.forEach(radio => {
        radio.addEventListener('change', function() {
            const fileInput = document.getElementById('fileInput');
            if (fileInput.files.length > 0) {
                validateCompressionSettings(
                    fileInput.files[0],
                    document.getElementById('compressionType').value,
                    this.value
                );
            }
        });
    });
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', initializeCompression); 