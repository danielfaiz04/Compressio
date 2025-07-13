// File upload and compression handling
class FileCompressor {
    constructor(checkCompressionLimitFn) {
        this.dropZone = document.getElementById('dropZone');
        this.fileInput = document.getElementById('fileInput');
        this.historyTable = document.getElementById('historyTable').querySelector('tbody');
        this.loadCompressionHistory();
        this.checkCompressionLimit = checkCompressionLimitFn; // Store the function
        this.setupEventListeners();
    }

    setupEventListeners() {
        // Event Listeners for drag and drop
        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            this.dropZone.addEventListener(eventName, this.preventDefaults, false);
        });

        ['dragenter', 'dragover'].forEach(eventName => {
            this.dropZone.addEventListener(eventName, () => this.dropZone.classList.add('highlight'), false);
        });

        ['dragleave', 'drop'].forEach(eventName => {
            this.dropZone.addEventListener(eventName, () => this.dropZone.classList.remove('highlight'), false);
        });

        this.dropZone.addEventListener('drop', (e) => {
            const dt = e.dataTransfer;
            const files = dt.files;
            this.handleFiles(files, 'compress'); // Always 'compress'
        }, false);

        // File input change handler is now in app.js, handled by displaySelectedFile and clearFileSelection
        // The actual file handling is initiated by submit button in app.js now.
    }

    preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    handleFiles(files, operation) {
        if (!this.checkCompressionLimit()) { // Use the stored function
            return;
        }

        Array.from(files).forEach(file => {
            if (this.isValidFile(file)) {
                if (operation === 'compress') {
                    this.compressFile(file);
                } else { // Decompression is not directly supported via upload anymore
                    showToast(translations[getCurrentLanguage()].decompressionNotSupported || 'Decompression is not supported via direct upload. Please download original file.', 'error');
                }
            } else {
                showToast(translations[getCurrentLanguage()].invalidFileType || 'Invalid file type. Please upload a valid file.', 'error');
            }
        });
    }

    isValidFile(file) {
        const validMimeTypes = [
            'image/jpeg', 'image/png', 'image/webp',
            'text/plain',
            'application/pdf',
            'application/msword',
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            'application/vnd.ms-excel',
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            'application/vnd.ms-powerpoint',
            'application/vnd.openxmlformats-officedocument.presentationml.presentation',
            'application/zip',
            'application/x-rar-compressed',
            'video/mp4', 'video/mpeg', 'video/quicktime',
            'audio/mpeg', 'audio/wav',
            'application/json',
            'application/octet-stream'
        ];
        const fileExtension = file.name.split('.').pop().toLowerCase();
        const validExtensions = [
            'jpg', 'jpeg', 'png', 'webp',
            'txt',
            'pdf',
            'doc', 'docx',
            'xls', 'xlsx',
            'ppt', 'pptx',
            'zip',
            'rar',
            'mp4', 'mpeg', 'mov',
            'mp3', 'wav',
            'json',
            'bin'
        ];

        return validMimeTypes.includes(file.type) || validExtensions.includes(fileExtension);
    }

    async compressFile(file) {
        try {
            this.showUploadingState(file.name);

            const API_KEY = "demo-key-123"; // Ganti dengan cara yang lebih aman untuk menangani kunci API di produksi
            const headers = {
                "X-API-Key": API_KEY
            };

            // Langkah 1: Unggah file
            const uploadFormData = new FormData();
            uploadFormData.append('file', file);

            const uploadResponse = await fetch(`${API_BASE_URL}/upload`, { // Endpoint unggah baru
                method: 'POST',
                headers: headers,
                body: uploadFormData
            });

            const uploadResult = await uploadResponse.json();

            if (!uploadResponse.ok) {
                throw new Error(uploadResult.detail || translations[getCurrentLanguage()].uploadFailed || 'Pengunggahan file gagal');
            }

            const fileId = uploadResult.id;

            // Langkah 2: Kompres file yang diunggah
            const compressFormData = new FormData();
            compressFormData.append('file_id', fileId);
            compressFormData.append('method', 'ai'); // Gunakan 'ai' untuk kompresi berbasis AI

            const compressResponse = await fetch(`${API_BASE_URL}/compress`, { // Endpoint kompresi baru
                method: 'POST',
                headers: headers,
                body: compressFormData
            });

            const compressResult = await compressResponse.json();

            if (!compressResponse.ok) {
                throw new Error(compressResult.detail || translations[getCurrentLanguage()].compressionFailed || 'Kompresi gagal');
            }

            // Setelah kompresi berhasil, ambil metadata hasil untuk detail lengkap
            const resultMetadataResponse = await fetch(`${API_BASE_URL}/result/${fileId}`, {
                method: 'GET',
                headers: headers
            });
            const resultMetadata = await resultMetadataResponse.json();

            if (!resultMetadataResponse.ok) {
                throw new Error(resultMetadata.detail || translations[getCurrentLanguage()].fetchResultFailed || 'Gagal mengambil hasil kompresi');
            }

            // Tambahkan ke riwayat menggunakan data dari resultMetadata
                const historyEntry = {
                fileId: fileId,
                fileName: resultMetadata.original_filename,
                originalSize: resultMetadata.size_before,
                compressedSize: resultMetadata.size_after,
                ratio: resultMetadata.ratio,
                compressionMethod: resultMetadata.compression_method,
                compressedFilename: resultMetadata.compressed_filename,
                downloadUrl: resultMetadata.download_url,
                    timestamp: new Date().toISOString(),
                status: 'success',
                message: translations[getCurrentLanguage()].compressedSuccessfully || `Berhasil dikompresi dengan ${resultMetadata.compression_method}`
                };
                this.addToHistory(historyEntry);

            // Tampilkan pesan sukses
                this.hideUploadingState();
            showToast(historyEntry.message, 'success');

        } catch (error) {
            console.error('Compression error:', error);
            this.hideUploadingState();
            showToast(error.message || translations[getCurrentLanguage()].compressionFailed || 'Kompresi gagal', 'error');
        }
    }

    showUploadingState(fileName) {
        showLoading(true, fileName); // Use the global showLoading from app.js
    }

    hideUploadingState() {
        showLoading(false); // Use the global showLoading from app.js
        // Restore drop zone content after upload is done
        const dropZone = document.getElementById('dropZone');
        if (dropZone) {
            dropZone.innerHTML = `
            <h3>${translations[getCurrentLanguage()].dragDrop}</h3>
            <p>${translations[getCurrentLanguage()].or}</p>
                <input type="file" id="fileInput" class="d-none" accept=".jpg,.jpeg,.png,.txt,.pdf,.doc,.docx,.xls,.xlsx,.ppt,.pptx,.zip,.rar,.mp4,.mpeg,.mov,.mp3,.wav,.json,.bin">
            <button class="btn btn-primary" onclick="document.getElementById('fileInput').click()">
                ${translations[getCurrentLanguage()].chooseFiles}
            </button>
        `;
             // Reattach event listener to the newly created fileInput element
            document.getElementById('fileInput').addEventListener('change', (e) => {
                displaySelectedFile(e.target.files[0].name);
            });
        }
    }

    addToHistory(entry) {
        const history = this.getCompressionHistory();
        history.unshift(entry);
        if (history.length > MAX_COMPRESSIONS) { // Use MAX_COMPRESSIONS from app.js
            history.pop();
        }
        localStorage.setItem('compressionHistory', JSON.stringify(history));
        this.updateHistoryTable();
    }

    getCompressionHistory() {
        const historyString = localStorage.getItem('compressionHistory');
        if (!historyString) {
            return [];
        }
        const history = JSON.parse(historyString);
        return history.map(entry => ({
            ...entry,
            originalSize: parseFloat(entry.originalSize),
            compressedSize: parseFloat(entry.compressedSize),
            ratio: parseFloat(entry.ratio)
        }));
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
                <td>${formatSize(entry.originalSize)}</td>
                <td>${formatSize(entry.compressedSize)}</td>
                <td>${entry.ratio.toFixed(1)}%</td>
                <td>
                    <button class="btn btn-sm btn-primary" onclick="fileCompressor.downloadFile('${entry.fileId}')">
                        ${translations[getCurrentLanguage()].download}
                    </button>
                    <button class="btn btn-sm btn-info ms-1" onclick="fileCompressor.showCompareModal('${entry.fileId}')">
                        ${translations[getCurrentLanguage()].compare}
                    </button>
                    <button class="btn btn-sm btn-danger ms-1" onclick="fileCompressor.deleteHistoryEntry('${entry.timestamp}')">
                        ${translations[getCurrentLanguage()].delete}
                    </button>
                </td>
            `;
            this.historyTable.appendChild(row);
        });
    }

    deleteHistoryEntry(timestamp) {
        let history = this.getCompressionHistory();
        history = history.filter(entry => entry.timestamp !== timestamp);
        localStorage.setItem('compressionHistory', JSON.stringify(history));
        this.updateHistoryTable();
        showToast(translations[getCurrentLanguage()].historyEntryDeleted, 'info');
    }

    async downloadFile(fileId, original = false) { // Sekarang menerima fileId dan flag 'original' opsional
        try {
            console.log(`Mencoba mengunduh file dengan ID: ${fileId}. Asli: ${original}`);
            const API_KEY = "demo-key-123";
            const headers = {
                "X-API-Key": API_KEY
            };

            const params = new URLSearchParams();
            if (original) {
                params.append('original', 'true');
            }

            const response = await fetch(`${API_BASE_URL}/download/${fileId}?${params.toString()}`, { // Endpoint unduhan baru
                method: 'GET',
                headers: headers
            });
            
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || translations[getCurrentLanguage()].downloadFailed || 'Pengunduhan file gagal');
            }

            const blob = await response.blob();
            const contentDisposition = response.headers.get('Content-Disposition');
            let filename = `download_${fileId}`;
            if (contentDisposition) {
                const filenameMatch = contentDisposition.match(/filename\*?=['"]?(?:UTF-8'')?([^"\r\n;]+)['"]?/);
                if (filenameMatch && filenameMatch[1]) {
                    filename = decodeURIComponent(filenameMatch[1]);
                }
            }

            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = filename;
            document.body.appendChild(a);
            a.click();
            a.remove();
            window.URL.revokeObjectURL(url);
            showToast(translations[getCurrentLanguage()].downloadSuccess || 'File downloaded successfully!', 'success');

        } catch (error) {
            console.error('Download error:', error);
            showToast(error.message || translations[getCurrentLanguage()].downloadFailed || 'Pengunduhan gagal', 'error');
        }
    }

    async showCompareModal(fileId) {
        try {
            const API_KEY = "demo-key-123";
            const headers = { "X-API-Key": API_KEY };
            // Ambil metadata hasil kompresi
            const resultRes = await fetch(`${API_BASE_URL}/result/${fileId}`, { method: 'GET', headers });
            const result = await resultRes.json();
            if (!resultRes.ok) throw new Error(result.detail || 'Failed to fetch result');
            // Ambil file asli (preview/info)
            const origRes = await fetch(`${API_BASE_URL}/download/${fileId}?original=true`, { method: 'GET', headers });
            const origBlob = await origRes.blob();
            // Ambil file kompresi (preview/info)
            const compRes = await fetch(`${API_BASE_URL}/download/${fileId}`, { method: 'GET', headers });
            const compBlob = await compRes.blob();
            // Buat URL untuk preview
            const origUrl = URL.createObjectURL(origBlob);
            const compUrl = URL.createObjectURL(compBlob);
            // Siapkan konten modal
            const lang = getCurrentLanguage();
            const t = translations[lang];
            let previewHtml = '';
            // Preview gambar
            if (result.original_filename.match(/\.(jpg|jpeg|png|webp)$/i)) {
                previewHtml = `
                    <div class="row mb-3">
                        <div class="col text-center">
                            <div><strong>${t.originalSize}</strong></div>
                            <img src="${origUrl}" alt="Original" style="max-width:100%;max-height:200px;">
                            <div class="small mt-1">${t.fileName}: ${result.original_filename}<br>${t.originalSize}: ${formatSize(result.size_before)}</div>
                        </div>
                        <div class="col text-center">
                            <div><strong>${t.compressedSize}</strong></div>
                            <img src="${compUrl}" alt="Compressed" style="max-width:100%;max-height:200px;">
                            <div class="small mt-1">${t.fileName}: ${result.compressed_filename}<br>${t.compressedSize}: ${formatSize(result.size_after)}</div>
                        </div>
                    </div>
                `;
            } else {
                // Untuk file non-gambar, tampilkan info saja
                previewHtml = `
                    <div class="row mb-3">
                        <div class="col">
                            <div><strong>${t.fileName}:</strong> ${result.original_filename}</div>
                            <div><strong>${t.originalSize}:</strong> ${formatSize(result.size_before)}</div>
                        </div>
                        <div class="col">
                            <div><strong>${t.fileName}:</strong> ${result.compressed_filename}</div>
                            <div><strong>${t.compressedSize}:</strong> ${formatSize(result.size_after)}</div>
                        </div>
                    </div>
                `;
            }
            // Info detail
            const infoHtml = `
                <div class="mb-2"><strong>${t.ratio}:</strong> ${result.ratio.toFixed(1)}%</div>
                <div class="mb-2"><strong>${t.method || 'Method'}:</strong> ${result.compression_method}</div>
            `;
            // Modal HTML
            let modal = document.getElementById('compareModal');
            if (!modal) {
                modal = document.createElement('div');
                modal.id = 'compareModal';
                modal.className = 'modal fade';
                modal.tabIndex = -1;
                modal.innerHTML = `
                    <div class="modal-dialog modal-lg">
                        <div class="modal-content">
                            <div class="modal-header">
                                <h5 class="modal-title">${t.compare}</h5>
                                <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                            </div>
                            <div class="modal-body" id="compareModalBody"></div>
                        </div>
                    </div>
                `;
                document.body.appendChild(modal);
            }
            document.getElementById('compareModalBody').innerHTML = previewHtml + infoHtml;
            // Tampilkan modal (Bootstrap 5)
            const bsModal = new bootstrap.Modal(modal);
            bsModal.show();
            // Revoke object URLs saat modal ditutup
            modal.addEventListener('hidden.bs.modal', () => {
                URL.revokeObjectURL(origUrl);
                URL.revokeObjectURL(compUrl);
            }, { once: true });
        } catch (err) {
            showToast(err.message || 'Failed to compare files', 'error');
        }
    }
}

// Translations for UI messages (add new keys as needed)
function getCurrentLanguage() {
    return localStorage.getItem('preferredLanguage') || 'en'; // Menggunakan preferredLanguage dari app.js
}

// Global constants and functions from app.js that are used here
// These are expected to be available globally in the HTML where compress.js is loaded.
// If not, they should be passed as arguments or imported.
// For now, assuming they are global as per the existing structure.

// Ensure that `showToast`, `showLoading`, `formatSize`, `MAX_COMPRESSIONS`, `API_BASE_URL`
// and `displaySelectedFile` are globally accessible from app.js.
// These are typically defined in app.js or a shared utility file.
// `API_BASE_URL` is now defined in app.js and passed implicitly through global scope.

// No longer directly calling initializeCompression here. It's called by app.js
// document.addEventListener('DOMContentLoaded', initializeCompression); 